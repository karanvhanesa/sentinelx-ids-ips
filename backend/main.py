import random
import asyncio
from datetime import datetime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uvicorn

DATABASE_URL = "sqlite:///./sentinelx.db"
engine   = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Session_ = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base     = declarative_base()

class AlertDB(Base):
    __tablename__ = "alerts"
    id          = Column(Integer, primary_key=True, index=True)
    timestamp   = Column(DateTime, default=datetime.utcnow)
    src_ip      = Column(String)
    attack_type = Column(String)
    severity    = Column(String)
    ai_score    = Column(Float)
    blocked     = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SentinelX API", version="2.4.1")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ATTACKS = ["Port Scan","SSH Brute Force","SYN Flood","ICMP Flood","SQL Injection","DNS Tunneling"]
SEVS    = ["CRITICAL","HIGH","MEDIUM","LOW"]

def rand_ip():
    return f"{random.randint(1,254)}.{random.randint(0,254)}.{random.randint(0,254)}.{random.randint(1,254)}"

class Manager:
    def __init__(self): self.active = []
    async def connect(self, ws):
        await ws.accept()
        self.active.append(ws)
    def disconnect(self, ws):
        if ws in self.active: self.active.remove(ws)

manager = Manager()

@app.get("/")
def root():
    return {"message": "SentinelX Running", "author": "SentinelX Platform"}

@app.get("/system/health")
def health():
    return {"status": "healthy", "version": "2.4.1", "time": str(datetime.utcnow())}

@app.get("/dashboard/stats")
def stats():
    db = Session_()
    total    = db.query(AlertDB).count()
    critical = db.query(AlertDB).filter(AlertDB.severity=="CRITICAL").count()
    blocked  = db.query(AlertDB).filter(AlertDB.blocked==True).count()
    db.close()
    return {
        "total_alerts": total,
        "critical":     critical,
        "blocked_ips":  blocked,
        "ai_accuracy":  97,
    }

@app.get("/alerts")
def get_alerts():
    db   = Session_()
    rows = db.query(AlertDB).order_by(AlertDB.timestamp.desc()).limit(50).all()
    db.close()
    return [
        {
            "id":          r.id,
            "time":        r.timestamp.strftime("%H:%M:%S"),
            "timestamp":   str(r.timestamp),
            "src_ip":      r.src_ip,
            "attack_type": r.attack_type,
            "severity":    r.severity,
            "ai_score":    r.ai_score,
            "blocked":     r.blocked,
        }
        for r in rows
    ]

@app.post("/alerts")
def create_alert(
    src_ip:      str,
    attack_type: str,
    severity:    str,
    ai_score:    float,
    blocked:     bool = False,
):
    db = Session_()
    alert = AlertDB(
        src_ip      = src_ip,
        attack_type = attack_type,
        severity    = severity,
        ai_score    = ai_score,
        blocked     = blocked,
    )
    db.add(alert)
    db.commit()
    db.close()
    return {
        "message":     "Alert saved successfully",
        "src_ip":      src_ip,
        "attack_type": attack_type,
        "severity":    severity,
        "ai_score":    ai_score,
        "blocked":     blocked,
    }

@app.delete("/alerts/clear")
def clear_alerts():
    db = Session_()
    db.query(AlertDB).delete()
    db.commit()
    db.close()
    return {"message": "All alerts cleared"}

@app.websocket("/ws/live")
async def ws_live(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            await asyncio.sleep(random.uniform(1,3))
            alert = {
                "type":        "alert",
                "timestamp":   datetime.utcnow().isoformat(),
                "src_ip":      rand_ip(),
                "attack_type": random.choice(ATTACKS),
                "severity":    random.choice(SEVS),
                "ai_score":    round(random.uniform(40,99),1),
                "blocked":     random.random() > 0.4,
            }
            db = Session_()
            db.add(AlertDB(
                src_ip      = alert["src_ip"],
                attack_type = alert["attack_type"],
                severity    = alert["severity"],
                ai_score    = alert["ai_score"],
                blocked     = alert["blocked"],
            ))
            db.commit()
            db.close()
            await ws.send_json(alert)
    except WebSocketDisconnect:
        manager.disconnect(ws)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
