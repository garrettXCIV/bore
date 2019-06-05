Find out how far from the project root you are and the paths to it.

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