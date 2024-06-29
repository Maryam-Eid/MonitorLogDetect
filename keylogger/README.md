# Remote Monitoring and Logging Script

This Python script monitors and logs various system activities, encrypts the logged data, and sends it via email for remote monitoring purposes.

## Key Features

- **System Monitoring**: Gathers and logs system information including hostname, IP address, OS details, CPU usage, and memory usage.
  

- **Clipboard Monitoring**: Captures clipboard contents and logs them periodically.
  

- **Screenshot Capture**: Takes screenshots at regular intervals for visual monitoring.
  

- **Keylogging**: Records keystrokes and logs them to a file.


- **Encryption**: Encrypts logged data using Fernet encryption for secure transmission.


- **Email Alert**: Sends encrypted logs as email attachments to a specified address for remote monitoring.

## Usage Notes

- **Generating Encryption Key**:
   - Run `generate-hash-key.py` to generate a Fernet encryption key.
   - The generated key is saved in a file named `hash_key.txt` in the current directory.


- **Decrypting Files**:
   - Use `decrypt.py` to decrypt the encrypted files generated by the script.
   - Specify the decryption key (`key`) and the directory (`path`) where encrypted files (`log.txt`, `system.txt`, `clipboard.txt`, `screenshot.png`) are located.

This script is designed only for educational purposes.