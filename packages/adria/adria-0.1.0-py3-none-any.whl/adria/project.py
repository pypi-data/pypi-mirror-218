import logging
import os
import shutil
import pathlib

from argparse import ArgumentParser
from glob import glob
from pathlib import Path

from adria.core.utils import mkdir


logger = logging.getLogger(__name__)


def main(args):
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    BASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

    dir_path = os.path.join(os.getcwd(), args.path)
    mkdir(dir_path)
    pt = os.path.join(BASE_PATH, "project_template")
    try:
        for d in ["_includes", "_layouts"]:
            for f in glob(os.path.join(pt, d, "*")):
                filename = Path(f).name
                mkdir(os.path.join(dir_path, d))
                shutil.copy2(f, os.path.join(dir_path, d, filename))

        mkdir(os.path.join(dir_path, "src"))
        shutil.copy2(
            os.path.join(pt, "src", "generator.py"),
            os.path.join(dir_path, "src", "generator.py")
        )
    except Exception as ex:
        # os.rmdir(dir_path)
        logger.error("Failed to create project dir", ex)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--debug", action="store_true", default=False)
    parser.add_argument("path", help="Path of new project")
    main(parser.parse_args())
