"""
Main
"""
import uvicorn

from app import factory, get_port, get_reload, get_workers, log_config

log_config.setup_logging()
app = factory.create_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=get_port(),
        reload=get_reload(),
        workers=get_workers()
    )
