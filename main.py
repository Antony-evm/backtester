"""
Main
"""
import uvicorn

from app import factory, log_config

log_config.setup_logging()
app = factory.create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, workers=1)
