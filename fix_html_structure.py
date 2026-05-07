#!/usr/bin/env python3
import os

def fix_html_structure():
    html_path = "/workspace/data-analytics-platform/index.html"
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修复进度标签的位置 - 应该在project-card内部
    # 当前进度标签在project-card外部，需要修复
    
    # 查找所有进度标签
    import re
    progress_tags = re.findall(r'<div class="progress-tag"[^>]*>.*?</div>\s*<div class="project-card[^>]*>', content, re.DOTALL)
    
    print(f"找到 {len(progress_tags)} 个进度标签")
    
    # 修复每个项目卡片的结构
    for i in range(1, 11):
        # 找到错误的结构：progress-tag 在 project-card 外面
        wrong_pattern = f'''<div class="progress-tag" id="progress-{i}"[^>]*>.*?</div>
                
                <div class="project-card'''
        
        correct_pattern = f'''<div class="project-card'''
        
        # 使用正则表达式替换
        pattern = f'<div class="progress-tag" id="progress-{i}".*?</div>\\s*\\n\\s*\\n\\s*<div class="project-card'
        replacement = '<div class="project-card'
        
        content = re.sub(pattern, replacement, content, flags=re.DOTALL, count=1)
    
    # 更新底部信息栏 - 版权年份
    content = content.replace('© 2024', '© 2025')
    
    # 添加联系信息和更新日志
    old_footer = '''<div class="footer-section">
                <h4>联系我们</h4>
                <ul>
                    <li>咨询邮箱：contact@dataschool.com</li>
                    <li>工作时间：周一至周五 9:00-18:00</li>
                </ul>
            </div>'''
    
    new_footer = '''<div class="footer-section">
                <h4>联系我们</h4>
                <ul>
                    <li>📧 邮箱：contact@dataschool.com</li>
                    <li>⏰ 工作时间：周一至周五 9:00-18:00</li>
                    <li>📝 <a href="#consultation" onclick="showConsultationModal()">在线咨询</a></li>
                </ul>
            </div>
            <div class="footer-section">
                <h4>其他信息</h4>
                <ul>
                    <li>📖 <a href="#changelog">更新日志</a></li>
                    <li>📜 <a href="#privacy">隐私政策</a></li>
                    <li>📋 <a href="#terms">使用条款</a></li>
                </ul>
            </div>'''
    
    content = content.replace(old_footer, new_footer)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ HTML结构修复完成！")

if __name__ == "__main__":
    fix_html_structure()
