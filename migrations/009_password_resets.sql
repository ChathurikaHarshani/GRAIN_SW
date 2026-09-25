CREATE TABLE IF NOT EXISTS password_resets (
 user_id BIGINT UNSIGNED PRIMARY KEY,
 token_hash CHAR(64) NULL UNIQUE,
 password_version CHAR(64) NULL,
 expires_at DATETIME NULL,
 requested_at DATETIME NOT NULL,
 window_started DATETIME NOT NULL,
 request_count INT NOT NULL DEFAULT 1,
 FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
