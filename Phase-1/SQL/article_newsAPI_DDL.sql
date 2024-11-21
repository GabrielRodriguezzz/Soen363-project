CREATE TABLE IF NOT EXISTS article_newsAPI (
    id SERIAL PRIMARY KEY, 
    source source_type, 
    author_id INT REFERENCES authors(id) ON DELETE SET NULL, 
    title VARCHAR(255) NOT NULL, 
    description TEXT, 
    url url_domain, 
    url_to_image TEXT, 
    published_at TIMESTAMP, 
    content TEXT 
);
