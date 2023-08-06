import argparse

def main():
    parser = argparse.ArgumentParser(prog='imgk', description='Image Processing Utility')
    subparsers = parser.add_subparsers(title='commands', dest='command')
    from imgk.commands import convert, crop, filter, metadata, resize
    convert.add_subparser(subparsers)
    crop.add_subparser(subparsers)
    filter.add_subparser(subparsers)
    metadata.add_subparser(subparsers)
    resize.add_subparser(subparsers)
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
    else:
        args.func(args)

if __name__ == "__main__":
    main()
