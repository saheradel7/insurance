from fastapi import HTTPException, Request
from src.config.env import env
from keycloak import KeycloakOpenID

keycloak_openid = KeycloakOpenID(
    server_url=f"http://{env.keycloak_host}:{env.keycloak_port}",
    client_id=env.keycloak_client,
    realm_name=env.keycloak_realm,
)


def inject_dependencies_authentication(request: Request) -> str:
    """
    Decorator to inject dependencies into a function.
    """
    try:
        token = request.headers.get("Authorization")

        if not token:
            raise HTTPException(status_code=403, detail="Not authenticated")
        token = token.split(" ")[1]
        # print("hi from authentication_dependency.py")
        decoded_token = keycloak_openid.decode_token(token, True)
        # decoded_token = keycloak_openid.decode_token(
        #     token, {"verify_signature": True, "verify_exp": True}
        # )
        # print("hi from decoding")
        if not decoded_token:
            raise HTTPException(status_code=400, detail="Invalid token")
        # print(decoded_token)
        keycloak_user_id = decoded_token.get("sub")
        # print("keycloak_user_id: ", keycloak_user_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        # print(e)
        raise HTTPException(status_code=400, detail="Error while authenticating user")
    return keycloak_user_id
