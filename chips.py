import numpy as np
import pyaudio

# dictionary of notes and 'frequencies'
NOTES =     {'0a': 110,
             '0ab': 103.82,
             '0b': 123.48,
             '0bb': 116.54,
             '0c': 65.4,
             '0d': 73.42,
             '0db': 69.3,
             '0e': 82.4,
             '0eb': 77.78,
             '0f': 87.3,
             '0g': 98,
             '0gb': 92.5,
             '1a': 220,
             '1ab': 207.64,
             '1b': 246.96,
             '1bb': 233.08,
             '1c': 130.8,
             '1d': 146.84,
             '1db': 138.6,
             '1e': 164.8,
             '1eb': 155.56,
             '1f': 174.6,
             '1g': 196,
             '1gb': 185.0,
             '2a': 440,
             '2ab': 415.28,
             '2b': 493.92,
             '2bb': 466.16,
             '2c': 261.6,
             '2d': 293.68,
             '2db': 277.2,
             '2e': 329.6,
             '2eb': 311.12,
             '2f': 349.2,
             '2g': 392,
             '2gb': 370.0,
             '3a': 880,
             '3ab': 830.56,
             '3b': 987.84,
             '3bb': 932.32,
             '3c': 523.2,
             '3d': 587.36,
             '3db': 554.4,
             '3e': 659.2,
             '3eb': 622.24,
             '3f': 698.4,
             '3g': 784,
             '3gb': 740.0,
             '4a': 1760,
             '4ab': 1661.12,
             '4b': 1975.68,
             '4bb': 1864.64,
             '4c': 1046.4,
             '4d': 1174.72,
             '4db': 1108.8,
             '4e': 1318.4,
             '4eb': 1244.48,
             '4f': 1396.8,
             '4g': 1568,
             '4gb': 1480.0,
             '5a': 3520,
             '5ab': 3322.24,
             '5b': 3951.36,
             '5bb': 3729.28,
             '5c': 2092.8,
             '5d': 2349.44,
             '5db': 2217.6,
             '5e': 2636.8,
             '5eb': 2488.96,
             '5f': 2793.6,
             '5g': 3136,
             '5gb': 2960.0,
             '6a': 7040,
             '6ab': 6644.48,
             '6b': 7902.72,
             '6bb': 7458.56,
             '6c': 4185.6,
             '6d': 4698.88,
             '6db': 4435.2,
             '6e': 5273.6,
             '6eb': 4977.92,
             '6f': 5587.2,
             '6g': 6272,
             '6gb': 5920.0,
             '7a': 14080,
             '7ab': 13288.96,
             '7b': 15805.44,
             '7bb': 14917.12,
             '7c': 8371.2,
             '7d': 9397.76,
             '7db': 8870.4,
             '7e': 10547.2,
             '7eb': 9955.84,
             '7f': 11174.4,
             '7g': 12544,
             '7gb': 11840.0,
             '8a': 28160,
             '8ab': 26577.92,
             '8b': 31610.88,
             '8bb': 29834.24,
             '8c': 16742.4,
             '8d': 18795.52,
             '8db': 17740.8,
             '8e': 21094.4,
             '8eb': 19911.68,
             '8f': 22348.8,
             '8g': 25088,
             '8gb': 23680.0,
             '9a': 56320,
             '9ab': 53155.84,
             '9b': 63221.76,
             '9bb': 59668.48,
             '9c': 33484.8,
             '9d': 37591.04,
             '9db': 35481.6,
             '9e': 42188.8,
             '9eb': 39823.36,
             '9f': 44697.6,
             '9g': 50176,
             '9gb': 47360.0}

# maps notes to 'frequencies' (?)
n_to_f = lambda n_list: np.array(map(NOTES.get, n_list))

class Melody:
#fs is SAMPLE RATE in pyaudio

#original values
#fs=44100
# 44.1 KHz seems to be some kinda standard samplping rate, hmm..
#phaser=0
    def __init__(self, freq_list, dur_list, tamb_list, 
                 fs=44100, phaser=0, vol=.2):
        self.fs = fs
        self.freqs = freq_list
        self.durs = dur_list
        self.tambs = tamb_list
        self.attacks = [np.ceil(t) for t in tamb_list]
        self.phaser = phaser
        self.n_notes = len(freq_list);
        self.vol = vol;

        p = pyaudio.PyAudio()
        self.stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=self.fs,
                output=True)

        self.melody = map(lambda t: self.__make_square(t[0], t[1], t[2], t[3]),
                          zip(freq_list, dur_list, tamb_list, self.attacks))

    def playForever(self):
        while(True):
            for samp in self.melody:
                self.stream.write(samp)

    def play(self):
        for samp in self.melody:
            self.stream.write(samp)



    def add_and_play(self, m2):
        new_m = map(lambda t: self.__add_waves(t[0], t[1]), zip(self.melody, m2.melody))
        while(True):
            for samp in new_m:
                self.stream.write(samp);

    def __add_waves(self, w1, w2):
        l = min(w1.shape[0], w2.shape[0])
        new_w = w1[:l] + w2[:l]
        return new_w / (new_w.max())

    def __make_square(self, f, d, p=.5, on=True):
        # if note is a rest, return zeros
        if on == False:
            return np.zeros(int(self.fs * 4 * d))
        # otherwise, build note with frequency f
        w_len = int(round(self.fs / float(f)))
        s_dur = int(round(self.fs * d / w_len))
        n0s = int(round(w_len*p))
        n1s = int(round(w_len*(1-p)))
        out  = ([0]*n0s + [1]*n1s) * 10 * s_dur
        return self.vol * np.array(out[0:int(self.fs * 4 * d)])

# DEMO
if __name__ == "__main__":

    notes = ["1d","1a","2db","2e","2gb","2b","3db","1d","1a","2db","2e","2gb","2b","3db","3e","3gb"]
    b = .48/4
    #melody init contract: frequency list, duration list, tamb list
    m = Melody(n_to_f(notes),
               [b]*len(notes),
               ([.3])*(len(notes)), phaser=0)

    m.playForever()


