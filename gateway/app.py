from fastapi import FastAPI
import uvicorn

app = FastAPI()

if __name__ == "__main__":
    # THIS APP FOR PIPER API GATEWAY
    uvicorn.run(app, host="localhost", port=8000)