# Basic Authentication API

This project implements **Basic Authentication** for a simple Flask-based API. The API provides a `status` endpoint that requires valid credentials to access. The authentication process involves **Base64 encoding** of the `username:password` pair, which is sent via the `Authorization` header in the HTTP request.

## Table of Contents

- [Installation Instructions](#installation-instructions)
- [Usage Instructions](#usage-instructions)
- [API Endpoints](#api-endpoints)
- [Testing the API](#testing-the-api)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Installation Instructions

Follow these steps to set up and run the project:

1. **Clone the repository** to your local machine:
   ```bash
   git clone https://github.com/your-username/alx-backend-user-data.git
   cd alx-backend-user-data
