import numpy as np
import os
import pandas as pd
import librosa
from sklearn.preprocessing import StandardScaler, MinMaxScaler


def extract_feature_for_audio(y, sr):
    n_fft = min(1024, len(y))  # Set n_fft to the smallest of 1024 or the length of the signal
    mfcc = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40, n_fft=n_fft).T, axis=0)
    mel = np.mean(librosa.feature.melspectrogram(y=y, sr=sr, n_fft=n_fft).T, axis=0)
    stft = np.abs(librosa.stft(y, n_fft=n_fft))
    chroma = np.mean(librosa.feature.chroma_stft(S=stft, y=y, sr=sr, n_fft=n_fft).T, axis=0)
    contrast = np.mean(librosa.feature.spectral_contrast(S=stft, y=y, sr=sr, n_fft=n_fft).T, axis=0)
    tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(y), sr=sr).T, axis=0)
    return mfcc, chroma, mel, contrast, tonnetz  # shape: (40,), (12,), (128,), (7,), (6,)


def generate_feature_file(folder_path, scaler=None, label_folder_map=None):
    columns = ['mfcc'] * 40 + ['chroma'] * 12 + ['mel'] * 128 + ['contrast'] * 7 + ['tonnetz'] * 6 + ['label']
    audio_df_list = []

    label = 0
    label_name_dict = {}

    if label_folder_map is None:
        for sub_directory in os.listdir(folder_path):
            audio_directory = os.path.join(folder_path, sub_directory)

            if not os.path.isdir(audio_directory):
                continue

            label_name_dict[label] = sub_directory

            for filename in os.listdir(audio_directory):
                file_path = os.path.join(audio_directory, filename)
                try:
                    audio, sr = librosa.load(file_path)
                    mfcc, chroma, mel, contrast, tonnetz = extract_feature_for_audio(audio, sr)
                    features = np.hstack([mfcc, chroma, mel, contrast, tonnetz, label])
                    features = np.expand_dims(features, axis=0)
                    audio_df_list.append(features)
                except Exception as e:
                    print(f"Error processing file {file_path}: {str(e)}")

            label += 1
    else:
        for label_name, sub_folders in label_folder_map.items():
            label_name_dict[label] = label_name

            for sub_folder in sub_folders:
                audio_directory = os.path.join(folder_path, sub_folder)

                if not os.path.isdir(audio_directory):
                    continue

                for filename in os.listdir(audio_directory):
                    file_path = os.path.join(audio_directory, filename)
                    try:
                        # noinspection PyTypeChecker
                        audio, sr = librosa.load(file_path)
                        mfcc, chroma, mel, contrast, tonnetz = extract_feature_for_audio(audio, sr)
                        features = np.hstack([mfcc, chroma, mel, contrast, tonnetz, label])
                        features = np.expand_dims(features, axis=0)
                        audio_df_list.append(features)
                    except Exception as e:
                        print(f"Error processing file {file_path}: {str(e)}")

                label += 1

    audio_df = pd.DataFrame(np.concatenate(audio_df_list, axis=0), columns=columns)
    audio_df = audio_df.sample(frac=1).reset_index(drop=True)

    if scaler is not None:
        if scaler == "standard":
            scaler = StandardScaler()
        elif scaler == "minmax":
            scaler = MinMaxScaler()
        else:
            raise ValueError("Invalid scaler type.")

        audio_df.iloc[:, :-1] = scaler.fit_transform(audio_df.iloc[:, :-1])

    return audio_df, label_name_dict
