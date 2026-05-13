# PBI-012 Endgame Mode (殘局模式)

**Status:** Done

## Goal
Provide a specialized game mode where players start with a revealed, symmetrical board layout instead of the standard hidden initialization, allowing for tactical practice and faster-paced matches.

## Implementation Plan
- [x] Extend the `GameEngine` to support a new `initialization_type`.
- [x] Implement a symmetrical piece placement algorithm (Left 3 columns vs Right 3 columns).
- [x] Modify the turn-handling logic to bypass the "first flip decides color" rule, as colors are pre-assigned.
- [x] Update the Frontend UI to allow mode selection before the game starts.
- [x] Integrate the mode selection into the Socket.IO communication flow.

## Design Breakdown
- **Piece Composition**: Fixed set of 8 pieces per side (1 King, 1 Guard, 1 Elephant, 1 Car, 1 Horse, 1 Cannon, 2 Soldiers).
- **Spatial Constraints**:
    - Red pieces: Columns [0, 1, 2], Rows [0, 1, 2, 3] (Total 12 slots for 8 pieces).
    - Black pieces: Columns [5, 6, 7], Rows [0, 1, 2, 3] (Total 12 slots for 8 pieces).
    - Empty Neutral Zone: Columns [3, 4] must be `Null`.
- **Pre-Revealed State**: All pieces must be in their "Revealed" state (e.g., `Red_King` instead of `Covered`) from move zero.
- **Pre-Defined Turn**: Black is hardcoded to move first in this mode.
- **Color Mapping**: Player A and Player B must be mapped to Red/Black immediately upon game start based on the mode settings.

## Acceptance Criteria
- [x] **Symmetrical Layout**: Verification script/test confirms pieces are restricted to side-specific columns and middle columns are empty.
- [x] **Revealed Initialization**: The `checkerboard_display` returns revealed piece names (not "Covered") at the start.
- [x] **Fixed Turn Order**: The game engine initializes `current_turn` to the Black player.
- [x] **UI Integration**: A toggle switch exists in `gameControls.vue` and its state is correctly sent to the backend.
- [x] **AI Support**: The AI player (`auto_ai.py`) can calculate moves correctly from a fully revealed board state.

## Subtasks
- [x] **Backend**: Add `initialize_endgame()` to `game_engine.py`.
- [x] **Backend**: Add `mode` parameter to `start_game` event in `socket_server.py`.
- [x] **Frontend**: Implement Mode Toggle UI in `gameControls.vue`.
- [x] **Frontend**: Pass `game_mode` in `socketService.ts`.
- [x] **Test**: Write a unit test to verify the 8-piece distribution and empty middle zone.
