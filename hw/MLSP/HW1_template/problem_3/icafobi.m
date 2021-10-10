%% Freeing Fourth Moments (FOBI) for ICA
% Mo Zhou <mzhou32@jhu.edu>
% Goal: given M. derive A such that AM.rows are independent.
function [A] = icafobi(M);

% 1. center data M
M = M - mean(M, 2);

% 2. autocorrelation R_MM
R_MM = (M * M.') / max(size(M)); % mean value for expectation

% 3. whitening matrix C via eigen decomposition
[E, S] = eig(R_MM);
C = S^(-1/2) * E.';

% 4. compute X = CM
X = C * M;

% 5. find the 4-th moment matrix D'
D = zeros(2, 2);
for i = 1:size(X, 2)
    x = X(:,i);
    dx = vecnorm(x, 2) * (x * x');
    dx = dx / size(X, 2);
    D = D + dx;
end

% 6. diagonalize D' via eig decomposition
[U, Lambda] = eig(D);

% 7. A = U^T C
A = U.' * C;