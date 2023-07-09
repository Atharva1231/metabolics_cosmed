# general import
import numpy as np
import os, logging, glob
import matplotlib.pyplot as plt
import pandas as pd

# specific import


class MainDataRead(object):
    def __init__(self, folder_path = 'data/', file_type = 'regular', file_path = None):
        if file_path == None:
            file_list = glob.glob('data/*.xlsx')
        else:
            file_list = [file_path]
        logging.debug(f'reading the following files {file_list}')
        self.file_list = file_list
        self.type = file_type
        self.start_index = 0
        # coutner for column index and the file counter
        self.Reset()
        self._setup()

    def _setup(self):
        self.start_prediction = True
        self.STATUS = True
        # setup the pandas for the reading
        if self.file_number > len(self.file_list):
            raise NotImplementedError('end of files')
        data = pd.read_excel(self.file_list[self.file_number])
        # regular excel created by cosmed
        if self.type == 'regular':
            VO2 = data['VO2'].iloc[2:].to_numpy()
            VCO2 = data['VCO2'].iloc[2:].to_numpy()
            met = 16.56 * VO2 / 60 + VCO2 * 4.52 / 60
            time = data['t'].iloc[2:len(met) + 2]
            time = [c.second + c.minute * 60 + c.hour * 60 * 60 for c in time]
            time = np.array(time)

        # de-identified data with only met and time
        elif self.type == 'de-identified':
            met =  data['met'].to_numpy()
            time = data['time'].to_numpy()

        self._data = np.vstack([met,time])

    def Read(self):
        # read the file in the incremented order
        self.counter += 1
        if self.counter > len(self._data[0,:]):
            try:
                self.file_number += 1
                self._setup()
            except NotImplementedError:
                raise NotImplementedError
        return self._data[:,self.start_index:self.counter]

    def Next(self):
        # to change the file to next
        self.file_number += 1
        try:
            self._setup()
        except NotImplementedError:
            raise NotImplementedError

    # function to make the code start when the optimization starts

    def Set_start(self):
        if self.counter > 10:
            self.start_index = self.counter - 5
        else:
            self.start_index = 0
    def Reset(self):
        # to reset the file number and the index number
        self.counter = 5
        self.file_number = 0

    def Get_data(self):
        """ send the current data"""
        return np.copy(self._data)
