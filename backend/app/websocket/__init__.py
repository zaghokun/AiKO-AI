"""
WebSocket module for real-time chat
"""

from .connection_manager import manager, ConnectionManager
from .chat import websocket_endpoint, authenticate_websocket

__all__ = [
    "manager",
    "ConnectionManager",
    "websocket_endpoint",
    "authenticate_websocket"
]
