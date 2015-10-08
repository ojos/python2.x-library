# -*- coding: utf-8 -*-
import json
import urllib2
from boto import ec2
from boto.exception import EC2ResponseError

EC2_USER_DATA_URL = 'http://169.254.169.254/latest/user-data/'
EC2_META_DATA_URL = 'http://169.254.169.254/latest/meta-data/'
DEFAULT_TAGS = {'Name': 'app',
                'Roles': 'app',
                'Environment': 'develop'}
DEFAULT_INSTANCE_ID = ''
DEFAULT_PUBLIC_IP = '127.0.0.1'


class Client(object):
    _access_key = None
    _secret = None
    _region = None
    _conn = None
    _instance_id = None
    _public_ip = None
    _tags = None

    def __init__(self, access_key, secret, region,
                 default_tags=DEFAULT_TAGS,
                 default_instance_id=DEFAULT_INSTANCE_ID,
                 default_public_ip=DEFAULT_PUBLIC_IP,):
        self._access_key = access_key
        self._secret = secret
        self._region = region
        self.default_tags = default_tags
        self.default_instance_id = default_instance_id
        self.default_public_ip = default_public_ip

    @property
    def conn(self):
        if self._conn is None:
            self._conn = ec2.connect_to_region(self._region,
                                               aws_access_key_id=self._access_key,
                                               aws_secret_access_key=self._secret)
        return self._conn

    @property
    def public_ip(self):
        if self._public_ip is None:
            return self.get_public_ip()
        return self._public_ip

    @property
    def instance_id(self):
        if self._instance_id is None:
            return self.get_instance_id()
        return self._instance_id

    @property
    def tags(self):
        if self._tags is None:
            return self.get_tags(self.instance_id, self.default_tags)
        return self._tags

    @property
    def name(self):
        tags = self.tags
        if 'Name' in tags:
            return tags['Name']
        return None

    @property
    def env(self):
        tags = self.tags
        if 'Environment' in tags:
            return tags['Environment']
        return None

    @property
    def roles(self):
        tags = self.tags
        if 'Roles' in tags:
            return tags['Roles'].split(',')
        return []

    def get_public_ip(self):
        url = '%s%s' % (EC2_META_DATA_URL, 'public-ipv4/')
        try:
            f = urllib2.urlopen(url, timeout=1)
            self._public_ip = f.read()
        except urllib2.URLError:
            self._public_ip = self.default_public_ip

        return self._public_ip

    def get_instance_id(self):
        url = '%s%s' % (EC2_META_DATA_URL, 'instance-id/')
        try:
            f = urllib2.urlopen(url, timeout=1)
            self._instance_id = f.read()
        except urllib2.URLError:
            self._instance_id = self.default_instance_id

        return self._instance_id

    def get_tags(self, instance_id, default=DEFAULT_TAGS):
        if self._tags is None:
            if instance_id == self.default_instance_id:
                self._tags = default
            else:
                filters = {'instance-id': instance_id}
                try:
                    instance = self.conn.get_all_instances(filters=filters)[0].instances[0]
                    self._tags = instance.tags
                except (EC2ResponseError, IndexError):
                    self._tags = default

        return self._tags


class UserDataClient(Client):

    @classmethod
    def get_user_data(cls):
        try:
            f = urllib2.urlopen(EC2_USER_DATA_URL, timeout=1)
            return json.loads(f.read())
        except:
            return {}

    def __init__(self, access_key, secret, region,
                 default_tags=DEFAULT_TAGS,
                 default_instance_id=DEFAULT_INSTANCE_ID,
                 default_public_ip=DEFAULT_PUBLIC_IP,):
        user_data = UserDataClient.get_user_data()
        self._access_key = user_data['access_key'] if user_data.has_key(
            'access_key') else access_key
        self._secret = user_data['secret'] if user_data.has_key('secret') else secret
        self._region = user_data['region'] if user_data.has_key('region') else region
        self.default_tags = default_tags
        self.default_instance_id = default_instance_id
        self.default_public_ip = default_public_ip
