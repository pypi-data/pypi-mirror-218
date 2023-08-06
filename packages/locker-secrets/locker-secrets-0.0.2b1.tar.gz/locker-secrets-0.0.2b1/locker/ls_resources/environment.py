from __future__ import absolute_import, division, print_function

from six.moves.urllib.parse import quote_plus

from locker.error import CliRunError
from locker.ls_resources.abstract import ListableAPIResource, CreateableAPIResource, UpdateableAPIResource, \
    DeletableAPIResource, DetailableAPIResource


class Environment(ListableAPIResource, DetailableAPIResource,
                  CreateableAPIResource, UpdateableAPIResource, DeletableAPIResource):

    OBJECT_NAME = "environment"

    @classmethod
    def get_environment(cls, name, access_key=None, api_base=None, api_version=None, **params):
        """
        Get Environment object by name
        :param name:
        :param access_key:
        :param api_base:
        :param api_version:
        :param params:
        :return:
        """
        base = cls.class_cli()
        cli_ = '%s get --id "%s"' % (base, name)
        instance = cls(None, access_key, **params)
        try:
            instance._call_and_refresh(
                cli_, access_key=access_key, api_base=api_base, api_version=api_version, params=params
            )
        except CliRunError as e:
            print(e)
            # TODO: Change the return result when not found the environment
            return None
        return instance

    @classmethod
    def modify(cls, **params):
        name = params.get("name")
        cli = '%s update --id "%s"' % (cls.class_cli(), quote_plus(name))
        return cls._static_call(cli, params=params)
