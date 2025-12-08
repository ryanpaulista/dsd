from typing import List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.activate_connections: List[WebSocket] = [] 

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.activate_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.activate_connections.remove(websocket)
    
    async def broadcast(self, message: str):
        for connection in self.activate_connections:
            try:
                await connection.send_text(message)
            except:
                self.disconnect(connection)

manager = ConnectionManager()