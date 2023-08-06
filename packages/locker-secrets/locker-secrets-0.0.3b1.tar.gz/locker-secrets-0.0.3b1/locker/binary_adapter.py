from __future__ import absolute_import, division, print_function

import json
import os
import stat
import sys
import subprocess
from six.moves.urllib.parse import urlencode

import locker
from locker import util
from locker.error import CliRunError, AuthenticationError


class BinaryAdapter(object):
    def __init__(self, access_key=None, api_base=None, api_version=None):
        self.access_key = access_key
        self.api_base = api_base or locker.api_base
        self.api_version = api_version or locker.api_version

    @classmethod
    def get_binary_file(cls):
        # Checking the os system, returns the corresponding binary
        system_platform = sys.platform
        # OS X
        if system_platform == "darwin":
            return os.path.join(locker.ROOT_PATH, "bin", "locker_secret_mac")
        # Windows
        elif system_platform == "win32":
            return os.path.join(locker.ROOT_PATH, "bin", "locker_secret.exe")
        # Default is linux
        else:
            return os.path.join(locker.ROOT_PATH, "bin", "locker_secret_linux")

    @classmethod
    def make_executable(cls, path):
        st = os.stat(path)
        os.chmod(path, st.st_mode | stat.S_IEXEC)

    def call(
        self,
        cli,
        params=None,
        asjson=True,
        load=False,
        shell=True,
        timeout=30,
    ):
        binary_file = self.get_binary_file()
        if binary_file:
            self.make_executable(binary_file)
        if self.access_key:
            my_access_key = self.access_key
        else:
            from locker import access_key
            my_access_key = access_key
        if my_access_key is None:
            raise AuthenticationError(
                "No Access key provided. (HINT: set your API key using "
                '"locker.access_key = <ACCESS-KEY>"). You can generate Access Key '
                "from the Locker Secret web interface."
            )

        default_user_agent = f"Python{sys.version_info[0]}"
        command = f'{binary_file} {cli} --access-key "{my_access_key}" --api-base {self.api_base} ' \
                  f'--client {default_user_agent}'

        # Building full command with params
        post_data = None
        if "get" in cli or "delete" in cli:
            encoded_params = urlencode(list(util.api_encode(params or {})))
            # Don't use strict form encoding by changing the square bracket control
            # characters back to their literals. This is fine by the server, and
            # makes these parameter strings easier to read.
            encoded_params = encoded_params.replace("%5B", "[").replace("%5D", "]")
            # TODO: Build api url by passing filter params to command
            # if params:
            #     abs_url = _build_api_url(abs_url, encoded_params)
            pass
        elif "update" in cli or "create" in cli:
            post_data = json.dumps(json.dumps(params or {}))

        if post_data:
            command += f' --data {post_data}'
        try:
            raw = subprocess.check_output(
                command,
                stderr=subprocess.STDOUT, shell=shell, universal_newlines=True, timeout=timeout
            )
        except subprocess.TimeoutExpired as e:
            exc = CliRunError(e.stdout)
            exc.process = e
            raise exc
        except subprocess.CalledProcessError as e:
            signs = ['"success": false', '"success": true']
            if any(s in e.output for s in signs):
                raw = e.output
            elif str(e.output).strip() == 'Killed' or 'returned non-zero exit status 1' in str(e):
                exc = CliRunError(e.stdout)
                exc.process = e
                raise exc
            else:
                print(f"[!] subprocess.CalledProcessError: {e} {e.output}. The command is: {command}")
                exc = CliRunError(e.stdout)
                exc.process = e
                raise exc
        if asjson:
            try:
                return json.loads(raw)
            except json.decoder.JSONDecodeError:
                exc = CliRunError(f"CLI JSONDecodeError:::{raw}\nis None:::{raw is None}\nis Empty:::{raw == ''}")
                exc.process = raw
                raise exc
        return raw

