"""Provide tests for the main program."""

import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from imdown.imdown import main, parse_args


def test_parse_args():
    """Test argument parsing."""
    testargs = ["imdown", "path/to/directory"]
    with patch.object(sys, "argv", testargs):
        args = parse_args()
        assert args.directory == Path("path/to/directory")
        assert args.filetypes == ["pdf", "png"]
        assert args.depth is None
        # Add more assertions for other arguments


def test_main_with_reference(tmp_path):
    """Test main function with a reference file."""
    # Create a reference file
    reference_path = tmp_path / "reference.md"
    reference_path.write_text("![ref1](ref1.png)\n![ref2](ref2.pdf)\n")

    # Create a temporary directory with some files
    temp_dir = TemporaryDirectory()
    temp_path = Path(temp_dir.name)
    (temp_path / "dir1").mkdir()
    (temp_path / "dir1" / "file1.png").touch()
    (temp_path / "dir2").mkdir()
    (temp_path / "dir2" / "file2.pdf").touch()

    # Run the main function with reference file
    testargs = [
        "imdown",
        str(temp_path),
        "--reference",
        str(reference_path),
        "-o",
        str(temp_path / "updated.md"),
    ]
    with patch.object(sys, "argv", testargs):
        main()

    # Check if the reference file is updated
    updated_reference_content = (temp_path / "updated.md").read_text()
    assert "![dir1/file1.png](dir1/file1.png)" in updated_reference_content
    assert "![dir2/file2.pdf](dir2/file2.pdf)" in updated_reference_content


def test_main_without_reference(tmp_path):
    """Test main function without a reference file."""
    # Create a temporary directory with some files
    temp_dir = TemporaryDirectory()
    temp_path = Path(temp_dir.name)
    (temp_path / "dir1").mkdir()
    (temp_path / "dir1" / "file1.png").touch()
    (temp_path / "dir2").mkdir()
    (temp_path / "dir2" / "file2.pdf").touch()

    outpath = temp_path / "new.md"

    # Run the main function without a reference file
    testargs = [
        "imdown",
        str(temp_path),
        "-o",
        str(outpath),
    ]
    with patch.object(sys, "argv", testargs):
        main()

    # check if the output contains the expected paths
    result = outpath.read_text()
    assert "![dir1/file1.png](dir1/file1.png)" in result
    assert "![dir2/file2.pdf](dir2/file2.pdf)" in result


def test_main_without_outfile(tmp_path):
    """Test main function without a out file."""
    # Create a temporary directory with some files
    temp_dir = TemporaryDirectory()
    temp_path = Path(temp_dir.name)
    (temp_path / "dir1").mkdir()
    (temp_path / "dir1" / "file1.png").touch()
    (temp_path / "dir2").mkdir()
    (temp_path / "dir2" / "file2.pdf").touch()

    # Run the main function without a reference file
    testargs = [
        "imdown",
        str(temp_path),
    ]
    with patch.object(sys, "argv", testargs):
        main()


def test_main_with_build_dir(tmp_path):
    """Test main function with a build directory."""
    # Create a temporary directory with some files
    temp_dir = TemporaryDirectory()
    temp_path = Path(temp_dir.name)
    (temp_path / "dir1").mkdir()
    (temp_path / "dir1" / "file1.png").touch()
    (temp_path / "dir2").mkdir()
    (temp_path / "dir2" / "file2.pdf").touch()

    outpath = temp_path / "new.md"

    # Run the main function without a reference file
    testargs = [
        "imdown",
        str(temp_path),
        "-o",
        str(outpath),
        "-b",
        str(temp_path),
    ]
    with patch.object(sys, "argv", testargs):
        main()

    # check if the output contains the expected paths
    result = outpath.read_text()
    assert "![dir1/file1.png](dir1/file1.png)" in result
    assert "![dir2/file2.pdf](dir2/file2.pdf)" in result


def test_main_filetypes(tmp_path):
    """Test main function with specified filetypes."""
    # Create a temporary directory with some files
    temp_dir = TemporaryDirectory()
    temp_path = Path(temp_dir.name)
    (temp_path / "dir1").mkdir()
    (temp_path / "dir1" / "file1.png").touch()
    (temp_path / "dir2").mkdir()
    (temp_path / "dir2" / "file2.pdf").touch()

    outpath = temp_path / "new.md"

    # Run the main function with specified filetypes
    testargs = [
        "imdown",
        str(temp_path),
        "-o",
        str(outpath),
        "-f",
        "pdf",
    ]
    with patch.object(sys, "argv", testargs):
        main()

    # check if the output contains the expected paths
    result = outpath.read_text()
    assert "![dir2/file2.pdf](dir2/file2.pdf)" in result
    assert "![dir1/file1.png]" not in result


def test_main_ignore(tmp_path):
    """Test main function with ignore option."""
    # Create a temporary directory with some files
    temp_dir = TemporaryDirectory()
    temp_path = Path(temp_dir.name)
    (temp_path / "dir1").mkdir()
    (temp_path / "dir1" / "file1.png").touch()
    (temp_path / "dir2").mkdir()
    (temp_path / "dir2" / "file2.pdf").touch()
    (temp_path / "ignore_dir").mkdir()

    outpath = temp_path / "new.md"

    # Specify ignore option in the command line
    testargs = [
        "imdown",
        str(temp_path),
        "-o",
        str(outpath),
        "-i",
        "ignore_dir",
    ]
    with patch.object(sys, "argv", testargs):
        main()

    # check if the output contains the expected paths
    result = outpath.read_text()
    assert "![ignore_dir]" not in result  # ignore_dir should be excluded
    assert "![dir1/file1.png](dir1/file1.png)" in result
    assert "![dir2/file2.pdf](dir2/file2.pdf)" in result


def test_main_absolute(tmp_path):
    """Test main function with absolute option."""
    # Create a temporary directory with some files
    temp_dir = TemporaryDirectory()
    temp_path = Path(temp_dir.name)
    (temp_path / "dir1").mkdir()
    (temp_path / "dir1" / "file1.png").touch()
    (temp_path / "dir2").mkdir()
    (temp_path / "dir2" / "file2.pdf").touch()

    outpath = temp_path / "new.md"

    # Specify absolute option in the command line
    testargs = [
        "imdown",
        str(temp_path),
        "-o",
        str(outpath),
        "-a",
    ]
    with patch.object(sys, "argv", testargs):
        main()

    # check if the output contains the expected absolute paths
    result = outpath.read_text()
    file_1_absolute = (temp_path / "dir1" / "file1.png").resolve()
    file_2_absolute = (temp_path / "dir2" / "file2.pdf").resolve()
    assert f"![{file_1_absolute}]({file_1_absolute})" in result
    assert f"![{file_2_absolute}]({file_2_absolute})" in result


def test_main_depth(tmp_path):
    """Test main function with depth option."""
    # Create a temporary directory with some files and subdirectories
    temp_dir = TemporaryDirectory()
    temp_path = Path(temp_dir.name)
    (temp_path / "dir1").mkdir()
    (temp_path / "dir1" / "file1.png").touch()
    (temp_path / "dir2").mkdir()
    (temp_path / "dir2" / "file2.pdf").touch()
    (temp_path / "dir3").mkdir()
    (temp_path / "dir3" / "subdir").mkdir()
    (temp_path / "dir3" / "subdir" / "file3.pdf").touch()

    outpath = temp_path / "new.md"

    # Specify depth option in the command line
    testargs = [
        "imdown",
        str(temp_path),
        "-o",
        str(outpath),
        "-d",
        "1",
    ]
    with patch.object(sys, "argv", testargs):
        main()

    # check if the output contains paths up to depth 1
    result = outpath.read_text()
    assert "![dir1/file1.png](dir1/file1.png)" in result
    assert "![dir2/file2.pdf](dir2/file2.pdf)" in result
    assert "![dir3]" not in result  # dir3 should be excluded


def test_main_absolute_with_reference(tmp_path):
    """Test main function with absolute option and a reference file."""
    # Create a reference file
    reference_path = tmp_path / "reference.md"
    reference_path.write_text("![ref1](ref1.png)\n![ref2](ref2.pdf)\n")

    # Create a temporary directory with some files
    temp_dir = TemporaryDirectory()
    temp_path = Path(temp_dir.name)
    (temp_path / "dir1").mkdir()
    (temp_path / "dir1" / "file1.png").touch()
    (temp_path / "dir2").mkdir()
    (temp_path / "dir2" / "file2.pdf").touch()

    outpath = temp_path / "new.md"

    # Specify absolute option in the command line
    testargs = [
        "imdown",
        str(temp_path),
        "--reference",
        str(reference_path),
        "-o",
        str(outpath),
        "-a",
    ]
    with patch.object(sys, "argv", testargs):
        main()

    file_1_absolute = (temp_path / "dir1" / "file1.png").resolve()
    file_2_absolute = (temp_path / "dir2" / "file2.pdf").resolve()

    # Check if the output contains the expected absolute paths
    result = outpath.read_text()
    assert f"![{file_1_absolute}]({file_1_absolute})" in result
    assert f"![{file_2_absolute}]({file_2_absolute})" in result
