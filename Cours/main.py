from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
@app.post("/user")
async def signup(user_form: UserForm, response: Response):
    response.status_code = HTTP_201_CREATED
    return {"message": "User created"}
