from models import db, Playlist, Song, PlaylistSong
from app import app

# Create the database tables
with app.app_context():
    db.drop_all()
    db.create_all()

    # Create some playlists
    playlist1 = Playlist(name="Cool Songs", description="The coolest")
    playlist2 = Playlist(name="Sad Songs", description="The saddest")
    playlist3 = Playlist(name="80s Music", description="Don't stop believing!")

    # Create some songs
    song1 = Song(title="Jump", artist="Van Halen")
    song2 = Song(title="Careless Whisper", artist="George Michael")
    song3 = Song(title="Walking on Sunshine", artist="Katrina and the Waves")

    # Add new objects to session, so they'll persist
    db.session.add(playlist1)
    db.session.add(playlist2)
    db.session.add(playlist3)
    db.session.add(song1)
    db.session.add(song2)
    db.session.add(song3)

    
    db.session.commit()

