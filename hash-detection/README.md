# File Extraction and Hash Calculation Script

This Python script automates the extraction of files from archives, calculates various hash values for each file, and compares them against known malicious hashes for security analysis.

## Key Features

- **File Extraction**: Recursively extracts files from archives (supports .zip and .rar formats) into specified directories.

  
- **Hash Calculation**: Computes hash values (MD5, SHA-1, SHA-256, etc.) for each extracted file, providing comprehensive data integrity checks.

  
- **Malicious Hash Comparison**: Compares calculated hash values against a predefined list of known malicious hashes to detect potentially harmful files.


- **Recursive Extraction**: Handles nested archives by extracting them recursively, ensuring all files are processed and analyzed.


- **Flexible Hash Algorithms**: Supports a wide range of hash algorithms available in Python's `hashlib` and specialized libraries like `Crypto.Hash` for MD4.


- **Detailed Detection Report**: Generates a detailed report listing detected malicious files, their paths, and the specific hash algorithm and value that matched the known malicious entries.
