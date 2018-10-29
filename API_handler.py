# !/usr/bin/python
"""
__email__ sgosman_chem@yahoo.com
__author__ Usman Shaik
"""

from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
import paginate
import datetime
import json
import queries
import traceback
import logging
import sys


USER_DATA = {
    "admin":"supercontacts"
}


LOGGER = None
if LOGGER is None:
    LOGGER = logging.getLogger('producer')
    if len(LOGGER.handlers) == 0:
        LOGGER.addHandler(logging.StreamHandler(sys.stdout))
        LOGGER.setLevel(logging.DEBUG)

app = Flask("Contacts")
auth = HTTPBasicAuth()



@auth.verify_password
def verify(username, password):
    """
    This function is used to do the basic verification
    :param username: username provided
    :param password: password provided
    :return: returns true if username and the password matches.
    """
    if not (username and password):
        return False
    return USER_DATA.get(username) == password



@app.route("/contacts/edit/",methods=["PUT"])
def editContact():

    """
    This function is used edit any contact which is already present.

    :return: On successful edit this function returns code 200 else it returns 404

    """
    result = {}
    try:
        name=0
        email=0
        organisation=0
        sex=0
        mobile=0
        new_req = request.get_json()

        logs = {}
        logs["TIME"] = "{0}".format(datetime.datetime.isoformat(datetime.datetime.now()))
        logs["@request"] = "{0}".format(new_req)
        LOGGER.info(json.dumps(logs))

        if "name" in new_req:
            name = new_req["name"]
        if "email" in new_req:
            email = new_req["email"]
        if "organisation" in new_req:
            organisation = new_req["organisation"]
        if "sex" in new_req:
            sex = new_req["sex"]
        if "mobile" in new_req:
            mobile=new_req["mobile"]

        if (queries.contact_exists(email)):
            edit_query=queries.edit_contact(name,email,organisation,sex,mobile)
        else:
            edit_query=0

        if edit_query:
            message="Update successful."
            code=200

        else:
            message = "Update Failed."
            code = 201


        result["data"] = {}
        result["data"]["message"] ="{0}".format(message)
        result["code"] = code
        return jsonify(result)

    except:
        result["code"] = 404
        result["data"] = {}
        logs = {}
        logs["TIME"] = "{0}".format(datetime.datetime.isoformat(datetime.datetime.now()))
        logs["message"] = "Insertion failed."
        logs["TraceBack"] = traceback.print_exc()
        LOGGER.info(json.dumps(logs))
        return jsonify(result)



@app.route("/contacts/add/",methods=["POST"])
@auth.login_required
def addContact():

    """
    This function is used to add a contact to the contact book.

    :return: On successful addition it returns code 200 else returns 404

    """
    result = {}
    try:
        name=0
        email=0
        organisation=0
        sex=0
        mobile=0
        new_req = request.get_json()

        logs = {}
        logs["TIME"] = "{0}".format(datetime.datetime.isoformat(datetime.datetime.now()))
        logs["@request"] = "{0}".format(new_req)
        LOGGER.info(json.dumps(logs))

        if "name" in new_req:
            name = new_req["name"]
        if "email" in new_req:
            email = new_req["email"]
        if "organisation" in new_req:
            organisation = new_req["organisation"]
        if "sex" in new_req:
            sex = new_req["sex"]
        if "mobile" in new_req:
            mobile=new_req["mobile"]

        if queries.contact_exists(email):
            add_query = 0
            logs = {}
            logs["TIME"] = "{0}".format(datetime.datetime.isoformat(datetime.datetime.now()))
            logs["message"] = "Insertion failed because contacts already exists with the given emailid."
            LOGGER.info(json.dumps(logs))

        else:
            add_query=queries.add_contact(name,email,organisation,sex,mobile)

        if add_query:
            message="insertion successful."
            code=200

        else:
            message = "insertion Failed."
            code = 201


        result["data"] = {}
        result["data"]["message"] ="{0}".format(message)
        result["code"] = code
        return jsonify(result)

    except:
        result["code"] = 404
        result["data"] = {}
        logs = {}
        logs["TIME"] = "{0}".format(datetime.datetime.isoformat(datetime.datetime.now()))
        logs["message"] = "Insertion failed."
        logs["TraceBack"] = traceback.print_exc()
        LOGGER.info(json.dumps(logs))
        return jsonify(result)








@app.route("/contacts/delete/",methods=["DELETE"])
@auth.login_required
def deleteContact():

    """
    This function is used delete the contact which is already present.

    :return: On successful deletion it returns 200 else returns 404

    """
    result = {}
    try:

        email=0
        new_req = request.get_json()

        logs = {}
        logs["TIME"] = "{0}".format(datetime.datetime.isoformat(datetime.datetime.now()))
        logs["@request"] = "{0}".format(new_req)
        LOGGER.info(json.dumps(logs))


        if "email" in new_req:
            email = new_req["email"]

        if queries.contact_exists(email):
            delete_query=queries.delete_contact(email)
        else:
            delete_query=0

        if delete_query:
            message="Deletion successful."
            code=200

        else:
            message = "Deletion Failed."
            code = 201


        result["data"] = {}
        result["data"]["message"] ="{0}".format(message)
        result["code"] = code
        return jsonify(result)

    except:
        result["code"] = 404
        result["data"] = {}
        logs = {}
        logs["TIME"] = "{0}".format(datetime.datetime.isoformat(datetime.datetime.now()))
        logs["message"] = "Insertion failed."
        logs["TraceBack"] = traceback.print_exc()
        LOGGER.info(json.dumps(logs))
        return jsonify(result)





@app.route("/contacts/Search/Name",methods=["GET"])
def searchContactByName():

    """
    This function is used to search the contact book by name.

    :return: On successful search it returns the list of items else returns 404

    """
    result = {}
    try:
        url="/contacts/Search/Name"
        name=request.args.get("name")
        start=request.args.get("start")
        if start==None:
            start=0
        limit=5

        if name==None:
            message= "No input has been provided to search"
            result["data"] = {}
            result["data"]["information"]=[]
            result["data"]["message"] = "{0}".format(message)
            result["code"] = 200
            return jsonify(result)

        result_data = queries.search_contacts_by_name(name,start,limit)

        logs = {}
        logs["TIME"] = "{0}".format(datetime.datetime.isoformat(datetime.datetime.now()))
        logs["@request"] = "{0}".format(request.args)
        LOGGER.info(json.dumps(logs))


        result["data"] = {}
        result["data"]["result"]=result_data
        message="Data retrieval Successful"
        result["data"]["message"] ="{0}".format(message)
        result["code"] = 200
        result=paginate.paginate_result(result,start,limit,url)
        return jsonify(result)

    except:
        result["code"] = 404
        result["data"] = {}
        logs = {}
        logs["TIME"] = "{0}".format(datetime.datetime.isoformat(datetime.datetime.now()))
        logs["message"] = "Search Query failed."
        logs["TraceBack"] = traceback.print_exc()
        LOGGER.info(json.dumps(logs))
        return jsonify(result)



@app.route("/contacts/Search/Email",methods=["GET"])
def searchContactByEmail():

    """
    This function is used to search the contact book by email.

    :return: On successful search this function returns code 200 with the list of emails else returns 404.

    """
    result = {}
    try:
        url = "/contacts/Search/Email"

        email = request.args.get("email")
        start = request.args.get("start")
        if start==None:
            start=0
        limit = 5

        if email==None:
            message= "No input has been provided to search"
            result["data"] = {}
            result["data"]["information"]=[]
            result["data"]["message"] = "{0}".format(message)
            result["code"] = 200
            return jsonify(result)

        result_data = queries.search_contacts_by_email(email,start,limit)

        logs = {}
        logs["TIME"] = "{0}".format(datetime.datetime.isoformat(datetime.datetime.now()))
        logs["@request"] = "{0}".format(request.args)
        LOGGER.info(json.dumps(logs))


        result["data"] = {}
        result["data"]["result"]=result_data
        message="Data retrieval Successful"
        result["data"]["message"] ="{0}".format(message)
        result["code"] = 200
        result = paginate.paginate_result(result, start, limit, url)
        return jsonify(result)

    except:
        result["code"] = 404
        result["data"] = {}
        logs = {}
        logs["TIME"] = "{0}".format(datetime.datetime.isoformat(datetime.datetime.now()))
        logs["message"] = "Search Query failed."
        logs["TraceBack"] = traceback.print_exc()
        LOGGER.info(json.dumps(logs))
        return jsonify(result)


if __name__ == '__main__':
    app.run(host='127.0.0.1',port=9090,debug=False)