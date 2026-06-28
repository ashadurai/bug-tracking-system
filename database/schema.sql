-- ================================================
-- Bug Tracking System - MySQL Database Schema
-- Author: Asha D
-- ================================================

CREATE DATABASE IF NOT EXISTS bug_tracking_db;
USE bug_tracking_db;

-- ================================================
-- TABLE 1: USERS
-- ================================================
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('Admin', 'Developer', 'Tester') DEFAULT 'Developer',
    status ENUM('Active', 'Inactive') DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ================================================
-- TABLE 2: PROJECTS
-- ================================================
CREATE TABLE projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id)
);

-- ================================================
-- TABLE 3: BUGS
-- ================================================
CREATE TABLE bugs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    steps_to_reproduce TEXT,
    expected_behavior VARCHAR(255),
    actual_behavior VARCHAR(255),
    severity ENUM('Critical', 'High', 'Medium', 'Low') NOT NULL,
    status ENUM('Open', 'In Progress', 'Resolved', 'Closed') DEFAULT 'Open',
    project_id INT,
    assigned_to INT,
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (assigned_to) REFERENCES users(id),
    FOREIGN KEY (created_by) REFERENCES users(id)
);

-- ================================================
-- TABLE 4: NOTIFICATIONS
-- ================================================
CREATE TABLE notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    message VARCHAR(255) NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- ================================================
-- TABLE 5: BUG COMMENTS
-- ================================================
CREATE TABLE comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bug_id INT,
    user_id INT,
    comment TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (bug_id) REFERENCES bugs(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- ================================================
-- SAMPLE DATA
-- ================================================

INSERT INTO users (name, email, password, role) VALUES
('Asha D', 'amutharani306745@gmail.com', 'hashed_password_1', 'Admin'),
('Ravi K', 'ravi.k@example.com', 'hashed_password_2', 'Developer'),
('Priya S', 'priya.s@example.com', 'hashed_password_3', 'Developer'),
('Karan M', 'karan.m@example.com', 'hashed_password_4', 'Tester');

INSERT INTO projects (name, description, created_by) VALUES
('Bug Tracking System', 'A full-stack web app to log, assign and resolve bugs', 1),
('E-Commerce Backend', 'Spring Boot based e-commerce backend system', 1);

INSERT INTO bugs (title, description, severity, status, project_id, assigned_to, created_by) VALUES
('Login page crash on wrong password', 'App crashes when wrong password is entered', 'Critical', 'Open', 1, 2, 4),
('Dashboard not loading on Safari', 'Dashboard shows blank page on Safari browser', 'High', 'In Progress', 1, 3, 4),
('Bug form submit returns 500 error', 'Submitting bug form gives internal server error', 'High', 'In Progress', 1, 1, 3),
('Notification email not sending', 'Email alerts not triggered on bug assignment', 'Medium', 'Resolved', 1, 2, 1),
('Typo in user profile page', 'Small typo in the user profile section', 'Low', 'Closed', 1, 3, 4);

INSERT INTO notifications (user_id, message) VALUES
(2, 'You have been assigned a new bug: Login page crash on wrong password'),
(3, 'You have been assigned a new bug: Dashboard not loading on Safari'),
(1, 'Bug #003 has been resolved by Priya S');
