import copy

from functools import partial

from play import play
from decorators import match


# TODO match an array of regexes

@match(r"play (?P<song>.+) by (?P<artist>.+)")
def play_song_by_artist_command(song, artist):
    return partial(play.add, type="song", artist_name=artist, song_name=song)


@match(r"play artist (?P<artist>.+)")
def play_artist_command(artist):
    return partial(play.add, type="artist", artist_name=artist)


@match(r"play album (?P<album>.+) by (?P<artist>.+)")
def play_album_by_artist_command(album, artist):
    return partial(play.add, type="album", album_name=album, artist_name=artist)


@match(r"^next$")
def play_next_song_command(*args, **kwargs):
    return partial(play.next)


@match(r"^pause$")
def pause_command(*args, **kwargs):
    return partial(play.pause)


@match(r"^play$")
def play_command(*args, **kwargs):
    return partial(play.play)


@match(r"^what'?s playing$")
def now_playing_command(*args, **kwargs):
    return partial(play.now_playing)


@match(r"^what'?s next$")
def queue_command(*args, **kwargs):
    return partial(play.queue)


# commands, an array of all commands defined in this module
commands = copy.copy(globals())
commands = [commands[attr] for attr in commands if attr.endswith("_command")]
