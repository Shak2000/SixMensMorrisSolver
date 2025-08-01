# Six Men's Morris Game

A complete implementation of the Six Men's Morris (also known as Nine Men's Morris) game with both console and web interfaces.

## Features

- **Console Interface**: Full-featured command-line game with AI opponent
- **Web Interface**: Modern web UI with real-time game state
- **AI Opponent**: Intelligent computer player using minimax algorithm with alpha-beta pruning
- **Game Rules**: Complete implementation of Six Men's Morris rules including:
  - Placement phase (first 12 pieces)
  - Movement phase
  - Mill formation and piece removal
  - Flying rule (when only 3 pieces remain)
  - Win conditions

## How to Play

### Console Version

Run the console version:
```bash
python main.py
```

**Game Controls:**
- **1**: Take an action (place/move pieces)
- **2**: Let computer play
- **3**: Undo last move
- **4**: Restart game
- **5**: Quit

### Web Version

Start the web server:
```bash
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Then open your browser to `http://localhost:8000`

**Web Interface Features:**
- Click on valid positions to place pieces during placement phase
- Click on your pieces then click destination during movement phase
- Use "Computer Move" button to let AI play
- Adjust AI depth for different difficulty levels
- Real-time game state updates

## Game Rules

1. **Placement Phase**: Players take turns placing their 6 pieces on valid board positions
2. **Movement Phase**: Players move their pieces along the lines to adjacent positions
3. **Mills**: Forming 3 pieces in a row allows you to remove an opponent's piece
4. **Flying**: When you have only 3 pieces left, you can move to any position
5. **Winning**: Reduce opponent to 2 pieces or block all their moves

## Technical Details

### Architecture
- **Backend**: Python with FastAPI for web endpoints
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **AI**: Minimax algorithm with alpha-beta pruning
- **Game Logic**: Pure Python implementation

### Files Structure
```
SixMensMorris/
├── main.py          # Console game and core game logic
├── app.py           # FastAPI web server
├── index.html       # Web UI HTML
├── styles.css       # Web UI styling
├── script.js        # Web UI JavaScript
└── README.md        # This file
```

### API Endpoints

The web interface communicates with the Python backend through these endpoints:

- `POST /start` - Start a new game
- `POST /place` - Place a piece
- `POST /move` - Move a piece
- `POST /remove_piece` - Remove opponent's piece
- `POST /switch` - Switch current player
- `POST /undo` - Undo last move
- `POST /computer_move` - Make computer move
- `GET /get_board` - Get current board state
- `GET /get_current_player` - Get current player
- `GET /check_win` - Check if game is won
- `GET /check_mill` - Check if position forms a mill

## Development

The game logic is centralized in the `Game` class in `main.py`. Both the console and web interfaces use the same game logic, ensuring consistency across platforms.

### Adding Features

To add new features:
1. Implement the logic in the `Game` class in `main.py`
2. Add corresponding endpoints in `app.py` if needed for web interface
3. Update the web UI in `script.js` if needed

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn (for web server)

Install dependencies:
```bash
pip install fastapi uvicorn
```

## License

This project is proprietary software. All rights reserved under copyright.
