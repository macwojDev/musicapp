from django.shortcuts import render
from . import getcontent

def index(request):
    return render(request, 'core/index.html')

def artist_stats(request):
    artist_name = request.GET.get('artist')
    token = getcontent.get_token()
    artist = getcontent.search_for_artist(token, artist_name)
    artist_id = artist['id']
    # img = getcontent.get_artist_image(token, artist_id)
    songs = getcontent.get_songs_by_artist(token, artist_id)
    context = {
        'artist_name':artist_name.title(),
        'songs':songs,
        # 'artist_img':img
    }
    return render(request, 'core/artist_stats.html', context)