function [SVMresults]=SVMlab(TrainingLDA,TestingLDA)

labels = reshape(repmat(1:40, 9, 1), 360, 1);
svm = fitcecoc(TrainingLDA, labels);
pred = predict(svm, TestingLDA);
SVMresults = pred;

end