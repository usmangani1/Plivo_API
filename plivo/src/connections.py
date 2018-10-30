# !/usr/bin/python
"""
__email__ sgosman_chem@yahoo.com
__author__ Usman Shaik
"""

import mysql.connector
import logging
import sys

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  passwd="Usmangani1@",
  database="ContactInfo"
)

mycursor = mydb.cursor()

def get_mysql_connection():
  global mydb

  return mydb


def get_logger():
  LOGGER = None
  if LOGGER is None:
    LOGGER = logging.getLogger('producer')
    if len(LOGGER.handlers) == 0:
      LOGGER.addHandler(logging.StreamHandler(sys.stdout))
      LOGGER.setLevel(logging.DEBUG)
  return LOGGER


