import librosa
import numpy as np

def extract_audio_features(audio_path):
    y, sr = librosa.load(audio_path, sr=None)

    rms = librosa.feature.rms(y=y)[0]
    energy = float(np.mean(rms))

    pitches, _ = librosa.piptrack(y=y, sr=sr)
    pitch_values = pitches[pitches > 0]
    pitch_variance = float(np.var(pitch_values)) if len(pitch_values) > 0 else 0

    silence_ratio = float(np.mean(rms < 0.01))
    duration = librosa.get_duration(y=y, sr=sr)

    return {
        "duration": duration,
        "energy": energy,
        "pitch_variance": pitch_variance,
        "silence_ratio": silence_ratio
    }
