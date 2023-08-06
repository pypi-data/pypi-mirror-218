from datetime import datetime

import locker
from locker import util


class TestUtil(object):
    def test_get_object_classes(self):
        assert isinstance(util.get_object_classes(), dict)

    def test_convert_to_ls_object(self):
        resp = {
            "object": "secret",
            "id": "secret-id",
            "data": {
              "key": "MOCK_KEY_SECRET",
              "value": "MOCK_VALUE_SECRET",
              "description": None
            },
            "creation_date": 1686109221.0,
            "revision_date": 1686109221.0,
            "updated_date": 1686109221.0,
            "deleted_date": None,
            "last_use_date": None,
            "project_id": 1,
            "environment_id": None
        }
        obj = util.convert_to_ls_object(resp)
        assert isinstance(obj, locker.Secret)
        assert obj.data.key == resp.get("data").get("key")

    def _test_read_special_variable(self):
        pass

    def test_encode_datetime(self):
        utc_ts = util.encode_datetime(datetime(2023, 1, 1))
        assert isinstance(utc_ts, int) or isinstance(utc_ts, float)
        assert utc_ts <= 1672506000 + 60

    def test_api_encode(self):
        data = {"search": "live_search_text", "page": "1", "size": 10}
        encoded_params = list(util.api_encode(data))
        for encoded_param in encoded_params:
            assert encoded_param[1] == data.get(encoded_param[0])
