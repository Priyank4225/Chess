# Online Chess Engine

A real-time multiplayer chess application built with FastAPI, WebSockets, and Pygame.

## Features

* Real-time multiplayer gameplay
* WebSocket-based communication
* Turn-based move system
* Basic chess move validation
* Lightweight client with Pygame

## Project Structure

```
chess-online/
│
├── server/
│   ├── main.py
│   ├── chess.py
│
├── client/
│   ├── client.py
│   ├── board.png
│   └── Resources/
│
├── requirements.txt
├── LICENSE
└── README.md
```

## Installation

Clone the repository:

```
git clone https://github.com/Priyank4225/Chess.git
cd Chess
```

Install dependencies:

```
pip install -r requirements.txt
```

## Running the Project

Start the server:

```
uvicorn server.main:app --reload
```

Run the client (in two separate terminals for multiplayer):

```
python client/client.py
```

## How It Works

* The server pairs two connected players into a game session.
* Each move is sent via WebSocket to the server.
* The server validates and updates the board state.
* The updated board is broadcast to both players.

## Controls

* Click on a piece to see available moves
* Click on a highlighted square to move

## Requirements

* Python 3.10+
* FastAPI
* Uvicorn
* WebSockets
* Pygame

## Future Improvements

* Check and checkmate detection
* Castling and en passant
* Pawn promotion
* Better UI and animations
* Game lobby system
* AI opponent integration

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
