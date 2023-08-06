"""
Python Utility that Displays out the Tree Structure of a Particular Directory.

Based off of https://pypi.org/project/directory-tree/
Original Author: rahulbordoloi

Modified to remove ascii characters and other redundant code.
"""
from pathlib import Path
import os
import stat


# Class for Directory Tree Path
class DirectoryPath:
    """
    Python Utility that Displays out the Tree Structure of a Particular Directory.
    """

    # Class Variables [Directions]
    display_Node_Prefix_Middle = "|--"
    display_Node_Prefix_Last = "'--"
    display_Parent_Prefix_Middle = "    "
    display_Parent_Prefix_Last = "|   "

    # Constructor
    def __init__(self, path=None, parent_path=None, is_last=0):
        # Instance Variables [Status of Parent-Node Files]
        self.path = Path(path)
        self.parent = parent_path
        self.is_last = is_last
        if self.parent:
            self.depth = self.parent.depth + 1
        else:
            self.depth = 0

    # Displaying Names of the Nodes [Parents/Inner Directories]
    @property
    def display_name(self):
        if self.path.is_dir():
            return self.path.name + "/"
        return self.path.name

    # Building the Tree [Directories-Nodes]
    @classmethod
    def build_tree(
        cls, root, parent=None, is_last=False, max_depth=float("inf"), show_hidden=False
    ):
        # Checking out for Root Directory for Each Iteration
        root = Path(root)

        # Yielding [Returning] Root Directory Name
        root_directory_display = cls(root, parent, is_last)
        yield root_directory_display

        ## Taking out the List of Children [Nodes] Files/Directories
        children = sorted(
            list(entityPath for entityPath in root.iterdir()),
            key=lambda s: str(s).lower(),
        )

        ## Checking for Hidden Entities Flag
        if not show_hidden:
            children = [
                entityPath
                for entityPath in children
                if not cls._hidden_files_filtering_(entityPath)
            ]

        ## Build the Tree
        count_nodes = 1
        for path in children:
            is_last = count_nodes == len(children)
            if path.is_dir() and root_directory_display.depth + 1 < max_depth:
                yield from cls.build_tree(
                    path,
                    parent=root_directory_display,
                    is_last=is_last,
                    max_depth=max_depth,
                    show_hidden=show_hidden,
                )
            else:
                yield cls(path, root_directory_display, is_last)
            count_nodes += 1

    @classmethod
    def _hidden_files_filtering_(cls, path) -> bool:
        """
        Check Condition for Hidden Entities [Files / Directories]

        :param path: Path of the File / Directory

        :return: Boolean Value
        """
        try:
            return bool(os.stat(path).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)
        except (AttributeError, OSError):
            return path.stem.startswith(".")

    def display_path(self):
        """
        Displaying the Tree Path [Directories-Nodes]
        """
        ## Check for Parent Directory Name
        if self.parent is None:
            return self.display_name

        # Checking for File-Name Prefix in Tree
        file_name_prefix = (
            DirectoryPath.display_Node_Prefix_Last
            if self.is_last
            else DirectoryPath.display_Node_Prefix_Middle
        )

        ## Adding Prefixes to Beautify Output [List]
        parts = [f"{file_name_prefix} {self.display_name}"]

        ## Adding Prefixes up for Parent-Node Directories
        parent = self.parent
        while parent and parent.parent is not None:
            parts.append(
                DirectoryPath.display_Parent_Prefix_Middle
                if parent.is_last
                else DirectoryPath.display_Parent_Prefix_Last
            )
            parent = parent.parent

        return "".join(reversed(parts))


def display_tree(
    dir_path: str = "",
    max_depth: float = float("inf"),
    show_hidden: bool = False,
):
    """
    Display Function to return Directory Tree

    :param dir_path: Root Path of Operation. By Default, Refers to the Current Working Directory
    :param max_depth: Max Depth of the Directory Tree. By Default, It goes upto the Deepest Directory/File
    :param show_hidden: Boolean Flag for Returning/Displaying Hidden Files/Directories if Value Set to `True`
    :return: (str)ing Representation of the Tree
    """

    dir_path = Path(dir_path)

    paths = DirectoryPath.build_tree(
        dir_path, max_depth=max_depth, show_hidden=show_hidden
    )

    output = str()
    for path in paths:
        output += path.display_path() + "\n"
    return output
