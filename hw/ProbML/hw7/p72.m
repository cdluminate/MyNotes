N = 1;
e = exp(1);
x = 0:.1:10;
y = .5;
p = x.^(N).*e.^(-x).*(y.^(x-1)).^N;
figure;
hold on;
plot(x, p);

xhat = N/(1-(y*N));
sigma2 = xhat.^2./N;
jx = N./(xhat^2);
approx = 1./(2*pi./jx) * exp(-0.5.*jx.*(x-xhat).^2);
plot(x, approx);
title(sprintf("N=%d", N));