function [V,D,TrainingLDA,TestingLDA]=LDAlab(TrainingPCA,TestingPCA,LDAdimension)

pcadim = size(TrainingPCA, 2);
num_class = 40; % hard coded paramter is bad, though.
sample_per_class = 9;

globalmean = mean(TrainingPCA, 1);

centroids = zeros(num_class, size(TrainingPCA, 2));
for i = 1:num_class
    idxs = (i-1)*sample_per_class+1;
    idxe = i*sample_per_class;
    this_class = TrainingPCA(idxs:idxe, :);
    center = mean(this_class, 1);
    centroids(i, :) = center;
end

SB = zeros(pcadim, pcadim);
for i = 1:num_class
    diff = centroids(i, :) - globalmean;
    tmp = sample_per_class * diff' * diff;
    SB = SB + tmp;
end

SW = zeros(pcadim, pcadim);
for i = 1:num_class
    idxs = (i-1)*sample_per_class+1;
    idxe = i*sample_per_class;
    for j = idxs:idxe
        diff = TrainingPCA(j,:) - centroids(i, :);
        tmp = diff' * diff;
        SW = SW + tmp;
    end
end

[V, D] = eigs(SB, SW, LDAdimension);
size(V);
size(D);

TrainingLDA = TrainingPCA * V;
TestingLDA = TestingPCA * V;

end