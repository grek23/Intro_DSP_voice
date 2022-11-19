from scipy.io.wavfile import read, write
import matplotlib.pyplot as plt
from numpy.fft import fft,ifft
import numpy as np

TEST = False

def main():
    print("Hello world dsp")

    Fs, data = read("hello_world_input.wav")
    print(Fs)
    print(data[0:10, 0])
    print(data[0:10, 1])
    
    data_ch1 = data[:, 0]
    t_axis = np.arange(len(data_ch1))/Fs
    time_plots(t_axis, data_ch1)

    #into the frequency domain
    X = fft(data_ch1)
    #data in the form of z = a + bj

    N = len(X)
    T = N/Fs
    freq_axis = np.arange(N)/T
    freq_plots(freq_axis, X, 5000)

    #lets build a filter
    H = filter_HP(freq_axis, X, 440.0)
    freq_plots(freq_axis, H, 5000)

    h = ifft(H)
    write("HP_filtered.wav", Fs, h.astype(np.int32))

def filter_HP(freq_axis, X, f):
    i = 0
    H = []
    cnt = 0

    while i < len(X):
        if freq_axis[i] < f:
            #supress
            H.append( X[i]/ abs(X[i]) )
            cnt = 1 + cnt
        else:
            H.append(X[i])
        i = 1 + i

    i = 1
    while i < cnt:
        H[len(H) - i] = H[len(H) - i]/ abs(H[len(H) - i])
        i = 1 + i

    return H

def time_plots(t, x):
    plt.figure()
    plt.plot(t, x)
    plt.ylabel("Signal")
    plt.xlabel("Time in [s]")
    plt.title("Signal vs Time")
    plt.show()

def freq_plots(freq_axis, X, N):
    plt.figure()
    plt.plot(freq_axis, np.abs(X))
    plt.ylabel("Amp")
    plt.xlabel("Frequency in [Hz]")
    plt.show()

    plt.figure()
    plt.plot(freq_axis[0:N], np.abs(X[0:N]))
    plt.ylabel("Amp")
    plt.xlabel("Frequency in [Hz]")
    plt.title("Left side")
    plt.show()

    plt.figure()
    plt.plot(freq_axis[len(X) - N:len(X)], np.abs(X[len(X) - N:len(X)]))
    plt.ylabel("Amp")
    plt.xlabel("Frequency in [Hz]")
    plt.title("Right side")
    plt.show()

if __name__ == '__main__':
    main()