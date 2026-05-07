#!/usr/bin/env python3
import os

def enhance_features():
    html_path = "/workspace/data-analytics-platform/index.html"
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 在每个项目卡片顶部添加登录提示
    login_prompt = '''<div class="project-login-prompt" style="display:none; background: linear-gradient(135deg, #fffbeb, #fef3c7); padding: 0.5rem 0.75rem; border-radius: 8px 8px 0 0; margin: -1.5rem -1.5rem 1rem -1.5rem; text-align: center;">
                <span style="font-size: 0.75rem; color: #92400e; display: flex; align-items: center; justify-content: center; gap: 0.375rem;">
                    <i class="fas fa-info-circle"></i>
                    登录后保存学习进度
                </span>
            </div>'''
    
    # 在每个项目卡片的开始处插入登录提示
    # 我们需要在 <div class="project-card-new"> 后面插入
    count = 0
    while '<div class="project-card-new">' in content and count < 10:
        content = content.replace('<div class="project-card-new">', 
                                '<div class="project-card-new">\n                ' + login_prompt, 1)
        count += 1
    
    # 2. 添加JavaScript来控制登录提示的显示
    js_code = '''
    <script>
        // 检查登录状态并显示提示
        function checkLoginStatus() {
            const currentUser = JSON.parse(localStorage.getItem('currentUser') || 'null');
            const prompts = document.querySelectorAll('.project-login-prompt');
            
            if (!currentUser) {
                // 未登录，显示提示
                prompts.forEach(prompt => {
                    prompt.style.display = 'block';
                });
            } else {
                // 已登录，隐藏提示
                prompts.forEach(prompt => {
                    prompt.style.display = 'none';
                });
            }
        }
        
        // 页面加载时检查
        document.addEventListener('DOMContentLoaded', checkLoginStatus);
        
        // 监听登录状态变化
        window.addEventListener('storage', checkLoginStatus);
    </script>'''
    
    # 在 </body> 之前插入JavaScript
    content = content.replace('</body>', js_code + '\n</body>')
    
    # 3. 增强CSS样式
    css_enhancement = '''
    <style>
        .project-login-prompt {
            transition: all 0.3s ease;
        }
        
        .project-login-prompt:hover {
            background: linear-gradient(135deg, #fef3c7, #fde68a) !important;
        }
        
        /* 增强导航栏进度显示 */
        .navbar-auth {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .user-profile {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.5rem 1rem;
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.08), rgba(139, 92, 246, 0.08));
            border-radius: 9999px;
            border: 1px solid rgba(59, 130, 246, 0.1);
        }
        
        .user-profile.hidden {
            display: none;
        }
        
        .avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            border: 2px solid var(--primary-color);
        }
        
        #user-name {
            font-weight: 600;
            color: var(--text-primary);
        }
        
        .user-progress-info {
            display: flex;
            align-items: center;
            gap: 0.375rem;
            padding: 0.375rem 0.75rem;
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(6, 182, 212, 0.1));
            border-radius: 9999px;
            font-size: 0.875rem;
            color: var(--success-color);
            font-weight: 600;
        }
        
        .user-progress-info.hidden {
            display: none;
        }
        
        .user-progress-info i {
            font-size: 0.75rem;
        }
        
        .logout-btn {
            padding: 0.5rem 1rem;
            background: var(--danger-color);
            color: white;
            border: none;
            border-radius: var(--border-radius);
            font-size: 0.875rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .logout-btn:hover {
            background: #dc2626;
            transform: translateY(-1px);
        }
        
        /* 增强按钮样式 */
        .auth-btn {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.625rem 1.25rem;
            border: none;
            border-radius: var(--border-radius);
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .login-btn {
            background: transparent;
            color: var(--primary-color);
            border: 2px solid var(--primary-color);
        }
        
        .login-btn:hover {
            background: rgba(59, 130, 246, 0.08);
            transform: translateY(-2px);
        }
        
        .register-btn {
            background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
            color: white;
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
        }
        
        .register-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
        }
    </style>
    '''
    
    # 在 <style> 标签之后插入增强样式
    content = content.replace('</style>', css_enhancement + '\n    </style>')
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 交互效果增强完成！")

if __name__ == "__main__":
    enhance_features()
