from PIL import Image
def crop_image(args):
    image = Image.open(args.input)
    cropped_image = image.crop((args.left, args.top, args.right, args.bottom))
    output_path = args.output or f"cropped_{args.input}"
    cropped_image.save(output_path)
    print(f"Image cropped and saved as {output_path}")
def add_subparser(subparsers):
    parser = subparsers.add_parser('crop', help='Crop image to a specific region')
    parser.add_argument('input', help='Input image file path')
    parser.add_argument('-o', '--output', help='Output image file path')
    parser.add_argument('--left', type=int, required=True, help='Left coordinate')
    parser.add_argument('--top', type=int, required=True, help='Top coordinate')
    parser.add_argument('--right', type=int, required=True, help='Right coordinate')
    parser.add_argument('--bottom', type=int, required=True, help='Bottom coordinate')
    parser.set_defaults(func=crop_image)
