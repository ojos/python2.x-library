# -*- coding: utf-8 -*-
import gzip
import logging
import StringIO

from boto.s3.connection import S3Connection
from boto.s3.key import Key

from ojos.misc.exceptions import ServiceUnavailableException
from ojos.misc.validators import validate_json


class Client(object):

    def __init__(self, access_key, secret, bucket, key=None, max_age=5):
        self._conn = S3Connection(access_key, secret, is_secure=False)
        self._bucket = self._conn.get_bucket(bucket)
        self._key = self._get_key(key)
        self._context = None
        self._file = None
        self._max_age = max_age

    def exist_key(self, key):
        return self._bucket.get_key(key) is not None

    def _get_key(self, key=None):
        if key is None:
            return self._key if hasattr(self, '_key') and self._key is not None else None

        self._key = Key(self._bucket)
        self._key.key = key

        return self._key

    def get_content_type(self, key=None):
        key = self._get_key(key)
        return key.content_type

    def get(self, key=None, cache=False, string=True):
        key = self._get_key(key)
        try:
            if string:
                if self._context is None or not cache:
                    self._context = self._key.get_contents_as_string()

                return self._context
            else:
                if self._file is None or not cache:
                    self._file = self._key.get_contents_to_file()

                return self._file
        except:
            raise ServiceUnavailableException(message='file get failure')

    def put(self, context, key=None, metadata={}, public=False, string=True):
        _key = self._get_key(key)

        for k, v in metadata.items():
            _key.set_metadata(k, v)

        policy = 'public-read' if public else 'private'

        try:
            if string:
                self._context = context
                _key.set_contents_from_string(self._context, policy=policy)
            else:
                self._file = context
                _key.set_contents_from_file(self._file, policy=policy)
        except:
            raise ServiceUnavailableException(message='file put failure')

        return key

    def delete(self, key):
        return self._bucket.delete_key(key)

    def _get_metadata(self, _metadata={}):
        metadata = {'Cache-Control': 'max-age=%s' % self._max_age}
        metadata.update(_metadata)
        return metadata

    def put_json(self, context, key=None, public=True, compress=False):
        _metadata = {'Content-Type': 'application/json; charset=UTF-8'}
        _json = validate_json(context)
        if compress:
            stringio = StringIO.StringIO()
            gzip_file = gzip.GzipFile(fileobj=stringio, mode='w')
            gzip_file.write(_json)
            gzip_file.close()
            _json = stringio.getvalue()
            _metadata.update({'Content-Encoding': 'gzip'})

        metadata = self._get_metadata(_metadata)
        return self.put(_json, key, metadata, public)

    def put_html(self, context, key=None, public=True):
        metadata = self._get_metadata({'Content-Type': 'text/html; charset=UTF-8'})
        return self.put(context, key, metadata, public)

    def put_image(self, context, key=None, public=True, extension=True):
        from PIL import Image
        ext = Image.open(StringIO(context)).format.lower()
        content_type = 'image/%s' % ext
        metadata = self._get_metadata({'Content-Type': '%s' % content_type})
        if key.find('.') == -1:
            key = '%s.%s' % (key, ext) if extension else key
        return self.put(context, key, metadata, public)
