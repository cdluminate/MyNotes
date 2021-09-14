%% Lab 2 / Mo Zhou <mzhou32@jhu.edu>

% create a function poly.m and write desired equation and return
% independent variable
f = @poly;     

% create a function poly_derivative.m and write desired equation and return
% independent variable
fder = @poly_derivative;

maxIters =  100;
tol = 1e-06;

% experiment with different values of xi
xi = 10.0;

% Initialization of relative errors, rel_errs
rel_errs = zeros(maxIters,1);
xr=xi;

% caluculate function values for each value of xlim_values using for loop
f_values=[];
xlim_values=[-abs(xr):0.1:abs(xr)];
%% write from here

for x = xlim_values
	f_values = [f_values, f(x)];
end

% plot the xlim_values vs function values and draw x-axis and y-axis
% centered at origin
%% write your code here

plot(xlim_values, f_values);
grid on;
xlim([-12, 12]);
xlabel('x');
ylim([-160, 160]);
ylabel('f');

% write xr as 'x0' to denote initial point. Use text function to write text on figures
%% write from here

text(xr, 0, 'x0');

% plot tangent at xr
%% write from here

% line: y = f'(x)x - f(xr)-fder(xr)*xr
tangent_line = fder(xr) .* xlim_values + f(xr)-fder(xr)*xr;
hold on;
plot(xlim_values, tangent_line, 'r');

% draw line from xr to f(xr). Use functions text and line
[xr] = newtons_update(f,fder, xi);
%% write from here

line([xr, xr], [0, f(xr)], 'Color', 'green', 'LineStyle', '--');
text(xr, 0, 'x1');


% find Newtons update and write on the same plot
%% write from here
tangent_line = fder(xr) .* xlim_values + f(xr)-fder(xr)*xr;
plot(xlim_values, tangent_line, 'r');
xi = xr;
[xr] = newtons_update(f, fder, xi);
line([xr, xr], [0, f(xr)], 'Color', 'green', 'LineStyle', '--');
text(xr, 0, 'x2');
pause

% M is the variable to hold frames of video. Use getframe function
M=[];
count=1;
% write command here and store in M[count]


count=count+1;
pause


for iter = 1:maxIters
    xrold=xr;
    % find Newtons update
    [xr] = newtons_update(f,fder, xrold);
    
    % Relative error from xr and xrold and stopping criteria and break if
    % rel_err<tol. 
    % write from here

    
    
    % plot the xlim_values vs function values and draw x-axis and y-axis
    % centered at origin
    % write from here

    
    % plot tangent at xr
    % write from here


    % write xr as xiter_no. ex: x1, x2 for first and second iteration
    % write from here


    % draw line from xr to f(xr)
    % write from here

    % find Newtons update and write on the same plot
    % write from here
    
    
    hold off
    % save the current frame for the video. Store in M(count)
    % write from here
    
    
    
    count=count+1;
    pause
 
end
  root = xr; % root found by your algorithm

 
%  play movie using movie commnad. 
% write from here



