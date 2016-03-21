import requests

def Verificationletter(usermail, token):
    return requests.post(
        "https://api.mailgun.net/v3/sandbox9715dcdec1e043b3ab37d4ccf5f7b3c4.mailgun.org/messages",
        auth=("api", "key-15f83f4a591c0a6e9f067550a967391b"),
        data={
            "from": "<waka@sandbox9715dcdec1e043b3ab37d4ccf5f7b3c4.mailgun.org>",
            "to": [usermail, "<waka@sandbox9715dcdec1e043b3ab37d4ccf5f7b3c4.mailgun.org>"],
            "subject": "Hello waka",
            "text": "localhost:5000/verifyuser?token={}".format(token),
            "html": """
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Document</title>
            </head>
            <body>
                <a href="localhost:5000/verifyuser?token={0}">localhost:5000/verifyuser?token={0}</a>
            </body>
            </html>
            """.format(token)
        }
    )

