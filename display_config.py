"""
Configuration settings for the display system.
Easily adjust display behavior for different use cases.
"""

class DisplayConfig:
    """Configuration class for display settings."""
    
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
    
    @classmethod
    def get_display_settings(cls):
        """Get display settings as a dictionary."""
        return {
            'clear_screen': cls.CLEAR_SCREEN,
            'delay': cls.DELAY_BETWEEN_MOVES,
            'show_move_info': cls.SHOW_MOVE_INFO,
            'show_game_info': cls.SHOW_GAME_INFO,
            'show_available_positions': cls.SHOW_AVAILABLE_POSITIONS,
            'use_emojis': cls.USE_EMOJIS,
            'show_row_col_numbers': cls.SHOW_ROW_COL_NUMBERS,
            'border_style': cls.BORDER_STYLE,
            'show_training_progress': cls.SHOW_TRAINING_PROGRESS,
            'progress_update_frequency': cls.PROGRESS_UPDATE_FREQUENCY,
            'minimal_mode': cls.MINIMAL_MODE,
            'pause_for_user_input': cls.PAUSE_FOR_USER_INPUT
        }
    
    @classmethod
    def set_training_mode(cls, episodes=1000):
        """Configure for training mode with many episodes."""
        cls.CLEAR_SCREEN = False
        cls.DELAY_BETWEEN_MOVES = 0.0
        cls.SHOW_MOVE_INFO = False
        cls.SHOW_GAME_INFO = False
        cls.SHOW_AVAILABLE_POSITIONS = False
        cls.SHOW_TRAINING_PROGRESS = True
        cls.PROGRESS_UPDATE_FREQUENCY = max(1, episodes // 20)  # Show progress 20 times
        cls.MINIMAL_MODE = True
    
    @classmethod
    def set_demo_mode(cls):
        """Configure for demonstration mode."""
        cls.CLEAR_SCREEN = True
        cls.DELAY_BETWEEN_MOVES = 1.0
        cls.SHOW_MOVE_INFO = True
        cls.SHOW_GAME_INFO = True
        cls.SHOW_AVAILABLE_POSITIONS = True
        cls.SHOW_TRAINING_PROGRESS = True
        cls.PROGRESS_UPDATE_FREQUENCY = 1
        cls.MINIMAL_MODE = False
        cls.PAUSE_FOR_USER_INPUT = True
    
    @classmethod
    def set_debug_mode(cls):
        """Configure for debugging mode."""
        cls.CLEAR_SCREEN = True
        cls.DELAY_BETWEEN_MOVES = 0.0
        cls.SHOW_MOVE_INFO = True
        cls.SHOW_GAME_INFO = True
        cls.SHOW_AVAILABLE_POSITIONS = True
        cls.SHOW_TRAINING_PROGRESS = False
        cls.MINIMAL_MODE = False
        cls.PAUSE_FOR_USER_INPUT = False

# Predefined configurations
TRAINING_CONFIG = {
    'clear_screen': False,
    'delay': 0.0,
    'show_move_info': False,
    'show_game_info': False,
    'show_available_positions': False,
    'minimal_mode': True
}

DEMO_CONFIG = {
    'clear_screen': True,
    'delay': 1.0,
    'show_move_info': True,
    'show_game_info': True,
    'show_available_positions': True,
    'minimal_mode': False
}

DEBUG_CONFIG = {
    'clear_screen': True,
    'delay': 0.0,
    'show_move_info': True,
    'show_game_info': True,
    'show_available_positions': True,
    'minimal_mode': False
}
