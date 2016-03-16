import json

message = {
    "successful": {
        "status": "successful"
    },
    "user_is_exist": {
        "status": "error",
        "message": "user is exist"
    },
    "passwd_confirm": {
        "status": "error",
        "message": "confirm fail"
    },
    "field_cantbe_empty": {
        "status": "fail",
        "message": "can't be empty"
    },
    "fail_to_login": {
        "status": "error",
        "message": "fail_to_login"
    },
    "user_unactive": {
        "status": "error",
        "message": "user_unactive"
    },
    "page_is_exist": {
        "status": "error",
        "message": "this page url is regist"
    },
    "page_is_not_exist": {
        "status": "error",
        "message": "this page url is not regist"
    },
    "email_unvalid": {
        "status": "error",
        "message": "email unvalid"
    },
    "password_unvalid": {
        "status": "error",
        "message": "password unvaild"
    }
}

for key in message:
    message[key] = json.dumps(message[key])
