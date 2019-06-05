#!/usr/bin/env python3
"""Find out how far from the project root you are and the paths to it."""
import argparse
import os


__version__ = '0.1.0'


def bore(*keys, max=8, plus=0, silent=True):
    """Bore down to your project root folder.

    Args:
        *keys (str): The name(s) of one or more files or dirs
            in your project's root dir. They must be files or
            dirs with names that exist exclusively in the root
            dir. Defaults to('setup.py', 'LICENSE', 'env', '.git').
        max (int): The max number of directories to travel up
            without finding a root file before quitting.
            Defaults to 8.
        plus (int): The number of file directories before root
            to stop at and return.
        silent (bool): Whether to print output or not. Used for
            bore cli.

    Returns:
        The path to the directory root, or a subdirectory if plus > 0.

    """
    # Verify argument values.
    keys = tuple(keys) if keys else ('setup.py', 'LICENSE', 'env', '.git')
    if len(keys) is 1 and keys[0] == 'None':
        keys = None
    if not isinstance(keys, tuple) or any('' == key for key in keys):
        raise ValueError(
            '*keys must contain only non-empty values, '
            'or can be left unset to use the defaults.'
        )

    this = 'bore.py'
    # Convert Windows style paths to Unix style.
    full_path = os.path.abspath(this).replace('\\', '/')
    depth = full_path.count('/') + 1

    # Create lists for printing at end.
    bullet_nums = []
    codes = []
    current_dirs = []

    # Append __file__.
    bullet_nums.append('0)')
    codes.append('__file__')
    current_dirs.append(this)

    # Start boring.
    for level in range(depth):
        # Create base code to print.
        code = 'os.path.abspath(__file__)'
        # Prep for following loop.
        current_dir = full_path
        # Wrap the code to be printed and move up from
        # the base path both the proper number of times.
        for i in range(level):
            code = f'os.path.dirname({code})'
            current_dir = os.path.dirname(current_dir)
        # Convert Windows style paths to Unix style.
        current_dir = current_dir.replace('\\', '/')

        # Create numbered bullets
        bullet_num = str(level) + ')'
        # Append level info to lists.
        bullet_nums.append(bullet_num)
        codes.append(code)
        current_dirs.append(current_dir)

        # Stop loop when we reach the project's root dir if keys exist.
        if level is 0:
            continue
        if keys:
            try:
                dir_contents = os.listdir(current_dir)
            except NotADirectoryError:
                raise NotADirectoryError('lol whoops')
            else:
                # If file/dir matches a value in keys, quit
                if any(file in dir_contents for file in keys):
                    break

        # If bore has traversed up the set max number of dirs, quit.
        if level + 1 == max:
            raise Exception(
                'Uh oh! We\'ve traversed up {max} parent directories and '
                'no files  matched "*keys" to denote a project root. '
                'Try setting "*keys" to match a file/dir in the project root, '
                'or raising "max" to traverse up a higher number of dirs '
                'before stopping.'
            ).format(max=max)

        hd_root = full_path.split('/')[0] + '/'

        # If bore reaches a hard drive root, quit.
        if current_dir == hd_root:
            raise Exception(
                f'Uh oh! We\'ve traversed up all the way to the root '
                'directory of drive "{hd_root}" and no files  matched '
                '"*keys" to denote a project root. Try setting "*keys" to '
                'match a file/dir in the project root.'
            )

    # Check that lists are equal in length.
    equal_lists = len(bullet_nums) == len(codes) == len(current_dirs)
    lists_len = len(codes)
    adjusted_len = lists_len - plus

    if equal_lists and not silent:
        # Print information for each dir level.
        for i in range(adjusted_len):
            print('{0:<4}{1} ==\n    {2}\n'.format(
                bullet_nums[i],
                codes[i],
                current_dirs[i],
            ))

    return eval(codes[adjusted_len - 1])


def cli():
    # Create CLI parser.
    parser = argparse.ArgumentParser(
        description='Bore down to your project root folder.',
    )

    # Add command line args.
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version=__version__,
    )
    parser.add_argument(
        '*keys',
        nargs='*',
        default=('setup.py', 'LICENSE', 'env', '.git'),
        type=str,
        help=(
            'The name(s) of one or more files or dirs '
            'in your project\'s root dir. They must be files or '
            'dirs with names that exist exclusively in the root '
            'dir. Defaults to "setup.py LICENSE env .git".'
        ),
    )
    parser.add_argument(
        '-m',
        '--max',
        default=8,
        type=int,
        help=(
            'The max number of directories to travel up without finding '
            'a root file before quitting. Defaults to 8.'
        )
    )
    parser.add_argument(
        '-p',
        '--plus',
        default=0,
        type=int,
        help=(
            'The number of file directories before root to stop '
            'at and return. Defaults to 0.'
        )
    )

    # Collect args from sys.argv.
    args = parser.parse_args().__dict__

    # Parse and convert args to proper values.
    keys = args.get('*keys')
    max = args.get('max')
    plus = args.get('plus')

    # Bore.
    bore(*keys, max=max, plus=plus, silent=False)
