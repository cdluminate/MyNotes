function output = foolinterp (input)
% foolish interpolation

[OI,OJ,OK] = size(input);

I=201;
J=201;
K=101;

output = zeros([I,J,K]);

% round 1
for x = 1:10:I
	for y = 1:10:J
		for z = 1:K-1
			%x %y %z
			ax = floor((x-1)/10)+1;
			ay = floor((y-1)/10)+1;
			az = floor((z-1)/10)+1;
			p0 = input(ax ,ay ,az );
			p1 = input(ax, ay, az+1);
			output (x,y,z) = p0 + ((p1-p0)/10)*( mod(z-1,10) );
		end
	end
end

% round 2
for x = 1:10:I
	for z = 1:K
		for y = 1:J-1
			ax = floor((x-1)/10)+1;
			ay = floor((y-1)/10)+1;
			az = floor((z-1)/10)+1;
			p0 = input(ax ,ay ,az );
			p1 = input(ax, ay+1, az);
			output (x,y,z) = p0 + ((p1-p0)/10)*( mod(y-1,10) );
		end
	end
end

% round 3
for x = 1:I-1
	for z = 1:K
		for y = 1:J
			ax = floor((x-1)/10)+1;
			ay = floor((y-1)/10)+1;
			az = floor((z-1)/10)+1;
			p0 = input(ax ,ay ,az );
			p1 = input(ax+1, ay, az);
			output (x,y,z) = p0 + ((p1-p0)/10)*( mod(x-1,10) );
		end
	end
end

output (I,J,K) = input(OI,OJ,OK);
