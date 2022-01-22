import scipy.io
from cca import CcaExtraction

# Credit for used SSVEP data:
# Bakardjian H, Tanaka T, Cichocki A,
# Optimization of SSVEP brain responses with application to eight-command Brain–Computer Interface,
# Neurosci Lett, 2010, 469(1):34-38.

# Check that everything's working using test data
# 128 channels, 256 Hz sampling rate, 5-15-5 seconds of SSVEP data

# 8 Hz
eeg_8 = scipy.io.loadmat('data/test_data.MAT')['EEGdata']
reference_8 = eeg_8[0]  # Reference channel which has to be subtracted
visual1_8 = eeg_8[14] - reference_8  # O1 channel
visual2_8 = eeg_8[27] - reference_8  # O2 channel
length_8 = len(visual1_8)  # 6330 data points

# 14 Hz
eeg_14 = scipy.io.loadmat('data/test_data_14.MAT')['EEGdata']
reference_14 = eeg_14[0]
visual1_14 = eeg_14[14] - reference_14
visual2_14 = eeg_14[27] - reference_14
length_14 = len(visual1_14)

# 28 Hz
eeg_28 = scipy.io.loadmat('data/test_data_28.MAT')['EEGdata']
reference_28 = eeg_28[0]
visual1_28 = eeg_28[14] - reference_28
visual2_28 = eeg_28[27] - reference_28
length_28 = len(visual1_28)

window_length = 256  # 1 sec
target_freqs = [8, 12, 28]
sampling_freq = 256  # 256 Hz
start = 5 * sampling_freq   # eliminating first 5 secs
end = length_8 - start  # eliminating last 5 secs

extractor = CcaExtraction(window_length, target_freqs, sampling_freq)

# Calculate predictions for every second of data
predictions_8 = []
predictions_14 = []
predictions_28 = []
while start + window_length < end:
    data_8 = []
    data_14 = []
    data_28 = []
    for i in range(start, start + window_length):
        data_8.append([visual1_8[i], visual2_8[i]])
        data_14.append([visual1_14[i], visual2_14[i]])
        data_28.append([visual1_28[i], visual2_28[i]])

    result_8 = extractor.extract_features(data_8)
    result_14 = extractor.extract_features(data_14)
    result_28 = extractor.extract_features(data_28)

    # Identify frequency with highest confidence
    index_8 = max(range(len(result_8)), key=lambda k: result_8[k])
    predictions_8.append(target_freqs[index_8])
    index_14 = max(range(len(result_14)), key=lambda k: result_14[k])
    predictions_14.append(target_freqs[index_14])
    index_28 = max(range(len(result_28)), key=lambda k: result_28[k])
    predictions_28.append(target_freqs[index_28])

    start += window_length

print("Predictions for 8 Hz:", predictions_8)
print("Predictions for 14 Hz:", predictions_14)
print("Predictions for 28 Hz:", predictions_28)
