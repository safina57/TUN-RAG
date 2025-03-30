import uvicorn
from src.agent import chat
from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
        except Exception:
            break  # Disconnect if there's an error or client disconnects
        response = chat(data)
        # Send only the answer text back
        print(f"Received question: {data}")
        print(f"Sending answer: {response['result']}")
        await websocket.send_text(response['result'])

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
