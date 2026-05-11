import os

COURSE_DIR = '/workspace/data-analytics-platform/course'

MODULE_PROJECT_MAP = {
    'module2': [
        {'id': 'project1', 'name': '销售数据清洗', 'difficulty': '初级', 'duration': '30分钟', 'desc': '清洗异常数据'},
        {'id': 'project2', 'name': '分组聚合分析', 'difficulty': '初级', 'duration': '25分钟', 'desc': '统计分析实战'},
    ],
    'module3': [
        {'id': 'project3', 'name': '购物篮分析', 'difficulty': '中级', 'duration': '40分钟', 'desc': '商品关联分析'},
        {'id': 'project4', 'name': '客户聚类分析', 'difficulty': '中级', 'duration': '45分钟', 'desc': '用户分群实战'},
        {'id': 'project7', 'name': '多数据集合并', 'difficulty': '中级', 'duration': '35分钟', 'desc': '多表关联操作'},
    ],
    'module4': [
        {'id': 'project5', 'name': '数据可视化', 'difficulty': '中级', 'duration': '35分钟', 'desc': '图表绘制实战'},
        {'id': 'project6', 'name': '时间序列分析', 'difficulty': '中级', 'duration': '40分钟', 'desc': '趋势预测分析'},
    ],
}

DIFFICULTY_COLORS = {
    '初级': {'bg': 'rgba(16, 185, 129, 0.15)', 'text': '#10b981'},
    '中级': {'bg': 'rgba(59, 130, 246, 0.15)', 'text': '#3b82f6'},
    '高级': {'bg': 'rgba(239, 68, 68, 0.15)', 'text': '#ef4444'},
}

def get_compact_cards(projects):
    cards_html = []
    for project in projects:
        diff_color = DIFFICULTY_COLORS.get(project['difficulty'], DIFFICULTY_COLORS['初级'])
        card = f'''
<div style="background:white;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,0.06);padding:1rem;transition:all 0.2s;">
    <h4 style="font-size:1rem;font-weight:700;color:#1e293b;margin:0 0 0.5rem 0;">{project['name']}</h4>
    <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.5rem;">
        <span style="padding:0.15rem 0.5rem;border-radius:9999px;font-size:0.65rem;font-weight:600;background:{diff_color['bg']};color:{diff_color['text']};">{project['difficulty']}</span>
        <span style="font-size:0.7rem;color:#94a3b8;">{project['duration']}</span>
    </div>
    <p style="font-size:0.75rem;color:#94a3b8;margin:0 0 0.75rem 0;">{project['desc']}</p>
    <a href="../../projects/{project['id']}.html" style="display:block;text-align:center;padding:0.45rem 1rem;background:linear-gradient(135deg,#3b82f6,#06b6d4);color:white;border-radius:6px;font-size:0.8rem;font-weight:500;text-decoration:none;">
        立即开始
    </a>
</div>
'''
        cards_html.append(card)
    return '\n'.join(cards_html)

def update_course_file(module_name, last_lesson_num):
    lesson_path = os.path.join(COURSE_DIR, module_name, f'lesson{last_lesson_num}.html')
    
    if not os.path.exists(lesson_path):
        print(f"文件不存在: {lesson_path}")
        return
    
    with open(lesson_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    start_marker = '<div style="max-width:1400px;margin:0 auto;padding:2rem;">'
    end_marker = '</div>\n</div>\n<script>'
    
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker, start_idx)
    
    if start_idx == -1 or end_idx == -1:
        print(f"未找到实战区域: {lesson_path}")
        return
    
    projects = MODULE_PROJECT_MAP.get(module_name, [])
    new_section = f'''
<div style="max-width:1400px;margin:0 auto;padding:1.5rem;">
<div style="padding:1.5rem;background:linear-gradient(135deg,#eff6ff,#f0fdf4);border-radius:10px;">
    <h3 style="font-size:1.1rem;font-weight:700;color:#1e293b;margin-bottom:1rem;">🎯 学完本章，去实战</h3>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:0.75rem;">
        {get_compact_cards(projects)}
    </div>
</div>
</div>
<script>
'''
    
    new_content = content[:start_idx] + new_section + content[end_idx + len(end_marker):]
    
    with open(lesson_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"已更新卡片: {lesson_path}")

def main():
    print("开始更新课程卡片...")
    
    update_course_file('module2', 7)
    update_course_file('module3', 7)
    update_course_file('module4', 5)
    
    print("更新完成！")

if __name__ == '__main__':
    main()