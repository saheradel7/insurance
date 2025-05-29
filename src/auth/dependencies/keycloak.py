from fastapi import FastAPI, HTTPException, Request
from src.config.env import env as env
from ..user_schema import UserCreate
from keycloak import KeycloakOpenIDConnection, KeycloakAdmin

keycloak_connection = KeycloakOpenIDConnection(
    server_url=f"http://{env.keycloak_host}:{env.keycloak_port}",
    username=env.keycloak_username,
    password=env.keycloak_password,
    realm_name=env.keycloak_realm,
    # user_realm_name="only_if_other_realm_than_master",
    client_id=env.keycloak_client,
    # client_secret_key="client-secret",
    verify=False,
)

keycloak_admin = KeycloakAdmin(connection=keycloak_connection)


# def get_keycloak_admin():
#     """
#     Get Keycloak admin connection.
#     """
#     return KeycloakAdmin(
#         server_url=f"http://{constants.KEYCLOAK_HOST}:{constants.KEYCLOAK_PORT}",
#         username=constants.KEYCLOAK_USERNAME,
#         password=constants.KEYCLOAK_PASSWORD,
#         realm_name=constants.KEYCLOAK_REALM,
#         client_id=constants.KEYCLOAK_CLIENT,
#         verify=False,
#     )


# def check_user_in_keycloak(keycloak_user_id: str):
def check_user_in_keycloak(user: UserCreate):
    """
    Check if the user exists in Keycloak.
    """
    # user_info = keycloak_openid.userinfo(token=keycloak_user_id)
    try:
        keycloak_user_id = user.keycloak_user_id
        print(type(keycloak_user_id))
        print("Keycloak user ID to check: ", keycloak_user_id)
        # keycloak_admin = get_keycloak_admin()
        # print("Keycloak admin connection established.")
        users = keycloak_admin.get_users({})
        print("Users in realm:", len(users))
        user = keycloak_admin.get_user("")
    except Exception as e:
        print("Error while checking user in Keycloak:", str(e))
        raise HTTPException(
            status_code=404, detail="User not found with this key cloak id"
        )
    # return user
