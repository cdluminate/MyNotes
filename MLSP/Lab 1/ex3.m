%% Ex3 aliasing effect

% problem 1

t = -pi/32:1/1200:pi/32; % this sampling rate matters
x = cos(2 * pi * 100 * t);
plot(t, x, 'r');
hold on;

y = cos(2 * pi * 600 * t);
plot(t, y, 'k');

% problem 2

hold off
t = -pi/32:1/500:pi/32; % sampling rate 500hz
z1 = cos(2 * pi * 100 * t);
z2 = cos(2 * pi * 600 * t);
plot(t, z1, t, z2);

% problem 3

% for the plots of 1)
% with a sampling rate of 1200, the two cosine waves
% look good. There are 6 cycles of the 600hz wave within
% 1 cycle of the 100hz wave.

% for the plots of 2)
% with a sampling rate of 1200, the two sampled
% waves are very similar. The frequency of the
% sampled 600hz wave has been changed already.
% namely, the two sampled waves have similar frequency.

