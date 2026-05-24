-- ============================================
-- ShopSense Product Analytics
-- Schema: Table Creation Script
-- Author: Brijesh Vaghela
-- Created: 2026
-- ============================================

-- Create and select database
CREATE DATABASE IF NOT EXISTS shopsense;
USE shopsense;

-- ============================================
-- Table: raw_events
-- Description: All user behavioral events
-- Source: GA4-style ecommerce event data
-- Grain: One row per user-product-event
-- ============================================

CREATE TABLE IF NOT EXISTS raw_events (
    id            BIGINT AUTO_INCREMENT PRIMARY KEY,
    event_time    DATETIME,
    event_type    VARCHAR(20),
    product_id    BIGINT,
    category_id   BIGINT UNSIGNED,
    category_code VARCHAR(100),
    brand         VARCHAR(50),
    price         DECIMAL(10,2),
    user_id       BIGINT,
    user_session  VARCHAR(36)
);

-- ============================================
-- Indexes for query performance
-- Created after data load
-- ============================================

CREATE INDEX idx_event_type ON raw_events(event_type);
CREATE INDEX idx_user_id    ON raw_events(user_id);
CREATE INDEX idx_event_time ON raw_events(event_time);