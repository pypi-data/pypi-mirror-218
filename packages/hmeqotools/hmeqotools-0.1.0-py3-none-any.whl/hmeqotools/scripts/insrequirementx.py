"""遍历检索文件夹中的 requirements.txt 文件并使用 pip 安装"""

import os
import sys
import argparse

ARG_PARSER = argparse.ArgumentParser("Setup")
ARG_PARSER.add_argument(
    "-a", "--args", nargs="?", type=str, default="",
    help="pip install 参数")
ARG_PARSER.add_argument(
    "-v", "--python-version", nargs="?", type=str, default="",
    help="python 版本")
ARG_PARSER.add_argument(
    "-i", "--index-url", nargs="?", type=str,
    default="https://pypi.tuna.tsinghua.edu.cn/simple/",
    help="pip install -i 参数")

fmt = "pip install"
requirements_filename = "requirements.txt"


def main():
    global fmt
    args = ARG_PARSER.parse_args(sys.argv[1:])
    if args.args:
        fmt = fmt + " " + args.args
    if args.index_url:
        fmt = fmt + " -i " + args.index_url
    if args.python_version:
        fmt = "py -%s -m %s" % (args.python_version, fmt)

    for dirpath, dirnames, _ in os.walk("."):
        for dirname in dirnames:
            text = f'{fmt} -r {os.path.join(dirpath, dirname)}'
            print(text)
            os.system(text)


if __name__ == "__main__":
    main()
