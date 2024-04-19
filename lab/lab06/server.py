import asyncio
import websockets

class DanmakuServer:
    def __init__(self):
        self.clients = set()  # Store connected clients

    async def register(self, websocket):
        # Register a new client
        self.clients.add(websocket)

    async def unregister(self, websocket):
        # Unregister a client
        self.clients.remove(websocket)

    async def broadcast(self, message):
        # Send a message to all connected clients
        if self.clients:
            await asyncio.wait([client.send(message) for client in self.clients])

    async def reply(self, websocket, path):
        await self.register(websocket)
        try:
            async for message in websocket:
                await self.broadcast(message)
        except websockets.ConnectionClosed:
            pass
        finally:
            await self.unregister(websocket)

if __name__ == "__main__":
    server = DanmakuServer()
    start_server = websockets.serve(server.reply, 'localhost', 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
