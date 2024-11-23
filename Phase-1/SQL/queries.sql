-- Basic select with simple where clause
-- Select all articles from article_worldNewsAPI with a sentiment score of 0.8 or higher
SELECT *
FROM article_worldNewsAPI
WHERE sentiment >= 0.8;

-- Basic select with simple group by clause (with and without having clause)
-- Group articles by category and count the number of articles
SELECT category, COUNT(*) AS article_count
FROM article_worldNewsAPI
GROUP BY category;

-- Group articles by category and include only categories with more than 5 articles
SELECT category, COUNT(*) AS article_count
FROM article_worldNewsAPI
GROUP BY category
HAVING COUNT(*) > 5;

-- A simple join query as well as its equivalent implementation using cartesian product and where clause.
-- Match and retrieve articles published on the same day from two different sources using join.
SELECT 
    n.id AS newsapi_article_id,                
    n.title AS newsapi_title,                 
    w.id AS worldnewsapi_article_id,          
    w.title AS worldnewsapi_title,            
    n.publish_date AS newsapi_publish_date,   
    w.publish_date AS worldnewsapi_publish_date
FROM 
    article_newsAPI n
JOIN 
    article_worldNewsAPI w
ON 
    DATE(n.publish_date) = DATE(w.publish_date);

-- Match and retrieve articles published on the same day from two different sources using a cartesian product.
SELECT 
    n.id AS newsapi_article_id,                
    n.title AS newsapi_title,                 
    w.id AS worldnewsapi_article_id,          
    w.title AS worldnewsapi_title,            
    n.publish_date AS newsapi_publish_date,   
    w.publish_date AS worldnewsapi_publish_date
FROM 
    article_newsAPI n, 
    article_worldNewsAPI w
WHERE 
    DATE(n.publish_date) = DATE(w.publish_date);

-- A few queries to demonstrate various join types on the same tables: inner vs. outer (left and right) vs. full join. 
--Inner join
SELECT
    w.id AS worldnews_id,
    w.title AS worldnews_title,
    n.id AS newsapi_id,
    n.title AS newsapi_title
FROM
    article_worldNewsAPI w
INNER JOIN
    article_newsAPI n ON LEFT(w.title, 3) = LEFT(n.title, 3);
--Left outer join
SELECT
    w.id AS worldnews_id,
    w.title AS worldnews_title,
    n.id AS newsapi_id,
    n.title AS newsapi_title
FROM
    article_worldNewsAPI w
LEFT JOIN
    article_newsAPI n ON LEFT(w.title, 3) = LEFT(n.title, 3);
--Right outer join
SELECT
    w.id AS worldnews_id,
    w.title AS worldnews_title,
    n.id AS newsapi_id,
    n.title AS newsapi_title
FROM
    article_worldNewsAPI w
RIGHT JOIN
    article_newsAPI n ON LEFT(w.title, 3) = LEFT(n.title, 3);
--Full outer join
SELECT
    w.id AS worldnews_id,
    w.title AS worldnews_title,
    n.id AS newsapi_id,
    n.title AS newsapi_title
FROM
    article_worldNewsAPI w
FULL OUTER JOIN
    article_newsAPI n ON LEFT(w.title, 3) = LEFT(n.title, 3);




--A few queries to demonstrate use of Null values for undefined / non-applicable
SELECT id, title, publish_date, category 
FROM article_worldNewsAPI 
WHERE category IS NULL;

SELECT id, title, publish_date, author 
FROM article 
WHERE author IS NULL;




--A couple of examples to demonstrate correlated queries.
SELECT aw.id, aw.title, aw.category, aw.sentiment
FROM article_worldNewsAPI aw
WHERE aw.sentiment > (
    SELECT AVG(sub_aw.sentiment)
    FROM article_worldNewsAPI sub_aw
    WHERE sub_aw.category = aw.category
);

SELECT id, title, category, publish_date 
FROM article_worldNewsAPI a1 
WHERE publish_date = (
    SELECT MAX(publish_date) 
    FROM article_worldNewsAPI a2 
    WHERE a1.category = a2.category
);


-- Set operations

-- Intersect
SELECT author 
FROM article_worldNewsAPI 
INTERSECT 
SELECT author 
FROM article_newsAPI;

SELECT a1.author, a1.title 
FROM article_worldNewsAPI a1 
INNER JOIN article_newsAPI a2 
ON a1.author = a2.author;

-- Union
SELECT id, title 
FROM article_worldNewsAPI 
UNION 
SELECT id, title 
FROM article_newsAPI;

SELECT id, title
FROM article_worldNewsAPI
WHERE TRUE 
OR id IN (
    SELECT id
    FROM article_newsAPI
    WHERE NOT EXISTS (
        SELECT 1
        FROM article_worldNewsAPI
        WHERE article_worldNewsAPI.id = article_newsAPI.id
          AND article_worldNewsAPI.title = article_newsAPI.title
    )
);

-- Difference
SELECT id, title
FROM article_worldNewsAPI
EXCEPT
SELECT id, title
FROM article_newsAPI;

SELECT a.id, a.title
FROM article_worldNewsAPI a
WHERE NOT EXISTS (
    SELECT 1
    FROM article_newsAPI b
    WHERE a.id = b.id AND a.title = b.title
);


-- View with hard coded criteria
CREATE VIEW hard_coded AS
(SELECT * FROM article_worldNewsAPI WHERE article_id = 265762636);


-- Queries with overlap and convering constraints

-- overlap
SELECT w.id, w.url, n.id AS news_id, n.url AS news_url
FROM article_worldNewsAPI w
JOIN article_newsAPI n
ON w.url = n.url;

-- covering
SELECT id
FROM article
WHERE id NOT IN (
    SELECT w.id
    FROM article_worldNewsAPI w
    WHERE NOT EXISTS (
        SELECT 1
        FROM article_newsAPI n
        WHERE w.id = n.id
    )
);

-- Division operator
-- NOT IN
SELECT a.id, a.title
FROM article a
WHERE NOT EXISTS (
    SELECT category
    FROM article_worldNewsAPI
    WHERE category NOT IN (
        SELECT category
        FROM article_worldNewsAPI w
        WHERE w.id = a.id
    )
);
-- NOT EXISTS and EXCEPT
SELECT a.author
FROM article a
WHERE NOT EXISTS (
    SELECT language
    FROM article_worldNewsAPI
    EXCEPT
    (
        SELECT DISTINCT w.language
        FROM article_worldNewsAPI w
        WHERE w.author = a.author
    )
);

