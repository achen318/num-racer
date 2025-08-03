from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

users = []


@router.get("/")
def read_users():
    return users


@router.get("/{username}")
def read_user(username: str):
    return {"username": username}


# temporary endpoint to add a user
@router.post("/{username}")
def create_user(username: str):
    if username not in users:
        users.append(username)
        return True

    return False
