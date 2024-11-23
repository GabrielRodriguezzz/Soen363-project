-- Select all articles from article_worldNewsAPI with a sentiment score of 0.8 or higher
SELECT *
FROM article_worldNewsAPI
WHERE sentiment >= 0.8;

-- Group articles by category and count the number of articles
SELECT category, COUNT(*) AS article_count
FROM article_worldNewsAPI
GROUP BY category;

-- Group articles by category and include only categories with more than 5 articles
SELECT category, COUNT(*) AS article_count
FROM article_worldNewsAPI
GROUP BY category
HAVING COUNT(*) > 5;


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



