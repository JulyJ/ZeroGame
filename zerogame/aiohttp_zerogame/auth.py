from aioauth_client import (
                            BitbucketClient,
                            FacebookClient,
                            GithubClient,
                            GoogleClient,
                            TwitterClient,
                            )


class AuthRoute:
    def __init__(self):
        self.clients = {
            ('bitbucket', Bitbucket),
            ('facebook', Facebook),
            ('github', Github),
            ('google', Google),
            ('twitter', Twitter),
        }

    async def oauth(self, request):
        provider = request.match_info.get('provider')
        Client = dict(self.clients).get(provider, None)
        client = Client()
        token, secret, _ = await client.get_request_token()
        user, info = await client.user_info()
        return user, info


class Twitter(TwitterClient):
    def __init__(self, *args, **kwargs):
        consumer_key = 'oUXo1M7q1rlsPXm4ER3dWnMt8'
        consumer_secret = 'L8qq9PZyRg6ieKGEKhZolGC0vJWLw8iEJ88DRdyOg'
        super().__init__(consumer_key=consumer_key,
                         consumer_secret=consumer_secret,
                         *args, **kwargs)


class Github(GithubClient):
    def __init__(self, *args, **kwargs):
        client_id = 'b6281b6fe88fa4c313e6'
        client_secret = '21ff23d9f1cad775daee6a38d230e1ee05b04f7c'
        super().__init__(client_id=client_id,
                         client_secret=client_secret,
                         *args, **kwargs)


class Google(GoogleClient):
    def __init__(self, *args, **kwargs):
        client_id = '150775235058-9fmas709maee5nn053knv1heov12sh4n.apps.googleusercontent.com'  # noqa
        client_secret = 'df3JwpfRf8RIBz-9avNW8Gx7'
        scope = 'email profile'
        super().__init__(client_id=client_id,
                         client_secret=client_secret,
                         scope=scope,
                         *args, **kwargs)


class Facebook(FacebookClient):
    def __init__(self, *args, **kwargs):
        client_id = '384739235070641'
        client_secret = '8e3374a4e1e91a2bd5b830a46208c15a'
        scope = 'email'
        super().__init__(client_id=client_id,
                         client_secret=client_secret,
                         scope=scope,
                         *args, **kwargs)


class Bitbucket(BitbucketClient):
    def __init__(self, *args, **kwargs):
        consumer_key = '4DKzbyW8JSbnkFyRS5'
        consumer_secret = 'AvzZhtvRJhrEJMsGAMsPEuHTRWdMPX9z'
        super().__init__(consumer_key=consumer_key,
                         consumer_secret=consumer_secret,
                         *args, **kwargs)
