
CREATE DOMAIN url_domain AS TEXT
    CHECK (VALUE ~* '^https?://');

CREATE TABLE IF NOT EXISTS authors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS article_worldNews (
    id INT PRIMARY KEY, 
    author_id INT REFERENCES authors(id) ON DELETE SET NULL,  
    title TEXT NOT NULL, 
    summary TEXT, 
    text TEXT, 
    url url_domain, 
    image TEXT, 
    publish_date TIMESTAMP, 
    source_country TEXT, 
    language TEXT, 
    sentiment DECIMAL(4, 3) CHECK (sentiment >= -1 AND sentiment <= 1), 
    category TEXT
);

CREATE TYPE source_type AS (
    id INT, 
    name VARCHAR(255)
);

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


