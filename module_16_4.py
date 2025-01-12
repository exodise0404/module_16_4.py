from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from typing import List, Annotated

app = FastAPI()


users = []

class User(BaseModel):
    id: int = None
    username: str
    age: int
@app.get('/users')
async def get_users() -> List[User]:
    return users

@app.post('/user/{username}/{age}')
async def post_user(user: User,
                    username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username')],
                    age: float = Path(ge=18, le=120, description='Enter age')) -> str:
    user.id = len(users) + 1
    user.username = username
    user.age = age
    users.append(user)
    return f"User {user.id} is registered"


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: Annotated[int, Path()],
                      username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username')],
                      age: float = Path(ge=18, le=120, description='Enter age')) -> str:
    try:
        edit_user = users[user_id - 1]
        edit_user.username = username
        edit_user.age = age
        return f"The User {user_id} is updated"
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/user/{user_id}')
async def delete_user(user_id: Annotated[int, Path()]) -> str:
    try:
        users.pop(user_id - 1)
        return f'User ID {user_id} deleted!'
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')