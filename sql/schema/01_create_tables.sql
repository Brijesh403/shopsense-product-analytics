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