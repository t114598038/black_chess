# PBI-003 AI Opponent Integration

## Status
Done

## Description
Integrate an AI player to allow Solo Play (PvE):
- Core move generator implemented in C for performance.
- Python bridge (`auto_ai.py`) to compile and call the C generator.
- Fallback logic to handle cases where the AI cannot find a move (e.g., flipping a random covered piece).
- Automated AI turns triggered by game state changes.
