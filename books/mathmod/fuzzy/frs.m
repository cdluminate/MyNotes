%!/usr/bin/octave
function output = frs (R1, R2)
% calculate the fuzzy relation synthesis matrix

[M,N] = size(R1)
if M ~= N
	display ('E: illegal R1');
	return
end
if sum(size(R1) - size(R2)) ~= 0
	display ('E: illegal size : R1 or R2');
	return
end

output = [];
for i = 1:M
	for j = 1:M
		output (i,j) = max(min([ R1(i,:) ; R2(:,j)' ]));
	end
end
return
