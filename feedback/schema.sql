CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
    usability_score INTEGER NOT NULL CHECK(usability_score BETWEEN 1 AND 5),
    feature_satisfaction INTEGER NOT NULL CHECK(feature_satisfaction BETWEEN 1 AND 5),

    missing_features TEXT,
    improvement_suggestions TEXT,
    user_experience TEXT,

    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_rating ON feedback(rating);