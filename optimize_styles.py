#!/usr/bin/env python3
import os

def update_styles():
    css_path = "/workspace/data-analytics-platform/styles.css"
    
    with open(css_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 更新CSS变量
    content = content.replace(
        ''':root {
    --primary-color: #1e40af;
    --primary-light: #3b82f6;
    --primary-dark: #1e3a8a;
    --secondary-color: #60a5fa;
    --accent-color: #06b6d4;
    --success-color: #10b981;
    --warning-color: #f59e0b;
    --danger-color: #ef4444;
    --bg-light: #f8fafc;
    --bg-white: #ffffff;
    --text-primary: #1e293b;
    --text-secondary: #64748b;
    --border-color: #e2e8f0;
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}''',
        ''':root {
    /* Modern Color Palette */
    --primary-color: #3b82f6;
    --primary-light: #60a5fa;
    --primary-dark: #2563eb;
    --secondary-color: #8b5cf6;
    --accent-color: #06b6d4;
    --success-color: #10b981;
    --warning-color: #f59e0b;
    --danger-color: #ef4444;
    
    /* Background Colors */
    --bg-light: #f8fafc;
    --bg-white: #ffffff;
    --bg-gradient-start: #eff6ff;
    --bg-gradient-end: #f8fafc;
    
    /* Text Colors */
    --text-primary: #1e293b;
    --text-secondary: #64748b;
    --text-muted: #94a3b8;
    
    /* Border & Shadow */
    --border-color: #e2e8f0;
    --border-radius: 12px;
    --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.08);
    --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.08);
    --shadow-lg: 0 10px 25px rgba(0, 0, 0, 0.1);
    --shadow-xl: 0 20px 35px rgba(0, 0, 0, 0.12);
}'''
    )
    
    # 更新body样式
    content = content.replace(
        '''body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    line-height: 1.6;
    color: var(--text-primary);
    background-color: var(--bg-light);
}''',
        '''body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    line-height: 1.7;
    color: var(--text-primary);
    background-color: var(--bg-light);
    font-size: 16px;
}'''
    )
    
    # 更新navbar样式
    content = content.replace(
        '''.navbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
    background-color: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    box-shadow: var(--shadow-sm);
    transition: all 0.3s ease;
}''',
        '''.navbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
    background-color: rgba(255, 255, 255, 0.98);
    backdrop-filter: blur(20px);
    box-shadow: var(--shadow-sm);
    transition: all 0.3s ease;
}'''
    )
    
    # 更新navbar-logo样式
    content = content.replace(
        '''.navbar-logo {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--primary-color);
    cursor: pointer;
}

.navbar-logo i {
    font-size: 1.75rem;
}''',
        '''.navbar-logo {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--primary-color);
    cursor: pointer;
    transition: transform 0.2s ease;
}

.navbar-logo:hover {
    transform: scale(1.02);
}

.navbar-logo i {
    font-size: 1.75rem;
}'''
    )
    
    # 更新nav-link样式
    content = content.replace(
        '''.nav-link {
    text-decoration: none;
    color: var(--text-secondary);
    font-weight: 500;
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
    transition: all 0.2s ease;
}

.nav-link:hover,
.nav-link.active {
    color: var(--primary-color);
    background-color: rgba(30, 64, 175, 0.05);
}''',
        '''.nav-link {
    text-decoration: none;
    color: var(--text-secondary);
    font-weight: 500;
    padding: 0.5rem 1rem;
    border-radius: var(--border-radius);
    transition: all 0.2s ease;
    position: relative;
}

.nav-link:hover,
.nav-link.active {
    color: var(--primary-color);
    background-color: rgba(59, 130, 246, 0.08);
}'''
    )
    
    # 更新course-card样式
    content = content.replace(
        '''.course-card {
    background-color: white;
    border-radius: 1rem;
    padding: 2rem;
    box-shadow: var(--shadow-sm);
    transition: all 0.3s ease;
    cursor: pointer;
    border: 1px solid var(--border-color);
}

.course-card:hover {
    transform: translateY(-5px);
    box-shadow: var(--shadow-lg);
    border-color: var(--primary-color);
}''',
        '''.course-card {
    background-color: white;
    border-radius: var(--border-radius);
    padding: 2rem;
    box-shadow: var(--shadow-md);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
    border: 1px solid transparent;
}

.course-card:hover {
    transform: translateY(-8px);
    box-shadow: var(--shadow-xl);
    border-color: var(--primary-light);
}'''
    )
    
    # 更新course-icon样式
    content = content.replace(
        '''.course-icon {
    width: 70px;
    height: 70px;
    background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
    border-radius: 1rem;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 1.5rem;
}

.course-icon i {
    font-size: 2.5rem;
    color: white;
}''',
        '''.course-icon {
    width: 70px;
    height: 70px;
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    border-radius: 1rem;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    transition: transform 0.3s ease;
}

.course-card:hover .course-icon {
    transform: scale(1.05);
}

.course-icon i {
    font-size: 2.5rem;
    color: white;
}'''
    )
    
    # 更新tag样式
    content = content.replace(
        '''.tag {
    padding: 0.375rem 0.875rem;
    background-color: rgba(30, 64, 175, 0.05);
    color: var(--primary-color);
    font-size: 0.8125rem;
    font-weight: 500;
    border-radius: 9999px;
}''',
        '''.tag {
    padding: 0.375rem 0.875rem;
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.08), rgba(139, 92, 246, 0.08));
    color: var(--primary-color);
    font-size: 0.8125rem;
    font-weight: 500;
    border-radius: 9999px;
    transition: all 0.2s ease;
}

.tag:hover {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(139, 92, 246, 0.15));
}'''
    )
    
    # 更新section-header样式
    content = content.replace(
        '''.section-header {
    text-align: center;
    margin-bottom: 4rem;
}

.section-header h2 {
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 1rem;
}

.section-header p {
    font-size: 1.125rem;
    color: var(--text-secondary);
}''',
        '''.section-header {
    text-align: center;
    margin-bottom: 4rem;
}

.section-header h2 {
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 1rem;
    background: linear-gradient(135deg, var(--text-primary), var(--text-secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.section-header p {
    font-size: 1.125rem;
    color: var(--text-secondary);
}'''
    )
    
    # 更新footer样式
    content = content.replace(
        '''.footer {
    background-color: var(--text-primary);
    color: white;
    padding: 4rem 2rem;
}''',
        '''.footer {
    background: linear-gradient(135deg, #1e293b, #334155);
    color: white;
    padding: 4rem 2rem;
}'''
    )
    
    # 更新submit-btn样式
    content = content.replace(
        '''.submit-btn {
    width: 100%;
    padding: 1rem;
    background-color: var(--primary-color);
    color: white;
    border: none;
    border-radius: 0.5rem;
    font-weight: 600;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.2s ease;
}

.submit-btn:hover {
    background-color: var(--primary-dark);
    transform: translateY(-1px);
    box-shadow: var(--shadow-md);
}''',
        '''.submit-btn {
    width: 100%;
    padding: 1rem;
    background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
    color: white;
    border: none;
    border-radius: var(--border-radius);
    font-weight: 600;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
}

.submit-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
}'''
    )
    
    # 更新achievement-card样式
    content = content.replace(
        '''.achievement-card {
    background-color: rgba(255, 255, 255, 0.95);
    border-radius: 1rem;
    padding: 2rem;
    text-align: center;
    border: 2px solid var(--border-color);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}''',
        '''.achievement-card {
    background-color: white;
    border-radius: var(--border-radius);
    padding: 2rem;
    text-align: center;
    border: 2px solid transparent;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow-md);
}'''
    )
    
    # 更新achievement-icon样式
    content = content.replace(
        '''.achievement-icon {
    width: 80px;
    height: 80px;
    background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 0 auto 1.5rem;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(30, 64, 175, 0.3);
}

.achievement-icon i {
    font-size: 2.5rem;
    color: white;
}''',
        '''.achievement-icon {
    width: 80px;
    height: 80px;
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 0 auto 1.5rem;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);
}

.achievement-card:hover .achievement-icon {
    transform: scale(1.1);
    box-shadow: 0 12px 35px rgba(59, 130, 246, 0.4);
}

.achievement-icon i {
    font-size: 2.5rem;
    color: white;
}'''
    )
    
    # 更新modal-content样式
    content = content.replace(
        '''.modal-content {
    background-color: white;
    border-radius: 1rem;
    width: 100%;
    max-width: 450px;
    overflow: hidden;
    box-shadow: var(--shadow-xl);
    animation: slideUp 0.3s ease;
}''',
        '''.modal-content {
    background-color: white;
    border-radius: var(--border-radius);
    width: 100%;
    max-width: 450px;
    overflow: hidden;
    box-shadow: var(--shadow-xl);
    animation: slideUp 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}'''
    )
    
    # 更新form-group input样式
    content = content.replace(
        '''.form-group input {
    width: 100%;
    padding: 0.875rem 1rem;
    border: 1px solid var(--border-color);
    border-radius: 0.5rem;
    font-size: 1rem;
    transition: all 0.2s ease;
    outline: none;
}

.form-group input:focus {
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px rgba(30, 64, 175, 0.1);
}''',
        '''.form-group input {
    width: 100%;
    padding: 0.875rem 1rem;
    border: 2px solid var(--border-color);
    border-radius: var(--border-radius);
    font-size: 1rem;
    transition: all 0.3s ease;
    outline: none;
}

.form-group input:focus {
    border-color: var(--primary-color);
    box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
}'''
    )
    
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ CSS样式优化完成！")

if __name__ == "__main__":
    update_styles()
