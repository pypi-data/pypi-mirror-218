from PIL import Image
def convert_image(args):
    image = Image.open(args.input)
    output_path = args.output or f"converted_{args.input}"
    image.save(output_path, format=args.format)
    print(f"Image converted and saved as {output_path}")
def add_subparser(subparsers):
    parser = subparsers.add_parser('convert', help='Convert image to a different format')
    parser.add_argument('input', help='Input image file path')
    parser.add_argument('-o', '--output', help='Output image file path')
    parser.add_argument('-f', '--format', help='Output image format', default='PNG')
    parser.set_defaults(func=convert_image)
