from django import forms

class PlaylistForm(forms.Form):
    playlist_url = forms.URLField(label='Spotify Playlist URL', widget=forms.URLInput(attrs={'class': 'form-control'}))
    quality = forms.ChoiceField(choices=[('128', '128 kbps'), ('192', '192 kbps'), ('320', '320 kbps')], widget=forms.Select(attrs={'class': 'form-control'}))
