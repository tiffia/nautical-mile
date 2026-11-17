Read 
Completed with input: {
  "path": "/workspaces/nautical-mile/app.py"
}

`app.py` is a small Flask web app for tracking skills and whether you’ve learned them.

- It stores skills in a local SQLite database, `skills.db`. On startup, `init_db()` creates a `skills` table if needed.
- `GET /` loads all skills and renders them in `index.html`.
- `POST /add` adds a submitted skill with the initial status **“To Learn”**.
- `GET /toggle/<skill_id>` switches that skill’s status between **“To Learn”** and **“Completed”**.
- After adding or toggling, it redirects back to the home page.

One note: toggling changes data via a `GET` request; a `POST` request is generally a better fit for actions that modify data. The app also runs with Flask’s debug mode enabled, which is intended for development.