# 🚀 Cloudflare Pages 部署指南

## 📋 项目结构

```
zuoye/
├── public/                 # 静态文件目录（部署到 Cloudflare Pages）
│   ├── index.html          # 首页
│   ├── courses.html        # 课程列表页
│   ├── course.html         # 课程详情页
│   ├── projects.html       # 项目列表页
│   ├── project.html        # 项目详情页
│   └── assessment.html     # 综合测评页
├── wrangler.toml           # Cloudflare 配置
└── README.md               # 项目说明
```

## 🌐 部署步骤

### 第1步：登录 Cloudflare

访问 **https://pages.cloudflare.com**，使用你的 Cloudflare 账号登录。

### 第2步：创建项目

1. 点击 **"Create a project"**
2. 在 GitHub 仓库列表中选择你的仓库 (`tanyachen03/zuoye`)
3. 点击 **"Begin setup"**

### 第3步：配置构建

| 配置项 | 值 |
|--------|-----|
| **Build command** | （留空） |
| **Output directory** | `public` |
| **Root directory** | `/` |

### 第4步：部署

点击 **"Save and Deploy"**，等待部署完成。

### 第5步：访问网站

部署完成后，Cloudflare 会自动分配一个域名，格式类似：
`https://zuoye.pages.dev`

---

## ✅ 部署成功后

你的网站将包含以下功能：

| 功能 | 状态 | 说明 |
|------|------|------|
| 📚 课程浏览 | ✅ 正常 | 5门精品课程展示 |
| 💼 项目实战 | ✅ 正常 | 10个实战项目展示 |
| 🧪 综合测评 | ✅ 正常 | 10道选择题，自动评分 |
| 🔐 用户登录 | ⚠️ 模拟 | 前端模拟登录功能 |
| 📊 代码执行 | ❌ 移除 | Cloudflare Pages 无法运行 Python |

---

## 📁 页面列表

| 页面 | URL |
|------|-----|
| 首页 | `/` |
| 课程列表 | `/courses.html` |
| 课程详情 | `/course.html?id=xxx` |
| 项目列表 | `/projects.html` |
| 项目详情 | `/project.html?id=xxx` |
| 综合测评 | `/assessment.html` |

---

## 💡 提示

1. **自定义域名**：在 Cloudflare Pages 设置中可以绑定自己的域名
2. **免费额度**：Cloudflare Pages 提供无限带宽和请求，完全免费使用
3. **CI/CD**：每次推送到 GitHub 仓库，Cloudflare 会自动重新部署

---

## 🎉 完成！

你的商务数据分析教育平台已经可以在 Cloudflare Pages 上运行了！
