%% Write the solution to Problem 3 here
close all;
clear;
s1 = audioread('data/sample1.wav');
s2 = audioread('data/sample2.wav');
M = [s1, s2].';

A = icafobi(M);
H = A * M;
H = H / max(H(:));
%sound(H(1, :), 44100);
sound(H(2, :), 44100);

audiowrite('results/source1.wav', H(1, :), 44100);
audiowrite('results/source2.wav', H(2, :), 44100);

M2 = A * H;
% M2 sounds too noisy.
save('results/matrix.csv', 'A', '-ascii');