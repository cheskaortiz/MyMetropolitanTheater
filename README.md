# MyMetropolitanTheater
A information management system for managing a seat theater.

### Environment Setup

#### Windows
Run the setup script:
```batch
setup_env.bat
```
Or manually:
```batch
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Running the Application
```bash
# Activate environment (if not already activated)
# Windows: .venv\Scripts\activate

# Run database connection test
python backend/database_connection.py
```

# Database Connection
Go to `backend/database_connection` to connect backend to PostgreSQL.