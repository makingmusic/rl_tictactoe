# =============================================================================
# All config lives here
# =============================================================================

# Board size for tic-tac-toe (default: 3x3)
TIC_TAC_TOE_SIZE = 3

# Player symbols
PLAYER_X = "X"
PLAYER_O = "O"
EMPTY_CELL = "_"
CELL_DELIMITER = " "

# Game outcome constants
GAME_WINNER_DRAW = "DRAW"
GAME_WINNER_NONE = "NOBODY WON"

# =============================================================================
# DISPLAY CONFIGURATION
# =============================================================================

# Basic display settings
CLEAR_SCREEN = True
DELAY_BETWEEN_MOVES = 0.5  # seconds
SHOW_MOVE_INFO = True
SHOW_GAME_INFO = True
SHOW_AVAILABLE_POSITIONS = True

# Visual settings
USE_EMOJIS = True
SHOW_ROW_COL_NUMBERS = True
BORDER_STYLE = "="  # Character for borders

# Training visualization settings
SHOW_TRAINING_PROGRESS = True
PROGRESS_UPDATE_FREQUENCY = 1  # Show progress every N episodes

# Performance settings
MINIMAL_MODE = False  # Set to True for maximum performance
PAUSE_FOR_USER_INPUT = False  # Set to True to pause between games


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================


def get_display_settings():
    """Get current display settings as a dictionary."""
    return {
        "clear_screen": CLEAR_SCREEN,
        "delay": DELAY_BETWEEN_MOVES,
        "show_move_info": SHOW_MOVE_INFO,
        "show_game_info": SHOW_GAME_INFO,
        "show_available_positions": SHOW_AVAILABLE_POSITIONS,
        "use_emojis": USE_EMOJIS,
        "show_row_col_numbers": SHOW_ROW_COL_NUMBERS,
        "border_style": BORDER_STYLE,
        "show_training_progress": SHOW_TRAINING_PROGRESS,
        "progress_update_frequency": PROGRESS_UPDATE_FREQUENCY,
        "minimal_mode": MINIMAL_MODE,
        "pause_for_user_input": PAUSE_FOR_USER_INPUT,
    }
