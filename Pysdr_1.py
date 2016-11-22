import matplotlib.pyplot as plt
from scipy import signal as sp_sig
import numpy as np
import wave
import sys


# ################### Signal ############################
f = 'C:\\Projekte\\Wetter\\rtl-weather-6.wav'
f = 'C:\\Projekte\\Wetter\\test_wav.wav'
spf = wave.open(f)

signal = spf.readframes(-1)
signal = np.fromstring(signal, 'Int16')*-0.1
signal_raw = signal * 1.0
signal[0:4800] = 0
signal_raw[0:4800] = 0

high_index = signal>=600
low_index = signal<600

signal[high_index] = 600
signal[low_index] = 0
signal[0] = 2
signal[1] = -1


fs = spf.getframerate()
sig_start = 0
sig_end = len(signal)/fs
sig_length = len(signal)
sig_time = np.linspace(sig_start, sig_end, num = sig_length)

# ######################## Clock #########################
pos_t = []
pos_i = []
for i in range(sig_length-1):
    if signal[i] == 0 and signal[i+1] == 600:
        pos_t.append( sig_time[i])
        pos_i.append (i)

delta = pos_t[0]
freq = 10/(pos_t[10]-pos_t[0])
duration_t = 1/freq
duration_i = int(round(duration_t*fs))

t = np.linspace(sig_start-delta, sig_end-delta, num = sig_length, endpoint=False)
#print(t)

#print(t)
#print(sig_time)
clock =  sp_sig.square(2 * np.pi * freq*2 * t)
clock = clock * 0.5 + 0.5
clock = clock *600
t = t + delta 


for i in range(pos_i[0]):
    clock[i] =0

for i in range(pos_i[-1]+int(duration_i),sig_length):
    clock[i] =0

for i in range(sig_length-1):
    if clock[i] == 1 and clock[i+1] == 0:
        #print(i)
        
        if signal[i] == 0 :
            print("1")
        if signal[i] == 1:
            print("0")
        
        
# ######################## Plot ##########################


plt.figure(1)
plt.title('Signal Wave...')
plt.plot(sig_time,signal)
plt.plot(sig_time,signal_raw)
plt.plot(t,clock)
plt.ylim(-2000, 2000)
plt.xlim(0.04, 0.29)
plt.show()
