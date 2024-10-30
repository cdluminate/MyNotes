from PIL import Image, ImageDraw, ImageStat
import argparse
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Zoom in on an image')
    parser.add_argument('--input', '-i', help='Input image file')
    parser.add_argument('--save', action='store_true', help='Save the result')
    parser.add_argument('x', type=int, help='crop position')
    parser.add_argument('y', type=int, help='crop position')
    parser.add_argument('s', type=int, help='crop size')
    parser.add_argument('place', type=str, help='paste place')
    args = parser.parse_args()

    # read image
    img = Image.open(args.input)
    draw = ImageDraw.Draw(img)
    width, height = img.size
    print('Original size:', width, height)

    # find contrast color
    stat = ImageStat.Stat(img)
    avg_color = tuple(int(c) for c in stat.mean[:3])
    contrast_color = tuple(255 - c for c in avg_color)

    # make crop
    crop = img.crop((args.x, args.y, args.x + args.s, args.y + args.s))
    zoomin_size = (int(width * (1-0.618)), int(height * (1-0.618)))
    print('Crop zoom in size:', zoomin_size)  
    crop = crop.resize(zoomin_size)
    #crop.show()

    # mark crop position
    rect = (args.x, args.y, args.x + args.s, args.y + args.s)
    draw.rectangle(rect, outline=contrast_color, width=4)
    #rect1 = (args.x - 1, args.y - 1, args.x + args.s + 1, args.y + args.s + 1)
    #draw.rectangle(rect1, outline='white', width=1)

    # paste crop
    if args.place == 'bl':
        # bottom left
        img.paste(crop, (0, height - zoomin_size[1]))
        # find bounding box
        rect_outline = (0, height - zoomin_size[1], zoomin_size[0], height)
        draw.rectangle(rect_outline, outline=contrast_color, width=4)
    elif args.place == 'br':
        # bottom right
        img.paste(crop, (width - zoomin_size[0], height - zoomin_size[1]))
        # find bounding box
        rect_outline = (width - zoomin_size[0], height - zoomin_size[1], width, height)
        draw.rectangle(rect_outline, outline=contrast_color, width=4)
    elif args.place == 'tl':
        # top left
        img.paste(crop, (0, 0))
        # find bounding box
        rect_outline = (0, 0, zoomin_size[0], zoomin_size[1])
        draw.rectangle(rect_outline, outline=contrast_color, width=4)
    elif args.place == 'tr':
        # top right
        img.paste(crop, (width - zoomin_size[0], 0))
        # find bounding box
        rect_outline = (width - zoomin_size[0], 0, width, zoomin_size[1])
        draw.rectangle(rect_outline, outline=contrast_color, width=8)
    else:
        raise NotImplementedError('Place not implemented')
    
    # mark the crop with yet another white rectangle
    rect1 = (rect_outline[0] - 1, rect_outline[1] - 1, rect_outline[2] + 1, rect_outline[3] + 1)
    draw.rectangle(rect1, outline='white', width=1)

    if args.save:
        dirname = os.path.dirname(args.input)
        basename = os.path.basename(args.input)
        name, ext = os.path.splitext(basename)
        savepath = os.path.join(dirname, name + f'-x{args.x}-y{args.y}-s{args.s}-place{args.place}' + ext)
        img.save(savepath)
        print('Save to', savepath)
    else:
        img.show()

