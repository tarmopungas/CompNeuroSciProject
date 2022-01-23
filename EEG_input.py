import argparse
import time
import logging
from cca import CcaExtraction
from GUI import GUI
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore

import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowError
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, WindowFunctions, DetrendOperations

class Graph:
    def __init__(self, board_shim):
        self.board_id = board_shim.get_board_id()
        self.board_shim = board_shim
        self.exg_channels = BoardShim.get_exg_channels(self.board_id)
        self.sampling_rate = BoardShim.get_sampling_rate(self.board_id)
        self.update_speed_ms = 125  # every 0.125 seconds, get fresh data
        self.window_size = 2.1  # size of the sliding window (seconds)
        self.num_points = int(self.window_size * self.sampling_rate)  # 2,1 * 250 = 525

        print("Sampling rate: {} Hz".format(self.sampling_rate))
        print("Open channels: {}".format(self.exg_channels))

        self.app = QtGui.QApplication([])
        #self.win = pg.GraphicsWindow(title='BrainFlow Plot', size=(800, 600))
        GUI.main()
        #self._init_timeseries()
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(self.update_speed_ms)
        QtGui.QApplication.instance().exec_()

    def _init_timeseries(self):
        self.plots = list()
        self.curves = list()
        for i in range(len(self.exg_channels)):
            p = self.win.addPlot(row=i, col=0)
            p.showAxis('left', False)
            p.setMenuEnabled('left', False)
            p.showAxis('bottom', False)
            p.setMenuEnabled('bottom', False)
            if i == 0:
                p.setTitle('TimeSeries Plot')
            self.plots.append(p)
            curve = p.plot()
            self.curves.append(curve)

    def update(self):
        # get_current_board_data doesn’t remove data from the internal buffer, so it allows us to implement sliding window using a single method and little effort
        data = self.board_shim.get_current_board_data(self.num_points)
        transmit_data = []  # this should be sent to the feature extractor (after reformatting!); contains data from 8 channels, each with length 257
        for count, channel in enumerate(self.exg_channels):
            # plot timeseries
            DataFilter.detrend(data[channel], DetrendOperations.LINEAR.value)
            # Band pass filter of 2-42 Hz
            DataFilter.perform_bandpass(data[channel], self.sampling_rate, 22, 20, 2,
                                        FilterTypes.BUTTERWORTH.value, 0)
            # Band stop filter 1 (notch filter) of 60 Hz (+/-1)
            DataFilter.perform_bandstop(data[channel], self.sampling_rate, 60.0, 1.0, 2,
                                        FilterTypes.BUTTERWORTH.value, 0)
            # Fast Fourier Transform (unnecessary)
            # fft = DataFilter.perform_fft(data[channel][:512], WindowFunctions.NO_WINDOW.value)  # data length has to be a power of 2 (currently 512)
            # transmit_data.append(fft.tolist())
            transmit_data.append(data[channel].tolist())
            #self.curves[count].setData(data[channel].tolist())
        # self.app.processEvents()
        print(transmit_data)

    def extractFeatures(self, data):
        window_length = 525  # 1 sec
        target_freqs = [8, 12, 28]
        sampling_freq = 250  # 256 Hz
        extractor = CcaExtraction(window_length, target_freqs, sampling_freq)
        return extractor.extract_features(data)


def main():
    BoardShim.enable_dev_board_logger()
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    # use docs to check which parameters are required for specific board, e.g. for Cyton - set serial port
    parser.add_argument('--timeout', type=int, help='timeout for device discovery or connection', required=False,
                        default=0)
    parser.add_argument('--ip-port', type=int, help='ip port', required=False, default=0)
    parser.add_argument('--ip-protocol', type=int, help='ip protocol, check IpProtocolType enum', required=False,
                        default=0)
    parser.add_argument('--ip-address', type=str, help='ip address', required=False, default='')
    parser.add_argument('--serial-port', type=str, help='serial port', required=False,
                        default='COM3')
    parser.add_argument('--mac-address', type=str, help='mac address', required=False, default='')
    parser.add_argument('--other-info', type=str, help='other info', required=False, default='')
    parser.add_argument('--streamer-params', type=str, help='streamer params', required=False, default='')
    parser.add_argument('--serial-number', type=str, help='serial number', required=False, default='')
    parser.add_argument('--board-id', type=int, help='board id, check docs to get a list of supported boards',
                        required=False, default=0)
    parser.add_argument('--file', type=str, help='file', required=False, default='')
    args = parser.parse_args()

    params = BrainFlowInputParams()
    params.ip_port = args.ip_port
    params.serial_port = args.serial_port
    params.mac_address = args.mac_address
    params.other_info = args.other_info
    params.serial_number = args.serial_number
    params.ip_address = args.ip_address
    params.ip_protocol = args.ip_protocol
    params.timeout = args.timeout
    params.file = args.file

    try:
        board_shim = BoardShim(args.board_id, params)
        board_shim.prepare_session()
        board_shim.start_stream(450000, args.streamer_params)  # 30 min stream
        time.sleep(2)  # wait for 2 secs (not enough data at the very beginning)
        g = Graph(board_shim)
    except BaseException as e:
        logging.warning('Exception', exc_info=True)
    finally:
        logging.info('End')
        if board_shim.is_prepared():
            logging.info('Releasing session')
            board_shim.release_session()


if __name__ == '__main__':
    main()
