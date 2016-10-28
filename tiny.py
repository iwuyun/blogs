import os
import sys
import argparse
import tinify

tinify.key = 'na7ZpCb_2wXfqxajkNE9MWpACExPTsmB'

def main():
    parser = argparse.ArgumentParser(description='Compress pictures in named directory')
    parser.add_argument('dir_name', help='the directory to be executed')
    args = parser.parse_args()

    dir_name = args.dir_name
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dir_name = os.path.join(base_dir, dir_name)
    pics = [dir_name + p for p in os.listdir(dir_name) if os.path.isfile(dir_name + p)]
    for pic in pics:
        src = tinify.from_file(pic)
        src.to_file(pic)


if __name__ == '__main__':
    main()
