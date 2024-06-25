import secrets

# Generate a secure random string of 32 bytes and convert it to a hexadecimal representation
secret_key = secrets.token_hex(32)

print(f"Generated Secret Key: {secret_key}")
print("You can use this key in your Flask application configuration.")
print("Remember to keep this key secret and don't share it publicly!")