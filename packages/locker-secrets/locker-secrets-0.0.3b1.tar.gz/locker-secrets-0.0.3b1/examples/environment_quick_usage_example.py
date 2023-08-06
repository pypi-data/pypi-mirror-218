import os
from dotenv import load_dotenv

import locker


# Set up access key
load_dotenv()
access_key = os.getenv("ACCESS_KEY_TEST")
locker.access_key = access_key


# Get list environments
environments = locker.list_environments()
for environment in environments:
    print(environment.id, environment.name, environment.external_url, environment.description)


# Get an environment by name
environment = locker.get_environment("prod")
print(environment.id, environment.name, environment.external_url, environment.description)


# Update an environment by name
environment = locker.modify_environment(name="prod", external_url="new.prod.cystack.net")
print(environment)


# Create new environment
new_environment = locker.create_environment(name="prod2", external_url="prod2.cystack.net")
print(new_environment)
