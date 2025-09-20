# CS Camp Crowdfunding System

A crowdfunding platform built using MVC design pattern with CSV data storage.

## Quick Start

1. **Setup**:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Run**:
   ```bash
   ./run.sh
   ```

## Features

- Browse and search crowdfunding projects
- Make pledges with optional reward tiers
- View project statistics and progress
- User authentication system

## Project Structure

```
├── app.py                      # Main application
├── data/                       # CSV data files
├── models/                     # Data classes
├── repositories/               # Data access
├── services/                   # Business logic
├── controllers/                # Controllers
└── views/                      # GUI views
```

## Data Files

- `categories.csv` - Project categories
- `users.csv` - User accounts  
- `projects.csv` - Crowdfunding projects
- `reward_tiers.csv` - Reward levels
- `pledges.csv` - User pledges

## Requirements

- Python 3.10+
- Tkinter (included with Python)
- No database required