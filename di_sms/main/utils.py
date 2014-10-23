import requests
from StringIO import StringIO


def make_ona_submission(url, xml_str):
    files = {'xml_submission_file': StringIO(xml_str)}
    response = requests.post(url, files=files)

    return response
