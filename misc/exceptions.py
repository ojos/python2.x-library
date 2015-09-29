# -*- coding: utf-8 -*-


class ResponseException(Exception):
    code = None
    message = None
    url = None
    header_code = True

    def __init__(self, code=None, message=None, url=None, header_code=None):
        self.code = self.code if code is None else code
        self.message = self.message if message is None else message
        self.url = self.url if url is None else url
        self.header_code = self.header_code if header_code is None else header_code

    def __str__(self):
        return 'code : %s, message : %s, url : %s, header_code : %s' %\
            (self.code, self.message, self.url, self.header_code)
