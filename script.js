class SixMensMorrisUI {
    constructor() {
        this.selectedPosition = null;
        this.gameState = {
            currentPlayer: 'W',
            phase: 'placement',
            whiteCount: 0,
            blackCount: 0,
            whiteRemoved: 0,
            blackRemoved: 0,
            placed: 0,
            gameActive: false
        };
        this.boardPositions = [];
        this.validPositions = [
            [0, 0], [2, 0], [4, 0],
            [1, 1], [2, 1], [3, 1],
            [0, 2], [1, 2], [3, 2], [4, 2],
            [1, 3], [2, 3], [3, 3],
            [0, 4], [2, 4], [4, 4]
        ];
        
        this.init();
    }

    async init() {
        this.setupEventListeners();
        this.showWelcomeScreen();
    }

    showWelcomeScreen() {
        // Reset game state
        this.gameState.gameActive = false;
        this.gameState.placed = 0;
        this.gameState.whiteCount = 0;
        this.gameState.blackCount = 0;
        this.gameState.currentPlayer = 'W';
        this.gameState.phase = 'placement';
        
        // Show welcome screen, hide game elements
        document.getElementById('welcome-screen').style.display = 'flex';
        document.getElementById('game-board').style.display = 'none';
        document.getElementById('message-area').style.display = 'none';
        document.getElementById('instructions').style.display = 'none';
        
        // Update button states
        this.updateButtonStates();
    }

    async startNewGame() {
        try {
            await fetch('/start', { method: 'POST' });
            this.gameState.gameActive = true; // Set game as active
            await this.updateGameState();
            this.selectedPosition = null;
            
            // Hide welcome screen and show game
            document.getElementById('welcome-screen').style.display = 'none';
            document.getElementById('game-board').style.display = 'flex';
            document.getElementById('message-area').style.display = 'block';
            document.getElementById('instructions').style.display = 'block';
            
            this.renderBoard();
            this.updateBoardDisplay();
            this.updateButtonStates();
            this.showMessage('New game started! White goes first.', 'success');
        } catch (error) {
            this.showMessage('Error starting game: ' + error.message, 'error');
        }
    }

    async restartGame() {
        try {
            await fetch('/start', { method: 'POST' });
            this.gameState.gameActive = true;
            await this.updateGameState();
            this.selectedPosition = null;
            
            // Re-render the board completely
            this.renderBoard();
            this.updateBoardDisplay();
            this.updateButtonStates();
            this.showMessage('Game restarted!', 'success');
        } catch (error) {
            this.showMessage('Error restarting game: ' + error.message, 'error');
        }
    }

    async updateGameState() {
        try {
            // Get current player and piece counts
            const [whiteCount, blackCount, whiteRemoved, blackRemoved, currentPlayer, placedCount, gameActive] = await Promise.all([
                this.getPieceCount('W'),
                this.getPieceCount('B'),
                this.getRemovedCount('W'),
                this.getRemovedCount('B'),
                this.getCurrentPlayer(),
                this.getPlacedCount(),
                this.getGameActive()
            ]);
            
            this.gameState.whiteCount = whiteCount;
            this.gameState.blackCount = blackCount;
            this.gameState.whiteRemoved = whiteRemoved;
            this.gameState.blackRemoved = blackRemoved;
            this.gameState.placed = placedCount;
            this.gameState.currentPlayer = currentPlayer;
            this.gameState.gameActive = gameActive;
            this.gameState.phase = this.gameState.placed < 12 ? 'placement' : 'movement';
            
            // Update UI elements
            document.getElementById('white-count').textContent = whiteCount;
            document.getElementById('black-count').textContent = blackCount;
            document.getElementById('white-removed').textContent = whiteRemoved;
            document.getElementById('black-removed').textContent = blackRemoved;
            document.getElementById('current-player').textContent = 
                `Current Player: ${this.gameState.currentPlayer === 'W' ? 'White' : 'Black'}`;
            document.getElementById('game-phase').textContent = 
                `Phase: ${this.gameState.phase === 'placement' ? 'Placement' : 'Movement'}`;
            
            console.log('Game state updated:', this.gameState);
            
        } catch (error) {
            console.error('Error updating game state:', error);
        }
    }

    setupEventListeners() {
        // Game control buttons
        document.getElementById('start-game').addEventListener('click', () => this.startNewGame());
        document.getElementById('restart-game').addEventListener('click', () => this.restartGame());
        document.getElementById('undo-move').addEventListener('click', () => this.undoMove());
        document.getElementById('computer-move').addEventListener('click', () => this.makeComputerMove());
    }

    renderBoard() {
        const boardGrid = document.querySelector('.board-grid');
        boardGrid.innerHTML = '';
        
        // Clear the board positions array
        this.boardPositions = [];

        // Define the visual structure exactly like in the Game class
        const visualStructure = [
            "*───*───*",
            "|   |   |",
            "| *─*─* |",
            "| |   | |",
            "*─*   *─*",
            "| |   | |",
            "| *─*─* |",
            "|   |   |",
            "*───*───*"
        ];

        // Create the board grid (9x9)
        for (let row = 0; row < 9; row++) {
            for (let col = 0; col < 9; col++) {
                const element = document.createElement('div');
                element.className = 'board-element';
                
                const char = visualStructure[row][col];
                
                if (char === '*') {
                    // This is a node position
                    element.classList.add('node');
                    element.textContent = '';
                    
                    // Map grid position to game coordinates
                    const gameCoords = this.gridToGameCoords(row, col);
                    if (gameCoords) {
                        element.dataset.x = gameCoords[0];
                        element.dataset.y = gameCoords[1];
                        element.addEventListener('click', () => this.handlePositionClick(gameCoords[0], gameCoords[1]));
                        this.boardPositions.push(element);
                    }
                } else if (char === '─') {
                    // Horizontal line
                    element.textContent = '─';
                } else if (char === '|') {
                    // Vertical line
                    element.textContent = '|';
                } else {
                    // Empty space
                    element.textContent = ' ';
                }
                
                boardGrid.appendChild(element);
            }
        }
        
        console.log('Board rendered with', this.boardPositions.length, 'positions');
    }

    gridToGameCoords(gridRow, gridCol) {
        // Map the 9x9 grid positions to game coordinates
        // Based on the visual structure and valid positions
        const nodeMap = {
            '0,0': [0, 0], '0,4': [2, 0], '0,8': [4, 0],
            '2,2': [1, 1], '2,4': [2, 1], '2,6': [3, 1],
            '4,0': [0, 2], '4,2': [1, 2], '4,6': [3, 2], '4,8': [4, 2],
            '6,2': [1, 3], '6,4': [2, 3], '6,6': [3, 3],
            '8,0': [0, 4], '8,4': [2, 4], '8,8': [4, 4]
        };
        
        const key = `${gridRow},${gridCol}`;
        return nodeMap[key] || null;
    }



    async handlePositionClick(x, y) {
        try {
            if (this.gameState.phase === 'placement') {
                await this.handlePlacement(x, y);
            } else {
                await this.handleMovement(x, y);
            }
        } catch (error) {
            this.showMessage('Error: ' + error.message, 'error');
        }
    }

    async handlePlacement(x, y) {
        try {
            const response = await fetch(`/place?x=${x}&y=${y}`, {
                method: 'POST'
            });

            if (response.ok) {
                const success = await response.json();
                if (success) {
                    await this.updateGameState();
                    this.updateBoardDisplay();
                    this.updateButtonStates();
                    
                    // Check for mill formation
                    const millFormed = await this.checkMill(x, y, this.gameState.currentPlayer);
                    if (millFormed) {
                        this.showMessage(`${this.gameState.currentPlayer === 'W' ? 'White' : 'Black'} formed a mill! Remove an opponent's piece.`, 'info');
                        await this.handleMillRemoval(this.gameState.currentPlayer);
                    } else {
                        // Check for win
                        const win = await this.checkWin();
                        if (win) {
                            this.showMessage(`${this.gameState.currentPlayer === 'W' ? 'White' : 'Black'} wins!`, 'success');
                            this.updateBoardDisplay();
                            return;
                        }
                        
                        // Player already switched in backend, just update UI
                        this.updateUI();
                    }
                } else {
                    // Don't show error message for failed placement - might be normal game state
                }
            } else {
                this.showMessage('Invalid placement. Try again.', 'error');
            }
        } catch (error) {
            this.showMessage('Error placing piece: ' + error.message, 'error');
        }
    }

    async handleMovement(x, y) {
        if (this.selectedPosition) {
            // This is a destination click
            const [srcX, srcY] = this.selectedPosition;
            console.log(`Attempting move from (${srcX}, ${srcY}) to (${x}, ${y})`);
            try {
                const response = await fetch(`/move?x=${srcX}&y=${srcY}&nx=${x}&ny=${y}`, {
                    method: 'POST'
                });

                if (response.ok) {
                    const success = await response.json();
                    if (success) {
                        this.clearSelection();
                        await this.updateGameState();
                        this.updateBoardDisplay();
                        this.updateButtonStates();
                        
                        // Check for mill formation
                        const millFormed = await this.checkMill(x, y, this.gameState.currentPlayer);
                        if (millFormed) {
                            this.showMessage(`${this.gameState.currentPlayer === 'W' ? 'White' : 'Black'} formed a mill! Remove an opponent's piece.`, 'info');
                            await this.handleMillRemoval(this.gameState.currentPlayer);
                        } else {
                            // Check for win
                            const win = await this.checkWin();
                            if (win) {
                                this.showMessage(`${this.gameState.currentPlayer === 'W' ? 'White' : 'Black'} wins!`, 'success');
                                this.updateBoardDisplay();
                                return;
                            }
                            
                            // Player already switched in backend, just update UI
                            this.updateUI();
                        }
                    } else {
                        this.showMessage('Invalid move. Try again.', 'error');
                        this.clearSelection();
                    }
                } else {
                    this.showMessage('Invalid move. Try again.', 'error');
                    this.clearSelection();
                }
            } catch (error) {
                this.showMessage('Error making move: ' + error.message, 'error');
                this.clearSelection();
            }
        } else {
            // This is a source click - check if it's the current player's piece
            const position = this.boardPositions.find(p => 
                parseInt(p.dataset.x) === x && parseInt(p.dataset.y) === y
            );
            
            console.log(`Click at (${x}, ${y}), current player: ${this.gameState.currentPlayer}`);
            console.log('Position found:', position);
            if (position) {
                console.log('Position classes:', position.classList.toString());
            }
            
            // Check if the position has a piece and if it belongs to the current player
            if (position && position.classList.contains('white') && this.gameState.currentPlayer === 'W') {
                this.selectedPosition = [x, y];
                this.updateBoardDisplay();
                this.showMessage('Select destination position.', 'info');
            } else if (position && position.classList.contains('black') && this.gameState.currentPlayer === 'B') {
                this.selectedPosition = [x, y];
                this.updateBoardDisplay();
                this.showMessage('Select destination position.', 'info');
            } else {
                this.showMessage('Select one of your pieces to move.', 'error');
            }
        }
    }

    async handleMillRemoval(playerWhoFormedMill) {
        // For simplicity, we'll let the user click on opponent pieces to remove them
        // In a full implementation, you'd want to highlight removable pieces
        this.showMessage('Click on an opponent piece to remove it.', 'info');
        
        // Add temporary event listeners for piece removal
        this.boardPositions.forEach(position => {
            const x = parseInt(position.dataset.x);
            const y = parseInt(position.dataset.y);
            
            // Check if this position has an opponent's piece
            const isOpponentPiece = (playerWhoFormedMill === 'W' && position.classList.contains('black')) ||
                                   (playerWhoFormedMill === 'B' && position.classList.contains('white'));
            
            if (isOpponentPiece) {
                position.style.cursor = 'pointer';
                position.addEventListener('click', async () => {
                    try {
                        const response = await fetch(`/remove_piece?x=${x}&y=${y}&player=${playerWhoFormedMill}`, {
                            method: 'POST'
                        });

                        if (response.ok) {
                            const success = await response.json();
                            if (success) {
                                console.log('Piece removal successful');
                                
                                // Update game state (backend already switched player)
                                await this.updateGameState();
                                console.log('Game state updated');
                                this.updateBoardDisplay();
                                console.log('Board display updated');
                                this.updateButtonStates();
                                
                                // Check for win
                                const win = await this.checkWin();
                                if (win) {
                                    this.showMessage(`${this.gameState.currentPlayer === 'W' ? 'White' : 'Black'} wins!`, 'success');
                                    this.updateBoardDisplay();
                                    return;
                                }
                                
                                console.log(`After mill removal, current player: ${this.gameState.currentPlayer}`);
                                
                                // Clear any mill removal state and reset board interactions
                                this.clearMillRemovalState();
                                
                                // Clear the mill removal instruction message
                                this.showMessage('', 'info');
                            } else {
                                this.showMessage('Invalid piece to remove. Try again.', 'error');
                            }
                        } else {
                            this.showMessage('Invalid piece to remove. Try again.', 'error');
                        }
                    } catch (error) {
                        this.showMessage('Error removing piece: ' + error.message, 'error');
                    }
                }, { once: true });
            }
        });
    }

    async makeComputerMove() {
        const depth = parseInt(document.getElementById('ai-depth').value) || 3;
        
        try {
            this.showMessage('Computer is thinking...', 'info');
            
            const response = await fetch(`/computer_move?depth=${depth}`, {
                method: 'POST'
            });

            if (response.ok) {
                await this.updateGameState();
                this.updateBoardDisplay();
                this.updateButtonStates();
                
                // Check for win
                const win = await this.checkWin();
                if (win) {
                    this.showMessage(`${this.gameState.currentPlayer === 'W' ? 'White' : 'Black'} wins!`, 'success');
                    this.updateBoardDisplay();
                    return;
                }
                
                // Switch player
                await fetch('/switch', { method: 'POST' });
                this.gameState.currentPlayer = this.gameState.currentPlayer === 'W' ? 'B' : 'W';
                this.updateUI();
                this.showMessage('Computer move completed.', 'success');
            } else {
                this.showMessage('Error making computer move.', 'error');
            }
        } catch (error) {
            this.showMessage('Error: ' + error.message, 'error');
        }
    }

    async undoMove() {
        try {
            const response = await fetch('/undo', { method: 'POST' });
            
                    if (response.ok) {
            await this.updateGameState();
            this.updateBoardDisplay();
            this.updateButtonStates();
            this.clearSelection();
            this.showMessage('Move undone.', 'success');
        } else {
            this.showMessage('No moves to undo.', 'error');
        }
        } catch (error) {
            this.showMessage('Error undoing move: ' + error.message, 'error');
        }
    }

    async updateBoardDisplay() {
        try {
            // Get the current board state from the server
            const boardResponse = await fetch('/get_board');
            const board = await boardResponse.json();
            
            console.log('Updating board display with', this.boardPositions.length, 'positions');
            console.log('Board state from server:', board);
            
            // Update each position on the board
            this.boardPositions.forEach((position, index) => {
                const x = parseInt(position.dataset.x);
                const y = parseInt(position.dataset.y);
                const piece = board[y][x];
                
                console.log(`Position (${x}, ${y}): piece = ${piece}`);
                
                // Reset classes
                position.className = 'board-element node';
                position.textContent = '';
                
                if (piece === 'W') {
                    position.classList.add('white');
                    position.textContent = '';
                    console.log(`Added white piece at (${x}, ${y})`);
                } else if (piece === 'B') {
                    position.classList.add('black');
                    position.textContent = '';
                    console.log(`Added black piece at (${x}, ${y})`);
                } else {
                    position.classList.add('valid');
                    console.log(`Position (${x}, ${y}) is empty`);
                }
                
                // Clear any temporary event listeners and re-add them
                const newPosition = position.cloneNode(true);
                position.parentNode.replaceChild(newPosition, position);
                this.boardPositions[index] = newPosition;
                
                // Re-add event listeners
                newPosition.addEventListener('click', () => this.handlePositionClick(x, y));
                
                console.log(`Updated position (${x}, ${y}) with classes: ${newPosition.className}`);
            });
            
            // Update selection if needed
            if (this.selectedPosition) {
                const selectedPos = this.boardPositions.find(p => 
                    parseInt(p.dataset.x) === this.selectedPosition[0] && 
                    parseInt(p.dataset.y) === this.selectedPosition[1]
                );
                if (selectedPos) {
                    selectedPos.classList.add('selected');
                }
            }
        } catch (error) {
            console.error('Error updating board display:', error);
        }
    }

    clearSelection() {
        this.selectedPosition = null;
        this.updateBoardDisplay();
    }

    clearMillRemovalState() {
        console.log('Clearing mill removal state');
        // Remove any temporary event listeners and reset cursor styles
        this.boardPositions.forEach(position => {
            position.style.cursor = 'pointer';
            // Don't clone here as it might interfere with board display
            // Just remove any temporary styling
        });
    }

    updateUI() {
        document.getElementById('current-player').textContent = 
            `Current Player: ${this.gameState.currentPlayer === 'W' ? 'White' : 'Black'}`;
        document.getElementById('game-phase').textContent = 
            `Phase: ${this.gameState.phase === 'placement' ? 'Placement' : 'Movement'}`;
    }

    updateButtonStates() {
        const restartButton = document.getElementById('restart-game');
        const undoButton = document.getElementById('undo-move');
        const computerButton = document.getElementById('computer-move');
        
        console.log('Updating button states. Game active:', this.gameState.gameActive);
        
        // Show buttons when game is active (not when pieces are placed)
        if (this.gameState.gameActive) {
            restartButton.style.display = 'inline-block';
            undoButton.style.display = 'inline-block';
            computerButton.style.display = 'inline-block';
            console.log('Showing game buttons');
        } else {
            restartButton.style.display = 'none';
            undoButton.style.display = 'none';
            computerButton.style.display = 'none';
            console.log('Hiding game buttons');
        }
    }

    showMessage(message, type = 'info') {
        const messageElement = document.getElementById('game-message');
        messageElement.textContent = message;
        messageElement.className = `message ${type}`;
    }

    // API helper methods
    async getPieceCount(player) {
        const response = await fetch(`/get_piece_count?player=${player}`);
        return await response.json();
    }

    async checkMill(x, y, player) {
        const response = await fetch(`/check_mill?x=${x}&y=${y}&player=${player}`);
        return await response.json();
    }

    async checkWin() {
        const response = await fetch('/check_win');
        return await response.json();
    }

    async getCurrentPlayer() {
        const response = await fetch('/get_current_player');
        return await response.json();
    }

    async getPlacedCount() {
        const response = await fetch('/get_placed_count');
        return await response.json();
    }

    async getGameActive() {
        const response = await fetch('/get_game_active');
        return await response.json();
    }

    async getRemovedCount(player) {
        const response = await fetch(`/get_removed_count?player=${player}`);
        return await response.json();
    }
}

// Initialize the game when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new SixMensMorrisUI();
});
