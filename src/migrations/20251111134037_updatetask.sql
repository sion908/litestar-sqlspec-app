-- SQLSpec Migration
-- Version: 20251111134037
-- Description: update_task
-- Created: 2025-11-11T13:40:37.915503+00:00
-- Author: sion908

-- name: migrate-20251111134037-up
ALTER TABLE tasks ADD COLUMN completed BOOLEAN DEFAULT 0;
ALTER TABLE tasks ADD COLUMN priority TEXT;
ALTER TABLE tasks ADD COLUMN due_date TIMESTAMP;

-- name: migrate-20251111134037-down
ALTER TABLE tasks DROP COLUMN completed;
ALTER TABLE tasks DROP COLUMN priority;
ALTER TABLE tasks DROP COLUMN due_date;
