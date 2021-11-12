N = 100;
e = exp(1);
x = 0:.1:10;
y = .5;
p = x.^(N).*e.^(-x).*(y.^(x-1)).^N;
figure;
hold on;
plot(x, p);

xhat = -N/(.5*N);
approx = x .* e.^(-x) .* (y.^(x-1)).^N + ...
    (-.5) .* (x - xhat) .* N ./ (xhat)^2;
plot(x, approx);
title(sprintf("N=%d", N));