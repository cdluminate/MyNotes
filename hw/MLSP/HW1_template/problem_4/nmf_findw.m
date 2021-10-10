%% NMF - Non-negative matrix factorization
% borrowed from my lab4 with modification
function [W, obj] = nmf_findw(V, B, W_init, max_iter)

% we offload initialization outside of this function
W = W_init;

% calculate the object function
obj = kld(V, B, W);
fprintf("NMF(find W): init: obj=%f\n", obj);

% perform the iterations and calculate the objective
obj_prev = obj;
for iter = 1:max_iter
    
    W = W .* ((B' * (V ./ (B*W)))./(B' * ones(size(V))));
	%W = abs(W);
	%W(W < 0) = 0;
    assert(min(min(W)) >= 0);
    
    obj = kld(V, B, W);
    fprintf("NMF (find W): iter %d: obj=%f, nrmW=%f\n", ...
        iter, obj, norm(W));
    if abs(obj - obj_prev) <= 1e-7
        break
    end
    obj_prev = obj;
end

end
