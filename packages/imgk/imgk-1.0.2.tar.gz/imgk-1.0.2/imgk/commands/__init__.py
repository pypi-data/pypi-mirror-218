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
        if args.command == 'convert':
            convert.convert_function(args)
        elif args.command == 'crop':
            crop.crop_function(args)
        elif args.command == 'filter':
            filter.filter_function(args)
        elif args.command == 'metadata':
            metadata.metadata_function(args)
        elif args.command == 'resize':
            resize.resize_function(args)
