CREATE TABLE IF NOT EXISTS user_emails (
    user_id BIGINT UNSIGNED NOT NULL PRIMARY KEY,
    email VARCHAR(254) NOT NULL UNIQUE,
    verified_at DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS user_invitations (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Grower_ID BIGINT UNSIGNED NOT NULL,
    email VARCHAR(254) NOT NULL,
    role ENUM('viewer','editor','admin') NOT NULL,
    invited_by BIGINT UNSIGNED NOT NULL,
    token_hash CHAR(64) NOT NULL UNIQUE,
    status ENUM('sending','pending','failed','accepted','revoked') NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME NOT NULL,
    accepted_at DATETIME NULL,
    failed_attempts INT UNSIGNED NOT NULL DEFAULT 0,
    UNIQUE KEY uq_grower_invitation (Grower_ID,email),
    FOREIGN KEY (Grower_ID) REFERENCES Grower(Grower_ID) ON DELETE CASCADE,
    FOREIGN KEY (invited_by) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
