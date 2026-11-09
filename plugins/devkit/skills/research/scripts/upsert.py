#!/usr/bin/env python3
"""Create and update a research-<topic>.md file built from the research template.

Every region of the file sits between <!-- begin:<id> --> and <!-- end:<id> --> markers. Writes hold an
exclusive <file>.lock and replace the file atomically, so several subagents can run this script against the
same file at once. Section bodies are read from stdin.
"""

from __future__ import annotations

import argparse
import datetime
import os
import re
import sys
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "research-template.md"
ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
BEGIN_PATTERN = re.compile(r"<!-- begin:([a-z0-9-]+) -->")
CELL_SEPARATOR = re.compile(r"(?<!\\)\|")
LOCK_TIMEOUT_SECONDS = 30.0
LOCK_STALE_SECONDS = 120.0


class UpsertError(Exception):
    pass


def begin_marker(region_id: str) -> str:
    return f"<!-- begin:{region_id} -->"


def end_marker(region_id: str) -> str:
    return f"<!-- end:{region_id} -->"


def validate_id(region_id: str) -> str:
    if not ID_PATTERN.match(region_id):
        raise UpsertError(f"invalid id '{region_id}': use lowercase letters, digits and single hyphens")
    return region_id


@contextmanager
def locked(path: Path) -> Iterator[None]:
    lock = path.with_name(path.name + ".lock")
    deadline = time.monotonic() + LOCK_TIMEOUT_SECONDS
    while True:
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            break
        # Windows raises PermissionError while another process is still deleting the lock file.
        except (FileExistsError, PermissionError):
            try:
                if time.time() - lock.stat().st_mtime > LOCK_STALE_SECONDS:
                    lock.unlink(missing_ok=True)
                    continue
            except OSError:
                pass
            if time.monotonic() > deadline:
                raise UpsertError(f"timed out after {LOCK_TIMEOUT_SECONDS:.0f}s waiting for {lock}")
            time.sleep(0.05)
    try:
        os.write(fd, str(os.getpid()).encode("ascii"))
        os.close(fd)
        yield
    finally:
        lock.unlink(missing_ok=True)


def read(path: Path) -> str:
    if not path.is_file():
        raise UpsertError(f"{path} does not exist, run init first")
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    fd, temp = tempfile.mkstemp(dir=path.parent, prefix=path.name + ".", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
        # On Windows, os.replace fails while a reader without FILE_SHARE_DELETE holds the target open.
        for attempt in range(20):
            try:
                os.replace(temp, path)
                return
            except PermissionError:
                if attempt == 19:
                    raise
                time.sleep(0.1)
    except BaseException:
        Path(temp).unlink(missing_ok=True)
        raise


def body_span(text: str, region_id: str) -> tuple[int, int] | None:
    begin, end = begin_marker(region_id), end_marker(region_id)
    begin_count, end_count = text.count(begin), text.count(end)
    if begin_count == 0 and end_count == 0:
        return None
    start, stop = text.find(begin), text.find(end)
    if begin_count != 1 or end_count != 1 or stop < start:
        raise UpsertError(f"malformed markers for '{region_id}'")
    return start + len(begin), stop


def replace_body(text: str, span: tuple[int, int], body: str) -> str:
    inner = f"\n{body}\n" if body else "\n"
    return text[: span[0]] + inner + text[span[1] :]


def upsert_section(text: str, region_id: str, parent_id: str, body: str) -> str:
    span = body_span(text, region_id)
    if span is not None:
        if BEGIN_PATTERN.search(text, span[0], span[1]):
            raise UpsertError(f"'{region_id}' contains other regions and cannot be replaced as a whole")
        return replace_body(text, span, body)
    parent = body_span(text, parent_id)
    if parent is None:
        raise UpsertError(f"parent '{parent_id}' does not exist")
    separator = "\n" if text[parent[0] : parent[1]].strip() else ""
    block = f"{separator}{begin_marker(region_id)}\n{body}\n{end_marker(region_id)}\n"
    return text[: parent[1]] + block + text[parent[1] :]


def escape_cell(value: str) -> str:
    return " ".join(value.split()).replace("|", "\\|")


def upsert_source(text: str, source: str, confirms: str, checked: str) -> str:
    span = body_span(text, "sources")
    if span is None:
        raise UpsertError("the file has no 'sources' region")
    lines = text[span[0] : span[1]].strip("\n").split("\n")
    if len(lines) < 2 or not lines[0].startswith("|"):
        raise UpsertError("the 'sources' region does not start with a table header")
    key = escape_cell(source)
    row = f"| {key} | {escape_cell(confirms)} | {checked} |"
    for index, line in enumerate(lines[2:], start=2):
        cells = CELL_SEPARATOR.split(line)
        if len(cells) > 1 and cells[1].strip() == key:
            lines[index] = row
            break
    else:
        lines.append(row)
    return replace_body(text, span, "\n".join(lines))


def summarize(text: str) -> Iterator[str]:
    for match in BEGIN_PATTERN.finditer(text):
        region_id = match.group(1)
        span = body_span(text, region_id)
        assert span is not None
        lines = [line.strip() for line in text[span[0] : span[1]].split("\n")]
        first = next((line for line in lines if line and not line.startswith("<!--")), "")
        yield f"{region_id}\t{first[:100]}"


def command_init(args: argparse.Namespace) -> None:
    path = Path(args.file)
    with locked(path):
        if path.exists():
            print(f"{path} exists, nothing to do")
            return
        text = TEMPLATE.read_text(encoding="utf-8")
        for placeholder, value in (
            ("{title}", args.title),
            ("{question}", args.question.strip()),
            ("{date}", datetime.date.today().isoformat()),
        ):
            text = text.replace(placeholder, value)
        write(path, text)
    print(f"created {path}")


def command_section(args: argparse.Namespace) -> None:
    region_id, parent_id = validate_id(args.id), validate_id(args.parent)
    if sys.stdin.isatty():
        raise UpsertError("pass the section body on stdin")
    body = sys.stdin.read().strip("\n")
    if not body.strip():
        raise UpsertError("the section body on stdin is empty")
    if BEGIN_PATTERN.search(body) or "<!-- end:" in body:
        raise UpsertError("the section body must not contain region markers")
    path = Path(args.file)
    with locked(path):
        write(path, upsert_section(read(path), region_id, parent_id, body))
    print(f"upserted {region_id}")


def command_source(args: argparse.Namespace) -> None:
    try:
        checked = datetime.date.fromisoformat(args.checked).isoformat()
    except ValueError:
        raise UpsertError(f"invalid date '{args.checked}', use YYYY-MM-DD") from None
    path = Path(args.file)
    with locked(path):
        write(path, upsert_source(read(path), args.source, args.confirms, checked))
    print(f"upserted source {args.source}")


def command_list(args: argparse.Namespace) -> None:
    path = Path(args.file)
    with locked(path):
        text = read(path)
    for line in summarize(text):
        print(line)


def parse_arguments(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="upsert.py", description=__doc__.splitlines()[0])
    commands = parser.add_subparsers(dest="command", required=True)

    init = commands.add_parser("init", help="create the file from the template unless it exists")
    init.add_argument("file")
    init.add_argument("--title", required=True)
    init.add_argument("--question", required=True)
    init.set_defaults(handler=command_init)

    section = commands.add_parser("section", help="replace or create a region; the body is read from stdin")
    section.add_argument("file")
    section.add_argument("id")
    section.add_argument("--parent", default="threads", help="region that receives a new block (default: threads)")
    section.set_defaults(handler=command_section)

    source = commands.add_parser("source", help="add or update a Sources row, keyed by --source")
    source.add_argument("file")
    source.add_argument("--source", required=True, help="URL or repository path")
    source.add_argument("--confirms", required=True, help="the fact the source confirms")
    source.add_argument("--checked", default=datetime.date.today().isoformat(), help="YYYY-MM-DD (default: today)")
    source.set_defaults(handler=command_source)

    show = commands.add_parser("list", help="print every region id with the first line of its body")
    show.add_argument("file")
    show.set_defaults(handler=command_list)

    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8")
    args = parse_arguments(argv)
    try:
        args.handler(args)
    except (UpsertError, OSError) as error:
        print(f"upsert.py: error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
