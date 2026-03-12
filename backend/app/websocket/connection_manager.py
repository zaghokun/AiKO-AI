"""
WebSocket Connection Manager
Handles multiple WebSocket connections, authentication, and message broadcasting
"""

from typing import Dict, Optional
from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime
import json
import asyncio


class ConnectionManager:
    """Manage WebSocket connections"""
    
    def __init__(self):
        # Active connections: {user_id: WebSocket}
        self.active_connections: Dict[str, WebSocket] = {}
        # User info: {user_id: {username, connected_at}}
        self.user_info: Dict[str, dict] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str, username: str):
        """
        Accept and register a new WebSocket connection
        
        Args:
            websocket: WebSocket connection
            user_id: User ID
            username: Username
        """
        # Accept the connection first
        await websocket.accept()
        
        # Disconnect existing connection for same user (if any)
        if user_id in self.active_connections:
            try:
                await self.disconnect(user_id)
            except:
                pass
        
        # Register connection
        self.active_connections[user_id] = websocket
        self.user_info[user_id] = {
            "username": username,
            "connected_at": datetime.now().isoformat()
        }
        
        print(f"✅ WebSocket connected: {username} (user_id: {user_id})")
        
        # Send welcome message (with error handling)
        try:
            await websocket.send_json({
                "type": "system",
                "content": f"Connected as {username}",
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            print(f"Failed to send welcome message to {username}: {e}")
    
    async def disconnect(self, user_id: str):
        """
        Disconnect and remove a WebSocket connection
        
        Args:
            user_id: User ID to disconnect
        """
        username = None
        
        if user_id in self.user_info:
            username = self.user_info[user_id]["username"]
            del self.user_info[user_id]
        
        if user_id in self.active_connections:
            websocket = self.active_connections[user_id]
            try:
                # Only try to close if still connected
                if websocket.client_state.value == 1:
                    await websocket.close()
            except:
                pass
            
            del self.active_connections[user_id]
            
            if username:
                print(f"❌ WebSocket disconnected: {username} (user_id: {user_id})")
    
    async def send_personal_message(self, message: dict, user_id: str):
        """
        Send a message to a specific user
        
        Args:
            message: Message dictionary
            user_id: Target user ID
        """
        if user_id not in self.active_connections:
            return
        
        websocket = self.active_connections[user_id]
        try:
            # Check if connection is still open
            if websocket.client_state.value == 1:  # WebSocketState.CONNECTED
                await websocket.send_json(message)
        except WebSocketDisconnect:
            await self.disconnect(user_id)
        except RuntimeError as e:
            if "WebSocket is not connected" in str(e):
                await self.disconnect(user_id)
            else:
                print(f"WebSocket error for {self.user_info.get(user_id, {}).get('username', user_id)}: {e}")
        except Exception as e:
            print(f"Error sending message to {user_id}: {e}")
            await self.disconnect(user_id)
    
    async def send_text_chunk(self, chunk: str, user_id: str):
        """
        Send a text chunk (for streaming responses)
        
        Args:
            chunk: Text chunk
            user_id: Target user ID
        """
        if user_id not in self.active_connections:
            return
        
        websocket = self.active_connections[user_id]
        try:
            # Check if connection is still open
            if websocket.client_state.value == 1:  # WebSocketState.CONNECTED
                await websocket.send_text(chunk)
        except WebSocketDisconnect:
            await self.disconnect(user_id)
        except RuntimeError as e:
            if "WebSocket is not connected" in str(e):
                await self.disconnect(user_id)
        except Exception as e:
            print(f"Error sending chunk to {user_id}: {e}")
            await self.disconnect(user_id)
    
    async def send_typing_indicator(self, user_id: str, is_typing: bool):
        """
        Send typing indicator
        
        Args:
            user_id: Target user ID
            is_typing: Whether Aiko is typing
        """
        await self.send_personal_message({
            "type": "typing",
            "is_typing": is_typing,
            "timestamp": datetime.now().isoformat()
        }, user_id)
    
    async def send_error(self, error_message: str, user_id: str):
        """
        Send error message
        
        Args:
            error_message: Error message
            user_id: Target user ID
        """
        await self.send_personal_message({
            "type": "error",
            "content": error_message,
            "timestamp": datetime.now().isoformat()
        }, user_id)
    
    def get_active_users(self) -> list:
        """Get list of active users"""
        return [
            {
                "user_id": user_id,
                "username": info["username"],
                "connected_at": info["connected_at"]
            }
            for user_id, info in self.user_info.items()
        ]
    
    def is_connected(self, user_id: str) -> bool:
        """Check if user is connected"""
        return user_id in self.active_connections
    
    async def broadcast(self, message: dict):
        """
        Broadcast message to all connected users
        
        Args:
            message: Message dictionary
        """
        disconnected_users = []
        
        for user_id in list(self.active_connections.keys()):
            try:
                await self.send_personal_message(message, user_id)
            except:
                disconnected_users.append(user_id)
        
        # Clean up disconnected users
        for user_id in disconnected_users:
            await self.disconnect(user_id)


# Global connection manager instance
manager = ConnectionManager()
