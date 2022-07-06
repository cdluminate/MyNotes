1. add auxiliary loss for decoder
2. augmentation methods
3. tiny-imagenet
4. cifar-100
5. imagenet-1k
6. fix x-y coord encoder as a constant random matrix
7. vtracer result too problematic for training. an image can contain more than
1000 paths. we must try LIVE : https://ma-xu.github.io/LIVE/
8. other than trying LIVE or DVG (too slow), maybe we can apply gaussian blur 
first to reduce the corner and number of paths in the resulting svg?

9. original understanding on a path was somewhat wrong in detail. When there is
a hole within the polygon, we should not break the corresponding path into two.

Vtracer for mnist 09999-6.svg looks like this. It uses absoluate position.
```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="28" height="28">
<path d="M0,0 L3,1 L-2,6 L-8,13 L-6,13 L-1,11 L4,11 L5,15 L1,19 L-1,20 L-10,20 L-13,17 L-12,12 L-7,5 L-9,4 Z M-4,15 L-5,17 L0,17 L1,15 Z " fill="#000000" transform="translate(19,2)"/>
</svg>
```

while inkscape uses relative position. Is relative position better for representing
a shape? Then the higher hierarchy picks up the shape and its position as well
as color and combine?
```xml
d="m 0,0 3,1 -5,5 -6,7 h 2 l 5,-2 h 5 l 1,4 -4,4 -2,1 h -9 l -3,-3 1,-5 5,-7 -2,-1 z m -4,15 -1,2 h 5 l 1,-2 z"
```
