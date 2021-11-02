function [trainingdata, testingdata] = loadImagesLab()
d1 = 112; d2 = 92; d = d1*d2; 
num_images = 9; num_people = 40; 
images = cell(num_people, num_images);
matX = zeros(d, num_people*num_images);

% training set

count = 1;
for i = 1:num_people
    for j = 1:num_images
        % filename = sprintf('/your/local/path/to/orl_faces/Train/s%i/%i.pgm', i, j);
        filename = sprintf('./orl_faces/Train/s%i/%i.pgm', i, j);
        img = double(imread(filename));

        matX(:,count) = reshape(img, d, 1);
        count = count+1;
    end
end
trainingdata = matX/max(matX(:));
meanTrain = mean(trainingdata, 2);
trainingdata = trainingdata - meanTrain;

% test set

count = 1;
matX = zeros(d, num_people * 1);
for i = 1:num_people
    filename = sprintf('./orl_faces/Test/s%i/10.pgm', i);
    img = double(imread(filename));
    
    matX(:,count) = reshape(img, d, 1);
    count = count + 1;
end
testingdata = matX / max(matX(:));
testingdata = testingdata - meanTrain;

% transpose data
% row (observation), column (variable)
trainingdata = trainingdata';
testingdata = testingdata';
    
end