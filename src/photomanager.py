import sys
import argparse
from indexer import index_image


def parse_args():
    parser = argparse.ArgumentParser(description="command line for manage photos")
    sub_parser = parser.add_subparsers(help='photo manager commands')
    parser.add_argument('folder', type=str, help="image folder")

    parser_index = sub_parser.add_parser("index", help="create index for images in folder")
    parser_index.add_argument("-f", "--force", help="force reindex all images")

    parser_list = sub_parser.add_parser("list", help="list images by conditions")
    parser_list.add_argument("-s", "--size", nargs=3,
                             help="get the images by size condition, -s greater|less width height")
    parser_list.add_argument("-T", "--tags", nargs=1, help="get the images by tags")
    parser_list.add_argument("-t", "--time", nargs=2, help="get the images by time")
    parser_list.add_argument("--show", help="show image list")

    parser_config = sub_parser.add_parser("config", help="configure photo manager")
    parser_config.add_argument("--minsize", nargs=1, help="skip the image which is less than min size")

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()

    if sys.argv[1] == "index":
        index_image(args.folder, args.force)

