from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy instance
db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)

class Playlist(db.Model):
    """Model for playlists."""
    __tablename__ = 'playlists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    # Relationship between Playlist and Song
    songs = db.relationship('Song', secondary='playlistsongs', backref='playlists')

    def __repr__(self):
        """Show info about playlist."""
        return f"<Playlist id={self.id} name={self.name} description={self.description}>"

class Song(db.Model):
    """Model for songs."""
    __tablename__ = 'songs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        """Show info about song."""
        return f"<Song id={self.id} title={self.title} artist={self.artist}>"

class PlaylistSong(db.Model):
    """Model for song-playlist relationship."""
    __tablename__ = 'playlistsongs'
    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'), nullable=False)

    def __repr__(self):
        """Show info about playlist-song."""
        return f"<PlaylistSong id={self.id} playlist_id={self.playlist_id} song_id={self.song_id}>"