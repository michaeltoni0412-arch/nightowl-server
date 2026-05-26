import asyncio
import websockets
import json

controller = None
client = None

async def handle_connection(websocket, path):
    global controller, client
    try:
        hello = await websocket.recv()
        data = json.loads(hello)
        role = data.get("role")

        if role == "client":
            client = websocket
            if controller:
                await controller.send(json.dumps({"type": "client_connected"}))
            try:
                async for message in websocket:
                    if controller:
                        await controller.send(message)
            except:
                client = None
                if controller:
                    await controller.send(json.dumps({"type": "client_disconnected"}))

        elif role == "controller":
            controller = websocket
            if client:
                await controller.send(json.dumps({"type": "client_connected"}))
            try:
                async for message in websocket:
                    if client:
                        await client.send(message)
            except:
                controller = None
    except Exception as e:
        print(f"Error: {e}")

async def main():
    async with websockets.serve(handle_connection, "0.0.0.0", 8765):
        print("NightOwl Server Running!")
        await asyncio.Future()

asyncio.run(main())
