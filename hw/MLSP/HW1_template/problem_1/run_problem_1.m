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
save('results/problem1a.dat', 'W', '-ascii');

% (b)
M = zeros(size(smagMusic));
for i = 1:15
    m = smagNote(:, i) * W(i, :);
    M = M + m;
end
recons = stft(M .* sphaseMusic, 2048, 256, 0, hann(2048));
sound(recons, fs);
clear sound;
audiowrite('results/problem1a_synthesis.wav', recons, fs);

% (comment)
disp('I. the rythms is still there. but the fidelity is poor.');

% (save .dat)
%save('results/problem2a.dat', 'W', '-ascii');
%disp('(I am not sure whether the filename in the comment is correct.');
%disp('(let me write another file with a file name that I think is correct.');
save('results/problem1a.dat', 'W', '-ascii');

%% Solution to Problem 1.2 here:  Synthesize Music
% Use the 'synthesize_music' function here.
% Use 'wavwrite' function to write the synthesized music as 'problem2b_synthesis.wav' to the 'results' folder.

W2 = pinv(smagNote) * smagMusic;
save('results/problem1b.dat', 'W2', '-ascii');
M2 = smagNote * W2;
% recons2 = stft(M2 .* sphaseMusic, 2048, 256, 0, hann(2048));
recons2 = synthesize_music(sphaseMusic, M2);
sound(recons2, 16000);
audiowrite('results/problem1b_synthesis.wav', recons2, fs);
% clear sound;

disp('II. similar to what I heard from I. low fidelity.');

disp('* Difference between reconstructions from I. and II.');
disp(mean(abs(recons2 - recons)));


