import requests
from config import MAILGUN_KEY as mailgunKey


def Verificationletter(usermail, token):
    return requests.post(
        "https://api.mailgun.net/v3/sandbox9715dcdec1e043b3ab37d4ccf5f7b3c4.mailgun.org/messages",
        auth=("api", mailgunKey),
        data={
            "from": "<waka@sandbox9715dcdec1e043b3ab37d4ccf5f7b3c4.mailgun.org>",
            "to": [usermail, "<waka@sandbox9715dcdec1e043b3ab37d4ccf5f7b3c4.mailgun.org>"],
            "subject": "Hello waka",
            "html": """
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Document</title>
            </head>
            <body>
                <a href="localhost:5000/verifyuser?key={0}">localhost:5000/verifyuser?key={0}</a>
            </body>
            </html>
            """.format(token)
        }
    )