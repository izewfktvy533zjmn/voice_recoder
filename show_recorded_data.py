#!/usr/bin/env python3

import os

import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf

PATH = "./data/"


if __name__ == "__main__":
    for file_name in sorted(os.listdir(PATH)):
        print(file_name)
        wave, fs = sf.read(PATH + file_name)

        time = np.arange(0,len(wave)) / fs

        plt.plot(time, wave)
        plt.title(file_name)
        plt.show()
        plt.close()
