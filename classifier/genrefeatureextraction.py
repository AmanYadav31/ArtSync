# -*- coding: utf-8 -*-


import librosa
import librosa.display
import IPython.display as ipd
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from scipy.stats import kurtosis, skew
from scipy.signal import find_peaks
from sklearn.preprocessing import StandardScaler

def feature_extraction(file_path):
  # Load the audio file
  x, sample_rate = librosa.load(file_path)
  features = {}
  spectrogram = librosa.stft(x)
  power_spectrogram = np.abs(spectrogram) ** 2

  chroma = np.mean(librosa.feature.chroma_stft(y=x, sr=sample_rate).T,axis=0)
  features['chroma_stft_mean'] = np.mean(chroma)
  features['chroma_stft_var'] = np.var(chroma)


  features['rms_mean'] = librosa.feature.rms(y=x).mean()
  features['rms_var'] = librosa.feature.rms(y=x).var()
  
  
  # Compute the spectral centroid feature
  spectral_centroids = librosa.feature.spectral_centroid(y=x, sr=sample_rate)
  features['spectral_centroid_mean'] = spectral_centroids.mean()
  features['spectral_centroid_var'] = spectral_centroids.var()
  
  # Compute the spectral spread feature
  spectral_spreads = librosa.feature.spectral_bandwidth(y=x, sr=sample_rate)
  features['spectral_bandwidth_mean'] = spectral_spreads.mean()
  features['spectral_bandwidth_var'] = spectral_spreads.var()

  # Calculate the rolloff feature
  rolloff = librosa.feature.spectral_rolloff(y=x, sr=sample_rate)
  features['rolloff_mean'] = np.mean(rolloff)
  features['rolloff_var'] = np.var(rolloff)

  # Calculate the zero-crossing rate feature
  zero_crossing_rate = librosa.feature.zero_crossing_rate(y=x)
  features['zero_crossing_rate_mean'] = np.mean(zero_crossing_rate)
  features['zero_crossing_rate_var'] = np.var(zero_crossing_rate)

  features['harmony_mean'] = librosa.feature.delta(power_spectrogram, order=1, axis=-1).mean()
  features['harmony_var'] = librosa.feature.delta(power_spectrogram, order=1, axis=-1).mean()


  # Extract perceptual spread
  spectral_contrast = librosa.feature.spectral_contrast(y=x, sr=sample_rate)

  # Compute mean and variance
  features['perceptr_mean'] = spectral_contrast.mean()
  features['perceptr_var'] = spectral_contrast.var()

  features['tempo'] = librosa.feature.tempo(y=x, sr=sample_rate)[0].mean()

  mfccs = librosa.feature.mfcc(y=x, sr=sample_rate, n_mfcc=21)
  for i in range(1,21):
    features[f'mfcc{i}_mean'] = mfccs[i-1].mean()
    features[f'mfcc{i}_var'] = mfccs[i-1].var()

 

  df1 = pd.DataFrame.from_dict(features, orient='index').T
  scaler = StandardScaler()
  data_scaled = scaler.fit_transform(df1)
 
  return df1


x = 'music_sample\Energetic.mp3'
features_1 = feature_extraction(x)
print(features_1)

