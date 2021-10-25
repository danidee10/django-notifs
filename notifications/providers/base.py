import abc
import importlib
import logging
from typing import List

from pydantic import BaseModel, ValidationError

from notifications import (
    InvalidNotificationProvider,
    InvalidNotificationProviderPayload,
)
from notifications.utils import classproperty


class BaseNotificationProvider(metaclass=abc.ABCMeta):
    def __init__(self, context=dict()):
        self.logger = logging.getLogger(f'{self.name}_provider')
        self.context = context

    @abc.abstractproperty
    def name(self):
        raise NotImplementedError

    @classproperty
    def providers(cls):
        return {
            klass.name: f'{klass.__module__}.{klass.__name__}'
            for klass in cls.__subclasses__()
        }

    @classmethod
    def get_provider_class(cls, provider):
        try:
            provider_class = cls.providers[provider]
        except KeyError:
            # Generate helpful error if the provider is valid
            # but it's dependencies are missing
            try:
                importlib.import_module(f'notifications.providers.{provider}')
            except ModuleNotFoundError:
                raise InvalidNotificationProvider(
                    f'{provider} is not a valid notification provider.\n'
                    f'Registered providers: {cls.providers}'
                )

        return provider_class

    @abc.abstractmethod
    def send(self, payload):
        raise NotImplementedError

    def get_validator(self):
        try:
            validator = self.validator
        except AttributeError as err:
            raise AttributeError(
                'You must set the `validator` attribute or override the'
                '`get_validator` method'
            ) from err

        if self.context.get('bulk', False):

            class BulkValidator(BaseModel):
                __root__: List[validator]

            BulkValidator.__name__ = f'Bulk{self.validator.__name__}'

            return BulkValidator

        return validator

    def validate(self, data):
        validator = self.get_validator()

        try:
            validator.parse_obj(data)
        except ValidationError as err:
            self.logger.error(err.json())
            raise InvalidNotificationProviderPayload from err

    def send_bulk(self, payloads):
        for payload in payloads:
            self.send(payload)
