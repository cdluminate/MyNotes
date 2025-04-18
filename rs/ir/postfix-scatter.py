'''
Make scatter plots based on specified file postfixes.
'''
import os
import sys
import matplotlib.pyplot as plt
import glob
import argparse


def read_float(path: str):
    with open(path, 'r') as f:
        return float(f.read().strip())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Make scatter plots based on specified file postfixes.')
    parser.add_argument('--read', '-r', type=str, required=True, action='append', help='Path to the file to read.')
    parser.add_argument('--glob', '-g', type=str, default='*.png', help='Glob pattern to match files.')
    parser.add_argument('--x', '-x', type=str, required=True, help='Postfix for x axis.')
    parser.add_argument('--y', '-y', type=str, required=True, help='Postfix for y axis.')
    parser.add_argument('--title', type=str, default='', help='Title of the plot.')

    args = parser.parse_args()
    print('reading directories:', args.read)

    # read data
    images = glob.glob(os.path.join(args.read[0], args.glob))
    basenames = [os.path.basename(i) for i in images]
    print('#images:', len(images))

    # make scatter plot
    plt.figure()

    xdata = [read_float(i + '.' + args.x) for i in images]
    ydata = [read_float(i + '.' + args.y) for i in images]
    plt.scatter(xdata, ydata)

    for readdir in args.read[1:]:
        images = [os.path.join(readdir, i) for i in basenames]
        xdata = [read_float(i + '.' + args.x) for i in images]
        ydata = [read_float(i + '.' + args.y) for i in images]
        plt.scatter(xdata, ydata)

    plt.legend(args.read)
    plt.xlabel(args.x)
    plt.ylabel(args.y)
    plt.title(args.title)
    plt.show()
