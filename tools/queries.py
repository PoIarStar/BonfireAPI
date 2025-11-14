import json
from struct import pack


class Query:
    def __init__(self, data: dict):
        self.data: dict = data

    def to_dict(self):
        return self.data

    def to_bytes(self):
        body_bytes = json.dumps(self.data).encode()
        return pack('>I', len(body_bytes)) + body_bytes


def login(email: str, password: str) -> Query:
    return Query({
        "query": """
        mutation LoginEmailMutation($input: LoginEmailInput!) {
            loginEmail(input: $input) {
                __typename
                ... on LoginResultSuccess {
                    accessToken
                    refreshToken
                }
                ... on LoginResultTfaRequired {
                    tfaType
                    tfaWaitToken
                }
            }
        }
        """,
        "variables": {
            "input": {
                "email": email,
                "password": password
            }
        },
        "operationName": "LoginEmailMutation",
        "J_REQUEST_NAME": ""
    })


def get_me():  # в будущем будет возвращать аккаунт, но пока только юзернейм
    return Query({
        "query": """
        query Me {
            me {
                username
                }
            }
        """,
        "J_REQUEST_NAME": "",
        "operationName": "Me"
    })  # у этого типочка надо отловить ошибку отсутствия авторизации. да у всех
