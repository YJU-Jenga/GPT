import os
import numpy as np
import librosa
import tensorflow as tf
from tensorflow.keras import layers


def load_timit_dataset(timit_path, sample_rate=16000):
    speakers = []
    data = []
    labels = []

    for speaker_path in os.listdir(timit_path):
        speaker_full_path = os.path.join(timit_path, speaker_path)

        for file_path in os.listdir(speaker_full_path):
            file_full_path = os.path.join(speaker_full_path, file_path)

            if file_full_path.endswith('.WAV'):
                label = 0 if speaker_path.startswith('F') else 1

                waveform, _ = librosa.load(file_full_path, sr=sample_rate, mono=True)
                mfccs = librosa.feature.mfcc(waveform, sr=sample_rate, n_mfcc=13)

                data.append(mfccs)
                labels.append(label)

    return np.array(data), np.array(labels)


def create_model(input_shape):
    model = tf.keras.Sequential([
        layers.Input(shape=input_shape),
        layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(128, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Flatten(),
        layers.Dense(128, activation="relu"),
        layers.Dropout(0.5),
        layers.Dense(1, activation="sigmoid")
    ])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(),
        loss=tf.keras.losses.BinaryCrossentropy(),
        metrics=["accuracy"]
    )

    return model


timit_path = 'path/to/TIMIT/dataset'
data, labels = load_timit_dataset(timit_path)

model_input_shape = data.shape[1:]
model = create_model(model_input_shape)

model.fit(data, labels, epochs=10, batch_size=32)
