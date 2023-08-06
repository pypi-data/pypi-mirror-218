from PIL import Image, ImageFilter
def apply_filter(args):
    image = Image.open(args.input)
    filtered_image = image.filter(ImageFilter.GaussianBlur(args.radius))
    output_path = args.output or f"filtered_{args.input}"
    filtered_image.save(output_path)
    print(f"Filter applied and image saved as {output_path}")
def add_subparser(subparsers):
    parser = subparsers.add_parser('filter', help='Apply image filter')
    parser.add_argument('input', help='Input image file path')
    parser.add_argument('-o', '--output', help='Output image file path')
    parser.add_argument('-r', '--radius', type=float, default=2.0, help='Blur radius')
    parser.set_defaults(func=apply_filter)
