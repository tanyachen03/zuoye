#!/usr/bin/env python3
import os

def update_css():
    css_path = "/workspace/data-analytics-platform/styles.css"
    
    with open(css_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 添加技能标签样式
    skill_tags_style = '''
/* ==================== 技能标签样式 ==================== */
.skill-tags {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-bottom: 0.75rem;
}

.skill-tags span {
    padding: 0.25rem 0.625rem;
    font-size: 0.75rem;
    font-weight: 500;
    border-radius: 9999px;
    color: white;
    transition: all 0.2s ease;
}

.skill-tags span:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
'''
    
    # 在文件末尾添加技能标签样式
    content += skill_tags_style
    
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 技能标签CSS样式添加完成！")

if __name__ == "__main__":
    update_css()
