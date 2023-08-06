import os
from dotenv import load_dotenv

import locker


load_dotenv()
access_key = os.getenv("ACCESS_KEY_TEST")
locker.access_key = access_key


# List environments
environments = locker.Environment.list()
for environment in environments:
    print(environment.id, environment.name, environment.external_url)


# Get environment by name
environment = locker.Environment.get_environment(name="NEW_KEY_3")
print(environment.id, environment.name, environment.external_url)


# Create new environment
environment = locker.Environment.create(name="staging", external_url="staging.cystack.net")
print(environment)


# Update environment
environment = locker.Environment.modify(name="staging", external_url="staging-cystack.net")
print(environment)