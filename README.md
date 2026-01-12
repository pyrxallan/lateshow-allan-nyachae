# Late Show API Challenge

A Flask-based REST API for managing episodes, guests, and appearances on a late-night show. This project implements a code challenge demonstrating database relationships, RESTful endpoints, and proper error handling.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup](#setup)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Database Models](#database-models)
- [Requirements](#requirements)

## Features
- **Episode Management**: Create and retrieve show episodes with dates and episode numbers
- **Guest Management**: Track guest appearances with names and occupations
- **Appearance Tracking**: Record guest appearances on episodes with ratings (1-5)
- **RESTful API**: Full CRUD operations with proper HTTP status codes
- **Data Validation**: Input validation with meaningful error messages
- **Relationships**: Many-to-many relationships between episodes and guests via appearances

## Technologies Used
- **Flask**: Lightweight Python web framework
- **Flask-SQLAlchemy**: ORM for database interactions
- **SQLite**: Database for development and testing
- **Postman**: API testing and documentation

## Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository** (replace with your actual repo name):
   ```bash
   git clone https://github.com/pyrxallan/lateshow-allan-nyachae.git
   cd lateshow-allan-nyachae
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Seed the database with sample data**:
   ```bash
   python seed.py
   ```

5. **Run the application**:
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5555`

## API Endpoints

### Episodes

#### GET /episodes
Returns a list of all episodes.
```json
[
  {
    "id": 1,
    "date": "1/11/99",
    "number": 1
  }
]
```

#### GET /episodes/:id
Returns a specific episode with all its appearances.
```json
{
  "id": 1,
  "date": "1/11/99",
  "number": 1,
  "appearances": [
    {
      "id": 1,
      "rating": 4,
      "guest_id": 1,
      "episode_id": 1,
      "guest": {
        "id": 1,
        "name": "Michael J. Fox",
        "occupation": "actor"
      }
    }
  ]
}
```

### Guests

#### GET /guests
Returns a list of all guests.
```json
[
  {
    "id": 1,
    "name": "Michael J. Fox",
    "occupation": "actor"
  }
]
```

### Appearances

#### POST /appearances
Creates a new appearance. Requires `rating` (1-5), `episode_id`, and `guest_id`.
```json
// Request body
{
  "rating": 5,
  "episode_id": 2,
  "guest_id": 3
}

// Response
{
  "id": 28,
  "rating": 5,
  "guest_id": 3,
  "episode_id": 2,
  "guest": {
    "id": 3,
    "name": "Sandra Bernhard",
    "occupation": "Comedian"
  },
  "episode": {
    "id": 2,
    "date": "1/12/99",
    "number": 2
  }
}
```

## Testing

### Using Postman
1. Download and install [Postman](https://www.postman.com/)
2. Import the collection: `challenge-4-lateshow.postman_collection.json`
3. Run the requests to test all endpoints

### Manual Testing
You can also test endpoints manually using curl:

```bash
# Get all episodes
curl http://localhost:5555/episodes

# Get episode by ID
curl http://localhost:5555/episodes/1

# Get all guests
curl http://localhost:5555/guests

# Create appearance
curl -X POST http://localhost:5555/appearances \
  -H "Content-Type: application/json" \
  -d '{"rating": 5, "episode_id": 2, "guest_id": 3}'
```

## Database Models

### Episode
- `id`: Primary key
- `date`: Episode date (string)
- `number`: Episode number (integer)

### Guest
- `id`: Primary key
- `name`: Guest name (string)
- `occupation`: Guest occupation (string, optional)

### Appearance
- `id`: Primary key
- `rating`: Rating 1-5 (integer, validated)
- `episode_id`: Foreign key to Episode
- `guest_id`: Foreign key to Guest

### Relationships
- An Episode has many Guests through Appearances
- A Guest has many Episodes through Appearances
- Appearances cascade delete when parent Episode or Guest is removed

## Requirements

### Models & Relationships
- Episode ↔ Appearance (one-to-many)
- Guest ↔ Appearance (one-to-many)
- Appearance validations (rating 1-5)
- Cascade deletes

### Routes
- GET /episodes - List episodes (id, date, number)
- GET /episodes/:id - Episode with appearances (nested guest data)
- GET /guests - List guests (id, name, occupation)
- POST /appearances - Create appearance with nested response

### Error Handling
- 404 for non-existent episodes
- Validation errors for invalid data
- Proper JSON error responses

## Submission Notes
- Ensure your repository is private
- Repository name format: `lateshow-firstname-lastname`
- Test all endpoints before submission
- README renders correctly on GitHub
- All requirements implemented and tested

---

*Built with ❤️ for Phase 4 Code Challenge*
