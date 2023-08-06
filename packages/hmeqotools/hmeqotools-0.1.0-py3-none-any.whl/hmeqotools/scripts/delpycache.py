"""Find and delete pycache directory."""

import os
import shutil
from collections import deque


def main():
    path_list = deque(["."])
    while path_list:
        for i in os.scandir(path_list.popleft()):
            if not i.is_dir():
                continue
            if i.name == "__pycache__":
                shutil.rmtree(i.path)
            else:
                path_list.append(i.path)


if __name__ == "__main__":
    main()
