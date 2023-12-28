import gpxpy
import numpy as np

# Loads GPX data
def load_gpx_data(gpx_files):
    tracks = []
    for file in gpx_files:
        print(f"Loading GPX file: {file}")
        try:
            with open(file, 'r') as f:
                gpx = gpxpy.parse(f)
            # Check for tracks
            for track in gpx.tracks:
                for segment in track.segments:
                    if segment.points:
                        tracks.append(np.array([(point.latitude, point.longitude) for point in segment.points]))
                    else:
                        print("No points in segment.")
            # Check for routes
            for route in gpx.routes:
                if route.points:
                    tracks.append(np.array([(point.latitude, point.longitude) for point in route.points]))
                else:
                    print("No points in route.")
        except Exception as e:
            print(f"Error loading GPX file {file}: {e}")
    return tracks

# Normalizes the tracks
def normalize_tracks(tracks):
    all_points = np.concatenate(tracks, axis=0)
    mean_lat, mean_lon = np.mean(all_points, axis=0)
    std_lat, std_lon = np.std(all_points, axis=0)

    normalized_tracks = []
    for track in tracks:
        normalized_track = (track - [mean_lat, mean_lon]) / [std_lat, std_lon]
        normalized_tracks.append(normalized_track)
    return normalized_tracks, (mean_lat, mean_lon), (std_lat, std_lon)

# Prepares sequences
def prepare_sequences(tracks, sequence_length):
    sequences = []
    next_points = []
    for track in tracks:
        for i in range(len(track) - sequence_length):
            sequences.append(track[i:i + sequence_length])
            next_points.append(track[i + sequence_length])
    return np.array(sequences), np.array(next_points)

# Main function to preprocess GPX files
def preprocess_gpx(files, sequence_length=5):
    tracks = load_gpx_data(files)
    if not tracks:
        print("No tracks to normalize. Exiting preprocessing.")
        return None, None, None, None

    print(f"Normalizing {len(tracks)} tracks.")
    normalized_tracks, mean_coords, std_coords = normalize_tracks(tracks)

    print(f"Preparing sequences from normalized tracks.")
    sequences, next_points = prepare_sequences(normalized_tracks, sequence_length)
    return sequences, next_points, mean_coords, std_coords