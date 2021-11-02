function [TrainingPCA,TestingPCA]=PCAlab(trainingdata,testingdata,PCAdimension)
% input:
% training data: row (observation) column (variable)

coef = pca(trainingdata);
coefK = coef(:, 1:PCAdimension);

TrainingPCA = trainingdata * coefK;
TestingPCA = testingdata * coefK;

end