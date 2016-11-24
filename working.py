import matplotlib.pyplot as plt
from scipy import signal as sp_sig
import numpy as np
import wave
import sys

for i in range(100):
    print(i)
    start = 15 +i*0.10
    # init
    string = ''
    valid_string = string
    
    # config
    file_name = 'C:\\Projekte\\Wetter\\home.wav'
    signal_start = start
    signal_duration = 0.2
    signal_end = signal_start+signal_duration
    
    # input
    file = wave.open(file_name)
    
    # calculate meta
    frame_rate = file.getframerate()
    signal_start_frame = int(signal_start * frame_rate)
    signal_duration_frames = int(signal_duration * frame_rate)
    
    # read in data

    if start+signal_duration < file.getnframes()/frame_rate:
        file.setpos(signal_start_frame)
    data = file.readframes(signal_duration_frames)
    data = np.fromstring(data, 'Int16')
    data_amplitude_shift = (max(data)+min(data))/2
    data = (data-data_amplitude_shift)/(2*data_amplitude_shift)
    
    data_length = len(data)
    data_time = np.linspace(signal_start, signal_end, num = data_length)
    
    # make analog data binary
    high_index = data>=0
    low_index = data<0
    
    digital_signal = np.zeros(data_length)
    digital_signal[high_index] = 1
    digital_signal[low_index] = 0
    
    # calculate pulse information
    pulse_duration = []
    gap_duration = []
    pos_up = 0
    pos_down = 0
    for i in range(len(digital_signal)-1):
        switch = False
        if digital_signal[i] == 0 and  digital_signal[i+1] == 1:
            pos_up = i
            switch = True
        if digital_signal[i] == 1 and  digital_signal[i+1] == 0:
            pos_down = i
            switch = True
            
        if switch == True and pos_up<pos_down:
            pulse_duration.append((pos_down-pos_up))
        if switch == True and pos_down<pos_up:
            gap_duration.append((pos_up-pos_down))
    
    #   create binary string
    low = 0
    low_count = 0
    mid = 0
    mid_count = 0
    high = 0
    high_count = 0
    string = ''
    for i in range(len(gap_duration)):
        sample = gap_duration.pop(0)
        if sample > 91 and sample <97:
            low += sample
            low_count += 1
            string += '0'
        if sample > 187 and sample <193:
            mid += sample
            mid_count += 1
            string += '1'
        if sample > 376 and sample <382:
            high += sample
            high_count += 1
            #print(string)
            if len(string) == 36:
                valid_string = string
            string = ''
    #print("short gap duration in ms: " + str((low/low_count)/frame_rate*1000))
    #print("long gap duration in ms: " + str((mid/mid_count)/frame_rate*1000))
    #print("separator gap duration in ms: " + str((high/high_count)/frame_rate*1000))
    #print("Pulse lenght in ms: " + str((sum(pulse_duration)/len(pulse_duration))/frame_rate*1000))
    
    # extract temperature
    string = valid_string
    
    adr = string[0:8]
    vxbt = string[8:12]
    temp = string[12:24]
    hum = string[24:32]
    chk = string[32:36]
    
    def complement_bitstring(s, bits):
        """calculates the decimal expressen of a MSB bitstring "s" with given bitcount "bits"  """
        if len(s) != bits:
            return
        sum = 0
        for i in range(bits):
            sum += int(s[i]) *(1<<bits-1-i)
        
        if s[0] == "1":
            sum = -1 * ((1<<bits) - sum)    
        return (sum)
        
    t = complement_bitstring(temp, 12)
    if t:
        print(str(t/10) + "°C")


# ######################## Plot ##########################


# plt.figure(1)
# plt.title('Signal Wave...')
# plt.plot(data_time,data)
# plt.plot(data_time,digital_signal)
# plt.ylim(-2000, 2000)
# plt.xlim(signal_start, signal_end)
# plt.show()
