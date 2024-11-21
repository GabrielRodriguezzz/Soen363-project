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