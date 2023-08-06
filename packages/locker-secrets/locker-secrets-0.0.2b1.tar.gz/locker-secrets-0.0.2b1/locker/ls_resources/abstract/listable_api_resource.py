from __future__ import absolute_import, division, print_function

from locker.ls_resources.abstract.api_resource import APIResource


class ListableAPIResource(APIResource):
    @classmethod
    def auto_paging_iter(cls, *args, **params):
        return cls.list(*args, **params).auto_paging_iter()

    @classmethod
    def list(cls, access_key=None, api_base=None, api_version=None, **params):
        return cls._static_call(
            f"{cls.class_cli()} list",
            access_key=access_key,
            api_base=api_base,
            api_version=api_version,
            params=params,
        )
