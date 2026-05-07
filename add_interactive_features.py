#!/usr/bin/env python3
import os

def add_interactive_features():
    html_path = "/workspace/data-analytics-platform/index.html"
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 添加项目筛选器
    filter_html = '''        <!-- 项目筛选器 -->
        <div class="project-filter">
            <button class="filter-btn active" data-filter="all">全部</button>
            <button class="filter-btn" data-filter="beginner">入门</button>
            <button class="filter-btn" data-filter="intermediate">进阶</button>
            <button class="filter-btn" data-filter="advanced">高级</button>
        </div>

        <div class="projects-grid">'''
    
    # 在 <div class="projects-grid"> 之前插入筛选器
    content = content.replace('<div class="projects-grid">', filter_html)
    
    # 2. 为每个项目卡片添加ID和进行中标签
    # 找到 <div class="project-card beginner"> 并添加ID
    for i in range(1, 11):
        difficulties = {
            1: 'beginner', 2: 'beginner', 3: 'intermediate', 4: 'intermediate',
            5: 'intermediate', 6: 'intermediate', 7: 'intermediate', 8: 'intermediate',
            9: 'beginner', 10: 'advanced'
        }
        difficulty = difficulties[i]
        
        # 添加卡片ID
        old_card = f'<div class="project-card {difficulty}">'
        new_card = f'<div class="project-card {difficulty}" id="project-card-{i}">'
        content = content.replace(old_card, new_card, 1)  # 只替换第一个匹配
        
        # 在卡片顶部添加进行中标签（初始隐藏）
        progress_tag = f'''<div class="progress-tag" id="progress-{i}" style="display:none;">
                    <i class="fas fa-spinner fa-spin"></i> 进行中
                </div>
                <div class="project-card {difficulty}" id="project-card-{i}">'''
        new_card_with_tag = f'''<div class="project-card {difficulty}" id="project-card-{i}">'''
        content = content.replace(new_card_with_tag, progress_tag.replace(f'<div class="project-card {difficulty}" id="project-card-{i}">', ''))
    
    # 3. 添加悬浮咨询按钮
    floating_btn = '''    <!-- 悬浮咨询按钮 -->
    <div class="floating-btn" id="consultation-btn">
        <button onclick="showConsultationModal()">
            <i class="fas fa-comments"></i>
            <span>咨询报名</span>
        </button>
    </div>

    <!-- 咨询表单弹窗 -->
    <div id="consultation-modal" class="modal hidden">
        <div class="modal-content">
            <div class="modal-header">
                <h3>咨询报名</h3>
                <button class="modal-close" onclick="closeModal('consultation-modal')">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <form id="consultation-form">
                <div class="form-group">
                    <label>姓名</label>
                    <input type="text" id="consult-name" required>
                </div>
                <div class="form-group">
                    <label>邮箱</label>
                    <input type="email" id="consult-email" required>
                </div>
                <div class="form-group">
                    <label>手机号（选填）</label>
                    <input type="tel" id="consult-phone">
                </div>
                <div class="form-group">
                    <label>想咨询的问题</label>
                    <textarea id="consult-question" rows="4" style="width:100%; padding:0.875rem 1rem; border:2px solid var(--border-color); border-radius:var(--border-radius); font-size:1rem; resize:vertical; outline:none;"></textarea>
                </div>
                <button type="submit" class="submit-btn">提交咨询</button>
            </form>
        </div>
    </div>
'''
    
    # 在 </footer> 之后插入悬浮按钮
    content = content.replace('</footer>\n\n    <!-- 登录弹窗 -->', f'</footer>\n\n{floating_btn}\n\n    <!-- 登录弹窗 -->')
    
    # 4. 添加CSS样式
    css_styles = '''
        /* 项目筛选器样式 */
        .project-filter {
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-bottom: 2rem;
            flex-wrap: wrap;
        }

        .filter-btn {
            padding: 0.625rem 1.5rem;
            border: 2px solid var(--border-color);
            border-radius: var(--border-radius);
            background: white;
            color: var(--text-secondary);
            font-weight: 600;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .filter-btn:hover {
            border-color: var(--primary-color);
            color: var(--primary-color);
            transform: translateY(-2px);
        }

        .filter-btn.active {
            background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
            border-color: var(--primary-color);
            color: white;
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
        }

        /* 项目卡片进行中标签 */
        .progress-tag {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.9), rgba(6, 182, 212, 0.9));
            color: white;
            padding: 0.5rem;
            text-align: center;
            font-size: 13px;
            font-weight: 600;
            border-radius: 10px 10px 0 0;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            z-index: 10;
        }

        .project-card {
            position: relative;
        }

        /* 悬浮咨询按钮 */
        .floating-btn {
            position: fixed;
            bottom: 30px;
            right: 30px;
            z-index: 999;
        }

        .floating-btn button {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 1rem 1.5rem;
            background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
            color: white;
            border: none;
            border-radius: 50px;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
            transition: all 0.3s ease;
        }

        .floating-btn button:hover {
            transform: translateY(-5px) scale(1.05);
            box-shadow: 0 12px 35px rgba(59, 130, 246, 0.5);
        }

        .floating-btn button i {
            font-size: 1.25rem;
        }

        /* 响应式悬浮按钮 */
        @media (max-width: 768px) {
            .floating-btn {
                bottom: 20px;
                right: 20px;
            }

            .floating-btn button {
                padding: 0.875rem 1.25rem;
                font-size: 14px;
            }

            .floating-btn button span {
                display: none;
            }

            .floating-btn button {
                padding: 1rem;
                border-radius: 50%;
            }
        }

        /* 隐藏的项目卡片 */
        .project-card.hidden {
            display: none !important;
        }

        /* 筛选动画 */
        .project-card {
            animation: fadeIn 0.3s ease;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
'''
    
    # 在 </style> 之前插入CSS
    content = content.replace('</style>', css_styles + '\n    </style>')
    
    # 5. 添加JavaScript功能
    js_code = '''
        // 项目筛选功能
        function initProjectFilter() {
            const filterBtns = document.querySelectorAll('.filter-btn');
            const projectCards = document.querySelectorAll('.project-card');

            filterBtns.forEach(btn => {
                btn.addEventListener('click', function() {
                    // 更新按钮状态
                    filterBtns.forEach(b => b.classList.remove('active'));
                    this.classList.add('active');

                    // 筛选项目
                    const filter = this.getAttribute('data-filter');
                    projectCards.forEach(card => {
                        if (filter === 'all' || card.classList.contains(filter)) {
                            card.classList.remove('hidden');
                        } else {
                            card.classList.add('hidden');
                        }
                    });
                });
            });
        }

        // 学习进度记录功能
        function initProgressTracking() {
            const startBtns = document.querySelectorAll('.start-btn');
            const progressKey = 'learning_progress';

            // 加载保存的进度
            loadProgress();

            // 为每个开始按钮添加点击事件
            startBtns.forEach((btn, index) => {
                btn.addEventListener('click', function() {
                    const projectId = index + 1;
                    saveProgress(projectId);
                });
            });
        }

        function saveProgress(projectId) {
            const progressKey = 'learning_progress';
            let progress = JSON.parse(localStorage.getItem(progressKey) || '{}');
            
            progress[projectId] = {
                status: 'in_progress',
                startTime: new Date().toISOString()
            };
            
            localStorage.setItem(progressKey, JSON.stringify(progress));
            loadProgress();
        }

        function loadProgress() {
            const progressKey = 'learning_progress';
            const progress = JSON.parse(localStorage.getItem(progressKey) || '{}');
            
            for (let projectId in progress) {
                const progressTag = document.getElementById(`progress-${projectId}`);
                if (progressTag && progress[projectId].status === 'in_progress') {
                    progressTag.style.display = 'flex';
                }
            }
        }

        // 显示咨询弹窗
        function showConsultationModal() {
            document.getElementById('consultation-modal').classList.remove('hidden');
        }

        // 页面加载完成后初始化
        document.addEventListener('DOMContentLoaded', function() {
            initProjectFilter();
            initProgressTracking();
        });
    '''
    
    # 在 </script> 之前添加新功能
    content = content.replace('</script>', js_code + '\n    </script>')
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 交互功能添加完成！")

if __name__ == "__main__":
    add_interactive_features()
