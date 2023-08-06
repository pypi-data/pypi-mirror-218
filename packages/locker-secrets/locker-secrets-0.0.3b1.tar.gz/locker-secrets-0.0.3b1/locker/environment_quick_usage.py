from locker.ls_resources import Environment


def list_environments(access_key=None, api_base=None, api_version=None, **params):
    return Environment.list(
        access_key=access_key, api_base=api_base, api_version=api_version, **params
    )


def get_environment(name, access_key=None, api_base=None, api_version=None, **params):
    return Environment.get_environment(
        name=name, access_key=access_key, api_base=api_base, api_version=api_version, **params
    )


def create_environment(access_key=None, api_base=None, api_version=None, **params):
    return Environment.create(access_key=access_key, api_base=api_base, api_version=api_version, **params)


def modify_environment(**params):
    return Environment.modify(**params)

