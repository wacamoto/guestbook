from guestbook import app
from .view import *


app.add_url_rule('/',           'index',        showIndexPage,  methods=['GET'])
app.add_url_rule('/register',   'register',     registerUser,   methods=['POST'])
app.add_url_rule('/login',      'login',        loginUser,      methods=['POST'])
app.add_url_rule('/logout',     'logout',       logoutUser,     methods=['GET'])
app.add_url_rule('/myboard',    'myboard',      getMyBoard,     methods=['GET'])
app.add_url_rule('/newboard',   'newboard',     addNewBoard,    methods=['POST'])
app.add_url_rule('/delboard',   'delboard',     delMyBoard,     methods=['GET'])
app.add_url_rule('/showboard',  'showboard',    showBoard,      methods=['GET'])

app.add_url_rule('/comments/<int:board_id>', 'comments', leaveComment, methods=['GET', 'POST'])


@app.route('/static/<path:path>')
def staticfile(path):
    return send_from_directory(path)
