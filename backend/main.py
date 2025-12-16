import json
import logging
from datetime import datetime
from typing import List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("IoT-Backend")

# --- Database Setup ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./readings.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ReadingDB(Base):
    __tablename__ = "readings"
    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float)
    humidity = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# --- Pydantic Models ---
class ReadingSchema(BaseModel):
    temperature: float
    humidity: float

class ReadingResponse(ReadingSchema):
    id: int
    timestamp: datetime
    class Config:
        from_attributes = True

# --- WebSocket Manager ---
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"✅ CLIENT CONNECTED! Active: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info("❌ Client disconnected")

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                self.disconnect(connection)

manager = ConnectionManager()
app = FastAPI()

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Routes ---

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Server is running on Port 8000"}

@app.post("/api/readings", response_model=ReadingResponse)
async def create_reading(reading: ReadingSchema, db: Session = Depends(get_db)):
    db_reading = ReadingDB(temperature=reading.temperature, humidity=reading.humidity)
    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)
    
    ws_data = json.dumps({
        "temperature": db_reading.temperature,
        "humidity": db_reading.humidity,
        "timestamp": db_reading.timestamp.isoformat()
    })
    
    await manager.broadcast(ws_data)
    return db_reading

@app.get("/api/readings", response_model=List[ReadingResponse])
def get_readings(limit: int = 50, db: Session = Depends(get_db)):
    readings = db.query(ReadingDB).order_by(ReadingDB.timestamp.desc()).limit(limit).all()
    return readings[::-1]

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)