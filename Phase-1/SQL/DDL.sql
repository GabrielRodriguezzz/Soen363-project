
CREATE DOMAIN url_domain AS TEXT
    CHECK (TRIM(LEADING FROM VALUE) ~* '^https?://');

CREATE TABLE IF NOT EXISTS authors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
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
    sentiment DECIMAL(4, 3), 
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

CREATE OR REPLACE FUNCTION check_sentiment_range()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.sentiment < -1 OR NEW.sentiment > 1 THEN
        RAISE EXCEPTION 'Sentiment value must be between -1 and 1. Given value: %', NEW.sentiment;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER validate_sentiment
BEFORE INSERT OR UPDATE ON article_worldNews
FOR EACH ROW
EXECUTE FUNCTION check_sentiment_range();


