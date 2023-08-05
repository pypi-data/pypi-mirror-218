'''A minimalist client for OpenAI APIs.'''

import confuse
import httpx

__version__ = '0.1.0'


class Api(httpx.Client):
    def __init__(self, api_key=None):
        super().__init__(base_url='https://api.openai.com/v1/', timeout=30.0)
        if api_key is None:
            try:
                api_key = confuse.Configuration('oaix').get()['api_key']
            except KeyError:
                pass
            else:
                self.headers['authorization'] = 'Bearer ' + api_key

    def request(self, method, url, **kwargs):
        r = super().request(method, url, **kwargs)
        try:
            r = r.json()
        except ValueError:
            pass
        else:
            try:
                e = r['error']
            except KeyError:
                pass
            else:
                raise ApiError(e)
        return r


class ApiError(Exception):
    def __init__(self, error):
        super().__init__(error['message'])
        self.error = error

    def __getattr__(self, name):
        try:
            return self.error[name]
        except KeyError:
            raise AttributeError(name)
