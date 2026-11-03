# Task Forge

A command-line task management application built with Python.

## Overview

Task Forge is a learning project focused on Python fundamentals, modular application design, data persistence, input validation, debugging, and automated testing.

## Features

- Create tasks
- View all tasks
- Filter tasks by pending or completed status
- Search tasks by title
- Edit task titles
- Mark tasks as completed
- Delete tasks
- Persist tasks using JSON
- Detect malformed JSON and invalid task IDs

## Tech Stack

- Python
- Python standard library (`json`)
- pytest

## Project Structure

```text
task_forge_rebuild/
├── main.py
├── task_service.py
├── storage.py
└── test/
    ├── test_task_service.py
    └── test_storage.py
```

## Getting Started

Requires Python 3.10 or newer.

```bash
cd task_forge_rebuild
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pytest
python main.py
```

## Running Tests

From the `task_forge_rebuild` directory:

```bash
python -m pytest test/ -v
```

## Architecture

The application separates responsibilities into three modules:

- **CLI (`main.py`):** Handles user input and displays results.
- **Service (`task_service.py`):** Implements task creation, updates, filtering, searching, and deletion.
- **Storage (`storage.py`):** Handles JSON persistence and loading errors.

## Known Limitations

- Single-user command-line application
- No concurrent access protection
- No database
- Limited validation of individual task records
- File-writing errors are not handled explicitly

## Learning Outcomes

This project demonstrates foundational Python programming, dictionary and list manipulation, modular design, JSON persistence, basic automated testing, input validation, and debugging.
