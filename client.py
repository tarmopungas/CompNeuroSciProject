import Pyro4
import scipy.io

mat = scipy.io.loadmat('data/test_data.MAT')  # 128 channels, 256 Hz sampling rate, 5-15-5 seconds of SSVEP data
eeg = mat['EEGdata']
data = []
for i in range(len(eeg)):
    data.append(list(eeg[i][1266:5064]))  # remove 5 secs from beginning and end; results in len 3798

EEG_input = Pyro4.Proxy("PYRONAME:EEG")
extractor = Pyro4.Proxy("PYRONAME:CCA")
features = extractor.extract_features(data)
print(features)
