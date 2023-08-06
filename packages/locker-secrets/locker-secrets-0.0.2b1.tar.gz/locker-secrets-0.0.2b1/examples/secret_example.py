import os
from dotenv import load_dotenv

import locker


load_dotenv()
access_key = os.getenv("ACCESS_KEY_TEST")
locker.access_key = access_key

# List secrets
secrets = locker.Secret.list()
for secret in secrets:
    print(secret.id, secret.data.key, secret.data.value)


# Get a secret value by secret key
secret_value = locker.Secret.get_secret("KEY_1", "default_value")
print(secret_value)


# Update a secret by key
updated_secret = locker.Secret.modify(
    key="NEW_KEY_2",
    value="NEW_VAL_2",
    description="NEW_DESC_2"
)
print(updated_secret)


# Create new secret
new_secret = locker.Secret.create(
    key="KEY_8",
    value="VAL_8",
    description="DESC_8",
    environment_id="ad2d5c24-a01d-4322-972a-659e2c666a96"
)
print(new_secret)
