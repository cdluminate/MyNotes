function [B,W,obj,k] = nmf(V,rank,max_iter,lambda)
% NMF - Non-negative matrix factorization
% [B,W,OBJ,NUM_ITER] = NMF(V,RANK,MAX_ITER,LAMBDA) 
% V - Input data.
% RANK - Rank size.
% MAX_ITER - Maximum number of iterations (default 50).
% LAMBDA - Convergence step size (default 0.0001). 
% B - Set of basis images.
% W - Set of basis coefficients.
% OBJ - Objective function output.
% NUM_ITER - Number of iterations run.

% Your code here

% 1. initialize B and W randomly
B = rand(size(V, 1), rank);
%B = abs(randn(size(V, 1), rank));
W = rand(rank, size(V, 2));
%W = abs(randn(rank, size(V, 2)));
W = W ./ sum(W, 1);

% 2. calculate the object function
obj = compute_objective(V, B, W);
fprintf("NMF: init: obj=%f\n", obj);

% 3. perform the iterations and calculate the objective
obj_prev = obj;
for iter = 1:max_iter
    
    B = B .* (((V ./ (B*W))* W')./(ones(size(V))*W'));
    W = W .* ((B' * (V ./ (B*W)))./(B' * ones(size(V))));
    assert(min(min(B)) >= 0);
    assert(min(min(W)) >= 0);
    
    obj = compute_objective(V, B, W);
    fprintf("NMF: iter %d: obj=%f, nrmB=%f, nrmW=%f\n", iter, obj, norm(B), norm(W));
    if abs(obj - obj_prev) <= lambda
        break
    end
    obj_prev = obj;
end

k = iter;
end

