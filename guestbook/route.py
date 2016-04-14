from . import app
from .view import *


route = app.add_url_rule

route('/', 'index', showIndexPage, methods=['GET'])
route('/register', 'register', userRegister, methods=['POST'])
route('/login', 'login', userLogin, methods=['POST'])
route('/logout', 'logout', userLogout, methods=['GET'])
route('/verifyuser', 'verifyuser', verifyUser, methods=['GET'])
route('/showboard', 'showboard', showBoard, methods=['GET'])
route('/board', 'getboard', getMyBoard, methods=['GET'])
route('/board', 'newboard', addMyBoard, methods=['POST'])
route('/board', 'delboard', delMyBoard, methods=['DELETE'])
route('/comment', 'getcomment', getcomment, methods=['GET'])
route('/comment', 'addcomment', addcomment, methods=['POST'])


@app.route('/static/<path:path>')
def staticfile(path):
    return send_from_directory(path)
