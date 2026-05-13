# PBI-013 Room Lifecycle & Reusability Improvements

**Status:** Done

## Goal
Ensure that room IDs can be reused immediately after a match ends and that clicking "End Match" (結束對戰) correctly terminates the room session for all participants, allowing the room to be created again from scratch.

## Implementation Plan
- [x] Modify `RoomManager.leave_room` to delete the room immediately if the **creator** leaves or ends the match, ensuring the ID is freed.
- [x] Update `RoomManager.create_room` to allow creating a room with an existing room ID if its state is `finished`.
- [x] Update the "End Match" (結束對戰) button logic to ensure it thoroughly cleans up the backend state.

## Design Breakdown
- **Creator Dominance**: In this architecture, the creator is the "owner" of the room. If they leave or end the match, the room should be considered closed for everyone and deleted from the manager.
- **Room Recreation**: When a room is recreated via `create_room` with a previously used ID, it should initialize as a completely fresh room.

## Acceptance Criteria
- [x] **ID Reusability**: After a game ends (or the creator leaves), the same room ID can be used to create a new room without the "Room already exists" error.
- [x] **Aggressive Cleanup**: When the creator clicks "End Match" or leaves, the backend room object is deleted, and AI tasks are cancelled.

## Subtasks
- [x] **Backend**: Update `RoomManager.leave_room` to delete room if `sid == creator_sid`.
- [x] **Backend**: Update `RoomManager.create_room` to support overriding/recreating `finished` rooms.
- [x] **Backend**: Update `end_match` event to ensure the room is deleted.
