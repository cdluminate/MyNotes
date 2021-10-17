clear;
I = [0.05; 0.10];
W1 = [0.15, 0.20; 0.25, 0.30];
b1 = 0.35;
W2 = [0.40, 0.45; 0.50, 0.55];
b2 = 0.60;
O_GT = [0.01; 0.99];

disp('forward layer 1');
H_ = W1 * I + b1
H = sigmoid(H_)
disp('forward layer 2');
O_ = W2 * H + b2
O = sigmoid(O_)
disp('MSE loss');
loss = sum((O - O_GT).^2)/2

disp('backward pass layer 2');
gO = O - O_GT
gO_ = O .* (1 - O) .* gO
gW2 = gO_ * H'
gH = W2' * gO_
gH_ = H .* (1 - H) .* gH
gW1 = gH_ * I'

lr = 0.5;
fprintf('learning rate is %f\n', lr);

disp('update parameters');
W1 = W1 - lr * gW1
W2 = W2 - lr * gW2