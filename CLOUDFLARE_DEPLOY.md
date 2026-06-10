# 🚀 Cloudflare Workers + Pages 部署指南

## 📋 架构概述

本项目使用 **Cloudflare 混合架构**：

```
┌─────────────────────────────────────────────────────┐
│                    Cloudflare                        │
│                                                      │
│  ┌──────────────────┐      ┌──────────────────┐    │
│  │  Cloudflare Pages │      │ Cloudflare Workers │    │
│  │   (前端静态文件)   │ ──── │     (后端 API)    │    │
│  │                   │      │                   │    │
│  │  public/index.html│      │  workers/api/     │    │
│  │  public/course.html│     │    index.js       │    │
│  │  public/project.html│    │                   │    │
│  └──────────────────┘      └──────────────────┘    │
│            │                         │              │
│            │                ┌────────┴────────┐    │
│            │                │  Cloudflare D1   │    │
│            │                │  (SQLite 数据库) │    │
│            │                └─────────────────┘    │
└─────────────────────────────────────────────────────┘
```

## ⚠️ 重要限制

由于 Cloudflare Workers 的技术限制：

1. **无法在线执行 Python 代码** - 已移除在线代码编辑器
2. **无文件系统** - 使用 Cloudflare D1 存储数据
3. **CPU 时间限制** - 免费版 10ms/请求
4. **内存限制** - 128MB

### ✅ 保留的功能
- ✅ 课程浏览和章节学习
- ✅ 练习题和综合测评
- ✅ 用户注册和登录
- ✅ 学习进度追踪
- ✅ 成就徽章系统
- ✅ 数据可视化示例

### ❌ 移除的功能
- ❌ 在线代码执行（Python 代码无法在 Workers 中运行）

---

## 🚂 部署步骤

### 第1步：准备工作

```bash
# 1. 安装 Node.js (v18+)
node --version

# 2. 安装 Wrangler CLI
npm install -g wrangler

# 3. 登录 Cloudflare
npx wrangler login
```

### 第2步：创建 D1 数据库

```bash
# 创建数据库
npx wrangler d1 create zuoye-db

# 会返回 database_id，复制下来
# 例如：abc123-def456-ghi789
```

### 第3步：更新配置文件

编辑 `wrangler.toml`，替换数据库 ID：

```toml
[[d1_databases]]
binding = "DB"
database_name = "zuoye-db"
database_id = "你的数据库ID"  # ← 替换这里
```

### 第4步：初始化数据库

```bash
# 执行数据库初始化脚本
npx wrangler d1 execute zuoye-db --file=./schema.sql --env production
```

### 第5步：部署 Workers API

```bash
# 部署到生产环境
npx wrangler deploy

# 或部署到预览环境
npx wrangler dev
```

### 第6步：部署 Pages 前端

方式1：通过 GitHub 部署
1. 登录 https://pages.cloudflare.com
2. 点击 "Create a project"
3. 选择 GitHub 仓库
4. 设置构建命令：（留空）
5. 输出目录：`public`
6. 点击 "Deploy site"

方式2：通过 Wrangler 部署
```bash
# 部署 Pages
npx wrangler pages deploy public
```

---

## 📁 项目结构

```
zuoye/
├── workers/
│   └── api/
│       └── index.js          # Cloudflare Workers API
├── public/
│   └── index.html            # 前端静态页面
├── schema.sql                # 数据库初始化脚本
├── wrangler.toml             # Cloudflare 配置文件
├── requirements.txt          # Python 依赖（Flask 版本用）
├── railway.toml              # Railway 配置（备用）
└── README.md                 # 项目说明
```

---

## 🔧 API 端点

Workers API 提供以下端点：

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/courses` | GET | 获取课程列表 |
| `/api/courses/:id` | GET | 获取单个课程详情 |
| `/api/projects` | GET | 获取项目列表 |
| `/api/register` | POST | 用户注册 |
| `/api/login` | POST | 用户登录 |
| `/api/progress` | GET/POST | 学习进度 |
| `/api/assessment` | GET | 获取测评题目 |
| `/api/badges` | GET | 获取成就徽章 |

---

## 🌐 自定义域名（可选）

### Workers API
```bash
npx wrangler routes update api.zuoye.example.com --zone-name example.com
```

### Pages
1. Cloudflare Dashboard > Pages > 你的项目
2. Custom Domains > Add custom domain
3. 输入你的域名，按提示配置 DNS

---

## 💰 费用说明

| 服务 | 免费额度 | 超出费用 |
|------|---------|---------|
| Cloudflare Workers | 100,000 请求/天 | $5/百万请求 |
| Cloudflare Pages | 500 构建/月, 无限带宽 | 免费 |
| Cloudflare D1 | 5MB 数据库, 1000万读/天 | $5/百万读 |

**总费用**：完全可以在免费额度内运行！

---

## ❓ 常见问题

### Q: Workers 和 Pages 有什么区别？
- **Workers**：运行 JavaScript 代码，提供 API 服务
- **Pages**：托管静态文件（HTML/CSS/JS/图片）
- 本项目两者结合使用

### Q: 为什么移除在线代码执行？
A: Cloudflare Workers 使用 V8 引擎，只能运行 JavaScript，无法执行 Python 代码。

### Q: 如何本地测试？
```bash
# 启动 Workers 开发服务器
npx wrangler dev

# 在另一个终端启动 Pages
npx wrangler pages dev public
```

### Q: 数据存储在哪里？
A: 使用 Cloudflare D1（基于 SQLite 的全球分布式数据库）

---

## 🎯 后续优化建议

1. **添加更多静态页面**：课程详情页、项目详情页等
2. **集成第三方代码执行 API**：如 Piston API
3. **添加实时通知**：使用 Cloudflare Durable Objects
4. **优化前端性能**：使用 Cloudflare Speed
5. **添加图片优化**：使用 Cloudflare Images

---

## 📞 获取帮助

- Cloudflare Workers 文档：https://developers.cloudflare.com/workers/
- Cloudflare Pages 文档：https://developers.cloudflare.com/pages/
- Cloudflare D1 文档：https://developers.cloudflare.com/d1/
- Wrangler CLI 文档：https://developers.cloudflare.com/workers/wrangler/

---

**祝你部署成功！🎉**
