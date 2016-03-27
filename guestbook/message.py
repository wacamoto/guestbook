class success(dict):
    def __init__(self, data=None, message="successful"):
        super().__init__()
        self['status'] = "success"
        self['message'] = message
        self['data'] = data

    def setMessage(self, message):
        self['message'] = message

    def setData(self, data):
        self['data'] = data


class fail(dict):
    def __init__(self, data=None, message="successful"):
        super().__init__()
        self['status'] = "fail"
        self['message'] = message
        self['data'] = data

    def setMessage(self, message):
        self['message'] = message

    def setData(self, data):
        self['data'] = data


class error(dict):
    def __init__(self, message="successful", code=0):
        super().__init__()
        self['status'] = "error"
        self['message'] = message
        self['code'] = code

    def setMessage(self, message):
        self['message'] = message

    def setCode(self, code):
        self['code'] = code


fail = {
    "user_is_exist": {
        "status": "fail",
        "message": "user already exist"
    },
    "passwd_confirm": {
        "status": "fail",
        "message": "confirm fail"
    },
    "field_cantbe_empty": {
        "status": "fail",
        "message": "field can't be empty"
    },
    "fail_to_login": {
        "status": "fail",
        "message": "usermail or password is not correct"
    },
    "user_unactive": {
        "status": "fail",
        "message": "user unactive"
    },
    "page_is_exist": {
        "status": "fail",
        "message": "this page already exist"
    },
    "page_is_not_exist": {
        "status": "fail",
        "message": "this page url does not exist"
    },
    "email_invalid": {
        "status": "fail",
        "message": "invaild email"
    },
    "password_invalid": {
        "status": "fail",
        "message": "invaild password"
    },
    "fail_to_verify": {
        "status": "fail",
        "message": "fail to verify"
    }
}
