from typing import List, Optional

try:
    import tweepy

    HAS_DEPENDENCIES = True
except ImportError:
    HAS_DEPENDENCIES = False

from pydantic import BaseModel, Field

from notifications import default_settings as settings

from . import BaseNotificationProvider


class TwitterStatusUpdateSchema(BaseModel):
    status: str = Field(description='The text of your status update')
    in_reply_to_status_id: str = Field(
        description='The ID of an existing status that the update is in reply to.'
        'Note: This parameter will be ignored unless the author of the Tweet this'
        'parameter references is mentioned within the status text.'
        'Therefore, you must include @username, where username'
        'is the author of the referenced Tweet, within the update.'
    )

    auto_populate_reply_metadata: Optional[bool]
    exclude_reply_user_ids: Optional[List[str]]
    attachment_url: Optional[str]
    media_ids: Optional[List[str]]
    possibly_sensitive: Optional[bool]
    lat: Optional[str]
    long: Optional[str]
    place_id: Optional[str]
    display_coordinates: Optional[bool]
    trim_user: Optional[bool]
    card_uri: Optional[str]


class TwitterStatusUpdateNotificationProvider(BaseNotificationProvider):
    name = 'twitter_status_update'
    validator = TwitterStatusUpdateSchema
    package = 'tweepy'

    HAS_DEPENDENCIES = HAS_DEPENDENCIES

    def __init__(self, context=dict()):
        super().__init__(context=context)
        auth = tweepy.OAuthHandler(
            settings.NOTIFICATIONS_TWITTER_CONSUMER_KEY,
            settings.NOTIFICATIONS_TWITTER_CONSUMER_SECRET,
        )
        auth.set_access_token(
            settings.NOTIFICATIONS_TWITTER_ACCESS_TOKEN,
            settings.NOTIFICATIONS_TWITTER_ACCESS_TOKEN_SECRET,
        )
        self.twitter_client = tweepy.API(auth)

    def send(self, payload):
        try:
            self.twitter_client.update_status(**payload)
        except tweepy.errors.Forbidden as e:
            print('Rate limit reached', e)
        except tweepy.errors.TooManyRequests as e:
            print('Too many requests', e)
