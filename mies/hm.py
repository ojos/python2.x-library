# -*- coding: utf-8 -*-
import json
import requests

from ojos.misc.validators import validate_str

USER_VOTE_URL = '%(endpoint)s/1/apps/%(app_id)s/user/%(user_id)s/votes'
USERS_URL = '%(endpoint)s/1/apps/%(app_id)s/users'
POLLS_URL = '%(endpoint)s/1/apps/%(app_id)s/polls'
OPTION_URL = POLLS_URL + '/%(poll_id)s/options'
VOTE_URL = POLLS_URL + '/%(poll_id)s/votes'


class Client(object):
    def __init__(self, app_id, app_secret, endpoint, timeout=None):
        self._app_id = validate_str(app_id)
        self._app_secret = validate_str(app_secret)
        self._endpoint = validate_str(endpoint)
        self._timeout = timeout
        self._auth = (self._app_id, self._app_secret)

    def _get_timeout(self, timeout):
        return self._timeout if timeout is None else timeout

    def auth(self, user_id, user_secret, timeout=None):
        url = USERS_URL % {'app_id': self._app_id,
                           'endpoint': self._endpoint}
        url = '%s/%s' % (url, user_id)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        payload = {'user_secret': user_secret}
        res = requests.put(url, data=json.dumps(payload), headers=headers,
                           auth=self._auth, verify=False,
                           timeout=self._get_timeout(timeout))
        res.raise_for_status()

        return res.json()

    def get_user(self, user_id, timeout=None):
        url = USERS_URL % {'app_id': self._app_id,
                           'endpoint': self._endpoint}
        url = '%s/%s' % (url, user_id)
        res = requests.get(url, verify=False, auth=self._auth,
                           timeout=self._get_timeout(timeout))
        res.raise_for_status()

        return res.json()

    def get_user_list(self, timeout=None):
        url = USERS_URL % {'app_id': self._app_id,
                           'endpoint': self._endpoint}
        res = requests.get(url, verify=False, auth=self._auth,
                           timeout=self._get_timeout(timeout))
        res.raise_for_status()

        return res.json()

    def delete_user(self, user_id, timeout=None):
        url = USERS_URL % {'app_id': self._app_id,
                           'endpoint': self._endpoint}
        url = '%s/%s' % (url, user_id)
        res = requests.delete(url, verify=False, auth=self._auth,
                              timeout=self._get_timeout(timeout))
        res.raise_for_status()

    def clear_user(self, timeout=None):
        url = USERS_URL % {'app_id': self._app_id,
                           'endpoint': self._endpoint}
        res = requests.delete(url, verify=False, auth=self._auth,
                              timeout=self._get_timeout(timeout))
        res.raise_for_status()

    def put_poll(self, poll_id, count_limit='', is_accepting=False, timeout=None):
        url = POLLS_URL % {'app_id': self._app_id,
                           'endpoint': self._endpoint}
        url = '%s/%s' % (url, poll_id)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        payload = {'count_limit': count_limit,
                   'is_accepting': is_accepting}
        res = requests.put(url, data=json.dumps(payload), headers=headers,
                           auth=self._auth, verify=False,
                           timeout=self._get_timeout(timeout))
        res.raise_for_status()

        return res.json()

    def get_poll(self, poll_id, timeout=None):
        url = POLLS_URL % {'app_id': self._app_id,
                           'endpoint': self._endpoint}
        url = '%s/%s' % (url, poll_id)
        res = requests.get(url, verify=False, auth=self._auth,
                           timeout=self._get_timeout(timeout))
        res.raise_for_status()

        return res.json()

    def get_poll_list(self, timeout=None):
        url = POLLS_URL % {'app_id': self._app_id,
                           'endpoint': self._endpoint}
        res = requests.get(url, verify=False, auth=self._auth,
                           timeout=self._get_timeout(timeout))
        res.raise_for_status()

        return res.json()

    def delete_poll(self, poll_id, timeout=None):
        url = POLLS_URL % {'app_id': self._app_id,
                           'endpoint': self._endpoint}
        url = '%s/%s' % (url, poll_id)
        res = requests.delete(url, verify=False, auth=self._auth,
                              timeout=self._get_timeout(timeout))
        res.raise_for_status()

    def put_option(self, poll_id, option, timeout=None):
        url = OPTION_URL % {'app_id': self._app_id,
                            'endpoint': self._endpoint,
                            'poll_id': poll_id}
        url = '%s/%s' % (url, option)
        res = requests.put(url, verify=False, auth=self._auth,
                           timeout=self._get_timeout(timeout))
        res.raise_for_status()

        return res.json()

    def get_option(self, poll_id, option, timeout=None):
        url = OPTION_URL % {'app_id': self._app_id,
                            'endpoint': self._endpoint,
                            'poll_id': poll_id}
        url = '%s/%s' % (url, option)
        res = requests.get(url, verify=False, auth=self._auth,
                           timeout=self._get_timeout(timeout))
        res.raise_for_status()

        return res.json()

    def get_poll_option(self, poll_id, timeout=None):
        url = OPTION_URL % {'app_id': self._app_id,
                            'endpoint': self._endpoint,
                            'poll_id': poll_id}
        res = requests.get(url, verify=False, auth=self._auth,
                           timeout=self._get_timeout(timeout))
        res.raise_for_status()

        return res.json()

    def delete_option(self, poll_id, option, timeout=None):
        url = OPTION_URL % {'app_id': self._app_id,
                            'endpoint': self._endpoint,
                            'poll_id': poll_id}
        url = '%s/%s' % (url, option)
        res = requests.delete(url, verify=False, auth=self._auth,
                              timeout=self._get_timeout(timeout))
        res.raise_for_status()

    def put_vote(self, poll_id, option, incr=1, value=None, timeout=None):
        url = VOTE_URL % {'app_id': self._app_id,
                          'endpoint': self._endpoint,
                          'poll_id': poll_id}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        payload = {'option': option,
                   'incr': incr,
                   'set': value}
        res = requests.post(url, data=json.dumps(payload), headers=headers,
                            auth=self._auth, verify=False,
                            timeout=self._get_timeout(timeout))
        res.raise_for_status()

        return res.json()

    def get_poll_vote(self, poll_id, timeout=None):
        url = VOTE_URL % {'app_id': self._app_id,
                          'endpoint': self._endpoint,
                          'poll_id': poll_id}
        res = requests.get(url, verify=False, auth=self._auth,
                           timeout=self._get_timeout(timeout))
        res.raise_for_status()

        return res.json()

    def get_poll_summary(self, poll_id, timeout=None):
        url = VOTE_URL % {'app_id': self._app_id,
                          'endpoint': self._endpoint,
                          'poll_id': poll_id}
        url = '%s/_summary' % url
        res = requests.get(url, verify=False, auth=self._auth,
                           timeout=self._get_timeout(timeout))
        res.raise_for_status()

        return res.json()

    def get_user_vote(self, user_id, timeout=None):
        url = USER_VOTE_URL % {'app_id': self._app_id,
                               'endpoint': self._endpoint,
                               'user_id': user_id}
        res = requests.get(url, verify=False, auth=self._auth,
                           timeout=self._get_timeout(timeout))
        res.raise_for_status()

        return res.json()

    def clear_vote(self, poll_id, timeout=None):
        url = VOTE_URL % {'app_id': self._app_id,
                          'endpoint': self._endpoint,
                          'poll_id': poll_id}
        url = '%s/_reset' % url
        res = requests.post(url, verify=False, auth=self._auth,
                            timeout=self._get_timeout(timeout))
        res.raise_for_status()
