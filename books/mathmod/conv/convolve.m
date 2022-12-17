%!/usr/bin/octave
function output = convolve (matrix)

imgsize = size(matrix);
conv_mask = [ 1 0 1; 0 1 0; 1 0 1 ];

if imgsize < size(conv_mask)
	display ('E: input matrix smaller than convolution mask')
	return
end

m = [];
for i = 1:imgsize(1)-2
	for j = 1:imgsize(2)-2
		m(i,j) = sum(sum( conv_mask .* matrix(i:i+2,j:j+2) ));
	end
end

output = m;
