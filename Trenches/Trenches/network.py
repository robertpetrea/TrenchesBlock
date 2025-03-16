import socket
import json
import threading
from typing import Set, Dict, Any
import requests

class P2PNode:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.peers: Set[str] = set()
        self.blockchain = None  # Will be set by main application
        
    def start(self):
        """Start P2P server"""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(5)
        
        # Start listener thread
        threading.Thread(target=self._listen_for_peers, args=(server,)).start()
        
    def _listen_for_peers(self, server: socket.socket):
        """Listen for incoming peer connections"""
        while True:
            client, address = server.accept()
            threading.Thread(target=self._handle_peer, args=(client,)).start()
            
    def _handle_peer(self, client: socket.socket):
        """Handle peer connection"""
        try:
            while True:
                message = client.recv(4096)
                if message:
                    self._process_message(json.loads(message.decode()))
        except:
            client.close()
            
    def broadcast_transaction(self, transaction: Dict[str, Any]):
        """Broadcast transaction to all peers"""
        message = {
            "type": "transaction",
            "data": transaction
        }
        self._broadcast(message)
        
    def broadcast_block(self, block: Dict[str, Any]):
        """Broadcast new block to all peers"""
        message = {
            "type": "block",
            "data": block
        }
        self._broadcast(message)
        
    def _broadcast(self, message: Dict[str, Any]):
        """Send message to all peers"""
        for peer in self.peers:
            try:
                requests.post(f"http://{peer}/message", json=message)
            except:
                self.peers.remove(peer) 