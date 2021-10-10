%% Write the solution to Problem 4 here
close all;
clear;

[s, fs] = audioread('data/speech.wav');
sspec = stft(s', 2048, 256, 0, hann(2048));
Ms = abs(sspec);

[m, fs] = audioread('data/music.wav');
mspec = stft(m', 2048, 256, 0, hann(2048));
Mm = abs(mspec);

[mix, fs] = audioread('data/mixed.wav');
mixspec = stft(mix', 2048, 256, 0, hann(2048));
mixphase = mixspec ./ (abs(mixspec) + eps);
Mix = abs(mixspec);

%% NMF Estimation: Learning Bases

% NMF for Mm
Bm = csvread('data/Bm_init.csv');
Wm = csvread('data/Wm_init.csv');
n_iters = [0, 50, 100, 150, 200, 250];
%n_iters = [0, 250];
losses = zeros(size(n_iters));
for i = 1:length(n_iters)
    [B, W, kld] = nmf_train(Mm, Bm, Wm, n_iters(i));
    losses(i) = kld;
end
Bm = B;
Wm = W;

plot(n_iters, log(losses));
xlabel('n-iter');
ylabel('log(kl)');
title('log(kl) v.s. n-iter');
saveas(gcf, 'results/problem4_part1_q2_Mm.png');
close gcf;
fprintf('NMF(Mm): loss value (kld) for n_iter=250 is %f\n', losses(end));

% NMF for Ms
Bs = csvread('data/Bs_init.csv');
Ws = csvread('data/Ws_init.csv');
losses = zeros(size(n_iters));
for i = 1:length(n_iters)
    [B, W, kld] = nmf_train(Ms, Bs, Ws, n_iters(i));
    losses(i) = kld;
end
Bs = B;
Ws = W;

plot(n_iters, log(losses));
xlabel('n-iter');
ylabel('log(kl)');
title('log(kl) v.s. n-iter');
saveas(gcf, 'results/problem4_part1_q2_Ms.png');
close gcf;
fprintf('NMF(Ms): loss value (kld) for n_iter=250 is %f\n', losses(end));

%% Signal Separation
[M_speech_rec, M_music_rec] = separate_signals(Mix, Bs, Bm, 500);
csvwrite('results/M_speech_rec.csv', M_speech_rec);
csvwrite('results/M_music_rec.csv', M_music_rec);

recons_speech = stft(M_speech_rec .* mixphase, 2048, 256, 0, hann(2048));
recons_speech = recons_speech ./ max(recons_speech(:));
recons_music = stft(M_music_rec .* mixphase, 2048, 256, 0, hann(2048));
recons_music = recons_music ./ max(recons_music(:));

audiowrite('results/speech_rec.wav', recons_speech, 16000);
audiowrite('results/music_rec.wav', recons_music, 16000);
