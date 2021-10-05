%  K-Means function to generate K clusters of an input image
%  Author Name: Mo Zhou
function [C, segmented_image] = KMeans(X,K,maxIter)

%% 1. Image vectorization based on RGB components
[Height, Width, Channel] = size(X);
X = single(X);
X = reshape(X, [Height*Width, Channel]); % a pixel per row

%% 2. Intial RGB Centroid Calculation

% I asked the CA. This step is not necessary for non-top-down kmeans.

%% 3. Randomly initializing K centroids (select those centroids from the actual points)
Ri = randi(Height*Width, [K, 1]);
C = X(Ri, :);

%% 4. Assign data points to K clusters using the following distance - dist = norm(C-X,1)
dist = zeros(Height*Width, K);
for i = 1:K
    d = vecnorm(C(i, :) - X, 1, 2);
    dist(:, i) = d;
end
[junk, argmin] = min(dist, [], 2);

%% 5. Re-computing K centroids
for i = 1:K
    idx = find(argmin == i);
    ci = mean(X(idx, :), 1);
    C(i, :) = ci;
end

%% Reiterate through steps 4 and 5 until maxIter reached. Set maxIter = 100
for iter = 2:maxIter
    
    % copy step 4
    dist = zeros(Height*Width, K);
    for i = 1:K
        d = vecnorm(C(i, :) - X, 1, 2);
        dist(:, i) = d;
    end
    [junk, argmin] = min(dist, [], 2);
    
    % copy step 5
    for i = 1:K
        idx = find(argmin == i);
        ci = mean(X(idx, :), 1);
        C(i, :) = ci;
    end
end

%% Return K centroid coordinates and segmented Image
dist = zeros(Height*Width, K);
for i = 1:K
    d = vecnorm(C(i, :) - X, 1, 2);
    dist(:, i) = d;
end
[junk, argmin] = min(dist, [], 2);
segmented_image = uint8(C(argmin, :));
segmented_image = reshape(segmented_image, [Height, Width, Channel]);
end
