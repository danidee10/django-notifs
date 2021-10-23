from notifications import ImproperlyInstalledNotificationProvider

try:
    import tweepy
except ImportError:
    raise ImproperlyInstalledNotificationProvider(
        missing_package='tweepy', provider='twitter'
    )

from notifications import default_settings as settings

from . import BaseNotificationProvider


class TwitterStatusUpdateNotificationProvider(BaseNotificationProvider):
    name = 'twitter_status_update'

    def __init__(self, context=dict()):
        auth = tweepy.OAuthHandler(
            settings.NOTIFICATIONS_TWITTER_CONSUMER_KEY,
            settings.NOTIFICATIONS_TWITTER_CONSUMER_SECRET,
        )
        auth.set_access_token(
            settings.NOTIFICATIONS_TWITTER_ACCESS_TOKEN,
            settings.NOTIFICATIONS_TWITTER_ACCESS_TOKEN_SECRET,
        )
        self.twitter_client = tweepy.API(auth)
        super().__init__(context=context)

    def send(self, payload):
        try:
            self.twitter_client.update_status(**payload)
        except tweepy.errors.Forbidden as e:
            print('Rate limit reached', e)
        except tweepy.errors.TooManyRequests as e:
            print('Too many requests', e)
