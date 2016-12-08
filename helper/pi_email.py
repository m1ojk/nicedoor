#!/usr/bin/env python
from __future__ import print_function
import subprocess
import logging

class PiEmail:
  send_msg_path = "/projects/scripts/email_msg.sh"
  send_attach_path = "/projects/scripts/email_attach.sh"
  send_msg_attach_path = "/projects/scripts/email_msg_attach.sh"

  subject = "PiCam"

  @staticmethod
  def email_attachment(file_path):
    subprocess.Popen([PiEmail.send_attach_path, PiEmail.subject, file_path])
    logging.debug("Email sent with attachment(%s)"%(file_path))

  @staticmethod
  def email_message(message):
    subprocess.Popen([PiEmail.send_msg_path, PiEmail.subject, message])
    logging.debug("Email sent with message(%s)"%(message))

  @staticmethod
  def email_message_attachment(message, file_path):
    tmp_msg_file_path = "/tmp/cv_email_message"
    f = open(tmp_msg_file_path, 'w')
    print(message, file=f)
    subprocess.Popen([PiEmail.send_msg_attach_path, PiEmail.subject, tmp_msg_file_path, file_path])
    logging.debug("Email sent with message(%s) and attachment from path(%s)"%(message, file_path))

