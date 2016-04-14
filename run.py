#! .env/bin/python3.5

from guestbook import app
from config import HOST, PORT

app.run(host=HOST, port=PORT)
