# ========================================
# Cloudflare Pages 部署说明
# ========================================

# ⚠️ 重要提示：
# Cloudflare Pages 主要用于静态网站托管。
# 对于完整的 Flask 应用（如本项目），建议使用以下平台之一：

# ========================================
# 方案1: Railway（推荐）- 简单的云部署
# ========================================
# 1. 访问 https://railway.app
# 2. 使用 GitHub 登录
# 3. 点击 "New Project" > "Deploy from GitHub repo"
# 4. 选择你的仓库
# 5. Railway 会自动检测 Python 并安装依赖
# 6. 设置启动命令：`gunicorn app:app`
# 7. 部署完成！

# ========================================
# 方案2: Render - 免费的云托管
# ========================================
# 1. 访问 https://render.com
# 2. 使用 GitHub 登录
# 3. 点击 "New" > "Web Service"
# 4. 连接你的 GitHub 仓库
# 5. 设置：
#    - Build Command: `pip install -r requirements.txt`
#    - Start Command: `gunicorn app:app`
# 6. 选择免费计划
# 7. 部署完成！

# ========================================
# 方案3: Heroku - 老牌 PaaS 平台
# ========================================
# 1. 安装 Heroku CLI
# 2. 登录：heroku login
# 3. 创建应用：heroku create your-app-name
# 4. 推送代码：git push heroku master
# 5. 启动应用：heroku ps:scale web=1

# ========================================
# 方案4: 阿里云/腾讯云 ECS
# ========================================
# 1. 购买云服务器（学生版很便宜）
# 2. 安装 Python 3.11+
# 3. 安装 Nginx + Gunicorn
# 4. 配置反向代理
# 5. 使用 systemd 管理服务

# ========================================
# 方案5: 传统虚拟主机（需支持Python）
# ========================================
# 推荐使用：
# - PythonAnywhere (pythonanywhere.com)
# - Vercel Serverless Functions
# - Netlify Functions

# ========================================
# Cloudflare Pages 配置（仅供参考，不推荐）
# ========================================

[[builds]]
command = "pip install -r requirements.txt"
directory = "/"

[env]
PYTHON_VERSION = "3.11"
