function [LDAresults]=distancesLab(TrainingLDA,TestingLDA)

% input
% row (observation) column (variable)

d = size(TrainingLDA, 2);

num_class = 40;
test_size = size(TestingLDA, 1);

LDAresults = zeros(test_size, 1);
for i = 1:test_size
    cursor = TestingLDA(i, :);
    dist = vecnorm(TrainingLDA - cursor, 2, 2);
    [junk, idx] = min(dist);
    pred = floor(idx / 9) + 1;
    LDAresults(i, 1) = pred;
end

accuracy = mean(LDAresults == [1:40]');
fprintf("LDA Test Set Accuracy: %f\n", accuracy);

end