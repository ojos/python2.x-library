# -*- coding: utf-8 -*-
import cookielib
import urllib
import urllib2
import urlparse


# ベーシック認証APIへアクセス
def post_basic_auth_api(name, password, api_uri, params={}, method='GET'):
    data = urllib.urlencode(params)

    # Basic認証用のパスワードマネージャーを作成
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, api_uri, name, password)

    # openerの作成とインストール
    # HTTPS通信とBasic認証用のHandlerを使用
    opener = urllib2.build_opener(urllib2.HTTPSHandler(),
                                  urllib2.HTTPBasicAuthHandler(password_mgr))
    urllib2.install_opener(opener)

    if method == 'GET':
        serv_req = urllib2.Request(api_uri, data)
        serv_res = urllib2.urlopen(serv_req)
    else:
        serv_req = urllib2.Request(api_uri)
        serv_req.get_method = lambda: method
        serv_res = urllib2.urlopen(serv_req, data)

    content = serv_res.read()
    return content


# urllib2でリダイレクトをさせない
class NoRedirectProcessor(urllib2.HTTPErrorProcessor):
    def http_response(self, request, response):
        code, msg, hdrs = response.code, response.msg, response.info()
        if code == 302:
            return response
        if not (200 <= code < 300):
            response = self.parent.error(
                'http', request, response, code, msg, hdrs)
        return response
    https_response = http_response


# 管理者権限認証APIへアクセス
def post_admin_required_api(email, password, api_uri, params={}, method='GET'):
    api_parse = urlparse.urlparse(api_uri)
    # base_uri = '%s://%s' % (api_parse[0], api_parse[1])
    app_name = api_parse[1].split('.')[0]
    authenticated = False

    cj = cookielib.LWPCookieJar()
    # 認証済みcookieを読み込む
    # cookie_path = '%s/.%s.auth_cookie' % (os.path.dirname(__file__),
    #                                       api_parse[1])
    # if os.path.exists(cookie_path):
    #     cj.load(cookie_path)
    #     authenticated = True
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj),
                                  NoRedirectProcessor)
    urllib2.install_opener(opener)

    if not authenticated:
        auth_uri = 'https://www.google.com/accounts/ClientLogin'
        authreq_data = urllib.urlencode({'Email': email,
                                         'Passwd': password,
                                         'service': 'ah',
                                         'source': app_name,
                                         'accountType': 'HOSTED_OR_GOOGLE'})

        auth_req = urllib2.Request(auth_uri, data=authreq_data)
        auth_res = urllib2.urlopen(auth_req)
        auth_content = auth_res.read()
        auth_resp_dict = dict(x.split('=')
                              for x in auth_content.split('\n') if x)
        auth_token = auth_resp_dict['Auth']

        serv_args = {}
        serv_args['continue'] = api_uri
        serv_args['auth'] = auth_token
        # login_uri = '%s/_ah/login?%s' % (base_uri, urllib.urlencode(serv_args))
        # login_req = urllib2.Request(login_uri)
        # login_res = urllib2.urlopen(login_req)

    if method == 'GET':
        api_uri = '%s?%s' % (api_uri, urllib.urlencode(params))
        serv_req = urllib2.Request(api_uri)
        serv_res = urllib2.urlopen(serv_req)
    else:
        serv_req = urllib2.Request(api_uri)
        serv_req.get_method = lambda: method
        serv_res = urllib2.urlopen(serv_req, urllib.urlencode(params))

    if serv_res.url == api_uri:
        content = serv_res.read()
    # else:
    #     os.remove(cookie_path)
    #     content = post_admin_required_api(email, password, api_uri,
    #                                       params, method)

    # cj.save(cookie_path)

    return content
