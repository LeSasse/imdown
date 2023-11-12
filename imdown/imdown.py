"""Provide main command line tool."""

import os
import re
from argparse import ArgumentParser
from pathlib import Path


def parse_args():
    """Parse the arguments."""
    parser = ArgumentParser(
        prog="imdown",
        description=(
            "Collect images from a directory tree and add write them to a "
            "markdown file that can be compiled using pandoc. "
            "(Author: Leonard Sasse)"
        ),
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
    parser.add_argument(
        "-r",
        "--reference",
        help=(
            "Path to an existing reference markdown file, which will be "
            "updated with new plots of filetypes, but where old plots with "
            "adjusted captions or other text passages will not be overwritten."
        ),
        type=Path,
    )
    parser.add_argument(
        "-b",
        "--build_directory",
        help=(
            "By default 'imdown' writes paths in the resulting markdown file"
            " relative to the directory in which the markdown will be written"
            " as it assumes 'pandoc' will be used in that directory to convert"
            " the markdown to another format. If that is not desired, a "
            "'build_directory' can be specified. If this is specified, all "
            "paths will be relative from this 'build_directory'."
        ),
        type=Path,
    )
    parser.add_argument(
        "-i",
        "--ignore",
        help=("Ignore certain sub-directories based on a pattern."),
        type=str,
        nargs="*",
    )
    parser.add_argument(
        "-a",
        "--absolute",
        action="store_true",
        help="Write out all paths as absolute.",
    )
    parser.add_argument(
        "-d",
        "--depth",
        default=None,
        type=int,
        help=(
            "Specify how many levels the program should walk the directory "
            "tree. If None (default) the program will walk all the way."
            " Specify 0 to only consider files in the initial directory."
            " For each level deeper add +1."
        ),
    )
    return parser.parse_args()


def _compare_and_adjust(paths, reference, rootdir, absolute):
    """Compare the paths from walking directory tree to reference md file.

    paths: list of Path
        Paths to the figures collected by walking the directory tree.
    reference: Path
        Path to the reference markdown file.
    rootdir: Path
        Path to the directory from which paths in the resulting markdown should
        be relative.

    """
    reference_root = reference.parents[0]
    with open(reference) as f:
        reference_text = f.read()
        paths_in_parentheses = re.findall(r"!\[.*?\]\((.*?)\)", reference_text)
        if absolute:
            mapping_new_paths = {
                old_path: (reference_root / old_path).resolve()
                for old_path in paths_in_parentheses
            }
        else:
            mapping_new_paths = {
                old_path: os.path.relpath(
                    reference_root / old_path, start=rootdir
                )
                for old_path in paths_in_parentheses
            }

        for original_path, new_path in mapping_new_paths.items():
            reference_text = reference_text.replace(
                str(original_path), str(new_path)
            )

        filtered = []
        for path in paths:
            if str(path) not in reference_text:
                filtered.append(path)

        for path in filtered:
            reference_text += f"\n![{path}]({path})\n"

    return reference_text


def main():
    """Run the main program."""
    args = parse_args()

    if args.build_directory is not None:
        root_directory_of_md = args.build_directory
    elif args.outfile is not None:
        root_directory_of_md = args.outfile.parents[0]
    else:
        root_directory_of_md = Path(".")

    args.filetypes = [f".{x}" for x in args.filetypes]
    outpaths = []
    for dirpath, _, filenames in os.walk(args.directory):
        # Calculate the depth relative to args.directory
        current_depth = len(Path(dirpath).relative_to(args.directory).parts)
        if args.ignore is not None and any(
            ignore in dirpath for ignore in args.ignore
        ):
            continue

        if args.depth is None or current_depth <= args.depth:
            if filenames:
                for filename in filenames:
                    if args.ignore is not None and any(
                        ignore in filename for ignore in args.ignore
                    ):
                        continue

                    if Path(filename).suffix in args.filetypes:
                        if args.absolute:
                            path = (Path(dirpath) / filename).resolve()
                        else:
                            path = os.path.relpath(
                                Path(dirpath) / filename,
                                start=root_directory_of_md,
                            )

                        outpaths.append(Path(path))

    if args.reference is not None:
        outstring = _compare_and_adjust(
            outpaths,
            args.reference,
            rootdir=root_directory_of_md,
            absolute=args.absolute,
        )
    else:
        outstring = "".join([f"\n![{path}]({path})\n" for path in outpaths])

    if args.outfile is None:
        print(outstring)
    else:
        with open(args.outfile, "w") as f:
            f.write(outstring)
