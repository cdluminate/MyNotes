function [smagNote, smagMusic, sphaseMusic] = load_data()
%% Argument Descriptions
% Required Input Arguments:
% None

% Required Output Arguments:
% smagNote: 1025 x 15 matrix containing the mean spectrum magnitudes of the notes. A correct sequence of the notes is REQUIRED. 
% The sequence is {"1C" ,"1D", "1E", "1F", "1G", "1A", "1B" ,"2C", "2D", "2E", "2F", "2G", "2A", "2B" ,"3C"}

% smagMusic: 1025 x K matrix containing the spectrum magnitueds of the music after STFT.
% sphaseMusic: 1025 x K matrix containing the spectrum phases of the music after STFT.

%% Load Spectrum Magnitudes of Notes
% Fill your code here to return 'smagNote'
names = ["1C" ,"1D", "1E", "1F", "1G", "1A", "1B" ,"2C", "2D", "2E", "2F", "2G", "2A", "2B" ,"3C"];
smagNote = zeros(1025, 15);
for i = 1:length(names)
    [s, fs] = audioread(sprintf('data/notes_15/%s.wav', names(i)));
    s = resample(s, 16000, fs);  % requires signal processing toolbox..
    % reduce to single sound channel or stft will not work
    s = mean(s, 2);
    % find the spectrum
    spectrum = stft(s', 2048, 256, 0, hann(2048));
    % find the central frame
    middle = ceil(size(spectrum, 2)/2);
    note = abs(spectrum(:, middle));
    % clean up everything more than 40db below the peak
    note(find(note < max(note(:))/100)) = 0;
    note = note/norm(note);
    % store
    smagNote(:, i) = note;
end

%% Load Spectrum Magnitues and Phases of The Provided Music
% Fill your code here to return 'smagMusic' and 'sphaseMusic'
[s, fs] = audioread('data/polyushka.wav');
s = resample(s, 16000, fs);
spectrum = stft(s', 2048, 256, 0, hann(2048));
smagMusic = abs(spectrum);
sphaseMusic = spectrum ./ (abs(spectrum) + eps);