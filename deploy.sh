#!/bin/bash

TOKEN="ghp_DqdLO4kfOhjyA82jJAn9weLOnezKw43EaND"
REPO="tanyachen03/xinde"
BRANCH="main"
COMMIT_MSG="修复所有项目文件的代码编辑器 - 恢复行号、自动补全、分屏等功能"

echo "🚀 开始部署到 GitHub..."
echo "📦 仓库: $REPO"
echo "🌿 分支: $BRANCH"
echo ""

# 获取当前分支的最新提交SHA
echo "📡 获取当前提交信息..."
LATEST_SHA=$(curl -s -H "Authorization: token $TOKEN" \
    "https://api.github.com/repos/$REPO/git/ref/heads/$BRANCH" | \
    grep -o '"sha": "[^"]*' | head -1 | cut -d'"' -f4)

if [ -z "$LATEST_SHA" ]; then
    echo "❌ 无法获取最新提交"
    exit 1
fi

echo "✓ 最新提交: ${LATEST_SHA:0:8}"
echo ""

# 要部署的文件列表
FILES=(
    "projects/project2.html"
    "projects/project3.html"
    "projects/project4.html"
    "projects/project5.html"
    "projects/project6.html"
    "projects/project7.html"
    "projects/project8.html"
    "projects/project9.html"
    "projects/project10.html"
)

# 上传每个文件
SUCCESS=0
FAIL=0

for FILE in "${FILES[@]}"; do
    echo "📤 上传: $FILE"
    
    # 检查文件是否存在
    if [ ! -f "/workspace/data-analytics-platform/$FILE" ]; then
        echo "  ⚠️  文件不存在: $FILE"
        continue
    fi
    
    # 获取文件当前SHA（如果存在）
    FILE_SHA=$(curl -s -H "Authorization: token $TOKEN" \
        "https://api.github.com/repos/$REPO/contents/$FILE?ref=$BRANCH" | \
        grep -o '"sha": "[^"]*' | head -1 | cut -d'"' -f4)
    
    # 准备API数据
    CONTENT=$(base64 -w 0 "/workspace/data-analytics-platform/$FILE")
    
    # 构建JSON数据
    if [ -z "$FILE_SHA" ]; then
        # 新文件
        JSON_DATA="{\"message\":\"$COMMIT_MSG\",\"content\":\"$CONTENT\",\"branch\":\"$BRANCH\"}"
    else
        # 更新文件
        JSON_DATA="{\"message\":\"$COMMIT_MSG\",\"content\":\"$CONTENT\",\"branch\":\"$BRANCH\",\"sha\":\"$FILE_SHA\"}"
    fi
    
    # 上传文件
    RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT \
        -H "Authorization: token $TOKEN" \
        -H "Content-Type: application/json" \
        -d "$JSON_DATA" \
        "https://api.github.com/repos/$REPO/contents/$FILE")
    
    HTTP_CODE=$(echo "$RESPONSE" | tail -1)
    
    if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "201" ]; then
        echo "  ✅ 成功"
        ((SUCCESS++))
    else
        echo "  ❌ 失败 (HTTP $HTTP_CODE)"
        echo "  响应: $(echo "$RESPONSE" | head -1)"
        ((FAIL++))
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 部署完成！"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✓ 成功: $SUCCESS"
if [ $FAIL -gt 0 ]; then
    echo "✗ 失败: $FAIL"
fi
echo ""
echo "🌐 网站地址: https://tanyachen03.github.io/xinde/"
echo ""
