function [Wnew, sigmanew] = em(samples, W, sigma, maxiter)

% (g) loop
for i = 1:maxiter
    % (d) log likelihood
    M = W' * W + sigma^2 * eye(K);
    U = chol(M);
    V = inv(U);
    M_1 = V * V';
    S = sum(vecnorm(samples, 2, 2));
    loglike = -N /2 * (...
        D * log(2 * pi) + log(det(M)) + trace(S * M_1));
    % (e) E step
    fprintf("E(%d)\n", i);
    Ezn = zeros(N, K);
    Eznznt = zeros(N, K, K);
    for j = 1:N
        xn = samples(j, :);
        zn = M_1 * W' * xn';
        Ezn(j, :) = zn;
        znznt = sigma^2 .* M_1 + zn' * zn;
        Eznznt(j, :, :) = znznt;
    end
    % (f) M step
    Wnew = zeros(D, K);
    for j = 1:N
        Wnew = Wnew + samples(j, :)' * Ezn(j, :);
    end
    Wnew = Wnew * inv(reshape(sum(Eznznt, 1), K, K));
    sigma2new = 0;
    for j = 1:N
        tmp = norm(samples(j, :));
        tmp = tmp - 2 * Ezn(j,:) * Wnew' * samples(j, :)';
        tmp = tmp + trace(reshape(Eznznt(j, :, :), K, K) * Wnew' * Wnew);
        sigma2new = sigma2new + tmp;
    end
    sigma2new = sigma2new / (N * D);
    % update
    %Wnew = Wnew;
    sigmanew = sqrt(sigma2new);
end

end