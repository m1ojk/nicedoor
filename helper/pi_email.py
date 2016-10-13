#!/usr/bin/env python
import subprocess

send_msg_path = "/products/scripts/email_msg.sh"
send_attach_path = "/products/scripts/email_attach.sh"
subject = "PiCam"

def email_attachment(file_path):
    subprocess.Popen([send_attach_path, subject, file_path])
    
def email_message(message):
    subprocess.Popen([send_msg_path, subject, message])
