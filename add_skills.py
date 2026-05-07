#!/usr/bin/env python3
import os

def update_index():
    html_path = "/workspace/data-analytics-platform/index.html"
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 定义每个项目的技能标签
    projects_skills = {
        "project1.html": ["Pandas", "数据清洗", "数据预处理"],
        "project2.html": ["Pandas", "groupby聚合", "数据可视化"],
        "project3.html": ["Pandas", "漏斗分析", "用户路径"],
        "project4.html": ["Pandas", "RFM模型", "客户分群"],
        "project5.html": ["Pandas", "Apriori算法", "关联规则"],
        "project6.html": ["Pandas", "统计检验", "转化率分析"],
        "project7.html": ["Pandas", "时间序列", "趋势分析"],
        "project8.html": ["Pandas", "留存分析", "cohort分析"],
        "project9.html": ["Matplotlib", "Seaborn", "数据可视化"],
        "project10.html": ["Pandas", "移动平均", "趋势预测"]
    }
    
    # 生成技能标签HTML
    def generate_skill_tags(skills):
        tags_html = '<div class="skill-tags" style="display:flex; gap:0.5rem; flex-wrap:wrap; margin-bottom:0.75rem;">'
        colors = [
            "background: linear-gradient(135deg, #3b82f6, #60a5fa);",
            "background: linear-gradient(135deg, #10b981, #34d399);",
            "background: linear-gradient(135deg, #8b5cf6, #a78bfa);",
            "background: linear-gradient(135deg, #f59e0b, #fbbf24);",
            "background: linear-gradient(135deg, #ef4444, #f87171);"
        ]
        
        for i, skill in enumerate(skills):
            color = colors[i % len(colors)]
            tags_html += f'''<span style="padding:0.25rem 0.625rem; {color} color:white; font-size:0.75rem; font-weight:500; border-radius:9999px;">{skill}</span>'''
        
        tags_html += '</div>'
        return tags_html
    
    # 为每个项目更新技能标签
    for i in range(1, 11):
        filename = f"project{i}.html"
        skill_tags = generate_skill_tags(projects_skills[filename])
        
        # 找到对应的卡片并插入技能标签
        old_pattern = f'''<div class="project-meta">
                    <span class="meta-item"><i class="fas fa-clock"></i> '''
        
        if old_pattern in content:
            # 找到所有匹配的位置
            import re
            pattern = re.compile(old_pattern)
            matches = list(pattern.finditer(content))
            
            # 找到对应项目的卡片（通过数据集名称）
            dataset_patterns = {
                "project1.html": "sales_data.csv",
                "project2.html": "store_sales.csv",
                "project3.html": "user_behavior.csv",
                "project4.html": "customer_data.csv",
                "project5.html": "basket_data.csv",
                "project6.html": "ab_test.csv",
                "project7.html": "time_series.csv",
                "project8.html": "retention.csv",
                "project9.html": "visualization.csv",
                "project10.html": "forecast_data.csv"
            }
            
            dataset = dataset_patterns[filename]
            
            # 在对应的数据集名称之前插入技能标签
            insert_point = f'''<div class="dataset-name">{dataset}</div>'''
            new_content = skill_tags + f'\n                ' + insert_point
            
            content = content.replace(insert_point, new_content, 1)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 项目技能标签添加完成！")

if __name__ == "__main__":
    update_index()
