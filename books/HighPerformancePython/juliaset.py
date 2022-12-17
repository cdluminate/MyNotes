#!/usr/bin/python3
'''
Calculate full julia set
 $$ f(z) = z^2 + c, const c \in C, z \in C $$
'''

import time
from PIL import Image
import array
from functools import wraps

# area of complex space to investigate
x1, x2, y1, y2 = -1.8, 1.8, -1.8, 1.8
c_real, c_imag = -0.62772, -.42193
draw_output = True

def timefn(fn):
  @wraps(fn)
  def measure_time(*args, **kwargs):
    t1 = time.time()
    result = fn(*args, **kwargs)
    t2 = time.time()
    print('@timefn:', fn, 'tooks', str(t2-t1), 'seconds')
    return result
  return measure_time

def show_greyscale(output_raw, width, height, max_iterations):
    """Convert list to array, show using PIL"""
    # convert our output to PIL-compatible input
    # scale to [0...255]
    max_iterations = float(max(output_raw))
    print(max_iterations)
    scale_factor = float(max_iterations)
    scaled = [int(o / scale_factor * 255) for o in output_raw]
    output = array.array('B', scaled)  # array of unsigned ints
    # display with PIL
    im = Image.new("L", (width, width))
    # EXPLAIN RAW L 0 -1
    im.frombytes(output.tostring(), "raw", "L", 0, -1)
    im.show()

def show_false_greyscale(output_raw, width, height, max_iterations):
    """Convert list to array, show using PIL"""
    # convert our output to PIL-compatible input
    # sanity check our 1D array and desired 2D form
    assert width * height == len(output_raw)
    # rescale output_raw to be in the inclusive range [0..255]
    max_value = float(max(output_raw))
    output_raw_limited = [int(float(o) / max_value * 255) for o in output_raw]
    # create a slightly fancy colour map that shows colour changes with
    # increased contrast (thanks to John Montgomery)
    output_rgb = (
        (o + (256 * o) + (256 ** 2) * o) * 16 for o in output_raw_limited)  # fancier
    # array of unsigned ints (size is platform specific)
    output_rgb = array.array('I', output_rgb)
    # display with PIL/pillow
    im = Image.new("RGB", (width, height))
    # EXPLAIN RGBX L 0 -1
    im.frombytes(output_rgb.tostring(), "raw", "RGBX", 0, -1)
    im.show()

# establish the coordinate lists as inputs to our calculation function
def calc_pure_python(desired_width, max_iterations):
  ''' create a list of complex coordinates (zs) and comples parameters (cs),
  build julia set, and display
  '''
  x_step = float(x2-x1) / float(desired_width)
  y_step = float(y1-y2) / float(desired_width)
  x = []
  y = []

  ycoord = y2
  while ycoord > y1:
    y.append(ycoord)
    ycoord += y_step

  xcoord = x1
  while xcoord < x2:
    x.append(xcoord)
    xcoord += x_step

  # build a list of coordinates and the initial condition for each cell
  zs = []
  cs = []
  for ycoord in y:
    for xcoord in x:
      zs.append(complex(xcoord, ycoord))
      cs.append(complex(c_real, c_imag))

  print('length of x:', len(x))
  print('total elements:', len(zs))
  start_time = time.time()
  output = calculate_z_serial_purepython(max_iterations, zs, cs)
  end_time = time.time()
  secs = end_time - start_time
  print('calculate_z_serial_purepython', 'tooks', secs, 'seconds')
  
  assert(sum(output)==33219980)
  if draw_output:
    show_false_greyscale(output, len(x), len(y), max_iterations)
    #show_greyscale(output, len(x), len(y), max_iterations)

@timefn
def calculate_z_serial_purepython(maxiter, zs, cs):
  ''' calculate output list using Julia update rule '''
  output = [0] * len(zs)
  for i in range(len(zs)):
    n = 0
    z = zs[i]
    c = cs[i]
    while abs(z) < 2 and n < maxiter:
      z = z * z + c
      n += 1
    output[i] = n
  return output

if __name__=='__main__':
  calc_pure_python(desired_width=1000, max_iterations=300)
