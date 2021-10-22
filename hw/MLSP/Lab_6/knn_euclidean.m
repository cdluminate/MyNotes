function [accuracy] = knn_euclidean(test, train, test_labels, train_labels)
pdist = pdist2(test, train, 'minkowski', 2);
[junk, idx] = min(pdist, [], 2);
accuracy = mean(train_labels(idx) == test_labels);
components = size(test, 2);
fprintf('KNN accuracy with %d components, euclidean distance is %f\n', ...
    components, accuracy);
end