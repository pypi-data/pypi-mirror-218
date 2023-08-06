import os
from dotenv import load_dotenv

import locker


load_dotenv()
access_key = os.getenv("ACCESS_KEY_TEST")
locker.access_key = access_key

# Get list secrets
secrets = locker.list()
for secret in secrets:
    print(secret.data.key, secret.data.value, secret.data.description)


# Get a secret value by secret key
secret_value = locker.get_secret("KEY_1", None)
print(secret_value)


# Update a secret value by secret key
secret = locker.modify(key="KEY_1", value="NEW_VAL_1", description="NEW_DESC_1")
print(secret.id, secret.data.key, secret.data.value, secret.data.description)


# Create new secret
new_secret = locker.create(key="KEY_11", value="VAL_11")
print(new_secret.id, new_secret.data.key, new_secret.data.value, new_secret.data.description)
