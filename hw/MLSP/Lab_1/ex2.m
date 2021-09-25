%% Ex 2 quantization

p = audioread('filename1.wav');
audiowrite('filename2.wav', p, 8000, 'BitsPerSample', 8);
p1 = audioread('filename2.wav');
p2 = single([p1 > 0]); % 1-bit

%sound(p, 8000);
%sound(p1, 8000);
sound(p2, 8000);