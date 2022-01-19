CREATE TABLE IF NOT EXISTS guild_settings(
    guild_id BIGINT PRIMARY KEY,
    prefix VARCHAR(30),
    leaderboard_message_url VARCHAR(150),
    quote_channel_id BIGINT,
    quote_reactions_needed SMALLINT DEFAULT 3
);
-- A default guild settings table.
-- This is required for VBU and should not be deleted.
-- You can add more columns to this table should you want to add more guild-specific
-- settings.


CREATE TABLE IF NOT EXISTS user_settings(
    user_id BIGINT PRIMARY KEY,
    timezone_name VARCHAR(250),
    timezone_offset INTEGER  -- Kept for legacy reasons
);
-- A default guild settings table.
-- This is required for VBU and should not be deleted.
-- You can add more columns to this table should you want to add more user-specific
-- settings.
-- This table is not suitable for member-specific settings as there's no
-- guild ID specified.
-- timzone.py requirements

CREATE TABLE IF NOT EXISTS user_points(
    guild_id BIGINT,
    user_id BIGINT,
    points INTEGER DEFAULT 0,
    PRIMARY KEY (guild_id, user_id)
);
--userpoint.py requirements

CREATE TABLE IF NOT EXISTS user_quotes(
    quote_id VARCHAR(5) PRIMARY KEY,
    guild_id BIGINT NOT NULL,
    channel_id BIGINT NOT NULL,
    message_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    quoter_id BIGINT
);

CREATE TABLE IF NOT EXISTS quote_aliases(
    alias VARCHAR(2000) PRIMARY KEY,
    quote_id VARCHAR(5) REFERENCES user_quotes(quote_id) ON DELETE CASCADE
);
-- Tables for quotes.py

CREATE TABLE IF NOT EXISTS role_list(
    guild_id BIGINT,
    role_id BIGINT,
    key VARCHAR(50),
    value VARCHAR(50),
    PRIMARY KEY (guild_id, role_id, key)
);
-- A list of role: value mappings should you need one.
-- This is not required for VBU, so is commented out by default.


CREATE TABLE IF NOT EXISTS channel_list(
    guild_id BIGINT,
    channel_id BIGINT,
    key VARCHAR(50),
    value VARCHAR(50),
    PRIMARY KEY (guild_id, channel_id, key)
);
-- A list of channel: value mappings should you need one.
-- This is not required for VBU, so is commented out by default.


