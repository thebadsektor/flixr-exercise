import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "backend.app:app",  # Make sure this points to your FastAPI app instance
        host="0.0.0.0",
        port=8081,
        log_level="info",
        reload=True)
    # uvicorn.run("app.app:app", host="0.0.0.0", port=8081, log_level="info", reload=True)
