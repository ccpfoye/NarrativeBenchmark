import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
import tempfile
import subprocess
from typing import Any

@dataclass
class MazeState:
    """Mutable runtime state for traversing an Ink maze."""

    current_knot: str
    finished: bool = False


class InkMaze:
    """Very small parser/runtime for a subset of Ink used by this benchmark."""

    def __init__(self, knots: dict[str, dict[str, Any]], start_knot: str):
        if start_knot not in knots:
            raise ValueError(f"Unknown start knot: {start_knot}")
        self.knots = knots
        self.state = MazeState(current_knot=start_knot)

    @classmethod
    def from_file(cls, path: str, start_knot: str) -> "InkMaze":
        file_path = Path(path)
        if file_path.suffix.lower() == ".json":
            with open(file_path, "r", encoding="utf-8") as handle:
                compiled_story = json.load(handle)
            knots = cls._parse_compiled_story_json(compiled_story)
        else:
            with open(file_path, "r", encoding="utf-8") as handle:
                source = handle.read()
            knots = cls._parse_knots(source)

            # If inklecate is available, compile to JSON and prefer that parse.
            # This reflects Ink's canonical serializable export format.
            compiled_knots = cls._try_parse_via_inklecate(file_path)
            if compiled_knots:
                knots = compiled_knots

        return cls(knots, start_knot=start_knot)

    @classmethod
    def _try_parse_via_inklecate(cls, ink_file: Path) -> dict[str, dict[str, Any]] | None:
        """Try parsing via Ink's compiled JSON export (`inklecate -o out.json in.ink`)."""
        inklecate = "inklecate"
        if not shutil.which(inklecate):
            return None

        with tempfile.TemporaryDirectory() as tmp_dir:
            out_path = Path(tmp_dir) / f"{ink_file.stem}.json"
            cmd = [inklecate, "-o", str(out_path), str(ink_file)]
            try:
                subprocess.run(cmd, check=True, capture_output=True, text=True)
            except (OSError, subprocess.CalledProcessError):
                return None

            if not out_path.exists():
                return None

            with open(out_path, "r", encoding="utf-8") as handle:
                compiled_story = json.load(handle)

        return cls._parse_compiled_story_json(compiled_story)

    @staticmethod
    def _parse_knots(source: str) -> dict[str, dict[str, Any]]:
        knot_header = re.compile(r"^===\s+([A-Za-z_][A-Za-z0-9_]*)\s+===$")
        choice_line = re.compile(r"^\*\s+\[(.+?)\]\s*->\s*([A-Za-z_][A-Za-z0-9_]*)$")
        divert_line = re.compile(r"^->\s*([A-Za-z_][A-Za-z0-9_]*)$")

        knots: dict[str, dict[str, Any]] = {}
        current_knot: str | None = None
        buffer: list[str] = []

        def commit() -> None:
            if current_knot is None:
                return

            description: list[str] = []
            choices: list[dict[str, str]] = []
            fallthrough: str | None = None

            for raw_line in buffer:
                line = raw_line.strip()
                if not line:
                    continue
                if match := choice_line.match(line):
                    choices.append({"label": match.group(1), "target": match.group(2)})
                    continue
                if match := divert_line.match(line):
                    fallthrough = match.group(1)
                    continue
                description.append(line)

            knots[current_knot] = {
                "description": "\n".join(description).strip(),
                "choices": choices,
                "fallthrough": fallthrough,
            }

        for raw_line in source.splitlines():
            line = raw_line.rstrip("\n")
            if match := knot_header.match(line.strip()):
                commit()
                current_knot = match.group(1)
                buffer = []
                continue
            if current_knot is not None:
                buffer.append(line)

        commit()

        if not knots:
            raise ValueError("No knots were parsed from the Ink file.")

        return knots

    @staticmethod
    def _parse_compiled_story_json(compiled_story: dict[str, Any]) -> dict[str, dict[str, Any]]:
        """Parse Ink compiled JSON (from inklecate) into knot/choice map.

        Ink's compiler serializes the story into a JSON container graph. For this maze
        use-case we only need:
        - named knot containers
        - visible text fragments
        - three-choice entries and their divert targets
        """
        if "root" not in compiled_story:
            raise ValueError("Compiled story JSON missing 'root'.")

        root = compiled_story["root"]
        if not isinstance(root, list) or not root:
            raise ValueError("Compiled story JSON has invalid 'root' container.")

        named_containers = InkMaze._extract_named_containers(root)
        if not named_containers:
            raise ValueError("No named containers found in compiled story JSON.")

        knots: dict[str, dict[str, Any]] = {}
        for knot_name, knot_container in named_containers.items():
            flat_items = InkMaze._flatten_container_items(knot_container)

            description_parts: list[str] = []
            choices: list[dict[str, str]] = []
            fallthrough: str | None = None

            pending_target: str | None = None
            awaiting_target_for_choice = False
            for item in flat_items:
                if isinstance(item, str) and item.startswith("^"):
                    description_parts.append(item[1:])
                    continue

                if isinstance(item, dict):
                    if "*" in item:
                        if isinstance(pending_target, str):
                            choices.append({"label": "choice", "target": pending_target})
                            pending_target = None
                        else:
                            awaiting_target_for_choice = True

                    divert_target = item.get("^->") or item.get("->")
                    if isinstance(divert_target, str):
                        if awaiting_target_for_choice:
                            choices.append({"label": "choice", "target": divert_target})
                            awaiting_target_for_choice = False
                        else:
                            pending_target = divert_target
                        if item.get("->") and not item.get("*"):
                            fallthrough = divert_target

            # Improve choice labels by collecting nearest text snippets around each choice.
            # This is a heuristic for compiled JSON where labels are emitted as text values.
            labels = InkMaze._extract_choice_labels(flat_items)
            for idx, label in enumerate(labels):
                if idx < len(choices):
                    choices[idx]["label"] = label

            # Avoid repeating extracted choice labels inside room description.
            label_set = {label.strip() for label in labels if label.strip()}
            cleaned_description = [
                part for part in description_parts if part.strip() and part.strip() not in label_set
            ]

            # Keep original behavior: only record node as a knot when it has content.
            if cleaned_description or choices or fallthrough:
                knots[knot_name] = {
                    "description": "\n".join(cleaned_description).strip(),
                    "choices": choices,
                    "fallthrough": fallthrough,
                }

        if not knots:
            raise ValueError("Compiled story JSON parse produced no knots.")

        return knots

    @staticmethod
    def _extract_named_containers(root: list[Any]) -> dict[str, Any]:
        # In inklecate output, a dict containing named sub-containers usually appears as
        # the last entry in a container list.
        for item in reversed(root):
            if isinstance(item, dict) and any(not k.startswith("#") for k in item):
                return {
                    key: value
                    for key, value in item.items()
                    if not key.startswith("#") and isinstance(value, list)
                }
        return {}

    @staticmethod
    def _flatten_container_items(node: Any) -> list[Any]:
        flat: list[Any] = []

        def walk(value: Any) -> None:
            if isinstance(value, list):
                for inner in value:
                    walk(inner)
            else:
                flat.append(value)

        walk(node)
        return flat

    @staticmethod
    def _extract_choice_labels(flat_items: list[Any]) -> list[str]:
        labels: list[str] = []
        pending_label: str | None = None
        for item in flat_items:
            if isinstance(item, str) and item.startswith("^"):
                text = item[1:].strip()
                if text:
                    pending_label = text
                continue

            if isinstance(item, dict) and "*" in item and pending_label:
                labels.append(pending_label)
                pending_label = None

        return labels
    
    def read_room(self) -> str:
        knot = self.knots[self.state.current_knot]
        description = knot["description"] or "(No room description.)"
        choices = knot["choices"]

        if self.state.finished:
            return f"Maze already completed at knot '{self.state.current_knot}'."

        if not choices:
            # Terminal knot or auto-divert knot.
            fallthrough = knot.get("fallthrough")
            if fallthrough in {"DONE", "END"}:
                self.state.finished = True
                return (
                    f"Reached terminal knot '{self.state.current_knot}'. "
                    f"Auto-diverted to {fallthrough}. Maze complete."
                )

            if fallthrough and fallthrough in self.knots:
                previous = self.state.current_knot
                self.state.current_knot = fallthrough
                return (
                    f"Auto-divert from '{previous}' to '{fallthrough}'. "
                    "Use read_current_room again."
                )

            return (
                f"At knot '{self.state.current_knot}' with no choices. "
                "No valid moves remain."
            )

        option_text = "\n".join(
            f"{idx + 1}. {choice['label']} -> {choice['target']}"
            for idx, choice in enumerate(choices)
        )
        return (
            f"Current knot: {self.state.current_knot}\n"
            f"Description: {description}\n"
            f"Three doors:\n{option_text}"
        )

    def choose_door(self, door_index: int) -> str:
        if self.state.finished:
            return "Maze is already finished."

        knot = self.knots[self.state.current_knot]
        choices = knot["choices"]
        if len(choices) != 3:
            return (
                f"Knot '{self.state.current_knot}' does not have exactly three doors "
                f"(found {len(choices)})."
            )

        if door_index not in {1, 2, 3}:
            return "door_index must be 1, 2, or 3."

        chosen = choices[door_index - 1]
        target = chosen["target"]
        self.state.current_knot = target

        if target in {"DONE", "END"}:
            self.state.finished = True
            return f"Chose door {door_index} ('{chosen['label']}'). Reached {target}."

        if target not in self.knots:
            return (
                f"Chose door {door_index} ('{chosen['label']}') -> '{target}', "
                "but target knot does not exist in file."
            )

        return (
            f"Chose door {door_index} ('{chosen['label']}') -> '{target}'. "
            "Now inspect the new room."
        )