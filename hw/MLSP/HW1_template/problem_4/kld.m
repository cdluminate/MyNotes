% KL divergence. M \approx B * W, KL(M||BW)
% modified from my code of lab4
function [obj] = compute_objective(V, B, W) 

% make sum to 1?
%pV = V ./ sum(sum(V));
%pBW = (B * W) / sum(sum(B * W));

% don't make sum to 1?
pV = V;
pBW = B * W;

tmp_1 = pV .* log((pV + 1e-7)./ (pBW + 1e-7)); % numerical stability
tmp_2 = pV; % slides
% tmp_2 = - pV; % HW1.pdf
tmp_3 = -pBW; % slides
% tmp_3 = pBW; % HW1.pdf
% maybe the equation in HW1 is wrong?

obj = sum(sum(tmp_1 + tmp_2 + tmp_3));
end
