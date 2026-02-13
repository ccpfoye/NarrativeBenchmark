from dataclasses import dataclass
from typing import Sequence, Optional
import re
import textwrap

@dataclass(frozen=True)
class InkKnot:
    """
    A Python-side representation of a single ink knot that can render itself
    into valid .ink syntax.

    - description becomes content lines inside the knot
    - answers become three * [choice] lines
    - targets are the divert destinations for each choice (required to be "proper ink")
    """
    description: str
    answers: Sequence[str]                 # length 3
    correct_answer_index: int              # 0..2
    name: str                              # ink knot name, e.g. "library_entrance"
    targets: Sequence[str]                 # length 3, e.g. ["open_drawer", "follow_whisper", "snuff_candle"]

    def __post_init__(self):
        if len(self.answers) != 3:
            raise ValueError("answers must have exactly 3 items")
        if len(self.targets) != 3:
            raise ValueError("targets must have exactly 3 items")
        if not (0 <= self.correct_answer_index < 3):
            raise ValueError("correct_answer_index must be 0..2")

        # ink identifiers: single token, no spaces (recommended) :contentReference[oaicite:1]{index=1}
        bad = [x for x in [self.name, *self.targets] if not _is_ink_identifier(x)]
        if bad:
            raise ValueError(f"Invalid ink identifier(s): {bad}")

    def to_ink(self, width: int = 0, show_solution: bool = False, end: Optional[str] = None) -> str:
        """
        Render a complete ink knot.

        width=0 disables wrapping. If >0, wraps description lines for readability.
        show_solution=True appends an inline comment on the correct option.
        end can be:
          - "END" to add '-> END'
          - a knot name to add '-> that_knot'
          - None to add nothing
        """
        lines: list[str] = [f"=== {self.name} ===", ""]

        desc = self.description.strip()
        if desc:
            if width and width > 0:
                lines += textwrap.fill(desc, width=width).splitlines()
            else:
                lines += desc.splitlines()

        lines.append("")

        for i, (ans, tgt) in enumerate(zip(self.answers, self.targets)):
            choice_text = _escape_choice_text(ans.strip())
            # Choice text in [] is a common pattern to suppress echoing in output :contentReference[oaicite:2]{index=2}
            choice_line = f"* [{choice_text}] -> {tgt}"  # :contentReference[oaicite:3]{index=3}

            if show_solution and i == self.correct_answer_index:
                choice_line += " // correct"

            lines.append(choice_line)

        if end is not None:
            lines.append("")
            lines.append(f"-> {end}")

        return "\n".join(lines).rstrip() + "\n"


def _is_ink_identifier(s: str) -> bool:
    # Conservative: letters/nums/underscore, must start with letter/underscore.
    # (Ink can be more permissive, but this keeps you out of trouble.)
    return bool(re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", s))


def _escape_choice_text(s: str) -> str:
    """
    Keep choice text safe inside [ ... ].
    In ink, ] would terminate the bracketed choice text, so escape or replace it.
    """
    return s.replace("]", r"\]")
