import os
import mne

directory = r'EDFs/DASS21-EDFs-Initial'
target_dir = r'segmented_DASS21_edfs'

for entry in os.scandir(directory):
    if (entry.path.endswith(".edf") and entry.is_file()):
        filepath = entry.path
        filename = entry.name
        filename = filename[:-4]
        print(filename)
        raw = mne.io.read_raw_edf(filepath, preload=True)
        raw_highpass = raw.filter(l_freq=0.1, h_freq=None)
        freqs = (50, 100)
        raw_notch = raw_highpass.copy().notch_filter(freqs=freqs)

        annot = raw_notch.annotations
        target_subject = os.path.join(target_dir, filename)
        if not os.path.exists(target_subject):
            os.mkdir(target_subject)
        for i in range(annot.__len__() - 1):
            raw_copy = raw_notch.copy()
            raw_i = raw_copy.crop(annot.onset[i], annot.onset[i+1])
            target_filename = annot.description[i] + '_' + annot.description[i+1] + '_raw.fif'
            target_path = os.path.join(target_subject, target_filename)
            raw_i.save(target_path, overwrite=True)
