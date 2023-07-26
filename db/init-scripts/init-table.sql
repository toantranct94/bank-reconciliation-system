CREATE TABLE transactions (
  id SERIAL PRIMARY KEY,
  date TIMESTAMP,
  content TEXT,
  amount NUMERIC,
  type TEXT
);
