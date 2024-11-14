# 0x02. Session Authentication

## Project Overview

In this project, we implement **session authentication** for an API built using Flask. Session authentication is a mechanism that allows a user to log in and maintain a session via cookies, enabling the user to access protected endpoints without having to log in repeatedly.

The project builds on the basic authentication from a previous project (0x06) but replaces it with session-based authentication to simulate real-world scenarios where sessions are managed by the server using cookies.

## Learning Objectives

At the end of this project, you should be able to explain and implement the following:

- What authentication means in the context of web applications.
- What **session authentication** means and how it differs from basic authentication.
- What **cookies** are and how they can be used to manage user sessions.
- How to send and parse cookies using Flask.
- How to implement session authentication in a REST API.

## Requirements

### General Requirements

- All your files will be interpreted/compiled on **Ubuntu 18.04 LTS** using **python3 (version 3.7)**.
- All files should end with a new line.
- The first line of all your files should be exactly `#!/usr/bin/env python3`.
- The `README.md` file is mandatory at the root of the project directory.
- The code should comply with **pycodestyle** version 2.5.
- All files must be executable.

### Project File Structure

This project contains the following key components:

- `api/`: Contains the API endpoints and related logic.
  - `v1/`: The first version of the API.
    - `views/`: Contains route definitions for various endpoints.
    - `auth/`: Contains authentication-related classes, such as `SessionAuth`.
    - `app.py`: Main Flask application file that initializes the app and configures routes and middleware.
- `models/`: Contains data models and database interactions.
- `tests/`: Contains unit and integration tests (if you write tests for this project).

## Installation and Setup

To get started with this project, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/alx-backend-user-data.git
   cd alx-backend-user-data/0x02-Session_authentication
