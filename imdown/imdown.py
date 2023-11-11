"""Provide main command line tool."""

import os
from argparse import ArgumentParser
from pathlib import Path


def parse_args():
    """Parse the arguments."""
    parser = ArgumentParser(
        "Collect images from a directory tree and add write them to a markdown"
        "file that can be compiled using pandoc."
    )
    parser.add_argument(
        "directory", help="Directory from which to collect images.", type=Path
    )
    parser.add_argument(
        "-o",
        "--outfile",
        help=(
            "Path to file in which markdown should be written. "
            "If not provided, output will be written to stdout."
        ),
        default=None,
        type=Path,
    )
    parser.add_argument(
        "-f",
        "--filetypes",
        help="File types to be collected",
        choices=["pdf", "png"],
        default=["pdf", "png"],
        nargs="*",
    )
    return parser.parse_args()


def main():
    """Run the main program."""
    args = parse_args()

    if args.outfile is not None:
        root_directory_of_md = args.outfile.parents[0]
    else:
        root_directory_of_md = Path(".")

    args.filetypes = [f".{x}" for x in args.filetypes]
    outstring = ""

    for dirpath, _, filenames in os.walk(args.directory):
        if filenames:
            for filename in filenames:
                if Path(filename).suffix in args.filetypes:
                    outstring += f"\n# {dirpath}\n"
                    path = os.path.relpath(
                        Path(dirpath) / filename, start=root_directory_of_md
                    )
                    outstring += f"\n![{filename}]({path})\n"

    if args.outfile is None:
        print(outstring)
    else:
        with open(args.outfile, "w") as f:
            f.write(outstring)
