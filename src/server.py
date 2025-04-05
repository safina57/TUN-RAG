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
            break  
        response = chat(data)
        # Send only the answer text back
        print(f"Received question: {data}")
        print(f"Sending answer: {response['result']}")
        for doc in response['source_documents']:
            print(f"Source Document: {doc.metadata['source']}")
            print(f"Content: {doc.page_content[:500]}")
            print("-" * 80)
        # Send the response back to the client
        await websocket.send_text(response['result'])

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
