# -*- coding: utf-8 -*-
import sys
import urllib
from threading import Thread

from tweepy import API as TwitterAPI
from tweepy.auth import OAuthHandler
from tweepy.parsers import RawParser
from tweepy.streaming import (Stream, StreamListener)

from ojos.misc.codepoint import characters


class KThread(Thread):
    """A subclass of threading.Thread, with a kill() method."""

    def __init__(self, *args, **keywords):
        Thread.__init__(self, *args, **keywords)
        self.killed = False

    def start(self):
        """Start the thread."""
        self.__run_backup = self.run
        self.run = self.__run
        Thread.start(self)

    def __run(self):
        """Hacked run function, which installs the trace."""
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, why, arg):
        if why == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, why, arg):
        if self.killed:
            if why == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True


class ExStream(Stream):

    def _start(self, async):
        self.running = True
        if async:
            self._thread = KThread(target=self._run)
            self._thread.start()
        else:
            self._run()


class Listener(StreamListener):

    def on_data(self, data):
        if data.startswith("{"):
            print data
        return True

    def on_error(self, status_code):
        return True  # keep stream alive


class Client(object):

    @classmethod
    def in_text_limit(cls, text, limit=140):
        words = text.split(' ')
        l = 0
        for w in words:
            if w[:4] == 'http':
                l = l + 23
            else:
                l = l + len(characters(w))
        l = l + len(words) - 1

        return l <= limit

    def __init__(self, consumer_key, consumer_secret, callback_url=None,
                 access_token=None, access_token_secret=None,
                 use_https=True, raw_json=False):
        self._api = None
        self._stream = None
        self._consumer_key = consumer_key
        self._consumer_secret = consumer_secret
        self._callback_url = callback_url
        self._access_token = access_token
        self._access_token_secret = access_token_secret
        self._use_https = bool(use_https)
        self._raw_json = raw_json

        if self._access_token and self._access_token_secret:
            self._setup_apis()

    @property
    def api(self):
        return self._api

    @property
    def stream(self):
        return self._stream

    @property
    def access_token(self):
        return self._access_token

    @property
    def access_token_secret(self):
        return self._access_token_secret

    def get_auth_url(self, params={}, callback_url=None):
        if callback_url is None:
            callback_url = self._callback_url
        callback = '%s?%s' % (callback_url, urllib.urlencode(params))
        auth = OAuthHandler(self._consumer_key, self._consumer_secret, callback)
        url = auth.get_authorization_url()

        return url, auth.request_token

    def get_token(self, oauth_token, oauth_token_secret, oauth_verifier):
        auth = OAuthHandler(self._consumer_key, self._consumer_secret)
        auth.request_token = {'oauth_token': oauth_token,
                              'oauth_token_secret': oauth_token_secret}

        auth.get_access_token(oauth_verifier)
        self._access_token = auth.access_token
        self._access_token_secret = auth.access_token_secret
        self._setup_apis()

        return self._access_token, self._access_token_secret

    def _setup_apis(self):
        auth = OAuthHandler(self._consumer_key, self._consumer_secret)
        auth.set_access_token(self._access_token, self._access_token_secret)

        if self._raw_json:
            self._api = TwitterAPI(auth, parser=RawParser())
        else:
            self._api = TwitterAPI(auth)

    def get_stream(self, listener=None):
        if self._stream is not None:
            self._stream.disconnect()
            if listener is None:
                listener = self._stream.listener

        auth = OAuthHandler(self._consumer_key, self._consumer_secret)
        auth.set_access_token(self._access_token, self._access_token_secret)
        self._stream = ExStream(auth, listener)

        return self._stream
