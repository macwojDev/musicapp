from dotenv import load_dotenv
import os
import base64
from requests import post,get
import json
import urllib.request

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
save_path = '/static/images/'

def get_token():
    auth_string = f'{client_id}:{client_secret}'
#   dekodowanie danych binarnych
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization':f'Basic {auth_base64}',
        'Content-Type':'application/x-www-form-urlencoded',
    }
    data = {'grant_type':'client_credentials'}
#   wysyłanie danych w celu otrzymania tokenu
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result['access_token']
    return token

def get_auth_header(token):
    return {'Authorization':f'Bearer {token}'}

def search_for_artist(token, artist_name):
    url = 'https://api.spotify.com/v1/search'
    headers = get_auth_header(token)
    query = f'?q={artist_name}&type=artist&limit=1'

    query_url = f'{url}{query}'
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)['artists']['items']
    if len(json_result) == 0:
        print("No artist with this name exists...")
        return None
    return json_result[0]

def get_songs_by_artist(token, artist_id):
    url = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US'
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)['tracks']
    return json_result

def get_artist_image(token, artist_id, save_path=save_path):
    headers = get_auth_header(token)
    url = f'https://api.spotify.com/v1/artists/{artist_id}'
    response = get(url, headers=headers)
    data = response.json()

    if 'images' in data and data['images']:
        image_url = data['images'][0]['url']
        urllib.request.urlretrieve(image_url, save_path)
        return image_url
    else:
        return None

'''
result = search_for_artist(token, 'Mery Spolsky')
artist_id = result['id']
print(result['name'])
songs = get_songs_by_artist(token, artist_id)
# wyświetlanie wyników jednocześnie numerując je, tworząc ranking
for idx, song in enumerate(songs):
    print(f'{idx + 1}. {song["name"]}')
'''