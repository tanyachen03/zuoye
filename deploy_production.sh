#!/bin/bash
# 生产环境部署脚本

# 停止现有服务
pkill -f gunicorn 2>/dev/null || true
pkill -f "python app.py" 2>/dev/null || true

# 安装生产依赖
echo "正在安装生产环境依赖..."
pip install gunicorn flask

# 使用 Gunicorn 启动服务
# -w 4: 4个worker进程
# -b 0.0.0.0:5000: 绑定到所有网络接口的5000端口
# --timeout 120: 超时时间设为120秒（数据分析代码运行时间较长）
echo "正在启动服务..."
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 --access-logfile - --error-logfile - app:app

echo "服务已在 http://0.0.0.0:5000 启动"
