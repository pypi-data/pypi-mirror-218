from PIL import Image
def extract_metadata(args):
    image = Image.open(args.input)
    print("Image Metadata:")
    print(f"Format: {image.format}")
    print(f"Size: {image.size}")
    print(f"Mode: {image.mode}")
def add_subparser(subparsers):
    parser = subparsers.add_parser('metadata', help='Extract image metadata')
    parser.add_argument('input', help='Input image file path')
    parser.set_defaults(func=extract_metadata)
