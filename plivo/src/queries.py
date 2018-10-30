# !/usr/bin/python
"""
__email__ sgosman_chem@yahoo.com
__author__ Usman Shaik
"""

import traceback
import redis
import connections
import logging
import sys

r = redis.StrictRedis()


mysql_connection= connections.get_mysql_connection()
mysql_connection_session=mysql_connection.cursor(buffered=True)

LOGGER = None
if LOGGER is None:
    LOGGER = logging.getLogger('producer')
    if len(LOGGER.handlers) == 0:
        LOGGER.addHandler(logging.StreamHandler(sys.stdout))
        LOGGER.setLevel(logging.DEBUG)

def contact_exists(email):
    """
    This function checks the redis whether the given email already exists or not.
    :param email: email which has to be checked
    :return: returns true if exists else returns false
    """
    value=r.get("{0}".format(email))
    if value=="exists":
        return True
    else:
        return False


def contact_redis_add(email):
    """
    This function adds the given email into exists
    :param email: email which has to be added
    :return: returns true on successful addition
    """
    r.set("{0}".format(email), "exists")
    value = r.get("{0}".format(email))
    if value == "exists":
        return True
    else:
        return False

def contact_redis_remove(email):
    """
    This function remove the given email
    :param email: email which has to be removed
    :return: returns true on successful addition
    """
    r.delete("{0}".format(email))
    print "Redis deletion successful"


def search_contacts_by_name(name,start,limit):
    """
    This function is used to search the given contacts by name
    :param name: Name of the contact used to search
    :param start: start index of pagination
    :param limit: limit of the value
    :return: returns the list of values
    """
    names = []
    try:

        cursor = mysql_connection.cursor()
        sql = "SELECT name FROM contacts where name LIKE '%{}%' LIMIT {} ,{} ".format(name,start,limit)

        cursor.execute(sql)
        if not cursor.rowcount:
            print "No results found"
        else:
            for row in cursor:
                names.append(row[0])

        print(mysql_connection_session.rowcount, "records Gathered.")

        return names
    except:
        print "Insertion Failed."
        traceback.print_exc()
        return names


def search_contacts_by_email(email,start,limit):
    """
    This function is used to search the given contacts by email
    :param email: email of the contact used to search
    :param start: start index of pagination
    :param limit: limit of the value
    :return: returns the list of emails
    """

    emails = []
    try:

        cursor = mysql_connection.cursor()
        sql = "SELECT email FROM contacts where email LIKE '%{}%' LIMIT {} ,{} ".format(email,start,limit)

        cursor.execute(sql)
        if not cursor.rowcount:
            print "No results found"
        else:
            for row in cursor:
                emails.append(row[0])

        return emails

    except:
        print "Insertion Failed."
        traceback.print_exc()
        return emails

def edit_contact(name,email,organisation,sex,mobile):
    """
    This function is used to edit the contact into the contact book
    :param name: name
    :param email: email
    :param organisation: organisation
    :param sex: gender
    :param mobile: mobile number
    :return: on successful edit returns true
    """
    try:

        sql="UPDATE contacts SET name =%s ,organization=%s,sex=%s,mobile=%s WHERE email = %s"
        val = ("{0}".format(name),"{0}".format(organisation),"{0}".format(sex),"{0}".format(mobile), "{0}".format(email))
        mysql_connection_session.execute(sql, val)
        mysql_connection.commit()
        print (mysql_connection_session.rowcount, "record Updated.")

        return True
    except:
        print "Insertion Failed."
        traceback.print_exc()
        return False

def add_contact(name,email,organisation,sex,mobile):
    """
    This function is used to add the contact into the contact book
    :param name: name
    :param email: email
    :param organisation: organisation
    :param sex: gender
    :param mobile: mobile number
    :return: on successful add returns true
    """
    try:

        sql = "INSERT INTO contacts (name,organization,sex,mobile,email) VALUES (%s,%s,%s,%s,%s)"
        val = ("{0}".format(name),"{0}".format(organisation),"{0}".format(sex),"{0}".format(mobile), "{0}".format(email))
        mysql_connection_session.execute(sql, val)
        mysql_connection.commit()
        print (mysql_connection_session.rowcount, "record Inserted.")
        contact_redis_add(email)
        return True
    except:
        print "Primary key already exists."
        traceback.print_exc()
        return False



def delete_contact(email):
    """
    This funtion is used to delete the contact.
    :param email: email id of the contact
    :return: returns true on successful deletion.
    """
    try:

        sql = "DELETE FROM contacts WHERE email='{}'".format(email)

        mysql_connection_session.execute(sql)
        mysql_connection.commit()
        print (mysql_connection_session.rowcount, "record Deleted.")
        contact_redis_remove(email)
        return True
    except:
        print "Record deletion unsuccessful."
        traceback.print_exc()
        return False

