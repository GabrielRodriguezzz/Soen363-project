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
--SQL QUERY MISSING HERE



--A couple of examples to demonstrate correlated queries.
--Find articles in article_worldNewsAPI that have a higher sentiment than the average sentiment of all articles in the same category
SELECT aw.id, aw.title, aw.category, aw.sentiment
FROM article_worldNewsAPI aw
WHERE aw.sentiment > (
    SELECT AVG(sub_aw.sentiment)
    FROM article_worldNewsAPI sub_aw
    WHERE sub_aw.category = aw.category
);

--ANOTHER EXAMPLE MUST BE ADDED HERE

