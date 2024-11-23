CREATE DOMAIN url_domain AS TEXT
    CHECK (TRIM(LEADING FROM VALUE) ~* '^https?://');



CREATE TABLE IF NOT EXISTS article (
    id SERIAL PRIMARY KEY, 
    title TEXT NOT NULL unique, 
    url url_domain, 
    publish_date TIMESTAMP,
    author TEXT
);

CREATE TYPE source_type AS (
    id INT, 
    name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS article_worldNewsAPI (
    article_id INT,
    summary TEXT, 
    text TEXT, 
    image TEXT, 
    source_country TEXT, 
    language TEXT, 
    sentiment DECIMAL(4, 3), 
    category TEXT
) INHERITS (article);

CREATE TABLE IF NOT EXISTS article_newsAPI (
    source source_type, 
    description TEXT, 
    url_to_image TEXT, 
    content TEXT
) INHERITS (article);



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
BEFORE INSERT OR UPDATE ON article_worldNewsAPI
FOR EACH ROW
EXECUTE FUNCTION check_sentiment_range();
