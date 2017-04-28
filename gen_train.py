import wave
import numpy as np
import math
import sys

if len(sys.argv) < 2:
    print('usage: python3 gen_train.py 10sec')

name = sys.argv[1]

sample_db_path = 'data/%s.label.csv' % name
wav_path = 'data/%s.input.wav' % name #16 bit
out_path = 'data/%s.input.csv' % name

sample_points = None
with open(sample_db_path) as f:
    sample_points = len(f.readlines()) - 1

wr = wave.open(wav_path)
dtype = {16:np.int16, 8:np.int8, 32:np.int32}[wr.getsampwidth() * 8]
framerate = int(wr.getframerate())
nchannels = wr.getnchannels()
nframes = wr.getnframes()
sampWidth = wr.getsampwidth()
seconds = nframes / nchannels / framerate # in seconds
compressname = wr.getcompname() # not compress
compresstype = wr.getcomptype() # NONE
signal = np.fromstring(wr.readframes(-1), dtype=dtype) #mono
time   = np.linspace(0, 100, signal.size)


# x0.15s      1/6.66666666s iOS db 采样率
# 0.0000625s 1/16000s      WAV    采样率
# 从 signal 取 sample_points 个采样点
ret = 'x\n'
step = int(nframes/sample_points)
for i in range(sample_points):
    frm = math.floor(i * step)
    to  = math.floor((i + 1) * step)
    # print(frm, to)
    signals = np.array(signal[frm:to], dtype=np.float64)
    ret += '%.4f\n' % np.mean(np.sqrt(signals ** 2))
    # db = np.log2(
    #     np.mean(
    #         np.abs(signal[frm:to]) / (2**16) ))
    # print(db * 3)

with open(out_path, 'w') as f:
    f.write(ret)
