# -*- coding: utf-8 -*-
import sys
import urllib
from threading import Thread

from tweepy import API as TwitterAPI
from tweepy.auth import OAuthHandler
from tweepy.parsers import RawParser
from tweepy.streaming import (Stream, StreamListener)


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
    def __init__(self, consumer_key, consumer_secret, callback_url=None,
                 token_key=None, token_secret=None, use_https=True,
                 raw_json=False):
        self._api = None
        self._stream = None
        self._consumer_key = consumer_key
        self._consumer_secret = consumer_secret
        self._callback_url = callback_url
        self._token_key = token_key
        self._token_secret = token_secret
        self._use_https = bool(use_https)
        self._raw_json = raw_json

        if self._token_key and self._token_secret:
            self._setup_apis()

    @property
    def api(self):
        return self._api

    @property
    def stream(self):
        return self._stream

    def get_auth_url(self, params, callback_url=None):
        if callback_url is None:
            callback_url = self._callback_url
        callback = '%s?%s' % (callback_url, urllib.urlencode(params))
        conn = OAuthHandler(self._consumer_key, self._consumer_secret, callback)
        url = conn.get_authorization_url() + '&lang=ja'
        request_token = (conn.request_token.key, conn.request_token.secret)

        return url, request_token

    def get_token(self, key, secret, oauth_verifier):
        conn = OAuthHandler(self._consumer_key, self._consumer_secret)
        conn.set_request_token(key, secret)

        access_token = conn.get_access_token(oauth_verifier)
        self._token_key = access_token.key
        self._token_secret = access_token.secret
        self._setup_apis()

        return self.api

    def _setup_apis(self):
        conn = OAuthHandler(self._consumer_key, self._consumer_secret)
        conn.set_access_token(self._token_key, self._token_secret)

        if self._raw_json:
            self._api = TwitterAPI(conn, parser=RawParser())
        else:
            self._api = TwitterAPI(conn)

    def get_stream(self, listener=None):
        if self._stream is not None:
            self._stream.disconnect()
            if listener is None:
                listener = self._stream.listener

        conn = OAuthHandler(self._consumer_key, self._consumer_secret)
        conn.set_access_token(self._token_key, self._token_secret)
        self._stream = ExStream(conn, listener)

        return self._stream
