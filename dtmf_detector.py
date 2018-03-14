#! /usr/bin/python
#-*- coding: utf-8 -*-
import time
import wave
import math
import numpy as np
import re
from cython_goertzel import goertzel

# ~ SearchRules ~
PAUSE = 0 # Fixed pause between 2 DTMF signals in seconds
SIGNAL_DURATION = 0.08 # Duration per one DTMF signal in seconds
LOUDER_COEFF = 2.5 # Times signal louder then AVG(power)

# Search for
def dtmf_keys():
    #KEYNAME = KEYCHARS
    OPEN_KEY = 'A21D'
    CLOSE_KEY = 'D12A'
    return locals()
# ~ END of SearchRules ~


class DTMFdetector():
    def __init__(self, filename):
        self.start_time = time.time()
        self.read_file(filename)
        self.GOERTZEL_N = int(self.samplerate * SIGNAL_DURATION)
        self.samples_normalized = self.normalize_shapes(self.samples_orig)
        self.chunks, self.chunk_duration = self.group_by_chunks(self.samples_normalized)
        self.freqs = [697, 770, 852, 941, 1209, 1336, 1477, 1633]
        self.signals = [["1", "2", "3", "A"], ["4", "5", "6", "B"], ["7", "8", "9", "C"], ["*", "0", "#", "D"]]
        self.coeffs = self.count_coeffs()


    def read_file(self, filename):
        wav = wave.open(filename, mode="r")
        nchannels, sampwidth, self.samplerate, self.nframes_orig, comptype, compname = wav.getparams()
        types = {1: np.int8, 2: np.int16, 4: np.int32}
        self.samples_orig = np.fromstring(wav.readframes(self.nframes_orig), dtype=types[sampwidth])

    def normalize_shapes(self, samples):
        # For equal shaped division
        return np.append(samples, [0]*(self.GOERTZEL_N - (len(samples) % self.GOERTZEL_N)))

    def group_by_chunks(self, samples):
        chunks = np.split(samples, len(samples) / self.GOERTZEL_N)
        chunk_duration = self.GOERTZEL_N * 1.0 / self.samplerate
        return chunks, chunk_duration

    def count_coeffs(self):
        return 2 * np.cos((2 * math.pi / self.samplerate) * np.array(self.freqs))

    def exec_time(self):
        print 'Exec time: %s' % (time.time() - self.start_time)

    def validate_signal(self, powers):
        if max(powers) == 0:
            return
        powers = list(powers)
        row = powers.index(max(powers[:4]))
        col = powers.index(max(powers[4:8]))
        return self.signals[row][col - 4], powers[row], powers[col]

    def catch_dtmfkeys(self, matched_signals):
        # Input structure: {second: [matched_char,....],}
        timing = sorted(matched_signals)
        keys = dtmf_keys()
        MAX_MATCHES = 2

        for key_name in keys:
            chars_cnt = len(keys[key_name])
            key_duration = SIGNAL_DURATION * chars_cnt + PAUSE * (chars_cnt - 1)
            pattern = re.compile(''.join(['%s{1,%s}' % (char, MAX_MATCHES) for char in keys[key_name]]))
            chars_sequence = ''.join([matched_signals[timepoint][0] for timepoint in timing])

            tag_matches = pattern.finditer(chars_sequence)
            for m in tag_matches:
                start_sec, end_sec = round(timing[m.span()[0]], 3), round(timing[m.span()[1]-1] + SIGNAL_DURATION, 3)
                matched_dur = round(end_sec - start_sec, 3)

                if matched_dur == key_duration:
                    self.matched_keys.append({'KEY': keys[key_name], 'time_from': start_sec, 'time_to': end_sec, 'offset': 0})

                else:
                    res = self.catch_dtmfkeys_offset(start_sec, keys[key_name], key_duration)
                    if res:
                        self.matched_keys.append(res)


    def catch_dtmfkeys_offset(self, start_sec, key_chars, key_duration):
        off_range = np.array(range(-50, 60, 10)) / 100.
        offsets = np.array(off_range) * self.chunk_duration * self.samplerate

        for off in offsets:
            start_frame = int(start_sec * self.samplerate + off)
            end_frame = int(start_sec * self.samplerate + off + key_duration * self.samplerate)
            chunks, chunk_dur = self.group_by_chunks(self.normalize_shapes(self.samples_orig[start_frame:end_frame]))

            matches = []
            for index, chunk in enumerate(chunks):
                matched = self.validate_signal(goertzel(chunk, self.coeffs))
                if matched:
                    cur_timepoint = start_frame*1./self.samplerate+index*self.chunk_duration
                    matches.append([cur_timepoint, matched])

            matched_chars = ''.join([char[1][0] for char in matches])

            if matched_chars == key_chars:
                offset_dur = off / self.samplerate
                tpoint_from = min([char[0] for char in matches])
                tpoint_to = max([char[0] for char in matches]) + SIGNAL_DURATION
                offset_dur, tpoint_from, tpoint_to = map(round, [offset_dur, tpoint_from, tpoint_to], [3]*3)
                return {'KEY': matched_chars, 'time_from': tpoint_from, 'time_to': tpoint_to, 'offset': offset_dur}

    def filter_by_avgpower(self, matched_signals):
        filtered = {}
        avg_power = sum([matched_signals[i][1]+matched_signals[i][2] for i in matched_signals]) / (len(matched_signals) * 2)
        match_minpower = avg_power * LOUDER_COEFF

        for timepoint in sorted(matched_signals):
            if matched_signals[timepoint][1] < match_minpower:
                continue
            if matched_signals[timepoint][2] < match_minpower:
                continue
            filtered[timepoint] = matched_signals[timepoint]

        return filtered

    def get_dtmfkeys(self):
        matched_signals, self.matched_keys = {}, []

        for index, chunk in enumerate(self.chunks):
            powers = goertzel(chunk, self.coeffs)
            matched = self.validate_signal(powers)

            if not matched:
                continue

            char, row_power, column_power = matched
            timepoint = index * self.chunk_duration
            matched_signals[timepoint] = [char, row_power, column_power]

        avgpow_filtered = self.filter_by_avgpower(matched_signals)

        self.catch_dtmfkeys(avgpow_filtered)
        self.exec_time()
        return self.matched_keys


for detected_key in DTMFdetector('sample.wav').get_dtmfkeys():
    print detected_key

