from locker.ls_resources import Secret


def list(access_key=None, api_base=None, api_version=None, **params):
    return Secret.list(
        access_key=access_key, api_base=api_base, api_version=api_version, **params
    )


def get(key, default_value=None, access_key=None, api_base=None, api_version=None, **params):
    return Secret.get_secret(
        key, default_value=default_value,
        access_key=access_key,
        api_base=api_base,
        api_version=api_version,
        **params
    )


def update(**params):
    return Secret.modify(**params)


def get_secret(key, default_value=None, access_key=None, api_base=None, api_version=None, **params):
    return get(
        key, default_value=default_value,
        access_key=access_key,
        api_base=api_base,
        api_version=api_version,
        **params
    )


# ------------ (DEPRECATED) --------------- #
def retrieve(id, access_key=None, **params):
    return Secret.retrieve(id, access_key, **params)


def create(access_key=None, api_base=None, api_version=None, **params):
    return Secret.create(access_key=access_key, api_base=api_base, api_version=api_version, **params)


def modify(**params):
    return Secret.modify(**params)


# ------- (DEPRECATED) --------------- #
def delete(sid, **param):
    """
    Currently, this method is not supported
    :param sid:
    :param param:
    :return:
    """
    pass
