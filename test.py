import scipy.io
from cca import CcaExtraction

# Check that everything's working using test data
mat = scipy.io.loadmat('data/test_data.MAT')  # 128 channels, 256 Hz sampling rate, 5-15-5 seconds of SSVEP data
eeg = mat['EEGdata']
reference = eeg[0]  # Reference channel
visual1 = eeg[14]  # O1 channel
visual2 = eeg[27]  # O2 channel
visual1 = visual1 - reference  # Subtract reference signal from others
visual2 = visual2 - reference
length = len(visual1)  # 6330 data points
sampling_freq = 256
window_length = 256  # 1 sec
start = 5 * sampling_freq   # eliminating first 5 secs
end = length - start  # eliminating last 5 secs

extractor = CcaExtraction(window_length, [8, 14, 28], sampling_freq)

while start + window_length < end:
    data = []
    for i in range(start, start + window_length):
        data.append([visual1[i], visual2[i]])
    print(extractor.extract_features(data))  # The correct signal is 8 Hz
    start += window_length