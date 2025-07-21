# QuartoPy

The Quarto board game implemented in Python using Kivy.

## Overview

QuartoPy is an implementation of the [**Quarto**](https://en.wikipedia.org/wiki/Quarto_(board_game)) board game, featuring an AI player implemented using techniques such as the **NegaMax algorithm with alpha-beta pruning**, **transposition tables**, **iterative deepening**, and **symmetry detection**. This project is a **fan recreation** of the Quarto game and is not affiliated with or endorsed by the official Quarto game or its publishers.

## Requirements

- **Python 3.8 or higher** (tested with Python 3.13)
- **Kivy** (with full dependencies)
- **NumPy** (for game state management and AI calculations)
- **filetype** (required by Kivy)

## Installation

### Option 1: Using pip with pyproject.toml

```bash
pip install -e .
```

### Option 2: Manual dependency installation

```bash
pip install "kivy[full]" numpy filetype
```

### Option 3: Install with the uv package manager
```bash
uv pip sync pyproject.toml
```

## Usage

To run the game, execute the following command:

```bash
python main.py
```

This will start the Kivy application and allow you to play Quarto.

## Features

* **Advanced AI Opponent**:
  - NegaMax algorithm with alpha-beta pruning
  - Transposition tables for move optimization
  - Iterative deepening for time-controlled search
  - Symmetry detection to reduce search space
  - Multiple difficulty levels
* **Game Modes**:
  - Single-player vs AI
  - Two-player local multiplayer
* **User Interface**:
  - Intuitive Kivy-based GUI
  - Pause menu
  - Keyboard support
* **Customizable Settings**: Modify settings through `kivy_config.ini`
* **Comprehensive Logging**: Detailed game logs for debugging and analysis

## License

The entire project, including the code and assets, is licensed under the [MIT License](./LICENSE). You are free to use, modify, and distribute the project, subject to the terms of the MIT License.

Note: This project is a fan recreation of the **Quarto** game and is not affiliated with or endorsed by the official Quarto game or its publishers.

## Contributing

Contributions are welcome! Please submit pull requests or report issues on the GitHub repository.

## Acknowledgments

* **Quarto** is a registered trademark of **Gigamic**.
* This project is inspired by the original **Quarto** board game and its innovative design by **Bruno Cathala** and **Marc Rivière**.
