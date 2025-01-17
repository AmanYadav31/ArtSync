# -*- coding: utf-8 -*-

import os
import base64
from requests import post, get
import json
import requests

import pandas as pd

client_id = "90c6a24b1f834ea983552408dff6216c"
client_secret = "41c75eca56444fc1a5cab604b79fcce6"

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_track_id(s_name, token):
    # Replace 'SONG_NAME' with the name of the song you want to search for
    song_name = s_name

# Make the API request to search for the song
    headers = {'Authorization': 'Bearer ' + token}
    url = f'https://api.spotify.com/v1/search?q={song_name}&type=track'
    response = requests.get(url, headers=headers)

# Parse the response and extract the track ID
    if response.status_code == 200:
        search_results = response.json()
        tracks = search_results['tracks']['items']
        if len(tracks) > 0:
            first_track = tracks[0]
            track_id = first_track['id']
            # print('Track ID:', track_id)
        else:
            print('No tracks found for the given search query.')
    else:
        print('Error occurred while searching for the song:', response.status_code)
    return track_id

def get_feature(song_id, token):

    headers = {'Authorization': 'Bearer ' + token}
    audio_features_url = f'https://api.spotify.com/v1/audio-features/{song_id}'
    track_url = f'https://api.spotify.com/v1/tracks/{song_id}'

    audio_features_response = requests.get(audio_features_url, headers=headers)
    track_response = requests.get(track_url, headers=headers)

    features = {}

    if audio_features_response.status_code == 200 and track_response.status_code == 200:
        audio_features = audio_features_response.json()
        track_info = track_response.json()



        tempo = audio_features['tempo']
        features['Beats Per Minute(BPM)'] = tempo
        energy = audio_features['energy']
        features['Energy'] = energy
        danceability = audio_features['danceability']
        features['Danceability'] = danceability
        loudness = audio_features['loudness']
        features['Loudness(dB)'] = loudness
        liveness = audio_features['liveness']
        features['Liveness'] = liveness
        valence = audio_features['valence']
        features['Valence'] = valence
        length = audio_features['duration_ms']
        features['Length (Duration)'] = length
        acousticness = audio_features['acousticness']
        features['Acousticness'] = acousticness
        speechiness = audio_features['speechiness']
        features['Speechiness'] = speechiness
        popularity = track_info['popularity']
        features['Popularity'] = popularity



    else:
        return 'Error occurred while retrieving audio features:', audio_features_response.status_code

    df1 = pd.DataFrame.from_dict(features, orient='index').T
    return df1

