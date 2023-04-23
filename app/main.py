from fastapi import FastAPI
from config import make_conf_dict
import uvicorn
from api import user_router

class Services:
    pass

def create_app():
    app = FastAPI()

    app.conf=make_conf_dict()

    @app.get("/ping")
    def ping():
        return {"data":"pong"}
    
    services=Services
    # services.user_service=UserService(user_model,app.config)
    user_router(app,services)
    
    return app



app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=app.conf.app_port, reload=app.conf.proj_reload)

    
    
