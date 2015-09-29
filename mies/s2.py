# -*- coding: utf-8 -*-
import requests

from ojos.misc.validators import (validate_json, validate_csv,
                                  validate_str, validate_int)

AUTH_URL = '%(endpoint)s/apps/%(appid)s/auth'
UPDATE_UEXT_URL = '%(endpoint)s/apps/%(appid)s/user/update'
GET_USER_URL = '%(endpoint)s/apps/%(appid)s/user/info'
UPDATE_GRAPH_URL = '%(endpoint)s/apps/%(appid)s/user/graph/replace'
CLEAR_GRAPH_URL = '%(endpoint)s/apps/%(appid)s/user/graph/clear'
GET_GRAPH_URL = '%(endpoint)s/apps/%(appid)s/user/graph/list'
POST_TIMELINE_URL = '%(endpoint)s/apps/%(appid)s/timeline/post'
PULL_TIMELINE_URL = '%(endpoint)s/apps/%(appid)s/timeline/post/list'
SEND_UNICAST_URL = '%(endpoint)s/apps/%(appid)s/send'
SEND_BROADCAST_URL = '%(endpoint)s/apps/%(appid)s/broadcast/send'
GET_LATEST_BROADCAST_URL = '%(endpoint)s/apps/%(appid)s/broadcast/latest'
BALS_URL = '%(endpoint)s/apps/%(appid)s/delete/bals'


class Client(object):
    def __init__(self, appid, appkey, endpoint, timeout=None):
        self._appid = validate_str(appid)
        self._appkey = validate_str(appkey)
        self._endpoint = validate_str(endpoint)
        self._timeout = timeout

    def _get_timeout(self, timeout):
        return self._timeout if timeout is None else timeout

    def auth(self, uid, uext=None, fids='', ss=None, timeout=None):
        url = AUTH_URL % {'appid': self._appid,
                          'endpoint': self._endpoint}
        payload = {'apikey': self._appkey,
                   'uid': validate_str(uid),
                   'uext': validate_json(uext, default={}),
                   'fids': validate_csv(fids, default=''),
                   'ss': ss}
        res = requests.post(url, data=payload, verify=False,
                            timeout=self._get_timeout(timeout))
        res.raise_for_status()

        return res.json()

    def update_uext(self, uid, uext=None, timeout=None):
        url = UPDATE_UEXT_URL % {'appid': self._appid,
                                 'endpoint': self._endpoint}
        payload = {'apikey': self._appkey,
                   'uid': validate_str(uid),
                   'uext': validate_json(uext, default={})}
        res = requests.post(url, data=payload, verify=False,
                            timeout=self._get_timeout(timeout))
        res.raise_for_status()

        return res.json()

    def get_user(self, uid, timeout=None):
        url = GET_USER_URL % {'appid': self._appid,
                              'endpoint': self._endpoint}
        payload = {'apikey': self._appkey,
                   'uid': validate_str(uid)}
        res = requests.get(url, params=payload, verify=False,
                           timeout=self._get_timeout(timeout))
        res.raise_for_status()

        return res.json()

    def update_graph(self, uid, fids='', timeout=None):
        url = UPDATE_GRAPH_URL % {'appid': self._appid,
                                  'endpoint': self._endpoint}
        payload = {'apikey': self._appkey,
                   'uid': validate_str(uid),
                   'fids': validate_csv(fids, default='')}
        res = requests.post(url, data=payload, verify=False,
                            timeout=self._get_timeout(timeout))
        res.raise_for_status()

        return res.json()

    def clear_graph(self, uid, timeout=None):
        url = CLEAR_GRAPH_URL % {'appid': self._appid,
                                 'endpoint': self._endpoint}
        payload = {'apikey': self._appkey,
                   'uid': validate_str(uid)}
        res = requests.post(url, data=payload, verify=False,
                            timeout=self._get_timeout(timeout))
        res.raise_for_status()

        return res.json()

    def get_graph(self, uid, timeout=None):
        url = GET_GRAPH_URL % {'appid': self._appid,
                               'endpoint': self._endpoint}
        payload = {'apikey': self._appkey,
                   'uid': validate_str(uid)}
        res = requests.get(url, params=payload, verify=False,
                           timeout=self._get_timeout(timeout))
        res.raise_for_status()

        return res.json()

    def post_timeline(self, uid, data, room=None, pub=None,
                      rpub=None, tag=None, timeout=None):
        url = POST_TIMELINE_URL % {'appid': self._appid,
                                   'endpoint': self._endpoint}
        payload = {'apikey': self._appkey,
                   'uid': validate_str(uid),
                   'data': validate_json(data),
                   'room': None if room is None else validate_str(room),
                   'pub': None if pub is None else validate_int(pub),
                   'rpub': None if rpub is None else validate_int(rpub),
                   'tag': None if tag is None else validate_str(tag)}
        res = requests.post(url, data=payload, verify=False,
                            timeout=self._get_timeout(timeout))
        res.raise_for_status()

        return res.json()

    def pull_timeline(self, uid, room=None, timeout=None):
        url = PULL_TIMELINE_URL % {'appid': self._appid,
                                   'endpoint': self._endpoint}
        payload = {'apikey': self._appkey,
                   'uid': validate_str(uid),
                   'room': room}
        res = requests.get(url, params=payload, verify=False,
                           timeout=self._get_timeout(timeout))
        res.raise_for_status()

        return res.json()

    def send_unicast(self, uid, data, room=None, socket_room=None, fids=None,
                     pub=None, rpub=None, tl=None, tag=None, timeout=None):
        url = SEND_UNICAST_URL % {'appid': self._appid,
                                  'endpoint': self._endpoint}
        payload = {'apikey': self._appkey,
                   'uid': validate_str(uid),
                   'data': validate_json(data),
                   'room': None if room is None else validate_str(room),
                   'socket_room': None if socket_room is None else validate_str(socket_room),
                   'fids': None if fids is None else validate_csv(fids),
                   'pub': None if pub is None else validate_int(pub),
                   'rpub': None if rpub is None else validate_int(rpub),
                   'tl': None if tl is None else validate_int(tl),
                   'tag': None if tag is None else validate_str(tag)}
        res = requests.post(url, data=payload, verify=False,
                            timeout=self._get_timeout(timeout))
        res.raise_for_status()

        return res.json()

    def send_broadcast(self, data, room=None, store=None,
                       socket=None, timeout=None):
        url = SEND_BROADCAST_URL % {'appid': self._appid,
                                    'endpoint': self._endpoint}
        payload = {'apikey': self._appkey,
                   'data': validate_json(data),
                   'room': None if room is None else validate_str(room),
                   'store': None if store is None else validate_int(store),
                   'socket': None if socket is None else validate_int(socket)}
        res = requests.post(url, data=payload, verify=False,
                            timeout=self._get_timeout(timeout))
        res.raise_for_status()

        return res.json()

    def get_latest_broadcast(self, room=None, timeout=None):
        url = GET_LATEST_BROADCAST_URL % {'appid': self._appid,
                                          'endpoint': self._endpoint}
        payload = {'apikey': self._appkey,
                   'room': None if room is None else validate_str(room)}
        res = requests.get(url, params=payload, verify=False,
                           timeout=self._get_timeout(timeout))
        res.raise_for_status()

        return res.json()

    def bals(self, timeout=None):
        url = BALS_URL % {'appid': self._appid,
                          'endpoint': self._endpoint}
        payload = {'apikey': self._appkey}
        res = requests.post(url, data=payload, verify=False,
                            timeout=self._get_timeout(timeout))
        res.raise_for_status()

        return res.json()
