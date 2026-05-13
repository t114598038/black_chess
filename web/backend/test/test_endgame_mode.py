import pytest
from services.game_engine import GameEngine

def test_initialize_endgame_layout():
    engine = GameEngine()
    engine.initialize_endgame()
    board = engine.checkerboard_display
    
    # 1. Verify dimensions
    assert len(board) == 4
    assert len(board[0]) == 8
    
    # 2. Verify middle columns are empty
    for r in range(4):
        assert board[r][3] == 'Null'
        assert board[r][4] == 'Null'
        
    # 3. Count pieces on Red side (Cols 0, 1, 2)
    red_count = 0
    red_piece_types = {}
    for r in range(4):
        for c in range(3):
            piece = board[r][c]
            if piece != 'Null':
                assert piece.startswith('Red_')
                red_count += 1
                p_type = piece.split('_')[1]
                red_piece_types[p_type] = red_piece_types.get(p_type, 0) + 1
                
    assert red_count == 8
    assert red_piece_types['King'] == 1
    assert red_piece_types['Guard'] == 1
    assert red_piece_types['Elephant'] == 1
    assert red_piece_types['Car'] == 1
    assert red_piece_types['Horse'] == 1
    assert red_piece_types['Cannon'] == 1
    assert red_piece_types['Soldier'] == 2
    
    # 4. Count pieces on Black side (Cols 5, 6, 7)
    black_count = 0
    black_piece_types = {}
    for r in range(4):
        for c in range(5, 8):
            piece = board[r][c]
            if piece != 'Null':
                assert piece.startswith('Black_')
                black_count += 1
                p_type = piece.split('_')[1]
                black_piece_types[p_type] = black_piece_types.get(p_type, 0) + 1
                
    assert black_count == 8
    assert black_piece_types['King'] == 1
    assert black_piece_types['Guard'] == 1
    assert black_piece_types['Elephant'] == 1
    assert black_piece_types['Car'] == 1
    assert black_piece_types['Horse'] == 1
    assert black_piece_types['Cannon'] == 1
    assert black_piece_types['Soldier'] == 2

def test_endgame_turn_and_colors():
    engine = GameEngine()
    engine.initialize_endgame()
    
    # Black (Player B) should move first
    assert engine.current_turn == 'B'
    assert engine.color_table['B'] == 'Black'
    assert engine.color_table['A'] == 'Red'

def test_endgame_no_flipping():
    engine = GameEngine()
    engine.initialize_endgame()
    board = engine.checkerboard_display
    
    # All pieces should be revealed, no 'Covered' pieces
    for r in range(4):
        for c in range(8):
            assert board[r][c] != 'Covered'
