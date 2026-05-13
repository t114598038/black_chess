# PBI-002 SocketIO & TCP Networking

## Status
Done

## Description
Develop a dual-server architecture to support both web and native clients:
- **Socket.IO Server**: Handles real-time communication for Vue 3 frontend.
- **TCP Server**: Provides a raw socket interface for C clients or external AI programs.
- **Room Management**: Support creating, joining, and spectating rooms.
- **State Synchronization**: Ensure board state is consistent across all connected clients (Web and TCP).
