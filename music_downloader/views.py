from django.shortcuts import render
from .forms import PlaylistForm
import yt_dlp
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def download_playlist(request):
    form = PlaylistForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            playlist_url = form.cleaned_data['playlist_url']
            quality = form.cleaned_data['quality']
            playlist_id = playlist_url.split('/')[-1].split('?')[0]

            sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
                client_id='757b0f4469114fde814fb7bdfc2b61ba',
                client_secret='6dc78dae9e8d43bcb79ff4a9a76038f0'))

            playlist = sp.playlist(playlist_id)
            tracks = playlist['tracks']['items']
            track_list = [{'name': item['track']['name'], 'artist': item['track']['artists'][0]['name']} for item in tracks]

            if 'fetch_songs' in request.POST:
                print(f"Tracks found: {track_list}")
                return render(request, 'music_downloader/playlist_details.html', {
                    'playlist': playlist,
                    'track_list': track_list,
                    'quality': quality,
                })

            elif 'download_selected' in request.POST:
                selected_tracks = request.POST.getlist('tracks')
                print(f"Selected tracks: {selected_tracks}")

                for track in selected_tracks:
                    track_name, artist_name = track.split('|')
                    download_song(track_name.strip(), artist_name.strip(), quality)

                return render(request, 'music_downloader/success.html')

        else:
            print("Form is not valid. Errors:", form.errors)

    return render(request, 'music_downloader/download.html', {'form': form})

def download_song(track_name, artist_name, quality='192'):
    query = f"{track_name} {artist_name}"
    ydl_opts = {
        'format': f'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': quality,
        }],
        'ffmpeg_location': 'C:\\Users\\prana\\Downloads\\ffmpeg-master-latest-win64-gpl\\ffmpeg-master-latest-win64-gpl\\bin',
        'outtmpl': f'{query}.mp3',
    }

    print(f"Downloading song: {query}")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"ytsearch:{query}"])
