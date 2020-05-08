from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class PlaylistForm(FlaskForm):
    festivalname = StringField('Festival Name', validators=[DataRequired()])
    festivalyear = StringField('Festival Year', validators=[DataRequired()])
    bands = TextAreaField('Bands', validators=[DataRequired(),
                          Length(min=1, max=1000)])
    submit = SubmitField('Generate Playlist')


class SendForm(FlaskForm):
    submit = SubmitField("Send Playlist to Spotify")
