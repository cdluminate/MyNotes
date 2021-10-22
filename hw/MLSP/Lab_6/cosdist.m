function [pdist] = cosdist(x, y)
% pairwise cosine distance between batch data x and y
% shape (x) = num_data_1 * data_dim
% shape (y) = num_data_2 * data_dim
X = x ./ vecnorm(x, 2);
Y = y ./ vecnorm(y, 2);
pdist = X * Y';
end