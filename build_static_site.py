#!/usr/bin/env python3
"""生成可部署到 Cloudflare Pages 的纯静态站点"""
import os
import shutil
import re

# 目录设置
PAGES_DIR = "/workspace/pages"
STATIC_DIR = "/workspace/static"
BUILD_DIR = "/workspace"  # 直接输出到工作目录根

# 课程数据（每门课程有3章）
COURSES = [
    ("course1", "Python编程基础", ["Python环境搭建", "基础语法与数据类型", "控制流程与函数"], [1, 2, 3]),
    ("course2", "NumPy数据分析", ["NumPy基础入门", "数组操作与运算", "高级技巧与实战"], [4, 5, 6]),
    ("course3", "Pandas数据处理", ["Pandas基础入门", "数据清洗与转换", "分组聚合与高级操作"], [7, 8, 9]),
    ("course4", "数据可视化", ["Matplotlib基础", "Seaborn高级图表", "交互式可视化"], [10, 11, 12]),
    ("course5", "统计分析基础", ["描述性统计", "推断统计与假设检验", "回归分析"], [13, 14, 15]),
    ("course6", "机器学习入门", ["机器学习概述", "监督学习算法", "无监督学习与模型评估"], [16, 17, 18]),
    ("course7", "商业数据分析", ["销售数据分析", "客户行为分析", "商业智能与决策"], [19, 20, 21]),
    ("course8", "实战项目演练", ["销售数据分析项目", "客户分群分析项目", "综合项目实战"], [22, 23, 24]),
]

PROJECTS = [
    ("销售数据分析", "分析销售数据趋势，找出业绩增长点", "初级", "10小时", ["Python", "Pandas", "数据可视化"]),
    ("客户分群分析", "使用RFM模型对客户进行分群分析", "中级", "15小时", ["Python", "聚类算法", "RFM分析"]),
    ("市场篮子分析", "商品关联规则挖掘，优化商品摆放", "中级", "12小时", ["Python", "关联规则", "Apriori"]),
    ("用户流失预测", "构建机器学习模型预测客户流失", "高级", "20小时", ["Python", "Scikit-learn", "分类算法"]),
    ("销售预测建模", "使用时间序列分析预测未来销售", "高级", "18小时", ["Python", "时间序列", "回归分析"]),
    ("产品推荐系统", "构建个性化产品推荐引擎", "高级", "22小时", ["Python", "推荐算法", "协同过滤"]),
    ("价格优化分析", "基于数据的产品定价策略分析", "中级", "14小时", ["Python", "回归分析", "定价模型"]),
    ("库存优化分析", "数据驱动的库存管理与补货策略", "中级", "12小时", ["Python", "库存模型", "优化算法"]),
    ("营销效果分析", "评估营销活动ROI与转化分析", "初级", "10小时", ["Python", "A/B测试", "转化率分析"]),
    ("综合商业分析", "端到端商业数据分析完整案例", "高级", "25小时", ["Python", "综合分析", "商业报告"]),
]

CHAPTERS_DATA = {
    1: ("Python环境搭建", ["Python语言概述", "安装Python环境", "配置开发工具", "第一个Python程序", "Python包管理器"]),
    2: ("基础语法与数据类型", ["变量与赋值", "数字类型与运算", "字符串操作", "列表与元组", "字典与集合"]),
    3: ("控制流程与函数", ["条件语句", "循环结构", "函数定义与调用", "函数参数与返回值", "模块与包"]),
    4: ("NumPy基础入门", ["NumPy介绍", "创建数组", "数组属性", "基本运算", "索引与切片"]),
    5: ("数组操作与运算", ["数组变形", "数组拼接与拆分", "数组运算", "广播机制", "统计函数"]),
    6: ("高级技巧与实战", ["条件索引", "文件读写", "性能优化", "随机数生成", "综合实战"]),
    7: ("Pandas基础入门", ["Pandas介绍", "Series数据结构", "DataFrame基础", "读取CSV数据", "基本操作"]),
    8: ("数据清洗与转换", ["缺失值处理", "数据类型转换", "数据筛选", "数据排序", "数据合并"]),
    9: ("分组聚合与高级操作", ["分组操作", "聚合函数", "透视表", "时间序列", "综合案例"]),
    10: ("Matplotlib基础", ["Matplotlib介绍", "折线图", "柱状图", "散点图", "饼图与热力图"]),
    11: ("Seaborn高级图表", ["Seaborn介绍", "分布图", "分类图", "相关性图", "多图布局"]),
    12: ("交互式可视化", ["Plotly介绍", "交互式图表", "仪表板设计", "动态更新", "实战案例"]),
    13: ("描述性统计", ["统计概述", "集中趋势", "离散程度", "分布形态", "数据摘要"]),
    14: ("推断统计与假设检验", ["概率分布", "抽样分布", "假设检验", "t检验", "卡方检验"]),
    15: ("回归分析", ["相关分析", "线性回归", "多元回归", "回归诊断", "实战案例"]),
    16: ("机器学习概述", ["机器学习介绍", "监督与非监督", "训练与测试", "模型评估", "常用库介绍"]),
    17: ("监督学习算法", ["线性回归", "逻辑回归", "决策树", "随机森林", "支持向量机"]),
    18: ("无监督学习与模型评估", ["K均值聚类", "层次聚类", "主成分分析", "模型选择", "模型优化"]),
    19: ("销售数据分析", ["销售数据概述", "销售趋势分析", "产品分析", "区域分析", "综合报告"]),
    20: ("客户行为分析", ["客户数据概述", "购买行为分析", "客户生命周期", "RFM分析", "客户价值"]),
    21: ("商业智能与决策", ["商业指标体系", "数据仪表盘", "数据驱动决策", "商业报告", "实战案例"]),
    22: ("销售数据分析项目", ["项目概述", "数据探索", "数据清洗", "分析建模", "报告撰写"]),
    23: ("客户分群分析项目", ["项目背景", "数据准备", "RFM建模", "客户画像", "策略建议"]),
    24: ("综合项目实战", ["项目规划", "数据收集", "探索分析", "模型构建", "成果展示"]),
}

NAV_TEMPLATE = """<nav class="navbar">
            <div class="logo">数析学院</div>
            <div class="nav-links">
                <a href="index.html"{active_index}>首页</a>
                <a href="courses.html"{active_courses}>课程体系</a>
                <a href="projects.html"{active_projects}>项目实战</a>
            </div>
        </nav>"""

def generate_index():
    courses_html = ""
    for i, (cid, title, chapters, chapter_nums) in enumerate(COURSES, 1):
        icons = ["💻", "📊", "📈", "🎨", "📐", "🤖", "💼", "🎯"]
        levels = ["入门", "初级", "初级", "初级", "中级", "中级", "高级", "高级"]
        durations = ["8小时", "10小时", "12小时", "8小时", "10小时", "12小时", "15小时", "20小时"]
        icon = icons[i-1]
        level = levels[i-1]
        duration = durations[i-1]
        desc = {
            1: "从零开始学习Python编程语言，掌握数据分析必备的编程基础",
            2: "学习使用NumPy进行高效的数值计算和数组操作",
            3: "掌握Pandas库进行数据读取、清洗、筛选和聚合分析",
            4: "使用Matplotlib、Seaborn等工具创建专业的数据可视化图表",
            5: "学习统计学基础，掌握数据描述、假设检验和回归分析",
            6: "了解机器学习基本概念，掌握常用监督和无监督学习算法",
            7: "将数据分析技术应用于实际商业场景，提升商业决策能力",
            8: "通过完整项目案例，综合运用所学知识解决实际问题",
        }[i]
        courses_html += f"""            <a href="{cid}.html" class="course-card">
                <div class="course-icon">{icon}</div>
                <h3 class="course-title">{title}</h3>
                <p class="course-desc">{desc}</p>
                <div class="course-meta">
                    <span class="tag">{level}</span>
                    <span class="duration">{duration}</span>
                </div>
            </a>
"""

    projects_html = ""
    for title, desc, level, duration, skills in PROJECTS:
        skills_html = " ".join(f'<span class="tag">{s}</span>' for s in skills)
        projects_html += f"""            <div class="project-card">
                <h3 class="project-title">{title}</h3>
                <p class="project-desc">{desc}</p>
                <div class="project-meta">
                    <span class="tag">{level}</span>
                    <span class="duration">{duration}</span>
                </div>
                <div class="project-skills">{skills_html}</div>
            </div>
"""

    nav = NAV_TEMPLATE.format(active_index=' class="active"', active_courses='', active_projects='')

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>数析学院 - 商务数据分析在线教育平台</title>
    <link rel="stylesheet" href="static/style.css">
</head>
<body>
    <div class="page-container">
        {nav}

        <h1 class="page-title">数析学院 - 商务数据分析在线教育平台</h1>
        <p class="page-subtitle">掌握商务数据分析技能，开启数据驱动决策之旅</p>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">8</div>
                <div class="stat-label">门课程</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">24</div>
                <div class="stat-label">个章节</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">10</div>
                <div class="stat-label">个项目</div>
            </div>
        </div>

        <h2 class="section-title">📚 课程体系</h2>
        <div class="courses-grid">
{courses_html}        </div>

        <h2 class="section-title">🎯 项目实战</h2>
        <div class="projects-grid">
{projects_html}        </div>
    </div>
</body>
</html>
"""

def generate_courses_page():
    courses_html = ""
    for i, (cid, title, chapters, chapter_nums) in enumerate(COURSES, 1):
        icons = ["💻", "📊", "📈", "🎨", "📐", "🤖", "💼", "🎯"]
        levels = ["入门", "初级", "初级", "初级", "中级", "中级", "高级", "高级"]
        durations = ["8小时", "10小时", "12小时", "8小时", "10小时", "12小时", "15小时", "20小时"]
        icon = icons[i-1]
        level = levels[i-1]
        duration = durations[i-1]
        desc = {
            1: "从零开始学习Python编程语言",
            2: "学习使用NumPy进行高效的数值计算",
            3: "掌握Pandas库进行数据处理",
            4: "创建专业的数据可视化图表",
            5: "学习统计学基础和假设检验",
            6: "掌握常用机器学习算法",
            7: "将数据分析应用于商业场景",
            8: "综合项目案例实战演练",
        }[i]
        courses_html += f"""            <a href="{cid}.html" class="course-card">
                <div class="course-icon">{icon}</div>
                <h3 class="course-title">{title}</h3>
                <p class="course-desc">{desc}</p>
                <div class="course-meta">
                    <span class="tag">{level}</span>
                    <span class="duration">{duration}</span>
                    <span class="chapter-count">{len(chapters)}个章节</span>
                </div>
            </a>
"""
    nav = NAV_TEMPLATE.format(active_index='', active_courses=' class="active"', active_projects='')
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>课程体系 - 数析学院</title>
    <link rel="stylesheet" href="static/style.css">
</head>
<body>
    <div class="page-container">
        {nav}

        <h1 class="page-title">📚 课程体系</h1>
        <p class="page-subtitle">系统化的学习路径，从入门到精通</p>

        <div class="courses-grid">
{courses_html}        </div>
    </div>
</body>
</html>
"""

def generate_projects_page():
    projects_html = ""
    for title, desc, level, duration, skills in PROJECTS:
        skills_html = " ".join(f'<span class="tag">{s}</span>' for s in skills)
        projects_html += f"""            <div class="project-card">
                <h3 class="project-title">{title}</h3>
                <p class="project-desc">{desc}</p>
                <div class="project-meta">
                    <span class="tag">{level}</span>
                    <span class="duration">{duration}</span>
                </div>
                <div class="project-skills">{skills_html}</div>
            </div>
"""
    nav = NAV_TEMPLATE.format(active_index='', active_courses='', active_projects=' class="active"')
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>项目实战 - 数析学院</title>
    <link rel="stylesheet" href="static/style.css">
</head>
<body>
    <div class="page-container">
        {nav}

        <h1 class="page-title">🎯 项目实战</h1>
        <p class="page-subtitle">通过真实项目案例，积累实战经验</p>

        <div class="projects-grid">
{projects_html}        </div>
    </div>
</body>
</html>
"""

def generate_course_page(course_idx):
    cid, title, chapter_titles, chapter_nums = COURSES[course_idx]
    icons = ["💻", "📊", "📈", "🎨", "📐", "🤖", "💼", "🎯"]
    levels = ["入门", "初级", "初级", "初级", "中级", "中级", "高级", "高级"]
    durations = ["8小时", "10小时", "12小时", "8小时", "10小时", "12小时", "15小时", "20小时"]
    icon = icons[course_idx]
    level = levels[course_idx]
    duration = durations[course_idx]

    sidebar_html = ""
    for ci, (chapter_title, chapter_num) in enumerate(zip(chapter_titles, chapter_nums)):
        sidebar_html += f'<li><a href="chapter{chapter_num}.html"><span class="chapter-number">{ci+1:02d}</span> {chapter_title}</a></li>\n'

    nav = NAV_TEMPLATE.format(active_index='', active_courses=' class="active"', active_projects='')

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - 数析学院</title>
    <link rel="stylesheet" href="static/style.css">
</head>
<body>
    <div class="page-container">
        {nav}

        <div class="course-header">
            <div class="course-icon-large">{icon}</div>
            <h1 class="course-title-large">{title}</h1>
            <p class="course-desc-large">系统学习{title}，掌握数据分析核心技能</p>
            <div class="course-meta-large">
                <span class="tag">{level}</span>
                <span class="duration">{duration}</span>
                <span class="chapter-count">{len(chapter_titles)}个章节</span>
            </div>
            <a href="courses.html" class="back-btn">← 返回课程体系</a>
        </div>

        <h2 class="section-title">📖 课程章节</h2>
        <div class="chapter-list-container">
            <ul class="chapter-list-large">
{sidebar_html}            </ul>
        </div>
    </div>
</body>
</html>
"""

def generate_chapter_page(chapter_num):
    title, sections = CHAPTERS_DATA[chapter_num]

    # 找到所属课程
    course_idx = None
    chapter_in_course_idx = None
    for ci, (cid, ctitle, cchapters, cnums) in enumerate(COURSES):
        if chapter_num in cnums:
            course_idx = ci
            chapter_in_course_idx = cnums.index(chapter_num)
            break

    cid, course_title, course_chapters, course_chapter_nums = COURSES[course_idx]

    # 侧边栏
    sidebar_html = ""
    for ci, (ct, cn) in enumerate(zip(course_chapters, course_chapter_nums)):
        is_active = ' class="active"' if cn == chapter_num else ''
        sidebar_html += f'<li><a href="chapter{cn}.html"{is_active}"><span class="chapter-number">{ci+1:02d}</span> {ct}</a></li>\n'

    # 下一章
    next_chapter = None
    if chapter_in_course_idx < len(course_chapter_nums) - 1:
        next_num = course_chapter_nums[chapter_in_course_idx + 1]
        next_title = course_chapters[chapter_in_course_idx + 1]
        next_chapter = f'<a href="chapter{next_num}.html" class="next-chapter-btn">下一章：{next_title} →</a>'

    # 上一章
    prev_chapter = None
    if chapter_in_course_idx > 0:
        prev_num = course_chapter_nums[chapter_in_course_idx - 1]
        prev_title = course_chapters[chapter_in_course_idx - 1]
        prev_chapter = f'<a href="chapter{prev_num}.html" class="prev-chapter-btn">← 上一章：{prev_title}</a>'

    sections_html = ""
    for s in sections:
        sections_html += f"""                <div class="section-block">
                    <h3 class="section-title">{s}</h3>
                    <p class="section-content">本节介绍{s}的核心概念和应用方法。通过理论讲解和实例演示，帮助你理解并掌握相关知识。</p>
                </div>
"""

    nav = NAV_TEMPLATE.format(active_index='', active_courses=' class="active"', active_projects='')

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - 数析学院</title>
    <link rel="stylesheet" href="static/style.css">
</head>
<body>
    <div class="page-container">
        {nav}

        <div class="chapter-layout">
            <div class="sidebar">
                <div class="sidebar-title">章节目录</div>
                <ul class="chapter-list">
{sidebar_html}                </ul>
                <a href="{cid}.html" class="back-btn">← 返回课程</a>
                <a href="courses.html" class="back-btn">← 课程体系</a>
            </div>

            <div class="chapter-content">
                <h1 class="chapter-title">{title}</h1>
                <p class="chapter-subtitle">课程：{course_title}</p>

{sections_html}
                <div class="key-point">
                    <h4>💡 要点总结</h4>
                    <p>本章介绍了{title}的核心知识点，包括{sections[0]}、{sections[1]}等关键内容。</p>
                </div>

                <div class="tip-box">
                    <h4>✏️ 小贴士</h4>
                    <p>建议在学习时结合实际代码练习，理论结合实践是掌握数据分析技能的最佳方式。</p>
                </div>

                <div class="warn-box">
                    <h4>⚠️ 注意事项</h4>
                    <p>学习过程中遇到问题不要气馁，数据分析是实践性很强的技能，需要持续练习和积累。</p>
                </div>

                <div class="chapter-nav-bottom">
                    {prev_chapter if prev_chapter else ''}
                    <a href="index.html" class="home-btn">🏠 回到首页</a>
                    {next_chapter if next_chapter else ''}
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

def main():
    print("=" * 50)
    print("生成静态站点...")
    print("=" * 50)

    # 清理旧文件（保留 static 目录）
    html_files = [f for f in os.listdir(BUILD_DIR) if f.endswith('.html') and f not in ['111.html', 'deepseek_html_20260524_0487e5.html', 'index.html.old']]
    for f in html_files:
        os.remove(os.path.join(BUILD_DIR, f))
        print(f"  清理旧文件: {f}")

    # 生成页面
    files_generated = []

    # 首页
    index_html = generate_index()
    with open(os.path.join(BUILD_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    files_generated.append("index.html")

    # 课程体系页
    courses_html = generate_courses_page()
    with open(os.path.join(BUILD_DIR, "courses.html"), "w", encoding="utf-8") as f:
        f.write(courses_html)
    files_generated.append("courses.html")

    # 项目实战页
    projects_html = generate_projects_page()
    with open(os.path.join(BUILD_DIR, "projects.html"), "w", encoding="utf-8") as f:
        f.write(projects_html)
    files_generated.append("projects.html")

    # 课程详情页
    for i in range(8):
        html = generate_course_page(i)
        fname = f"course{i+1}.html"
        with open(os.path.join(BUILD_DIR, fname), "w", encoding="utf-8") as f:
            f.write(html)
        files_generated.append(fname)

    # 章节详情页
    for ch_num in range(1, 25):
        html = generate_chapter_page(ch_num)
        fname = f"chapter{ch_num}.html"
        with open(os.path.join(BUILD_DIR, fname), "w", encoding="utf-8") as f:
            f.write(html)
        files_generated.append(fname)

    print(f"\n✅ 生成完成！共 {len(files_generated)} 个页面")
    print(f"   - 首页: 1 个")
    print(f"   - 课程列表: 1 个")
    print(f"   - 项目列表: 1 个")
    print(f"   - 课程详情: 8 个")
    print(f"   - 章节详情: 24 个")
    print(f"\n   static/ 目录: CSS 样式文件")
    print(f"\n📂 站点根目录: {BUILD_DIR}")
    print(f"   入口文件: index.html")
    print(f"\n🌐 Cloudflare Pages 部署:")
    print(f"   Build command: (留空)")
    print(f"   Build output directory: / (或当前目录)")

    # 验证文件
    print(f"\n🔍 验证生成的文件:")
    for fname in sorted(files_generated)[:10]:
        size = os.path.getsize(os.path.join(BUILD_DIR, fname))
        print(f"   - {fname} ({size} bytes)")
    if len(files_generated) > 10:
        print(f"   ... 以及 {len(files_generated) - 10} 个其他文件")

if __name__ == "__main__":
    main()
