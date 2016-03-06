import json

message = {
    "successful": {"successful": "successful"},
    "user_is_exist": {"error": "user_is_exist"},
    "passwd_confirm": {"error": "password confirm not same"},
    "field_cantbe_empty": {"error": "can't be empty"},
    "fail_to_login":{"error": "fail_to_login"}
}

for key in message:
    message[key] = json.dumps(message[key])
