function [obj] = compute_objective_ss(V,B,W, alpha, beta) 

% Your code here

lambda = 1.0;

% KL Divergence
pV = V;
pBW = B * W;
tmp_1 = pV .* log((pV + 1e-7)./ (pBW + 1e-7)); % numerical stability
tmp_2 = pV;
tmp_3 = -pBW;
obj = sum(sum(tmp_1 + tmp_2 + tmp_3));

norm1 = sum(sum(abs(W)));
obj = obj + lambda * norm1;

clear tmp_1
clear tmp_2
clear tmp_3