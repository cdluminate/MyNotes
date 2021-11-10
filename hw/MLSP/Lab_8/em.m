function [Wnew, sigma2new] = em(samples, W, sigma2, K, maxiter)

N = size(samples, 1);
D = size(samples, 2);
center = mean(samples, 1);
samples = samples - center;
LL = [];

% (g) loop
for i = 1:maxiter
    % (d) log likelihood
    M = W.' * W + sigma2 * eye(K);
    U = chol(M);
    V = inv(U);
    M_1 = V * V.';
    %M_1 = inv(M);
    %M_1 = pinv(M);
    S = sum(vecnorm(samples, 2, 2));
    loglike = - N /2 * (...
        D * log(2 * pi) + log(det(M)) + trace(S * M_1));
    LL = [LL, loglike];
    % (e) E step
    %fprintf("EM(%d): loglike %f\n", i, loglike);
    Ezn = zeros(N, K);
    Eznznt = zeros(N, K, K);
    for j = 1:N
        xn = samples(j, :);
        zn = M_1 * W.' * xn.';
        Ezn(j, :) = zn;
        znznt = sigma2 .* M_1 + zn * zn.';
        Eznznt(j, :, :) = znznt;
    end
    % (f) M step
    Wnew = zeros(D, K);
    for j = 1:N
        Wnew = Wnew + samples(j, :).' * Ezn(j, :);
    end
    Wnew = Wnew * inv(reshape(sum(Eznznt, 1), K, K));
    sigma2new = 0;
    for j = 1:N
        tmp = norm(samples(j, :));
        tmp = tmp - 2 * Ezn(j,:) * Wnew.' * samples(j, :).';
        tmp = tmp + trace(reshape(Eznznt(j, :, :), K, K) * Wnew.' * Wnew);
        sigma2new = sigma2new + tmp / (N * D);
    end
    % update
    W = Wnew;
    sigma2 = sigma2new;
    if sigma2 < 0
        sigma2 = 0.5;
    end
end

% return
Wnew = W;
sigma2new = sigma2;

end