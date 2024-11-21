CREATE TABLE IF NOT EXISTS article (
    id SERIAL PRIMARY KEY, 
    source_id INT REFERENCES source (id) ON DELETE SET NULL, 
    author VARCHAR(255), 
    title VARCHAR(255) NOT NULL, 
    description TEXT, 
    url TEXT NOT NULL, 
    url_to_image TEXT, 
    published_at TIMESTAMP, 
    content TEXT 
);
