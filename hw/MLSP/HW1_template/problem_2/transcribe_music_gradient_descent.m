function [T, E, transMatT, smagMusicProj] = transcribe_music_gradient_descent(M, N, lr, num_iter, threshold)
% Input: 
%   M: (smagMusic) 1025 x K matrix containing the spectrum magnitueds of the music after STFT.
%   N: (smagNote) 1025 x 15 matrix containing the spectrum magnitudes of the notes.
%   lr: learning rate, i.e. eta as in the assignment instructions
%   num_iter: number of iterations
%   threshold: threshold

% Output:
%   T: (transMat) 15 x K matrix containing the transcribe coefficients.
%   E: num_iter x 1 matrix, error (Frobenius norm) from each iteration
%   transMatT: 15 x K matrix, threholded version of T (transMat) using threshold
%   smagMusicProj: 1025 x K matrix, reconstructed version of smagMusic (M) using transMatT

% random initialization
K = size(M, 2);
W = ones(15, K);
DT = prod(size(M));
loss = norm(M - N * W, 'fro')/DT;
fprintf('* Initial loss %f\n', loss);
E(1) = loss;

for i = 1:num_iter
    % we don't divide the gradient by DT because that will make
    % the magnitude of gradient tooooooooooooooooooo small.
    % in that case a much larger learning rate will be needed.
    gradW = (-2)*(N.' * (M - N * W));%/DT;
    prevW = W;
    W = W - lr * gradW;
    %disp(norm(W - prevW));
    W = max(W, 0);
    loss = norm(M - N * W, 'fro')/DT;
    fprintf('* iter %d, loss=%f, nrm(gradW)=%f\n', i, loss, norm(gradW));
    E(i+1) = loss;
end
T = W;

transMatT = T;
transMatT(find(transMatT < threshold)) = 0;

smagMusicProj = N * W;