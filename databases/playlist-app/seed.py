from models import db, Playlist, Song, PlaylistSong
from app import app

# Create the database tables
with app.app_context():
    db.drop_all()
    db.create_all()

    # Create some playlists
    playlists = [
        Playlist(name="Cool Songs", description="The coolest"),
        Playlist(name="Sad Songs", description="The saddest"),
        Playlist(name="80s Music", description="Don't stop believing!")
    ]

    # Create some songs
    songs = [
        Song(title="Jump", artist="Van Halen"),
        Song(title="Careless Whisper", artist="George Michael"),
        Song(title="Walking on Sunshine", artist="Katrina and the Waves")
    ]

    # Add new objects to session, so they'll persist
    db.session.add_all(playlists)
    db.session.add_all(songs)
    db.session.commit()

    # Create playlist-song relationships
    playlist_songs = [
        PlaylistSong(playlist_id=playlists[0].id, song_id=songs[0].id),
        PlaylistSong(playlist_id=playlists[1].id, song_id=songs[1].id),
        PlaylistSong(playlist_id=playlists[2].id, song_id=songs[2].id)
    ]

    # Add playlist-song relationships to the session
    db.session.add_all(playlist_songs)
    db.session.commit()