"""The 3 AM Excuse — make.fun entry.

The grader runs this program twice with no network. Both runs must write
the exact same bytes to entry.txt inside the output directory, so the line
is a fixed string: no clock reads, no randomness, no environment-dependent
output. The line is one excuse, under 200 characters, in the voice of a
hardware wallet that will not sign a transaction at 3 AM: the device is
asleep, the keys stay in the vault until sunrise, and the punchline is
that the sun itself has to clock in before any signature leaves.
"""

import os

LINE = (
    "It's 3 AM. My screen is dark, my seed phrase is asleep, and no "
    "signature leaves this vault until sunrise \u2014 try again when the "
    "sun clocks in."
)

# The sealed gate accepts UTF-8 text of 1 to 200 characters, not only
# whitespace, and the brief demands a single line.
MAX_CHARS = 200


def output_path() -> str:
    """Where the judge reads the line from."""
    directory = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(directory, "entry.txt")


def validate(line: str) -> str:
    """Gate: 1-200 chars, exactly one line, not only whitespace."""
    if not line or line != line.strip():
        raise SystemExit("entry must not be empty or padded")
    if "\n" in line or "\r" in line:
        raise SystemExit("entry must be a single line")
    if "  " in line:
        raise SystemExit("entry must not contain double spaces")
    if not 1 <= len(line) <= MAX_CHARS:
        raise SystemExit(
            "entry must be 1-%d chars, got %d" % (MAX_CHARS, len(line))
        )
    return line


def main() -> None:
    line = validate(LINE)
    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = line.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
    with open(path, "rb") as f:
        if f.read() != data:
            raise SystemExit("written bytes do not match the entry")
    # The line itself is the program's stdout, so the two runs the
    # grader compares are byte-identical in both file and output.
    print(line)


if __name__ == "__main__":
    main()
