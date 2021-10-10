function [M_speech_rec, M_music_rec] = separate_signals( ...
    M_mixed, B_speech, B_music, n_iter)

%Bsm = [B_speech, B_music];
%W = rand(size(Bsm, 2), size(M_mixed, 2));
%[W, obj] = nmf_findw(M_mixed, Bsm, W, n_iter);
%W_speech = W(1:size(W,1)/2, :);
%W_music = W(size(W,1)/2+1:end, :);

W_speech = rand(size(B_speech, 2), size(M_mixed, 2));
%W_speech = zeros(size(B_speech, 2), size(M_mixed, 2));
%W_speech = ones(size(B_speech, 2), size(M_mixed, 2));
[W_speech, obj] = nmf_findw(M_mixed, B_speech, W_speech, n_iter);

W_music = rand(size(B_music, 2), size(M_mixed, 2));
%W_music = zeros(size(B_music, 2), size(M_mixed, 2));
%W_music = ones(size(B_music, 2), size(M_mixed, 2));
[W_music, obj] = nmf_findw(M_mixed, B_music, W_music, n_iter);

M_speech_rec = B_speech * W_speech;
M_music_rec = B_music * W_music;
end
