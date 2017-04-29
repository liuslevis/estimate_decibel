import wave
import numpy as np
import math
from scipy.io.wavfile import read
import matplotlib.pyplot as plt



name = '10sec'
label_path = 'data/%s.label.csv' % name
wav_path =   'data/%s.input.wav' % name #16 bit
bit = 16

ios_decibels = []
with open(label_path) as f:
    for line in f.readlines()[1:]:
        ios_decibels.append(float(line))

samples = len(ios_decibels)

samprate, wavdata = read(wav_path)
numchunks = samples
chunks = np.array_split(wavdata, numchunks)
chunks = list(map(lambda x:x.astype(np.float32), chunks))
decibels = []
chunk_rms = []

for chunk in chunks:
    rms = np.mean(np.sqrt(np.abs(chunk ** 2)))
    # db = 20 * math.log10(rms/(2**bit))  # Acoustic dB
    # db = math.log2(rms) * 6.0  - 80 # our dB
    db = math.log10(rms) * 10  - 50 # our dB
    
    decibels.append(db)
    chunk_rms.append(rms)



fig = plt.figure()

ax1 = fig.add_subplot(321)
ax1.set_title('estimate dB')
ax1.set_autoscale_on(False)
ax1.plot(decibels)
plt.axis([0,samples,-50,0])

ax5 = fig.add_subplot(322)
ax5.set_title('target dB')
ax5.set_autoscale_on(False)
ax5.plot(ios_decibels)
plt.axis([0,samples,-50,0])


ax2 = fig.add_subplot(323)
ax2.set_title('wave')
ax2.plot(wavdata)

ax3 = fig.add_subplot(324)
ax3.set_title('p_rms')
ax3.plot(chunk_rms)

plt.show()