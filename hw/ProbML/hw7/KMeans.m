% K-Means function to locate K clusters from input dataset
% Author Name: Mo Zhou
function [C, labels] = KMeans(X, K, maxIter)
% Input:
%  X: dataset, observations in rows, variables in columns.
%  K: "K"-means
% Output:
%  C: centroids
%  labels: class labels assigned to each observation in X

N = size(X, 1);

% Randomly initializing K centroids
Ri = randi(N, [K, 1]);
C = X(Ri, :);

% start k-means loop
for iter = 1:maxIter
    % assign data to clusters
    dist = zeros(N, K);
    for i = 1:K
        d = vecnorm(C(i, :) - X, 2, 2);
        dist(:, i) = d;
    end
    [~, argmin] = min(dist, [], 2);
    % re-compute centroids
    for i = 1:K
        idx = find(argmin == i);
        ci = mean(X(idx, :), 1);
        C(i, :) = ci;
    end
end

% assign labels to X
dist = zeros(N, K);
for i = 1:K
    d = vecnorm(C(i, :) - X, 2, 2);
    dist(:, i) = d;
end
[~, argmin] = min(dist, [], 2);
labels = argmin;

end
