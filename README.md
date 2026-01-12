Instructions
Setup
Create a new PRIVATE repository. Ensure your repository has a name in the following format; lateshow-firstname-lastname (Example: lateshow-jane-doe). 
You have been provided a Postman collection Download Postman collection. This collection contains all the endpoints that you are required to create with this API. You can download and import it into your Postman application to test that your app works correctly. 
How to import postman collection.

Select `Upload Files`, navigate to this repo folder, and select `challenge-4-lateshow.postman_collection.json` as the file to import.
Before you submit! Save and run your code to verify that it works as you expect. 
You MUST have a well-written README in your repository. Ensure your markdown renders correctly before submission. You can use Visual Studio Code Markdown preview to see how it would appear on your GitHub repository.
Resources
How to write a good README.
 

Deliverables
Your job is to build out the Flask API to add the functionality described in the deliverables below.

Models
You will implement an API for the following data model:

domain.png

Now you can implement the relationships as shown in the ER Diagram:

- An `Episode` has many `Guest`s through `Appearance`
- A `Guest` has many `Episode`s through `Appearance`
Instructions

Setup

Create a new PRIVATE repository. Ensure your repository has a name in the following format: lateshow-firstname-lastname (example: lateshow-jane-doe).

You have been provided a Postman collection: `challenge-4-lateshow.postman_collection.json`. Import that into Postman (Upload Files) to test endpoints.

Deliverables

Your job is to build out the Flask API to add the functionality described below.

Models & Relationships

- An `Episode` has many `Guest`s through `Appearance`.
- A `Guest` has many `Episode`s through `Appearance`.
- An `Appearance` belongs to a `Guest` and belongs to an `Episode`.

Apperances should cascade-delete when their parent `Episode` or `Guest` is removed.

Validations

- `Appearance.rating` must be an integer between 1 and 5 (inclusive).

Routes Required

a. GET /episodes

Return an array of episodes with `id`, `date`, and `number`.

b. GET /episodes/:id

Return the episode with `appearances` array. Each appearance should include `episode_id`, `guest` (with `id`, `name`, `occupation`), `guest_id`, `id`, and `rating`. If the episode is not found, return `{ "error": "Episode not found" }` with a 404 status.

c. GET /guests

Return an array of guests with `id`, `name`, and `occupation`.

d. POST /appearances

Create a new `Appearance` tied to an existing `Episode` and `Guest`. Body example:

```json
{ "rating": 5, "episode_id": 2, "guest_id": 3 }
```

On success return the created appearance including nested `episode` (id/date/number) and `guest` (id/name/occupation). On failure return `{ "errors": [ ... ] }` with an appropriate status code.

Setup and run (local)

1. Create a Python virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Seed the database with sample data:

```bash
python seed.py
```

3. Run the app:

```bash
python app.py
```

Endpoints

- `GET /episodes` - returns list of episodes (id, date, number)
- `GET /episodes/:id` - returns an episode with `appearances` (includes nested guest)
- `GET /guests` - returns list of guests
- `POST /appearances` - create an appearance; body: `{ "rating": 5, "episode_id": 2, "guest_id": 3 }`

Postman

Import `challenge-4-lateshow.postman_collection.json` into Postman via Upload Files and test endpoints.

Notes

This repository includes a minimal Flask app (`app.py`), models (`models.py`), and a `seed.py` script that populates sample data matching the examples in the assignment.
```