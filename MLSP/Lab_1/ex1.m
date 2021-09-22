%% Ex1. Image Manupulation
cameraman_image = imread('cameraman.tif');

figure(1);
imshow(cameraman_image);

size(cameraman_image)
% 256x256

fade_factor = 0.5;

Fade_image = cameraman_image * fade_factor;
figure(2);
imshow(Fade_image);
% the pictures becomes darker because the
% pixel values being closer to zero

first_part_image = cameraman_image(1:100,1:100);
imshow(first_part_image);
% cropped to the top left corner

[X, Y] = size(cameraman_image);
last_part_image = cameraman_image(X-100:end, Y-100:end);
imshow(last_part_image);
% cropped to the bottom right corner

%% ex 1 part 2 version 1

Moon_image = imread('5.1.09.tiff');
figure(1);
imshow(Moon_image);
% size = 256x256

cameraman_image = imread('cameraman.tif');
tmp = single(cameraman_image) * 0.8;
tmp = tmp + single(Moon_image) * 0.2;
Mixte_image = uint8(Mixte_image);
figure(2);
imshow(Mixte_image);
% mixed.

figure(11);
First_part_image_1 = Mixte_image(1:100, 1:100);
imshow(First_part_image_1);

[X, Y] = size(Mixte_image);
last_part_image_2 = Mixte_image(X-99:end, Y-99:end);
imshow(last_part_image_2);

last_part_Mixte_image = single(last_part_image_2) * 0.8 + single(First_part_image_1) * 0.2;
last_part_Mixte_image = uint8(last_part_Mixte_image);

%% ex 1 part 2 version 2

mi_col = reshape(Moon_image, prod(size(Moon_image)), 1);
ci_col = reshape(cameraman_image, prod(size(cameraman_image)), 1);
Both_images = single([mi_col, ci_col]);
Fade_vector = [0.8, 0.2]';
mixing_image_vector = Both_images * Fade_vector;
mixing_image_matrix = reshape(mixing_image_vector, 256, 256);
Mixte_image = uint8(mixing_image_matrix);

% done here.
