
import sklearn.cross_decomposition
import scipy.signal
import numpy as np


class CcaExtraction:
    def __init__(self, window_length, target_freqs, sampling_freq):
        """
        Implements Canonical Correlation Analysis (CCA) feature extraction method.
        To extract features, just call extract_features.
        :param window_length: number of samples in one window (sampling_freq times window length in seconds)
        :param target_freqs: list of target frequencies
        :param sampling_freq: sampling frequency of the device
        """
        self.cca_model = sklearn.cross_decomposition.CCA(n_components=1)
        n_targets = len(target_freqs)
        self.reference_signals = self.get_reference_signals(window_length, target_freqs, sampling_freq, [[1,2]]*n_targets)

    def get_reference_signals(self, window_length, target_freqs, sampling_freq, harmonics):
        """
        Construct reference signals for each target frequency.
        :param harmonics: list of harmonics to use for each target frequency. Each entry in the list is list of integers,
        each integer corresponds to harmonic that will be used.
        :return: constructed reference signals in shape (number of targets, window length, number of harmonics times 2)
        """
        reference_signals = []
        t = np.arange(0, window_length, step=1.0) / sampling_freq
        for freq, harmonics_for_target in zip(target_freqs, harmonics):
            reference_signals.append([])
            for harmonic in harmonics_for_target:
                reference_signals[-1].append(np.sin(np.pi * 2 * harmonic * freq * t))
                reference_signals[-1].append(np.cos(np.pi * 2 * harmonic * freq * t))
        return np.transpose(reference_signals, axes=[0, 2, 1])

    def get_corr(self, signal, reference):
        """
        Calculates the canonical correlation between multichannel EEG signal and the set of reference signals for one target.
        :param signal: multichannel EEG
        :param reference: reference signals for one target
        :return: canonical correlation
        """
        self.cca_model.fit(signal, reference)
        res_x, res_y = self.cca_model.transform(signal, reference)
        corr = np.corrcoef(res_x.T, res_y.T)[0][1]
        return corr

    def extract_features(self, multichannel_signal):
        """
        Extracts features from the multichannel EEG signal.
        :param multichannel_signal: multichannel EEG signal of shape (window length, number of channels)
        :return: list of extracted features, features are in the same order as frequencies in target_freqs.
        """
        detrended_signal = scipy.signal.detrend(multichannel_signal, type="linear", axis=0)
        return [self.get_corr(detrended_signal, reference) for reference in self.reference_signals]
