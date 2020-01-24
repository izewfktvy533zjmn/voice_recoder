#!/usr/bin/env python3

from datetime import datetime
import multiprocessing as mp
import os
import wave
import zipfile

import pyaudio

RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 6 # change base on firmwares, 1_channel_firmware.bin as 1 or 6_channels_firmware.bin as 6
RESPEAKER_WIDTH = 2
# run getDeviceInfo.py to get index
RESPEAKER_INDEX = 2  # refer to input device id
CHUNK = 2**11
RECORD_SECONDS = 60

audio = pyaudio.PyAudio()


def zip_recorded_data(file_name_str, extension):
    with zipfile.ZipFile(file_name_str + ".zip", 'w', compression=zipfile.ZIP_DEFLATED) as new_zip:
        new_zip.write(file_name_str + extension)


def store_recorded_data(audio, file_name_str, recorded_data):
    print("* storing recorded data")

    wf = wave.open(file_name_str + ".wav", 'wb')
    wf.setnchannels(RESPEAKER_CHANNELS)
    wf.setsampwidth(audio.get_sample_size(audio.get_format_from_width(RESPEAKER_WIDTH)))
    wf.setframerate(RESPEAKER_RATE)
    wf.writeframes(b''.join(recorded_data))
    wf.close()

    zip_recorded_data(file_name_str, ".wav")

    os.remove(file_name_str + ".wav")

    print("* done storing recorded data")
    print()


if __name__ == '__main__':
    while True:
        stream = audio.open(
            rate=RESPEAKER_RATE,
            format=audio.get_format_from_width(RESPEAKER_WIDTH),
            channels=RESPEAKER_CHANNELS,
            input=True,
            input_device_index=RESPEAKER_INDEX,)
    
        timestamp_datetime = datetime.now()
        file_name_str = "./data/" + timestamp_datetime.strftime("%Y-%m-%dT%H:%M:%S")
        recorded_data = []
        
        print(file_name_str)
        print("* recording")

        for i in range(0, int(RESPEAKER_RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            recorded_data.append(data)
        
        stream.stop_stream()
        stream.close()
        print("* done recording")
        print()

        process = mp.Process(target=store_recorded_data, args=(audio, file_name_str, recorded_data))
        process.start()
        
    audio.terminate()

