"""
An example on how to encrypt a simple password using cryptography.Fernet vault-object.

Input: Password in bytes.

Returns: The encrypted password in unreadable bytes structure.
"""



from cryptography.fernet import Fernet

# 1. Create key
key = Fernet.generate_key()

# 2. Initialize Vault-Object
cipher = Fernet(key)

# 3. Encryption (Only Bytes allowed!)
secret_bytes = "MyPassword123!".encode()
encrypted = cipher.encrypt(secret_bytes)

print(encrypted) # This is now an unreadable bytes structure