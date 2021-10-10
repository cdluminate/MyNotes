%% NMF - Non-negative matrix factorization
% borrowed from my lab4 with modification
function [B, W, obj] = nmf_train(V, B_init, W_init, max_iter)

% we offload initialization outside of this function
B = B_init;
W = W_init;

% calculate the object function
obj = kld(V, B, W);
fprintf("NMF: init: obj=%f\n", obj);

% perform the iterations and calculate the objective
obj_prev = obj;
for iter = 1:max_iter
    
    B = B .* (((V ./ (B*W))* W')./(ones(size(V))*W'));
    W = W .* ((B' * (V ./ (B*W)))./(B' * ones(size(V))));
    assert(min(min(B)) >= 0);
    assert(min(min(W)) >= 0);
    
    obj = kld(V, B, W);
    fprintf("NMF: iter %d: obj=%f, nrmB=%f, nrmW=%f\n", ...
        iter, obj, norm(B), norm(W));
    if abs(obj - obj_prev) <= 1e-7
        break
    end
    obj_prev = obj;
end

end