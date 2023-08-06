from PIL import Image
def resize_image(args):
    image = Image.open(args.input)
    width, height = image.size
    new_width = int(width * args.scale)
    new_height = int(height * args.scale)
    resized_image = image.resize((new_width, new_height))
    output_path = args.output or f"resized_{args.input}"
    resized_image.save(output_path)
    print(f"Image resized and saved as {output_path}")
def add_subparser(subparsers):
    parser = subparsers.add_parser('resize', help='Resize image')
    parser.add_argument('input', help='Input image file path')
    parser.add_argument('-o', '--output', help='Output image file path')
    parser.add_argument('-s', '--scale', type=float, required=True, help='Scale factor')
    parser.set_defaults(func=resize_image)
