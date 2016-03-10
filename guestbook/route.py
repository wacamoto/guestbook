from guestbook import app
from .view import *


route = app.add_url_rule

route('/', 'index', showIndexPage, methods=['GET'])
route('/register', 'register', userRegister, methods=['POST'])
route('/login', 'login', userLogin, methods=['POST'])
route('/logout', 'logout', userLogout, methods=['GET'])
route('/getboard', 'getboard', getMyBoard, methods=['GET'])
route('/newboard', 'newboard', addNewBoard, methods=['GET'])
route('/delboard', 'delboard', delMyBoard, methods=['GET'])
route('/showboard', 'showboard', showBoard, methods=['GET'])
route('/verifyuser', 'verifyuser', verifyUser, methods=['GET'])
route('/addcomment', 'addcomment', addcomment, methods=['GET'])
route('/getcomment', 'getcomment', getcomment, methods=['GET'])


@app.route('/static/<path:path>')
def staticfile(path):
    return send_from_directory(path)
