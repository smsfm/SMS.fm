import copy

from functools import partial

from play import play
from decorators import match


# TODO match an array of regexes

@match(r"play (?P<song>.+) by (?P<artist>.+)")
def play_song_by_artist_command(song, artist):
    return partial(play.add, type="song", artist_name=artist, song_name=song)


@match(r"^next$")
def play_next_song_command(*args, **kwargs):
    return partial(play.next)


# commands, an array of all commands defined in this module
commands = copy.copy(globals())
commands = [commands[attr] for attr in commands if attr.endswith("_command")]
