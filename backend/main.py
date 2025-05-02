# 🔄 Import necessary modules and dependencies
from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes import auth, upload, video
from fastapi.middleware.cors import CORSMiddleware
from db.base import Base
from db.db import get_engine, dispose_engine


# ⚙️ Configure application lifecycle management
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🚀 Startup: Create engine and tables if needed
    engine = get_engine()
    Base.metadata.create_all(engine)

    yield  # 🏃 Application runs while this yield is active

    # 🔌 Shutdown: Dispose engine and close connections
    dispose_engine()

# 📱 Initialize FastAPI application
app = FastAPI(lifespan=lifespan)

# 🌐 Configure CORS origins
origins = ["http://localhost", "http://localhost:3000"]

# 🔒 Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🛣️ Include authentication routes
app.include_router(auth.router, prefix="/auth")
app.include_router(upload.router, prefix="/upload/video")
app.include_router(video.router, prefix="/video")


# 🏠 Root endpoint
@app.get("/")
def root():
    return "hello world"
