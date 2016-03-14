import json

message = {
    "successful": {"successful": "successful"},
    "user_is_exist": {"error": "user_is_exist"},
    "passwd_confirm": {"error": "confirm fail"},
    "field_cantbe_empty": {"error": "can't be empty"},
    "fail_to_login": {"error": "fail_to_login"},
    "user_unactive": {"error": "user_unactive"},
    "page_is_exist": {"error": "this page url is regist"},
    "page_is_not_exist": {"error": "this page url is not regist"}
}

for key in message:
    message[key] = json.dumps(message[key])
