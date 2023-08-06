from __future__ import absolute_import, division, print_function

import logging

from six.moves.urllib.parse import quote_plus

from locker.error import CliRunError
from locker.ls_resources.abstract import ListableAPIResource, CreateableAPIResource, UpdateableAPIResource, \
    DeletableAPIResource


class Secret(ListableAPIResource, CreateableAPIResource, UpdateableAPIResource, DeletableAPIResource):
    OBJECT_NAME = "secret"

    @classmethod
    def get_secret(cls, key, default_value=None, access_key=None, api_base=None, api_version=None, **params):
        base = cls.class_cli()
        cli_ = '%s get --id "%s"' % (base, key)
        instance = cls(None, access_key, **params)
        try:
            instance._call_and_refresh(
                cli_, access_key=access_key, api_base=api_base, api_version=api_version, params=params
            )
        except CliRunError as e:
            logging.warning(f"[!] CliRunError when get_secret of {key}. So return default value is {default_value}\n"
                            f"Traceback: {e}")
            return default_value
        try:
            return instance.data.value
        except AttributeError:
            return default_value

    @classmethod
    def modify(cls, **params):
        key = params.get("key")
        cli = '%s update --id "%s"' % (cls.class_cli(), quote_plus(key))
        return cls._static_call(cli, params=params)
