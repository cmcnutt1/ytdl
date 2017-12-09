import spotipy

sp = spotipy.Spotify()
result = sp.search(q='radiohead', type='artist')
print(result)
