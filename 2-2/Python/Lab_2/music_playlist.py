# music_playlist.py
import random
from collections import defaultdict, deque
from songs import songs_database, genre_index, artist_index
from datetime import datetime

class Playlist:
    def __init__(self, name):
        self.name = name
        self.songs = []
        self.total_duration = 0

    def add_song(self, song):
        self.songs.append(song)
        self.total_duration += song["duration"]

    def analyze(self):
        genre_distribution = defaultdict(int)
        decade_distribution = defaultdict(int)

        for song in self.songs:
            for genre in song["genre"]:
                genre_distribution[genre] += 1
            
            decade = (song["year"] // 10) * 10
            decade_distribution[decade] += 1

        return {
            "total_duration": self.total_duration,
            "genre_distribution": dict(genre_distribution),
            "decade_distribution": dict(decade_distribution),
        }

    def generate_playlist(self, duration, genre_limits=None, artist_limits=None, shuffle_mode='random'):
        """
        Generate a playlist based on duration, genre and artist constraints.
        """
        playlist = []
        total_duration = 0
        genre_count = defaultdict(int)
        artist_count = defaultdict(int)
        
        available_songs = list(songs_database.values())  
        random.shuffle(available_songs)
        
        for song in available_songs:
            if total_duration + song['duration'] > duration:
                continue
            
            if genre_limits:
                for genre in song['genre']:
                    if genre_count[genre] >= genre_limits.get(genre, float('inf')):
                        break
                else:
                    playlist.append(song)
                    total_duration += song['duration']
                    for genre in song['genre']:
                        genre_count[genre] += 1
            else:
                playlist.append(song)
                total_duration += song['duration']
                for genre in song['genre']:
                    genre_count[genre] += 1
            
            if artist_limits and artist_count[song['artist']] >= artist_limits.get(song['artist'], float('inf')):
                continue
            
            artist_count[song['artist']] += 1
        
        if shuffle_mode == 'smart':
            self.smart_shuffle(playlist)
        elif shuffle_mode == 'time_based':
            self.time_based_shuffle(playlist)
        else:
            random.shuffle(playlist)
        
        return playlist

    def smart_shuffle(self, playlist):
        """ Ensures better genre distribution. """
        random.shuffle(playlist)
        playlist.sort(key=lambda x: x['genre'])
        
    def time_based_shuffle(self, playlist):
        """ Adjusts order based on time of day (hypothetically). """
        if 6 <= self.get_hour() < 12:
            playlist.sort(key=lambda x: x['energy'], reverse=True)
        elif 12 <= self.get_hour() < 18:
            playlist.sort(key=lambda x: x['energy'], reverse=True)
        else:
            playlist.sort(key=lambda x: x['energy'], reverse=True)

    def get_hour(self):
        """Повертає поточну годину (0-23)."""
        return datetime.now().hour

playlists = {}
play_history = []
recently_played = deque(maxlen=10)

while True:
    print("\nМеню:")
    print("1. Створити плейлист")
    print("2. Додати пісню до плейлиста")
    print("3. Аналізувати плейлист")
    print("4. Вивести всі плейлисти")
    print("5. Вивести історію відтворення")
    print("6. Вивести список пісень")
    print("7. Вивести унікальні жанри та виконавців")
    print("8. Згенерувати плейлист")
    print("9. Вийти")

    command = input("Введіть команду: ")

    if command == "1":
        name = input("Введіть назву плейлиста: ")
        playlists[name] = Playlist(name)

    elif command == "2":
        playlist_name = input("Введіть назву плейлиста: ")
        song_title = input("Введіть назву пісні: ")

        playlist = playlists.get(playlist_name)
        
        song = next((song for song in songs_database.values() if song["title"].lower() == song_title.lower()), None)

        if playlist and song:
            playlist.add_song(song)
            print(f"Пісня '{song['title']}' додана до плейлиста '{playlist_name}'.")
            
            play_history.append({"song_title": song["title"], "playlist_id": playlist_name})
            recently_played.append(song["title"])
        else:
            print("Плейлист або пісня не знайдені.")

    elif command == "3":
        playlist_name = input("Введіть назву плейлиста: ")
        playlist = playlists.get(playlist_name)

        if playlist:
            analysis = playlist.analyze()
            print("Аналіз плейлиста:", analysis)
        else:
            print("Плейлист не знайдено.")

    elif command == "4":
        if playlists:
            print("Список всіх плейлистів:")
            for name, playlist in playlists.items():
                print(f"- {name} (Кількість пісень: {len(playlist.songs)}, Загальна тривалість: {playlist.total_duration} сек)")
        else:
            print("Немає створених плейлистів.")

    elif command == "5":
        if play_history:
            print("Історія відтворення:")
            for record in play_history:
                print(f"Пісня '{record['song_title']}' була відтворена в плейлисті {record['playlist_id']}")
        else:
            print("Історія відтворення порожня.")

    elif command == "6":
        print("Список доступних пісень:")
        for song in songs_database.values():
            print(f"- {song['title']} ({song['artist']}, {', '.join(song['genre'])})")

    elif command == "7":
        unique_artists = set(song["artist"] for song in songs_database.values())
        unique_genres = set(genre for song in songs_database.values() for genre in song["genre"])

        print(f"Унікальні жанри: {', '.join(unique_genres)}")
        print(f"Унікальні виконавці: {', '.join(unique_artists)}")

    elif command == "8":
        playlist_name = input("Введіть назву плейлиста: ")
        duration = int(input("Введіть тривалість плейлиста (в секундах): "))
        genre_limits = {}
        artist_limits = {} 
        shuffle_mode = input("Введіть режим перемішування (random/smart/time_based): ")

        playlist = playlists.get(playlist_name)

        if playlist:
            generated_playlist = playlist.generate_playlist(duration, genre_limits, artist_limits, shuffle_mode)
            
            playlist.songs.extend(generated_playlist)
            playlist.total_duration = sum(song['duration'] for song in playlist.songs)
            
            print("Згенерований плейлист:")
            for song in generated_playlist:
                print(f"- {song['title']} ({song['artist']}, {', '.join(song['genre'])})")
        else:
            print("Плейлист не знайдено.")

    elif command == "9":
        break

    else:
        print("Невірна команда.")
