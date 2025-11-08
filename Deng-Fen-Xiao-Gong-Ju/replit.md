# Overview

This is a Streamlit-based web application for managing a dictionary of predefined numeric keys and their associated values. The application provides a simple interface for users to map specific numbers (from a fixed set of valid keys) to integer values. Data is persisted to a JSON file (`numbers_dict.json`) and automatically cleared on application startup.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture

**Framework**: Streamlit
- Single-page web application built with Streamlit
- Uses Streamlit's session state for managing application state between reruns
- Main application logic resides in `app.py`

**State Management**:
- Session state (`st.session_state`) stores the numbers dictionary and startup messages
- Dictionary is initialized on first load and persists throughout the session
- Auto-clear mechanism resets all values to `None` on application startup

## Data Storage

**File-Based Persistence**:
- Uses local JSON file (`numbers_dict.json`) for data persistence
- No database required - simple file I/O operations
- Data structure: Dictionary with integer keys (stored as strings in JSON) mapping to integer values or `None`

**Data Model**:
- Fixed set of 54 valid keys (non-sequential integers between 1-64)
- Values can be integers or `None`
- JSON serialization handles conversion between integer keys and string keys for storage

## Application Logic

**Initialization Strategy**:
- Application automatically clears all stored values on startup
- Ensures clean state for each new session
- All valid keys are initialized to `None` by default

**Key Constraints**:
- Only predefined keys from `VALID_KEYS` list are allowed
- Keys are: 1, 2, 5, 8, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 23, 24, 25, 26, 27, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 40, 41, 42, 43, 44, 45, 46, 47, 49, 50, 51, 52, 53, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64
- Missing keys from 1-64 sequence: 3, 4, 6, 7, 9, 16, 21, 22, 29, 39, 48, 54

**Error Handling**:
- Try-except blocks protect file operations
- Graceful fallback to empty/initialized dictionary on load failures
- Boolean return values indicate success/failure of save operations

# External Dependencies

## Python Libraries

**Streamlit**: Web application framework
- Primary UI framework for the application
- Provides session state management and interactive widgets

**pyperclip**: Clipboard operations
- Imported but functionality not yet implemented in current codebase
- Likely intended for copy-to-clipboard features

**Standard Library**:
- `json`: JSON serialization/deserialization for file persistence
- `os`: File system operations (checking file existence)

## File System

**Local Storage**:
- `numbers_dict.json`: Primary data storage file
- UTF-8 encoding for file operations
- No external database or cloud storage dependencies