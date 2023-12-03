from flask import Flask, redirect, render_template, session, request
from models import db, connect_db, Playlist, Song, PlaylistSong
from forms import NewSongForPlaylistForm, SongForm, PlaylistForm

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///playlist-app"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secretkey"

# Connect to database
connect_db(app)

@app.route("/")
def root():
    """Redirect to homepage"""
    return redirect("/playlists")

@app.route("/playlists")
def show_all_playlists():
    """Show all playlists"""
    playlists = Playlist.query.all()
    form = PlaylistForm() 
    return render_template("playlists.html", playlists=playlists, form=form)

@app.route("/playlists/<int:playlist_id>")
def show_playlist(playlist_id):
    """Show details of a specific playlist."""
    playlist = Playlist.query.get_or_404(playlist_id)
    songs = playlist.songs
    playlist_song = PlaylistSong.query.filter(PlaylistSong.playlist_id == playlist_id).all()
    return render_template("playlist.html", playlist=playlist, songs=songs, playlist_song=playlist_song)

@app.route("/playlists/add", methods=["GET", "POST"])
def add_playlist():
    """Handle form to add a playlist"""
    form = PlaylistForm()
    if form.is_submitted() and form.validate():
        name = form.name.data
        description = form.description.data
        playlist = Playlist(name=name, description=description)
        db.session.add(playlist)
        db.session.commit()
        return redirect("/playlists")
    return render_template("new_playlist.html", form=form)

@app.route("/songs")
def show_all_songs():
    """Show list of songs."""
    songs = Song.query.all()
    form = SongForm()
    return render_template("songs.html", songs=songs, form=form)

@app.route("/songs/<int:song_id>")
def show_song(song_id):
    """Show details of a specific song."""
    song = Song.query.get_or_404(song_id)
    playlists = Playlist.query.all()
    playlist = Playlist.query.filter(Playlist.id == song.id).first()
    return render_template("song.html", song=song, playlists=playlists, playlist=playlist)

@app.route("/song/<int:song_id>/songs_details", methods=["GET", "POST"])
def show_song_details(song_id):
    """Show details of a specific song."""
    song = Song.query.get_or_404(song_id)
    playlists = Playlist.query.all()
    playlist = Playlist.query.filter(Playlist.id == song.id).first()
    return render_template("song_details.html", song=song, playlists=playlists, playlist=playlist)

@app.route("/songs/add", methods=["GET", "POST"])
def add_song():
    """Handle form to add a song"""
    form = SongForm()
    if form.is_submitted() and form.validate():
        title = form.title.data
        artist = form.artist.data
        song = Song(title=title, artist=artist)
        db.session.add(song)
        db.session.commit()
        return redirect("/songs")
    return render_template("new_song.html", form=form)

@app.route("/songs/<int:song_id>/add-to-playlist", methods=["POST"])
def add_song_to_playlist(song_id):
    """Add a song to a playlist and redirect to the playlist."""
    song = Song.query.get_or_404(song_id)
    playlist_id = request.form.get("playlist_id")
    playlist = Playlist.query.get_or_404(playlist_id)
    playlist.songs.append(song)
    db.session.commit()
    return redirect(f"/playlists/{playlist_id}")

if __name__ == '__main__':
    app.run(debug=True)