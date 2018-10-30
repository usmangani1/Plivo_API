# !/usr/bin/python
"""
__email__ sgosman_chem@yahoo.com
__author__ Usman Shaik
"""

def paginate_result(result,start,limit,url):
    """
    This function paginates the given results
    :param result: The dictonary before pagination
    :param start: starting value of the index
    :param limit: limit of the indec
    :param url:  url
    :return: returns the json with the pagination result.
    """

    result["data"]["_links"]={}
    result["data"]["_links"]["self"]=url
    if start>limit:
        result["data"]["_links"]["prev"] = "{}?start={}&limit={}".format(url,int(start)-int(limit),int(start))
    result["data"]["_links"]["next"] = "{}?start={}&limit={}".format(url,int(start)+int(limit),int(start)+2*(int(limit)))
    result["data"]["limit"]=limit

    return result
