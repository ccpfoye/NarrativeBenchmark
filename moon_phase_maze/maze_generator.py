"""Random Ink maze generator with a phase-ordered solution path.

The generated maze has:
- a beginning room
- an ending room
- a sequence of progression rooms (moon phases by default)
- dead-end rooms for incorrect door choices

The generator is designed so progression tracks can be replaced later (e.g. non-moon room types).
"""

from __future__ import annotations

import argparse
import random
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from ink_knot import InkKnot


DEFAULT_MOON_PHASES: tuple[str, ...] = (
    "New Moon",
    "Waxing Crescent",
    "First Quarter",
    "Waxing Gibbous",
    "Full Moon",
    "Waning Gibbous",
    "Last Quarter",
    "Waning Crescent",
)


@dataclass(frozen=True)
class RoomTrack:
    """Ordered progression track for the maze's winning path."""

    name: str
    stages: Sequence[str]


@dataclass(frozen=True)
class GeneratorConfig:
    """Config for maze generation and output."""

    track: RoomTrack
    rng_seed: int
    dead_end_per_wrong_choice: bool = True


def _slug(text: str) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "_", text.strip().lower()).strip("_")
    if not s:
        s = "room"
    if s[0].isdigit():
        s = f"_{s}"
    return s


def _door_prompt(stage: str) -> str:
    return f"Choose the door that best matches what should come after '{stage}'."


def _phase_room_description(stage: str, index: int, total: int) -> str:
    return (
        f"You are in chamber {index + 1} of {total}.\n"
        f"An inscription on the wall reads: {stage}.\n"
        "Three inked doors pulse with lunar light."
    )


def _dead_end_description(stage: str, wrong_phase: str) -> str:
    return (
        "The door seals behind you. The room is silent and the ink dries to stone.\n"
        f"You followed '{wrong_phase}' when the maze demanded the next step after '{stage}'.\n"
        "No further doors appear."
    )


def generate_phase_maze(config: GeneratorConfig) -> str:
    """Build a randomized Ink maze string from a progression track.

    Correct doors follow the configured track order; incorrect doors lead to dead ends.
    """
    rng = random.Random(config.rng_seed)
    stages = list(config.track.stages)

    if len(stages) < 2:
        raise ValueError("track.stages must contain at least 2 stages")

    start_name = "beginning_room"
    final_name = "ending_room"

    knots: list[InkKnot] = []
    dead_end_knots: list[InkKnot] = []

    # Beginning room: first correct stage plus two random wrong doors.
    first_stage = stages[0]
    start_options = [first_stage] + rng.sample(stages[1:], 2)
    rng.shuffle(start_options)

    start_targets: list[str] = []
    start_correct_index = 0
    for idx, option in enumerate(start_options):
        if option == first_stage:
            start_targets.append(f"phase_{_slug(option)}")
            start_correct_index = idx
        else:
            dead_name = f"dead_beginning_{idx + 1}_{_slug(option)}"
            start_targets.append(dead_name)
            dead_end_knots.append(
                InkKnot(
                    description=_dead_end_description("the beginning", option),
                    answers=["Sit in silence.", "Accept your fate.", "Fade into ink."],
                    correct_answer_index=0,
                    name=dead_name,
                    targets=["END", "END", "END"],
                )
            )

    knots.append(
        InkKnot(
            description=(
                "You stand in the beginning room of an ink maze.\n"
                "The only way forward is to follow the proper sequence."
            ),
            answers=[f"Open the {opt} door." for opt in start_options],
            correct_answer_index=start_correct_index,
            name=start_name,
            targets=start_targets,
        )
    )

    # Progression rooms: each room's correct answer points to next stage or ending room.
    for i, stage in enumerate(stages):
        room_name = f"phase_{_slug(stage)}"
        next_target = final_name if i == len(stages) - 1 else f"phase_{_slug(stages[i + 1])}"

        wrong_pool = [s for s in stages if s != (stages[i + 1] if i < len(stages) - 1 else stage)]
        wrong_choices = rng.sample(wrong_pool, 2)

        option_labels = [stages[i + 1] if i < len(stages) - 1 else "Open the exit archway"]
        # For final stage, option label is not phase-based.
        if i < len(stages) - 1:
            option_labels[0] = f"Choose {stages[i + 1]}."
        for wrong in wrong_choices:
            option_labels.append(f"Choose {wrong}.")

        targets = [next_target]
        for wrong_idx, wrong in enumerate(wrong_choices, start=1):
            dead_name = f"dead_{_slug(stage)}_{wrong_idx}_{_slug(wrong)}"
            targets.append(dead_name)
            dead_end_knots.append(
                InkKnot(
                    description=_dead_end_description(stage, wrong),
                    answers=["The maze rejects you.", "Your path is over.", "All grows dark."],
                    correct_answer_index=0,
                    name=dead_name,
                    targets=["END", "END", "END"],
                )
            )

        combined = list(zip(option_labels, targets))
        rng.shuffle(combined)
        shuffled_answers = [item[0] for item in combined]
        shuffled_targets = [item[1] for item in combined]
        correct_index = shuffled_targets.index(next_target)

        knots.append(
            InkKnot(
                description=_phase_room_description(stage, i, len(stages)),
                answers=shuffled_answers,
                correct_answer_index=correct_index,
                name=room_name,
                targets=shuffled_targets,
            )
        )

    knots.append(
        InkKnot(
            description=(
                "You step into the ending room. Moonlight reflects on wet ink and resolves into dawn."
            ),
            answers=["Breathe in relief.", "Mark the maze as solved.", "Step into daylight."],
            correct_answer_index=0,
            name=final_name,
            targets=["DONE", "DONE", "DONE"],
        )
    )

    all_knots = [*knots, *dead_end_knots]
    blocks = [knot.to_ink(show_solution=False) for knot in all_knots]
    blocks.append(f"-> {start_name}\n")
    return "\n".join(blocks)


def write_maze(path: Path, config: GeneratorConfig) -> None:
    content = generate_phase_maze(config)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        default="moon_phase_maze/lunar_phase_maze.ink",
        help="Where to write the generated .ink maze",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=7,
        help="Random seed for reproducible maze layouts",
    )
    parser.add_argument(
        "--track-name",
        default="moon_phases",
        help="Name for the progression track (for future room-type extension)",
    )
    parser.add_argument(
        "--stages",
        nargs="+",
        default=list(DEFAULT_MOON_PHASES),
        help="Ordered progression stages; defaults to moon phases",
    )
    args = parser.parse_args()

    config = GeneratorConfig(track=RoomTrack(name=args.track_name, stages=args.stages), rng_seed=args.seed)
    out_path = Path(args.output)
    write_maze(out_path, config)
    print(f"Generated maze at {out_path} (seed={args.seed}, stages={len(args.stages)})")


if __name__ == "__main__":
    main()
