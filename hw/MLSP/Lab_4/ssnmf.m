function [B,W,obj,k] = ssnmf(V,rank,max_iter,lambda,alpha,beta) 
% SSNMF - Non-negative matrix factorization
% [W,H,OBJ,NUM_ITER] = SSNMF(V,RANK,MAX_ITER,LAMBDA)
% V - Input data.
% RANK - Rank size.
% MAX_ITER - Maximum number of iterations (default 50). 
% LAMBDA - Convergence step size (default 0.0001).
% ALPHA - Sparse coefficient for W.
% BETA - Sparse coefficient for B.
% W - Set of basis images.
% H - Set of basis coefficients.
% OBJ - Objective function output.
% NUM_ITER - Number of iterations run.

% Your code here


% 1. initialize B and W randomly
B = rand(size(V, 1), rank);
W = rand(rank, size(V, 2));
W = W ./ sum(W, 1);

% 2. calculate the object function
obj = compute_objective_ss(V, B, W);
fprintf("ssNMF: init: obj=%f\n", obj);

% 3. perform the iterations and calculate the objective
obj_prev = obj;
for iter = 1:max_iter
    
    B = B .* (((V ./ (B*W))* W')./(ones(size(V))*W' + beta));
    W = W .* ((B' * (V ./ (B*W)))./(B' * ones(size(V)) + alpha));
    B(B<0) = 0;
    W(W<0) = 0;
    assert(min(min(B)) >= 0.0);
    assert(min(min(W)) >= 0.0);
    
    obj = compute_objective_ss(V, B, W);
    fprintf("ssNMF: iter %d: obj=%f, nrmB=%f, nrmW=%f\n", iter, obj, norm(B), norm(W));
    if abs(obj - obj_prev) <= lambda
        break
    end
    obj_prev = obj;
end

k = iter;
end

