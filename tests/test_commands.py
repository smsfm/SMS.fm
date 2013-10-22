import unittest

from sms.fm import commands
from sms.fm.play import play
from sms.fm.exceptions import NoMatchFound


def filter_comands(excl):
    for command in commands.commands:
        if command != excl:
            yield command


class TestCommands(unittest.TestCase):
    def test_song_by_artist_matches_command(self):
        command = commands.play_song_by_artist_command("play Foo by Bar")
        self.assertEqual(play.add, command.func)
        self.assertEqual(dict(type="song", artist_name="Bar", song_name="Foo"), command.keywords)
        self.assertIsNone(None, command.args)

    def test_song_by_artist_matches_no_other_commands(self):
        for command in filter_comands(commands.play_song_by_artist_command):
            self.assertRaises(NoMatchFound, command, "play Foo by Bar")

    def test_song_containing_by_by_artist_matches_command(self):
        command = commands.play_song_by_artist_command("play One by One by Foo Fighters")
        self.assertEqual(play.add, command.func)
        self.assertEqual(dict(type="song", artist_name="Foo Fighters", song_name="One by One"), command.keywords)
        self.assertIsNone(None, command.args)

    def test_artist_matches_command(self):
        command = commands.play_artist_command("play artist Wham")
        self.assertEqual(play.add, command.func)
        self.assertEqual(dict(type="artist", artist_name="Wham"), command.keywords)
        self.assertIsNone(None, command.args)

    def test_artist_matches_no_other_commands(self):
        for command in filter_comands(commands.play_artist_command):
            self.assertRaises(NoMatchFound, command, "play artist Wham")

    def test_album_by_artist_matches_command(self):
        command = commands.play_album_by_artist_command("play album An Awesome Wave by alt-J")
        self.assertEqual(play.add, command.func)
        self.assertEqual(dict(type="album", album_name="An Awesome Wave", artist_name="alt-J"), command.keywords)
        self.assertIsNone(None, command.args)

    def test_album_by_artist_matches_no_other_commands(self):
        for command in filter_comands(commands.play_album_by_artist_command):
            self.assertRaises(NoMatchFound, command, "play album An Awesome Wave by alt-J")

    def test_next_song_matches_command(self):
        command = commands.next_song_command("next")
        self.assertEqual(play.next, command.func)
        self.assertIsNone(None, command.keywords)
        self.assertIsNone(None, command.args)

    def test_next_song_matches_no_other_commands(self):
        for command in filter_comands(commands.next_song_command):
            self.assertRaises(NoMatchFound, command, "next")

    def test_pause_matches_command(self):
        command = commands.pause_command("pause")
        self.assertEqual(play.pause, command.func)
        self.assertIsNone(None, command.keywords)
        self.assertIsNone(None, command.args)

    def test_pause_matches_no_other_commands(self):
        for command in filter_comands(commands.pause_command):
            self.assertRaises(NoMatchFound, command, "pause")

    def test_play_matches_command(self):
        command = commands.start_command("play")
        self.assertEqual(play.play, command.func)
        self.assertIsNone(None, command.keywords)
        self.assertIsNone(None, command.args)

    def test_play_matches_no_other_commands(self):
        for command in filter_comands(commands.start_command):
            self.assertRaises(NoMatchFound, command, "play")

    def test_now_playing_matches_command(self):
        command = commands.now_playing_command("what's playing")
        self.assertEqual(play.now_playing, command.func)
        self.assertIsNone(None, command.keywords)
        self.assertIsNone(None, command.args)

    def test_now_playing_no_apostrophe_matches_command(self):
        command = commands.now_playing_command("whats playing")
        self.assertEqual(play.now_playing, command.func)
        self.assertIsNone(None, command.keywords)
        self.assertIsNone(None, command.args)

    def test_now_playing_matches_no_other_commands(self):
        for command in filter_comands(commands.now_playing_command):
            self.assertRaises(NoMatchFound, command, "what's playing")

    def test_queue_matches_command(self):
        command = commands.queue_command("what's next")
        self.assertEqual(play.queue, command.func)
        self.assertIsNone(None, command.keywords)
        self.assertIsNone(None, command.args)

    def test_queue_no_apostrophe_matches_command(self):
        command = commands.queue_command("whats next")
        self.assertEqual(play.queue, command.func)
        self.assertIsNone(None, command.keywords)
        self.assertIsNone(None, command.args)

    def test_queue_matches_no_other_commands(self):
        for command in filter_comands(commands.queue_command):
            self.assertRaises(NoMatchFound, command, "what's next")

