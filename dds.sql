CREATE SCHEMA IF NOT EXISTS dds;
CREATE TABLE IF NOT EXISTS dds.hub_post (
    post_hk CHAR(32) PRIMARY KEY, 
    post_id INTEGER NOT NULL,
    load_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_system VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS dds.hub_user (
    user_hk CHAR(32) PRIMARY KEY,
    user_id INTEGER NOT NULL,
    load_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_system VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS dds.link_post_user (
    link_hk CHAR(32) PRIMARY KEY, 
    post_hk CHAR(32) NOT NULL,
    user_hk CHAR(32) NOT NULL,
    load_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_system VARCHAR(50),
    FOREIGN KEY (post_hk) REFERENCES dds.hub_post(post_hk),
    FOREIGN KEY (user_hk) REFERENCES dds.hub_user(user_hk)
);

CREATE TABLE IF NOT EXISTS dds.sat_post (
    post_hk CHAR(32) NOT NULL,
    title TEXT,
    body TEXT,
    hash_diff CHAR(32), 
    load_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_system VARCHAR(50),
    effective_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (post_hk, hash_diff) 
);