import os

COURSE_DIR = '/workspace/data-analytics-platform/course'
PROJECTS_DIR = '/workspace/data-analytics-platform/projects'

MODULE_PROJECT_MAP = {
    'module2': [
        {'id': 'project1', 'name': '销售数据清洗', 'difficulty': '初级', 'dataset': '电商销售数据'},
        {'id': 'project2', 'name': '分组聚合分析', 'difficulty': '初级', 'dataset': '销售订单数据'},
    ],
    'module3': [
        {'id': 'project3', 'name': '购物篮分析', 'difficulty': '中级', 'dataset': '电商交易数据'},
        {'id': 'project4', 'name': '客户聚类分析', 'difficulty': '中级', 'dataset': '客户行为数据'},
        {'id': 'project7', 'name': '多数据集合并', 'difficulty': '中级', 'dataset': '多表关联数据'},
    ],
    'module4': [
        {'id': 'project5', 'name': '数据可视化', 'difficulty': '中级', 'dataset': '销售统计数据'},
        {'id': 'project6', 'name': '时间序列分析', 'difficulty': '中级', 'dataset': '时序数据'},
    ],
}

PROJECT_COURSE_MAP = {
    'project1': [
        {'module': 'module2', 'lesson': 'lesson1', 'name': 'Pandas与Series'},
        {'module': 'module2', 'lesson': 'lesson2', 'name': 'DataFrame结构'},
        {'module': 'module2', 'lesson': 'lesson6', 'name': '缺失值与重复值'},
    ],
    'project2': [
        {'module': 'module2', 'lesson': 'lesson4', 'name': '数据查看方法'},
        {'module': 'module2', 'lesson': 'lesson5', 'name': '行列选取与筛选'},
        {'module': 'module2', 'lesson': 'lesson7', 'name': '类型转换与重命名'},
    ],
    'project3': [
        {'module': 'module3', 'lesson': 'lesson2', 'name': '字符串数据清洗'},
        {'module': 'module3', 'lesson': 'lesson6', 'name': '分组聚合groupby'},
    ],
    'project4': [
        {'module': 'module3', 'lesson': 'lesson1', 'name': '异常值识别与处理'},
        {'module': 'module3', 'lesson': 'lesson6', 'name': '分组聚合groupby'},
        {'module': 'module3', 'lesson': 'lesson7', 'name': '透视表实战'},
    ],
    'project5': [
        {'module': 'module4', 'lesson': 'lesson1', 'name': 'Matplotlib基础'},
        {'module': 'module4', 'lesson': 'lesson2', 'name': '常用图表类型'},
    ],
    'project6': [
        {'module': 'module3', 'lesson': 'lesson3', 'name': '时间日期处理'},
        {'module': 'module4', 'lesson': 'lesson3', 'name': '分布分析图表'},
    ],
    'project7': [
        {'module': 'module3', 'lesson': 'lesson5', 'name': '多表合并'},
    ],
    'project8': [
        {'module': 'module2', 'lesson': 'lesson3', 'name': '读取各类数据'},
        {'module': 'module3', 'lesson': 'lesson4', 'name': '新增字段与分箱'},
    ],
    'project9': [
        {'module': 'module3', 'lesson': 'lesson3', 'name': '时间日期处理'},
        {'module': 'module4', 'lesson': 'lesson2', 'name': '常用图表类型'},
    ],
    'project10': [
        {'module': 'module3', 'lesson': 'lesson6', 'name': '分组聚合groupby'},
        {'module': 'module4', 'lesson': 'lesson5', 'name': '业务报表实战'},
    ],
}

DIFFICULTY_COLORS = {
    '初级': {'bg': 'rgba(16, 185, 129, 0.15)', 'text': '#10b981', 'border': '#10b981'},
    '中级': {'bg': 'rgba(59, 130, 246, 0.15)', 'text': '#3b82f6', 'border': '#3b82f6'},
    '高级': {'bg': 'rgba(239, 68, 68, 0.15)', 'text': '#ef4444', 'border': '#ef4444'},
}

def get_project_cards(projects):
    cards_html = []
    for project in projects:
        diff_color = DIFFICULTY_COLORS.get(project['difficulty'], DIFFICULTY_COLORS['初级'])
        card = f'''
<div style="background:white;border-radius:12px;box-shadow:0 4px 12px rgba(0,0,0,0.08);padding:1.5rem;transition:transform 0.2s,box-shadow 0.2s;">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1rem;">
        <h4 style="font-size:1rem;font-weight:600;color:#1e293b;margin:0;">{project['name']}</h4>
        <span style="padding:0.25rem 0.75rem;border-radius:9999px;font-size:0.75rem;font-weight:600;background:{diff_color['bg']};color:{diff_color['text']};">{project['difficulty']}</span>
    </div>
    <div style="display:flex;align-items:center;gap:0.5rem;color:#64748b;font-size:0.85rem;margin-bottom:1.25rem;">
        <i class="fas fa-database"></i>
        <span>{project['dataset']}</span>
    </div>
    <a href="../../projects/{project['id']}.html" style="display:inline-flex;align-items:center;justify-content:center;gap:0.5rem;padding:0.625rem 1.25rem;background:linear-gradient(135deg,#3b82f6,#06b6d4);color:white;border-radius:8px;font-size:0.9rem;font-weight:500;text-decoration:none;transition:all 0.2s;">
        <i class="fas fa-arrow-right"></i> 去练习
    </a>
</div>
'''
        cards_html.append(card)
    return '\n'.join(cards_html)

def get_prerequisite_section(courses):
    links_html = []
    for course in courses:
        link = f'''
<a href="../course/{course['module']}/{course['lesson']}.html" style="display:flex;align-items:center;gap:0.5rem;padding:0.5rem 0.75rem;background:white;border-radius:6px;color:#3b82f6;text-decoration:none;font-size:0.9rem;margin-bottom:0.5rem;transition:all 0.2s;">
    <i class="fas fa-book-open"></i>
    <span>{course['name']}</span>
</a>
'''
        links_html.append(link)
    return '\n'.join(links_html)

def add_practice_section_to_module(module_name, last_lesson_num):
    lesson_path = os.path.join(COURSE_DIR, module_name, f'lesson{last_lesson_num}.html')
    
    if not os.path.exists(lesson_path):
        print(f"文件不存在: {lesson_path}")
        return
    
    with open(lesson_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '学完本章，去实战' in content:
        print(f"已存在实战区域: {lesson_path}")
        return
    
    projects = MODULE_PROJECT_MAP.get(module_name, [])
    if not projects:
        return
    
    practice_section = f'''
</main>
</div>
<div style="max-width:1400px;margin:0 auto;padding:2rem;">
<div style="padding:2rem;background:linear-gradient(135deg,#eff6ff,#f0fdf4);border-radius:12px;">
    <h3 style="font-size:1.25rem;font-weight:700;color:#1e293b;margin-bottom:1.5rem;">🎯 学完本章，去实战</h3>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:1rem;">
        {get_project_cards(projects)}
    </div>
</div>
</div>
<script>
'''
    
    content = content.replace('</main>\n</div>\n<script>', practice_section)
    
    with open(lesson_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"已添加实战区域: {lesson_path}")

def add_prerequisite_to_project(project_name):
    project_path = os.path.join(PROJECTS_DIR, f'{project_name}.html')
    
    if not os.path.exists(project_path):
        print(f"文件不存在: {project_path}")
        return
    
    with open(project_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '📚 前置课程' in content:
        print(f"已存在前置课程区域: {project_path}")
        return
    
    courses = PROJECT_COURSE_MAP.get(project_name, [])
    if not courses:
        return
    
    prerequisite_section = f'''
        <div class="project-container">
            <div class="project-sidebar">
                <div style="background:#fef3c7;border-left:4px solid #f59e0b;border-radius:0 8px 8px 0;padding:1rem;margin-bottom:1rem;">
                    <h3 style="font-size:0.95rem;font-weight:600;color:#92400e;margin-bottom:0.75rem;">📚 前置课程</h3>
                    <div style="display:flex;flex-direction:column;">
                        {get_prerequisite_section(courses)}
                    </div>
                </div>
    '''
    
    content = content.replace('<div class="project-container">', prerequisite_section)
    
    with open(project_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"已添加前置课程区域: {project_path}")

def main():
    print("开始添加课程与项目关联...")
    
    print("\n=== 在课程小节添加实战推荐 ===")
    add_practice_section_to_module('module2', 7)
    add_practice_section_to_module('module3', 7)
    add_practice_section_to_module('module4', 5)
    
    print("\n=== 在项目页面添加前置课程 ===")
    for project in PROJECT_COURSE_MAP.keys():
        add_prerequisite_to_project(project)
    
    print("\n关联完成！")

if __name__ == '__main__':
    main()