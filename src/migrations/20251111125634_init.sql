-- SQLSpec Migration
-- Version: 20251111125634
-- Description: init
-- Created: 2025-11-11T12:56:34.974238+00:00
-- Author: sion908


-- name: migrate-20251111125634-up
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT DEFAULT '',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER trg_tasks_set_updated_at
AFTER UPDATE ON tasks
FOR EACH ROW
BEGIN
    UPDATE tasks SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
END;

-- name: migrate-20251111125634-down
DROP TRIGGER IF EXISTS trg_tasks_set_updated_at;
DROP TABLE IF EXISTS tasks;
