# Importing requisite packages
import os
from os.path import join, exists
from glob import glob
from pathlib import Path

import mne
from mne.preprocessing import ICA

import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()


def perform_ica(data_folder, subject):
    data_raw_files = glob(join(data_folder, '*'))

    for data_raw_file in data_raw_files:
        segment_name = data_raw_file.split('/')[-1]

        raw = mne.io.read_raw_fif(data_raw_file, preload=True)
        raw.plot(title='Raw plot ('+segment_name+')', block=True)

        ica = ICA(n_components=32, random_state=97)
        ica.fit(raw)

        # Plotting ICA components
        ica.plot_sources(raw,
                         title='ICA components ('+segment_name+')',
                         block=True)
        '''
        After the ICA components have been plotted, one only needs to
        select the components that are to be excluded from the process
        of signal reconstruction
        '''

        reconst_raw = raw.copy()    # Creating a copy of the initial raw file
        ica.apply(reconst_raw)      # Applying ICA to the copy

        # Plotting reconstructed signal
        reconst_raw.plot(title='Reconstructed signal ('+segment_name+')',
                         block=True)

        reconst_raw.save(join(reconstructed,
                              subject,
                              segment_name), overwrite=True)


home = str(Path.home())
reconstructed = join(home, 'Reconstructed')
if not exists(reconstructed):
    os.mkdir(reconstructed)

subjects_chosen = []

while(True):
    print('Choose a subject folder')
    data_folder = filedialog.askdirectory()
    subject = data_folder.split('/')[-1]
    if subject in subjects_chosen:
        print('Subject has already been chosen before. Choose another subject')
        continue

    if not exists(join(reconstructed, subject)):
        os.mkdir(join(reconstructed, subject))

    perform_ica(data_folder, subject)
    subjects_chosen.append(subject)

    another_one = input('Do you wish to choose another subject [y/n]: ')
    if another_one == 'n':
        break
