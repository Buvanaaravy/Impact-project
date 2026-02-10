def aggregate_features(audio, video, words):
    wpm = (words / audio["duration"]) * 60 if audio["duration"] > 0 else 0
    return {
        **audio,
        **video,
        "words": words,
        "wpm": wpm
    }
