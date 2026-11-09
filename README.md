
# TournamentLab 🏆

A Python command-line tournament management system.

TournamentLab is a local tournament management application built with Python. It is designed to help organizers register teams, generate round-robin fixtures, record match results, calculate league standings, and identify tournament champions.

The project focuses on clean Python code, reliable data handling, automated testing, and fair tournament rules.

# Features

# Team Management
- Register between 4 and 8 teams.
- Generate unique team IDs.
- Prevent duplicate team names.
- Validate team names before registration.

# Fixture Management
- Generate single round-robin fixtures.
- Ensure every team plays every other team once.
- Prevent duplicate pairings and self-play.
- Generate unique fixture IDs.

# Match Results
- Record match scores.
- Accept only non-negative whole-number scores.
- Reject invalid scores, including decimals and Boolean values.
- Prevent a fixture from receiving a second result.

# League Standings
- Calculate matches played, wins, draws, and losses.
- Calculate goals scored, goals conceded, and goal difference.
- Award 3 points for a win and 1 point for a draw.
- Rank teams using consistent tie-break rules.

# Champion Reports
- Identify the champion when all fixtures are completed.
- Detect a mathematical champion when no rival can catch the leader on points.

# Data Storage
- Save tournament information in JSON format.
- Load previously saved tournament data.
- Check the saved data schema version.

# Technology Stack

- Language: Python
- Storage: JSON
- Testing: Python: unittest
- Dependencies: Python standard library

No third-party Python packages are required.

# Tournament Rules

TournamentLab follows these rules:

1. A tournament requires at least 4 teams and allows a maximum of 8.
2. Each team plays every other team exactly once.
3. A win earns 3 points.
4. A draw earns 1 point for each team.
5. A loss earns 0 points.
6. Invalid match scores are rejected.
7. A completed fixture cannot be recorded again.

# League Ranking

Teams are ranked using the following criteria:

1. Highest points.
2. Highest goal difference.
3. Highest goals scored.
4. Fewest goals conceded.
5. Alphabetical team name when all numerical criteria are equal.

# Development Status

TournamentLab is under active development.

Implemented modules and tests include:

- Team registration.
- Fixture generation.
- Match result recording.
- League standings.
- Champion reports.
- Basic JSON saving and loading.
- Initial storage validation.

Further work includes stronger JSON data validation, complete CLI integration, and end-to-end tournament testing.

# Learning Goals

This project is also a practical Python learning exercise, focusing on:

- Functions and modular programming.
- Lists and dictionaries.
- Loops and conditional statements.
- Exception handling.
- File handling and JSON.
- Unit testing.
- Git and GitHub version control.

# Project Philosophy

TournamentLab aims to make tournament management simple, transparent, and reliable.

Built with Python. Developed through continuous learning and testing.