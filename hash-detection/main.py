import os
import hashlib
import patoolib
from Crypto.Hash import MD4
import zlib

# Paths for extraction and storing hashes
extract_from_path = " "
extract_to_path = " "


# Function to recursively extract archives
def extract(from_path, to_path):
    patoolib.extract_archive(from_path, outdir=to_path)
    for root, dirs, files in os.walk(to_path):
        for file in files:
            path = os.path.join(root, file)
            # Extract nested archives if found (supports .zip and .rar)
            if path.endswith('.zip') or path.endswith('.rar'):
                sub_path = os.path.join(root, os.path.splitext(file)[0])
                os.makedirs(sub_path, exist_ok=True)
                extract(path, sub_path)
                os.remove(path)  # Remove the extracted archive after extraction


# Function to calculate various hash values for a file
def calc_hash(path, hashes_dir):
    os.makedirs(hashes_dir, exist_ok=True)

    with open(path, 'rb') as f:
        data = f.read()

    hash_file = os.path.join(hashes_dir, os.path.splitext(os.path.basename(path))[0] + ".txt")

    with open(hash_file, 'a') as f:
        for algo in hashlib.algorithms_available:

            # Skip shake algorithms which are not supported by MD4
            if algo.startswith('shake_'):
                continue

            # Process other algorithms supported by MD4
            hash_obj = hashlib.new(algo)
            hash_obj.update(data)
            hash_value = hash_obj.hexdigest()
            f.write(f"{algo}: {hash_value}\n")

        # Calculate MD4 hash (using Crypto.Hash)
        md4_hash = MD4.new()
        md4_hash.update(data)
        f.write(f"md4: {md4_hash.hexdigest()}\n")

        # Calculate CRC32 hash (using zlib)
        f.write(f"crc32: {hex(zlib.crc32(data))[2:]}\n")


# Function to compare calculated hashes against known malicious hashes
def compare(message_path, hashes_path, to_path):
    detected_files = set()

    with open(message_path, 'r') as msg_file:
        mal_hashes = {line.strip() for line in msg_file if line.strip()}

    for root, _, files in os.walk(hashes_path):
        for file_name in files:
            hash_file_path = os.path.join(root, file_name)

            with open(hash_file_path, 'r') as hash_file:
                for line in hash_file:
                    line = line.strip()
                    if line:
                        hash_name, hash_value = line.split(': ', 1)
                        hash_value = hash_value.strip()

                        if hash_value in mal_hashes:
                            detected_files.add((os.path.splitext(file_name)[0], hash_value, hash_name))

    with open(to_path, 'w') as detect_file:
        detect_file.write("Detected Hashes:\n\n")

        for file_name, hash_value, hash_name in detected_files:
            detected = False
            for root, _, files in os.walk(extract_to_path):
                for file in files:
                    if file.startswith(file_name) and not file.endswith('.txt'):
                        if not detected:
                            detect_file.write(f"File Name: {file}\n")
                            detect_file.write(f"File Path: {os.path.join(root, file)}\n")
                            detected = True
                        detect_file.write(f"Detected Hash: {hash_value} ({hash_name})\n")
            if detected:
                detect_file.write("\n")


# Main function to manage extraction, hash calculation, and comparison of files
def main():
    # Step 1: Extract files from source archive
    extract(extract_from_path, extract_to_path)

    # Step 2: Calculate hashes for all extracted files
    for root, dirs, files in os.walk(extract_to_path):
        for file in files:
            path = os.path.join(root, file)
            calc_hash(path, " ")

    # Step 3: Compare calculated hashes against known malicious hashes
    compare(" ", " ", " ")


if __name__ == "__main__":
    main()
