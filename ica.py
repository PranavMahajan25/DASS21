
# Importing requisite packages
from os.path import join
import mne
from mne.preprocessing import ICA

# Loading a preprocessed file and plotting
data_folder = join('..', 'Data', 'DASS21-Leah-10-01-2018_20180110_032644_fil')
data_raw_file = join(data_folder, 'Q011_Q02B_raw.fif')

raw = mne.io.read_raw_fif(data_raw_file, preload=True)
raw.plot(title='Raw plot', block=True)

ica = ICA(n_components=32, random_state=97)
ica.fit(raw)

# Plotting ICA components
ica.plot_sources(raw, title='ICA components', block=True)
'''
After the ICA components have been plotted, one only needs to
select the components that are to be excluded from the process
of signal reconstruction
'''

reconst_raw = raw.copy()    # Creating a copy of the initial raw file
ica.apply(reconst_raw)      # Applying ICA to the copy

# Plotting reconstructed signal
reconst_raw.plot(title='Reconstructed signal using ICA components', block=True)
