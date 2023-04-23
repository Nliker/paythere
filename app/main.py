from fastapi import FastAPI
from config import make_conf_dict
import uvicorn
from fastapi import APIRouter

def create_app():
    app = FastAPI()

    app.conf=make_conf_dict()

    @app.get("/ping")
    def ping():
        return {"data":"pong"}
    return app

    

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=app.conf.app_port, reload=app.conf.proj_reload)

    
    
