CREATE DOMAIN url_domain AS TEXT
    CHECK (VALUE ~* '^https?://');