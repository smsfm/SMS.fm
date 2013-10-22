import unittest

import mock

import flaskapp


class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        flaskapp.app.config['TESTING'] = True
        flaskapp.app.requests = []
        self.app = flaskapp.app.test_client()

    def _post(self, msg):
        return self.app.post('/', data=dict(
            Body=msg
        ))

    @mock.patch("twilio.twiml")
    @mock.patch("sms.fm.play.play.add")
    def test_play_song_by_artist_added(self, add, twiml):
        resp = self._post("play need you tonight by inxs")

        add.assert_called_once_with(type="song", artist_name="inxs", song_name="need you tonight")

        self.assertEqual(1, len(flaskapp.app.requests))
        self.assertEqual(200, resp.status_code)

    @mock.patch("twilio.twiml")
    @mock.patch("sms.fm.play.play.add")
    def test_play_album_by_artist_added(self, add, twiml):
        resp = self._post("play album kick by inxs")

        add.assert_called_once_with(type="album", artist_name="inxs", album_name="kick")

        self.assertEqual(1, len(flaskapp.app.requests))
        self.assertEqual(200, resp.status_code)

    @mock.patch("twilio.twiml")
    @mock.patch("sms.fm.play.play.add")
    def test_artist_added(self, add, twiml):
        resp = self._post("play artist inxs")

        add.assert_called_once_with(type="artist", artist_name="inxs")

        self.assertEqual(1, len(flaskapp.app.requests))
        self.assertEqual(200, resp.status_code)

    @mock.patch("twilio.twiml")
    @mock.patch("sms.fm.play.play.next")
    def test_next_song(self, next, twiml):
        resp = self._post("next")

        next.assert_called_once()

        self.assertEqual(0, len(flaskapp.app.requests))
        self.assertEqual(200, resp.status_code)

    @mock.patch("twilio.twiml")
    @mock.patch("sms.fm.play.play.pause")
    def test_pause(self, pause, twiml):
        resp = self._post("pause")

        pause.assert_called_once()

        self.assertEqual(0, len(flaskapp.app.requests))
        self.assertEqual(200, resp.status_code)

    @mock.patch("twilio.twiml")
    @mock.patch("sms.fm.play.play.play")
    def test_play(self, play, twiml):
        resp = self._post("play")

        play.assert_called_once()

        self.assertEqual(0, len(flaskapp.app.requests))
        self.assertEqual(200, resp.status_code)

    @mock.patch("twilio.twiml")
    @mock.patch("sms.fm.play.play.queue")
    def test_whats_next(self, queue, twiml):
        queries = ("whats next", "what's next", "whats next?", "what's next?")
        for query in queries:
            resp = self._post(query)

            queue.assert_called_once()

            self.assertEqual(0, len(flaskapp.app.requests))
            self.assertEqual(200, resp.status_code)

    @mock.patch("twilio.twiml")
    @mock.patch("sms.fm.play.play.now_playing")
    def test_whats_playing(self, now_playing, twiml):
        queries = ("whats playing", "what's playing", "whats playing?", "what's playing?")
        for query in queries:
            resp = self._post(query)

            now_playing.assert_called_once()

            self.assertEqual(0, len(flaskapp.app.requests))
            self.assertEqual(200, resp.status_code)

    @mock.patch("sms.fm.play.play.add")
    def test_no_match(self, add):
        resp = self._post("need you tonight by inxs")

        self.assertEqual(0, add.call_count)
        self.assertEqual(0, len(flaskapp.app.requests))
        self.assertEqual(200, resp.status_code)

    def tearDown(self):
        pass
