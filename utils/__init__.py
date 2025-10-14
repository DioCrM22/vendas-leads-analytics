"""
Utils package for Streamlit dashboard application.
Contains core functionality and module-specific utilities.
"""

from .core.session_manager import SessionManager
from .core.validation import DataValidator
from .components import UIComponents  # ✅ CORRETO
from .import_helpers import (
    get_session_df, 
    save_to_session, 
    clear_session_data,
    get_session_value,
    set_session_value,
    initialize_session_defaults
)

__all__ = [
    'SessionManager', 
    'DataValidator', 
    'UIComponents',
    'get_session_df',
    'save_to_session', 
    'clear_session_data',
    'get_session_value',
    'set_session_value',
    'initialize_session_defaults'
]