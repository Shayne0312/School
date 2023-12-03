from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import InputRequired

class PlaylistForm(FlaskForm):
    """Form for adding/updating a Playlist."""
    name = StringField("Playlist Name", validators=[InputRequired()])
    description = StringField("Playlist Description", validators=[InputRequired()])

class SongForm(FlaskForm):
    """Form for adding/updating a Song."""
    title = StringField("Song Title", validators=[InputRequired()])
    artist = StringField("Artist Name", validators=[InputRequired()])

class NewSongForPlaylistForm(FlaskForm):
    """Form for adding a Song to a Playlist."""
    # Note: coerce=int makes sure the data is converted to int
    song = SelectField('Song To Add', coerce=int)