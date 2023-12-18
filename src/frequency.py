from external_libraries import *


class Frequency:
    def __init__(self, directory: str):
        self.directory = directory

    def get_spectral_centroid(self) -> List[float]:
        spectral_centroids = []
        for root, dirs, files in os.walk(self.directory):
            for file in files:
                if file.endswith(".mp3") or file.endswith(".wav"):
                    file_path = os.path.join(root, file)
                    y, sr = librosa.load(file_path, sr=None)
                    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
                    spectral_centroids.append(spectral_centroid)

                    print(f"Processing {file_path}: Spectral Centroid = {spectral_centroid}")

                    # self._plot_spectral_centroid(spectral_centroid, file_path)

        return spectral_centroids

    def get_spectrogram(self) -> List[List[float]]:
        spectrograms = []
        for root, dirs, files in os.walk(self.directory):
            for file in files:
                if file.endswith(".mp3") or file.endswith(".wav"):
                    file_path = os.path.join(root, file)
                    y, sr = librosa.load(file_path, sr=None)
                    spectrogram = librosa.amplitude_to_db(librosa.stft(y), ref=np.max)
                    spectrograms.append(spectrogram)

                    print(f"Processing {file_path}: Spectrogram = {spectrogram}")

                    # self._plot_spectrogram(spectrogram, file_path)

        return spectrograms

    def _plot_spectral_centroid(self, spectral_centroid, file_path):
        plt.figure(figsize=(10, 6))
        plt.semilogy(spectral_centroid.T, label='Spectral Centroid')
        plt.ylabel('Hz')
        plt.xticks([])
        plt.xlim([0, spectral_centroid.shape[-1]])
        plt.legend(loc='upper right')
        plt.title(f"Spectral Centroid for {file_path}")
        plt.show()

    def _plot_spectrogram(self, spectrogram, file_path):
        plt.figure(figsize=(10, 6))
        librosa.display.specshow(spectrogram, sr=sr, x_axis='time', y_axis='log')
        plt.colorbar(format='%+2.0f dB')
        plt.title(f"Spectrogram for {file_path}")
        plt.show()


def main():
    path = "../data/demo/songs_demo"
    frequency = Frequency(path)

    spectral_centroids = frequency.get_spectral_centroid()
    spectrograms = frequency.get_spectrogram()


if __name__ == "__main__":
    main()
