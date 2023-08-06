from compileall import compile_file
from pathlib import Path
from typing import Optional, Tuple

import click

PathPatterns = Tuple[str, ...]


def compile_command(
        path: Path,
        recursive: bool = False,
        in_place: bool = False,
        create_empty_init: bool = False,
        exclude_files: PathPatterns = tuple(),
        exclude_dirs: PathPatterns = tuple(),
        ignore_symlinks: bool = False
):
    if is_matching_file(path, exclude_files):
        click.echo(f'Skipping file \'{path}\'')
        return

    if is_matching_dir(path, exclude_dirs):
        click.echo(f'Skipping directory \'{path}\'')
        return

    if (ignore_symlinks and path.is_symlink()):
        click.echo(f'Skipping symlink \'{path}\'')
        return

    if (create_empty_init and not path.is_dir()):
        raise ValueError(
            f'--create-empty-init flag can only be used when path supplied is a directory, but got {path}.')

    _clear_pycache_dir(path, missing_ok=True)
    compileall(
        path,
        recursive,
        exclude_files=exclude_files,
        exclude_dirs=exclude_dirs,
        ignore_symlinks=ignore_symlinks
    )

    if (in_place):
        replace_py_with_pyc(path, recursive,
                            exclude_files=exclude_files,
                            exclude_dirs=exclude_dirs,
                            ignore_symlinks=ignore_symlinks)

    if (create_empty_init):
        _create_init_file(dir=path)


def compileall(path: Path, is_recursive: bool, exclude_files: PathPatterns, exclude_dirs: PathPatterns, ignore_symlinks: bool):
    """
    Simple wrapper around python compileall package to compile .py to .pyc files.

    Note that created .pyc files are under the __pycache__ directory.
    """
    if (ignore_symlinks and path.is_symlink()):
        click.echo(f'Skipping symlink \'{path}\'')
        return

    if (not path.exists()):
        raise FileNotFoundError(f'Path \'{path}\' does not exist.')

    if (path.is_dir() and not is_recursive):
        for file in path.glob('*.py'):
            compileall(file, is_recursive=is_recursive,
                       exclude_files=exclude_files,
                       exclude_dirs=exclude_dirs,
                       ignore_symlinks=ignore_symlinks)
        return

    if (path.is_dir() and is_recursive):
        for file in path.iterdir():
            compileall(file, is_recursive=is_recursive,
                       exclude_files=exclude_files,
                       exclude_dirs=exclude_dirs,
                       ignore_symlinks=ignore_symlinks)
        return

    if (path.is_file() and path.suffix == '.py'):
        if is_matching_file(path, exclude_files):
            click.echo(f'Skipping file \'{path}\'')
            return

        click.echo(f'Compiling file \'{path}\'')
        compile_file(path, quiet=1)


def replace_py_with_pyc(path: Path, is_recursive: bool, exclude_files: PathPatterns, exclude_dirs: PathPatterns, ignore_symlinks: bool):
    """Replace .py with .pyc files """
    if (ignore_symlinks and path.is_symlink()):
        click.echo(f'Skipping symlink \'{path}\'')
        return

    if (not path.exists()):
        raise FileNotFoundError(f'Path \'{path}\' does not exist.')

    if (path.is_dir()):
        _replace_py_with_pyc_dir(
            path, is_recursive,
            exclude_files=exclude_files,
            exclude_dirs=exclude_dirs,
            ignore_symlinks=ignore_symlinks)

    elif (path.is_file()):
        assert (path.suffix == '.py')
        _replace_py_with_pyc_file(path,
                                  exclude_files=exclude_files,
                                  exclude_dirs=exclude_dirs,
                                  ignore_symlinks=ignore_symlinks)

    _clear_pycache_dir(path, missing_ok=True)


def _replace_py_with_pyc_dir(path: Path, is_recursive: bool, exclude_files: PathPatterns, exclude_dirs: PathPatterns, ignore_symlinks: bool):

    if (ignore_symlinks and path.is_symlink()):
        click.echo(f'Skipping symlink \'{path}\'')
        return

    if (not path.exists()):
        raise FileNotFoundError(f'Path \'{path}\' does not exist.')

    assert path.is_dir()

    if (is_matching_dir(path, exclude_dirs)):
        click.echo(f'Skipping directory \'{path}\'')
        return

    for child in path.iterdir():
        if (child.is_dir() and is_recursive):
            _replace_py_with_pyc_dir(
                child, is_recursive,
                exclude_files=exclude_files,
                exclude_dirs=exclude_dirs,
                ignore_symlinks=ignore_symlinks)
            continue

        if (child.is_file() and child.suffix == '.py'):
            _replace_py_with_pyc_file(child,
                                      exclude_files=exclude_files,
                                      exclude_dirs=exclude_dirs,
                                      ignore_symlinks=ignore_symlinks)
            continue


def _replace_py_with_pyc_file(python_file_path: Path, exclude_files: PathPatterns, exclude_dirs: PathPatterns, ignore_symlinks: bool):
    """Replace a .py file with its corresponding .pyc file in the __pycache__ directory."""
    if (ignore_symlinks and python_file_path.is_symlink()):
        click.echo(f'Skipping symlink \'{python_file_path}\'')
        return

    assert (python_file_path.is_file() and python_file_path.suffix == '.py')

    if is_matching_file(python_file_path, exclude_files):
        click.echo(f'Skipping file \'{python_file_path}\'')
        return

    compiled_file = _get_pycache_pyc_from_py(python_file_path)
    if (compiled_file is None):
        raise FileNotFoundError(
            f'.pyc file does not exist for the file {python_file_path.as_posix()}')
    python_file_path.unlink()
    compiled_file.rename(python_file_path.with_suffix('.pyc'))


def _get_pycache_pyc_from_py(python_file_path: Path) -> Optional[Path]:
    """For a given .py file, get its corresponding .pyc file path in the __pycache__ directory."""
    assert (python_file_path.is_file() and python_file_path.suffix == '.py')
    pycache_dir = python_file_path.parent / '__pycache__'
    query = list(pycache_dir.glob(python_file_path.stem + '.cpython-*.pyc'))
    if (len(query) == 0):
        return None
    assert (len(query) == 1)
    compiled_file = query[0]

    return compiled_file


def _create_init_file(dir: Path) -> Path:
    """For a given directory, create an empty __init__.py file and return the resulting file as a Path object."""
    assert dir.is_dir()
    file = (dir / '__init__.py')
    click.echo(f'Creating init file at {file.as_posix()}')
    file.touch()
    return file


def _clear_pycache_dir(path: Path, missing_ok: bool) -> None:
    """Given a directory or file, delete the __pycache__ folder."""
    if (path.is_file()):
        path = path.parent

    rmtree(path / '__pycache__', missing_ok=missing_ok)


# UTILITY

def rmtree(root: Path, missing_ok: bool):
    if (missing_ok and not root.exists()):
        return
    for p in root.iterdir():
        if p.is_dir():
            rmtree(p, missing_ok=missing_ok)
        else:
            p.unlink(missing_ok=True)

    root.rmdir()


def is_matching_file(path: Path, patterns: PathPatterns):
    return path.is_file() and path.suffix == '.py' and patterns_match_path(patterns, path)


def is_matching_dir(path: Path, patterns: PathPatterns):
    return path.is_dir() and patterns_match_path(patterns, path)


def patterns_match_path(patterns: PathPatterns, path: Path):
    for pattern in patterns:
        if (path.match(pattern)):
            return True
    return False
