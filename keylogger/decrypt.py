import os
from cryptography.fernet import Fernet

# Define the path to the directory where files are stored
path = "/path/to/your/directory"

# Decryption key
# Replace with your decryption key
key = " "

files = {
    "log": os.path.join(path, "log.txt"),
    "system": os.path.join(path, "system.txt"),
    "clipboard": os.path.join(path, "clipboard.txt"),
    "screenshot": os.path.join(path, "screenshot.png")
}

# Decrypt each file
for file in files.values():
    with open(file, 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)

    with open(file, 'wb') as f:
        f.write(decrypted)
