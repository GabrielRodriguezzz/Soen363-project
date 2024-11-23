-- Creating the view

CREATE OR REPLACE VIEW article_view AS
SELECT 
    a.id,
    a.title,
    CASE 
        WHEN CURRENT_USER IN (SELECT rolname FROM pg_roles WHERE rolname = 'full_access_user') THEN a.url
        ELSE NULL
    END AS url,
    a.publish_date,
    CASE 
        WHEN CURRENT_USER IN (SELECT rolname FROM pg_roles WHERE rolname = 'full_access_user') THEN wn.article_id
        ELSE NULL
    END AS article_id,
    CASE 
        WHEN CURRENT_USER IN (SELECT rolname FROM pg_roles WHERE rolname = 'full_access_user') THEN wn.summary
        ELSE NULL
    END AS summary,
    CASE 
        WHEN CURRENT_USER IN (SELECT rolname FROM pg_roles WHERE rolname = 'full_access_user') THEN wn.text
        ELSE NULL
    END AS text,
    CASE 
        WHEN CURRENT_USER IN (SELECT rolname FROM pg_roles WHERE rolname = 'full_access_user') THEN wn.image
        ELSE NULL
    END AS image,
    wn.source_country,
    wn.language,
    CASE 
        WHEN CURRENT_USER IN (SELECT rolname FROM pg_roles WHERE rolname = 'full_access_user') THEN wn.sentiment
        ELSE NULL
    END AS sentiment,
    wn.category,
    CASE 
        WHEN CURRENT_USER IN (SELECT rolname FROM pg_roles WHERE rolname = 'full_access_user') THEN na.source
        ELSE NULL
    END AS source,
    CASE 
        WHEN CURRENT_USER IN (SELECT rolname FROM pg_roles WHERE rolname = 'full_access_user') THEN na.description
        ELSE NULL
    END AS description,
    CASE 
        WHEN CURRENT_USER IN (SELECT rolname FROM pg_roles WHERE rolname = 'full_access_user') THEN na.url_to_image
        ELSE NULL
    END AS url_to_image,
    CASE 
        WHEN CURRENT_USER IN (SELECT rolname FROM pg_roles WHERE rolname = 'full_access_user') THEN na.content
        ELSE NULL
    END AS content
FROM article a
LEFT JOIN article_worldNewsAPI wn ON a.id = wn.id
LEFT JOIN article_newsAPI na ON a.id = na.id;


-- Creating the role for access
CREATE ROLE full_access_user;

-- Giving or revoking the role to the user

GRANT full_access_user to postgres;

REVOKE full_access_user from postgres;

-- Seing the view with or without access
SELECT * FROM article_view;