import json

def success(data=None, message="successful"):
    return {
        "status": "success",
        "message": message,
        "data": data
    }

def fail(data=None, message="successful"):
    return {
        "status": "fail",
        "message": message
    }

def error(data=None, message="successful", code=0):
    return {
        "status": "error",
        "message": message,
        "code": code
    }


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
