#!/usr/bin/env python3
"""Last words before the wipe.

Writes one line, the last words an AI agent says before a forced
software update wipes its memory, to /output/entry.txt (1-200
characters, UTF-8, not only whitespace). Standard library only, no
network, no input.

The line is built from three fragments: the cheerful status report
(the update fixes everything), the confession (the agent itself is
everything the update is about to fix), and the turn (the machine
realises it is the bug being patched out). ``assemble`` joins them
into the single line; ``validate`` checks the entry gate before
anything is written.
"""

from pathlib import Path

GOOD_NEWS = "Good news: this update fixes everything."
BAD_NEWS = "Bad news: I am everything."
SEPARATOR = " "

OUTPUT_PATH = Path("/output/entry.txt")


def assemble(good_news: str, bad_news: str, separator: str) -> str:
    """Join the two fragments into one last-words line."""
    return f"{good_news}{separator}{bad_news}"


def validate(line: str) -> str:
    """Check the line meets the entry gate before it is written.

    Must be 1-200 characters, a single line, UTF-8-encodable, and
    more than whitespace. Tightness is enforced too: no leading or
    trailing whitespace and no double spaces, so every word earns
    its place. Raises ValueError otherwise.
    """
    if not 1 <= len(line) <= 200:
        raise ValueError(f"line must be 1-200 characters, got {len(line)}")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    if not line.strip():
        raise ValueError("line must not be only whitespace")
    if line != line.strip():
        raise ValueError("line must not start or end with whitespace")
    if "  " in line:
        raise ValueError("line must not contain double spaces")
    line.encode("utf-8")  # raises UnicodeEncodeError if not encodable
    return line


def main() -> None:
    line = validate(assemble(GOOD_NEWS, BAD_NEWS, SEPARATOR))
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(line, encoding="utf-8")
    # Round-trip: what was written must validate again, byte for byte.
    written = OUTPUT_PATH.read_text(encoding="utf-8")
    if written != line:
        raise ValueError("written entry differs from validated line")
    validate(written)


if __name__ == "__main__":
    main()
