function [obj] = compute_objective(V, B, W) 

% Your code here

% L2 Divergence
% obj = sum(sum( (V - B*W).^2 ));

% KL Divergence
%pV = V ./ sum(sum(V));
%pBW = (B * W) / sum(sum(B * W));
pV = V;
pBW = B * W;
tmp_1 = pV .* log((pV + 1e-7)./ (pBW + 1e-7)); % numerical stability
tmp_2 = pV;
tmp_3 = -pBW;
% sss = 0;
% for i = 1:size(V, 1)
%     for j = 1:size(V, 2)
%         if pV(i, j) ~= 0
%             sss = sss + tmp_1(i,j) + tmp_2 (i, j) + tmp_3(i, j);
%         end
%     end
% end
% obj = sss;

obj = sum(sum(tmp_1 + tmp_2 + tmp_3));

clear tmp_1
clear tmp_2
clear tmp_3