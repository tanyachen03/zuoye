-- ============================================
-- Cloudflare D1 数据库初始化脚本
-- ============================================
-- 
-- 执行方式：
-- 1. 方式一：使用 Wrangler CLI
--    npx wrangler d1 execute zuoye-db --file=./schema.sql --env production
--
-- 2. 方式二：直接在 Cloudflare Dashboard 中执行
--    登录 Cloudflare Dashboard > D1 > 你的数据库 > Query
--
-- ============================================

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL,
    last_login TEXT
);

-- 章节进度表
CREATE TABLE IF NOT EXISTS chapter_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    chapter_id TEXT NOT NULL,
    completed INTEGER DEFAULT 0,
    completed_at TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE(user_id, chapter_id)
);

-- 项目进度表
CREATE TABLE IF NOT EXISTS project_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    project_id TEXT NOT NULL,
    completed INTEGER DEFAULT 0,
    completed_at TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE(user_id, project_id)
);

-- 成就徽章表
CREATE TABLE IF NOT EXISTS badges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    badge_id TEXT NOT NULL,
    earned_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE(user_id, badge_id)
);

-- 测评成绩表
CREATE TABLE IF NOT EXISTS assessment_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    score INTEGER NOT NULL,
    total INTEGER NOT NULL,
    passed INTEGER DEFAULT 0,
    taken_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_chapter_progress_user ON chapter_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_project_progress_user ON project_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_badges_user ON badges(user_id);

-- ============================================
-- 插入示例数据（可选）
-- ============================================

-- 示例用户（密码都是 "password123" 的 SHA-256 哈希）
-- INSERT INTO users (username, email, password_hash, created_at) VALUES
-- ('demo', 'demo@example.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', datetime('now'));
