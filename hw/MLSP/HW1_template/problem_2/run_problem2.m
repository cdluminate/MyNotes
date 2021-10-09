%% Load Notes and Music
% You may reuse your 'load_data' function from prob 1
close all;
clear all;
[smagNote, smagMusic, sphaseMusic] = load_data();
fs = 16000;

%% Compute The Transcribe Matrix: non-negative projection with gradient descent
% Use the 'transcribe_music_gradient_descent' function here

% Store final W for each eta value in a text file called "problem2b_eta_xxx.dat"
% where xxx is the actual eta value. E.g. for eta = 0.01, xxx will be "0.01".

% Print the plot of E vs. iterations for each eta in a file called
% "problem2b_eta_xxx_errorplot.png", where xxx is the eta value.
% Print the eta vs. E as a bar plot stored in "problem2b_eta_vs_E.png".

num_iter = 250;

[T01, E01, tT, s01] = transcribe_music_gradient_descent( ...
    smagMusic, smagNote, 0.1, num_iter, 0);
save('results/problem2b_eta_0.1.dat', 'T01', '-ascii');
plot(E01);
title('lr=0.1');
saveas(gcf, 'results/problem2b_eta_0.1_errorplot.png');
close gcf;

[T001, E001, tT, s001] = transcribe_music_gradient_descent( ...
    smagMusic, smagNote, 0.01, num_iter, 0);
save('results/problem2b_eta_0.01.dat', 'T001', '-ascii');
plot(E001);
title('lr=0.01');
saveas(gcf, 'results/problem2b_eta_0.01_errorplot.png');
close gcf;

[T0001, E0001, tT, s0001] = transcribe_music_gradient_descent( ...
    smagMusic, smagNote, 0.001, num_iter, 0);
save('results/problem2b_eta_0.001.dat', 'T0001', '-ascii');
plot(E0001);
title('lr=0.001');
saveas(gcf, 'results/problem2b_eta_0.001_errorplot.png');
close gcf;

[T00001, E00001, tT, s00001] = transcribe_music_gradient_descent( ...
    smagMusic, smagNote, 0.0001, num_iter, 0);
save('results/problem2b_eta_0.0001.dat', 'T00001', '-ascii');
plot(E00001);
title('lr=0.0001');
saveas(gcf, 'results/problem2b_eta_0.0001_errorplot.png');
close gcf;

bar([E01(end), E001(end), E0001(end), E00001(end)]);
xlabel('$0.1^x$');
ylabel('Last loss');
saveas(gcf, 'results/problem2b_eta_vs_E.png');
close gcf;


%% Synthesize Music
% You may reuse the 'synthesize_music' function from prob 1.
% write the synthesized music as 'polyushka_syn.wav' to the 'results' folder.

recons = synthesize_music(sphaseMusic, s01);
sound(recons, 16000)
audiowrite('results/polyushka_syn.wav', recons, 16000);
disp('this sounds a little bit better than the construction from problem_1');