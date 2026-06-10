# Railway 部署配置
# 详细文档：https://docs.railway.app

# 1. 访问 https://railway.app
# 2. 使用 GitHub 登录
# 3. 点击右上角 "New Project"
# 4. 选择 "Deploy from GitHub repo"
# 5. 搜索并选择你的仓库：tanyachen03/zuoye
# 6. Railway 会自动检测 Python 项目

# ========================================
# Railway 控制台配置
# ========================================

# 在 Railway 控制台中设置以下内容：

# ----------------------------------------
# 1. 构建命令（Build Command）
# pip install -r requirements.txt
# ----------------------------------------

# ----------------------------------------
# 2. 启动命令（Start Command）
# gunicorn app:app --host 0.0.0.0 --port $PORT
# ----------------------------------------

# ----------------------------------------
# 3. 环境变量（Environment Variables）
# PORT = 8000 (Railway 会自动设置)
# PYTHON_VERSION = 3.11
# ----------------------------------------

# ========================================
# 或使用 railway.toml（可选）
# ========================================

[railway]
region = "us-east"
runtime = "python"

[build]
command = "pip install -r requirements.txt"

[deploy]
startCommand = "gunicorn app:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/"
