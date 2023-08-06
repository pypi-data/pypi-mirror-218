import json
import os
import os.path

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


class GoogleCredentials(object):
    # shared credentials descriptor

    def __get__(self, *args, **kwargs):
        if not hasattr(self, f'_credentials'):
            credentials = os.environ.get('GSUITE_CREDENTIALS', None)
            if isinstance(credentials, str):
                if os.path.isfile(credentials):
                    setattr(self, '_credentials',
                            Credentials.from_service_account_file(credentials))
                else:
                    try:
                        setattr(self, '_credentials',
                                Credentials.from_service_account_info(
                                    json.loads(credentials)))
                    except json.JSONDecodeError:
                        raise RuntimeError('The credentials string is not JSON parseable.')
            elif isinstance(credentials, dict):
                setattr(self, '_credentials',
                        Credentials.from_service_account_info(credentials))
            else:
                raise RuntimeError('Invalid or missing credentials.')
        return getattr(self, '_credentials')


class GoogleAPI(type):
    credentials = GoogleCredentials()

    def __new__(mcs, name, bases, class_dict, **kwargs):
        if not hasattr(mcs, f"_{kwargs['service']}"):
            setattr(mcs, f"_{kwargs['service']}",
                    build(kwargs['service'], kwargs['version'],
                          credentials=mcs.credentials))
        cls = super().__new__(mcs, name, bases, class_dict)
        cls.service = getattr(mcs, f"_{kwargs['service']}")
        return cls
