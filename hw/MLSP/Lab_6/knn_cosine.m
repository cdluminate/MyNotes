function [accuracy] = knn_cosine(test, train, test_labels, train_labels)
pdist = cosdist(test, train);
[junk, idx] = min(pdist, [], 2);
accuracy = mean(train_labels(idx) == test_labels);
components = size(test, 2);
fprintf('KNN accuracy with %d components, cosine distance is %f\n', ...
    components, accuracy);
end