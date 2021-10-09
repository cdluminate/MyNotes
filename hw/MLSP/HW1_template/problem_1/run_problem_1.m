%% Load Notes and Music
% Use the 'load_data' function here
close all;
clear all;
[smagNote, smagMusic, sphaseMusic] = load_data();
fs = 16000;
% recon = stft(smagMusic .* sphaseMusic, 2048, 256, 0, hann(2048));
% sound(recon, 16000)

%% Solution for Problem 1.1 here
% Place all the 15 scores W_i (for the 15 notes) into a single matrix W. 
% Place  the score for the i-th note in the i-th row of W.
% W will be a 15xT matrix, where T is the number of frames in the music.
% Store W in a text file called "problem2a.dat"

% (a)
W = zeros(15, 8869);
for i = 1:15
    nrmN = smagNote(:, i) / vecnorm(smagNote(:, i), 2);
    w_i = (smagMusic.' * nrmN).'; % projection
    W(i, :) = w_i;
end

% (b)
M = zeros(size(smagMusic));
for i = 1:15
    m = smagNote(:, i) * W(i, :);
    M = M + m;
end
recons = stft(M .* sphaseMusic, 2048, 256, 0, hann(2048));
sound(recons, fs);
%clear sound;

% (comment)
disp('the rythms is basically there. but the fidelity is poor.')

% (save .dat)
save('problem2a.dat', 'W', '-ascii');

%% Solution to Problem 1.2 here:  Synthesize Music
% Use the 'synthesize_music' function here.
% Use 'wavwrite' function to write the synthesized music as 'problem2b_synthesis.wav' to the 'results' folder.

