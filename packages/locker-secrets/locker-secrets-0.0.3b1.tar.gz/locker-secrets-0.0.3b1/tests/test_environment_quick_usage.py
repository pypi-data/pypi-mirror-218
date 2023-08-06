import os
from dotenv import load_dotenv

import locker
from locker import environment_quick_usage


MOCK_NAME = "new_prod"
MOCK_EXTERNAL_URL = "new.prod.host"


class TestEnvironmentQuickUsage(object):
    load_dotenv()
    access_key = os.getenv("ACCESS_KEY_TEST")
    locker.access_key = access_key

    def test_list_environments(self):
        environments = environment_quick_usage.list_environments()
        assert isinstance(environments, list)
        for environment in environments:
            assert isinstance(environment, locker.Environment)
            assert isinstance(environment.id, str)
            assert isinstance(environment.name, str)
            assert isinstance(environment.external_url, str)

    def test_create_environment(self):
        environment = environment_quick_usage.create_environment(name=MOCK_NAME, external_url=MOCK_EXTERNAL_URL)
        assert isinstance(environment, locker.Environment)
        assert environment.name == MOCK_NAME
        assert environment.external_url == MOCK_EXTERNAL_URL

    def test_get_environment(self):
        environment = environment_quick_usage.get_environment(name=MOCK_NAME)
        assert isinstance(environment, locker.Environment) or environment is None
        if isinstance(environment, locker.Environment):
            assert isinstance(environment.id, str)
            assert environment.name == MOCK_NAME
            assert environment.external_url == MOCK_EXTERNAL_URL

    def test_modify_environment(self):
        environment = environment_quick_usage.modify_environment(name=MOCK_NAME, external_url=MOCK_EXTERNAL_URL)
        assert isinstance(environment, locker.Environment) or environment is None
        if isinstance(environment, locker.Environment):
            assert isinstance(environment.id, str)
            assert environment.name == MOCK_NAME
            assert environment.external_url == MOCK_EXTERNAL_URL

