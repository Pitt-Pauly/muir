DROP TABLE IF EXISTS users;
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT null,
  email TEXT NOT null
);

DROP TABLE IF EXISTS locations;
CREATE TABLE locations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT null,
  coordinates TEXT NOT null,
  description TEXT NOT null,
  status TEXT DEFAULT 'new',
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS location_adjustments;
CREATE TABLE location_adjustments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NULL,
  location_id INTEGER NULL,
  FOREIGN KEY(user_id) REFERENCES users(id),
  FOREIGN KEY(location_id) REFERENCES locations(id)
);