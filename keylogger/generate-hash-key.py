from cryptography.fernet import Fernet

# Generate a key using Fernet
key = Fernet.generate_key()

# Write the key to a file named "hash_key.txt"
file = open("hash_key.txt", 'wb')
file.write(key)
file.close()
