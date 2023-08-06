# Locker Secret Python SDK

<p align="center">
  <img src="https://cystack.net/images/logo-black.svg" alt="CyStack" width="50%"/>
</p>


---

The Locker Secret Python SDK provides convenient access to the Locker Secret API from applications written in the 
Python language. It includes a pre-defined set of classes for API resources that initialize themselves dynamically 
from API responses which makes it compatible with a wide range of versions of the Locker Secret API.


## The Developer - CyStack

The Locker Secret Python SDK is developed by CyStack, one of the leading cybersecurity companies in Vietnam. 
CyStack is a member of Vietnam Information Security Association (VNISA) and Vietnam Association of CyberSecurity 
Product Development. CyStack is a partner providing security solutions and services for many large domestic and 
international enterprises.

CyStack’s research has been featured at the world’s top security events such as BlackHat USA (USA), 
BlackHat Asia (Singapore), T2Fi (Finland), XCon - XFocus (China)... CyStack experts have been honored by global 
corporations such as Microsoft, Dell, Deloitte, D-link...


## Documentation

The documentation will be updated later.

## Requirements

- Python 3.6+

## Installation

Install from PyPip:

```
pip install --upgrade locker
```

Install from source with:

```
python setup.py install
```

## Usages

The SDK needs to be configured with your access key which is available in your Locker Secret Dashboard. 
Set locker.access_key to its value:

```
import locker
locker.access_key = "your_access_key_..."
```

You also need to set base_api value (default is `https://secrets-core.locker.io`)

```
import locker
locker.base_api = "your_base_api.host"
```

Now, you can use SDK to get or set values:
```
# Get list secrets quickly
secrets = locker.list()

# Get a secret value by key
secret_value = locker.get_secret("YOUR_SECRET_TOKEN")

# Or, we also get a secret by get() function
secret_value = locker.get("YOUR_SECRET_TOKEN")

# Create new secret
secret = locker.create(key="YOUR_NEW_SECRET_KEY", value="YOUR_NEW_SECRET_VALUE")

# Update new secret
secret = locker.modify(key="YOUR_NEW_SECRET_KEY", value="UPDATED_SECRET_VALUE")

# List environments
environments = locker.list_environments()

# Get an environment object by name
environment = locker.get_environment("prod")

# Create new environment
new_environment = locker.create_environment(name="staging", external_url="staging.host")

# Update an environment by name
environment = locker.modify_environment(name="staging", external_url="new.staging.host")
```

## Examples

See the [examples' folder](/examples).

## Development

First install for development.
```
pip install -r requirements-dev.txt
```

### Run tests

Test by using tox. We test against the following versions.
- 3.6
- 3.7
- 3.8
- 3.9
- 3.10

To run all tests against all versions, use:
```
tox
```

Run all tests for a specific Python version:
```
tox -e py3.10
```

Run all tests in a single file:
```
tox -e py3.10 -- tests/test_util.py
```


## Reporting security issues

We take the security and out users' trust very seriously. If you found a security issue in Locker SDK Python, please 
report the issue by contacting us at <contact@locker.io>. Do not file an issue on the tracker. 


## Contributing

Please check [CONTRIBUTING](CONTRIBUTING.md) before making a contribution.


## Help and media

- FAQ: https://support.locker.io

- Community Q&A: https://forum.locker.io

- News: https://locker.io/blog


## License
