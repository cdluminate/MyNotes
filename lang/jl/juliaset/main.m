%% draw julia set

%% configure
C = -0.62772 -0.42193i;
xmin = -1.8;
xmax = 1.8;
ymin = -1.8;
ymax = 1.8;
samples = 1000;
maxiter = 300;

%% prepare
[ X, Y ] = meshgrid(linspace(xmin, xmax, samples), linspace(ymin, ymax, samples));
Z = X + Y .* i;
output = zeros(size(Z));

%% main -- serial version
%[ I, J ] = size(Z);
%for i = 1:I
%   disp(sprintf('iteration %d', i));
%   for j = 1:J
%      n = 0;
%      while abs(Z(i,j))<2 && n<maxiter
%         Z(i,j) = Z(i,j).^2 + C;
%         n += 1;
%      end
%      output(i,j) = n;
%   end
%end

n = 0;
mem = ones(size(output));
while n<maxiter && sum(Z>2)!=prod(size(Z))
   disp(sprintf('iteration %d', n));
   Z = Z .* Z + C;
   output += mem .* (abs(Z)<2)*1;
   mem = mem .* abs(Z)<2;
   n += 1;
end

image(output)
print -dpng output

save -ascii res.txt output
