from core.setup_app import init_app

APP = init_app()

# uvicorn main:APP --workers 4 --port 8000 --host 0.0.0.0 --reload --loop uvloop
