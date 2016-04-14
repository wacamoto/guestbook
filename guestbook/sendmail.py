import os
import codecs
import requests
from flask import url_for

import config

f = codecs.open(os.path.join(config.basedir, 'guestbook/templates/Verificationletter.html'), 'r')
html = f.read()

def Verificationletter(usermail, token):
    return requests.post(
        config.MAILGUN_API,
        auth=("api", config.MAILGUN_KEY),
        data={
            "from": config.MAILGUN_SERVER,
            "to": [usermail, config.MAILGUN_SERVER],
            "subject": "Hello waka",
            "html": html.format(token, config.SITENAME + url_for('verifyuser'))
        }
    )
