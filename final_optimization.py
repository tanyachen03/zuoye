#!/usr/bin/env python3
import os

def final_optimization():
    html_path = "/workspace/data-analytics-platform/index.html"
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. SEO优化 - 更新meta标签
    old_meta = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
    new_meta = '''<meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="无需安装，在线运行Pandas代码，掌握数据清洗、可视化、AB测试、时序分析等核心技能，10个实战项目可写入简历">
    <meta name="keywords" content="Pandas,数据分析,Python,数据可视化,数据清洗,AB测试,时间序列">
    <meta name="author" content="数析学院">
    <meta name="robots" content="index, follow">'''
    
    content = content.replace(old_meta, new_meta)
    
    # 2. 更新title标签
    old_title = '<title>Pandas 数据分析实战训练营 - 数析学院</title>'
    new_title = '<title>Pandas 数据分析实战训练营｜10个项目浏览器在线练 - 数析学院</title>'
    content = content.replace(old_title, new_title)
    
    # 3. 确保h1层级正确
    old_h1 = '<h1>Pandas 数据分析实战训练营</h1>'
    new_h1 = '''<h1>Pandas 数据分析实战训练营</h1>'''
    content = content.replace(old_h1, new_h1)
    
    # 4. 添加增强的响应式CSS
    responsive_css = '''
        /* 增强的响应式设计 */
        @media (max-width: 768px) {
            /* 基础调整 */
            html {
                font-size: 14px;
            }

            body {
                font-size: 14px;
            }

            /* 英雄区域优化 */
            .hero {
                padding: 120px 1.5rem 60px;
                min-height: auto;
            }

            .hero h1 {
                font-size: 1.5rem !important;
                line-height: 1.4;
                padding: 0 1rem;
            }

            .hero .subtitle {
                font-size: 0.9rem;
                padding: 0 1rem;
            }

            .hero-features {
                flex-direction: column;
                align-items: center;
                gap: 0.75rem;
                padding: 0 1rem;
            }

            .hero-feature {
                width: 100%;
                max-width: 280px;
                padding: 0.625rem 1rem;
                font-size: 13px;
                justify-content: center;
            }

            /* 通用容器 */
            .container {
                padding: 0 1rem;
            }

            /* 所有section的padding */
            .projects-section,
            .path-section,
            .audience-section,
            .skills-section,
            .service-section,
            .testimonials-section,
            .instructor-section,
            .benefits-section,
            .faq-section {
                padding: 3rem 1rem;
            }

            /* section标题 */
            .section-header h2 {
                font-size: 1.5rem;
            }

            .section-header p {
                font-size: 0.9rem;
            }

            /* 项目筛选器 */
            .project-filter {
                flex-wrap: wrap;
                gap: 0.5rem;
                padding: 0 1rem;
            }

            .filter-btn {
                padding: 0.5rem 1rem;
                font-size: 13px;
                min-height: 44px;
                min-width: 70px;
            }

            /* 项目卡片网格 */
            .projects-grid {
                grid-template-columns: 1fr;
                gap: 1rem;
                padding: 0 1rem;
            }

            .project-card {
                padding: 1.25rem;
            }

            .project-card h3 {
                font-size: 1rem;
            }

            .project-info p {
                font-size: 13px;
            }

            .start-btn {
                min-height: 44px;
                font-size: 14px;
            }

            /* 路径时间轴 */
            .path-timeline {
                flex-direction: column;
                gap: 1rem;
            }

            .path-arrow {
                transform: rotate(90deg);
                font-size: 1.25rem;
            }

            .path-item {
                max-width: 100%;
                min-width: auto;
            }

            .path-icon {
                width: 60px;
                height: 60px;
            }

            .path-icon i {
                font-size: 1.5rem;
            }

            /* 网格卡片 */
            .audience-grid,
            .skills-grid,
            .service-grid,
            .testimonials-grid {
                grid-template-columns: 1fr;
                gap: 1rem;
            }

            .audience-card,
            .skill-item,
            .service-card,
            .testimonial-card {
                padding: 1.5rem;
            }

            .audience-icon,
            .skill-icon,
            .service-icon {
                width: 56px;
                height: 56px;
            }

            .audience-icon i,
            .skill-icon i,
            .service-icon i {
                font-size: 1.5rem;
            }

            /* 师资简介 */
            .instructor-wrapper {
                padding: 1.5rem;
            }

            .instructor-image img {
                width: 120px;
                height: 120px;
            }

            .instructor-content h2 {
                font-size: 1.25rem;
            }

            .instructor-content h3 {
                font-size: 1rem;
            }

            .instructor-bio p {
                font-size: 13px;
            }

            /* FAQ */
            .faq-list {
                padding: 0 1rem;
            }

            .faq-item {
                padding: 1.25rem;
            }

            .faq-item h4 {
                font-size: 0.95rem;
            }

            .faq-item p {
                font-size: 13px;
            }

            /* 底部 */
            .footer {
                padding: 3rem 1rem 1.5rem;
            }

            .footer-content {
                grid-template-columns: 1fr;
                gap: 2rem;
            }

            .footer-section h4 {
                font-size: 1rem;
            }

            .footer-section ul li {
                font-size: 13px;
                margin-bottom: 0.5rem;
            }

            .footer-bottom {
                font-size: 12px;
            }

            /* 悬浮按钮 */
            .floating-btn {
                bottom: 20px;
                right: 20px;
            }

            .floating-btn button {
                padding: 1rem;
                min-width: 44px;
                min-height: 44px;
                border-radius: 50%;
                box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
            }

            .floating-btn button span {
                display: none;
            }

            /* 模态框 */
            .modal-content {
                max-width: 95%;
                margin: 1rem;
            }

            .modal-header h3 {
                font-size: 1.125rem;
            }

            .form-group {
                margin-bottom: 1rem;
            }

            .form-group label {
                font-size: 14px;
            }

            .form-group input,
            .form-group textarea {
                padding: 0.75rem;
                font-size: 14px;
            }

            .submit-btn {
                padding: 0.875rem;
                font-size: 14px;
                min-height: 44px;
            }

            /* 认证按钮 */
            .navbar-auth {
                gap: 0.5rem;
            }

            .auth-btn {
                padding: 0.375rem 0.75rem;
                font-size: 12px;
            }

            .auth-btn i {
                display: none;
            }
        }

        /* 超小屏幕优化 */
        @media (max-width: 480px) {
            .hero h1 {
                font-size: 1.25rem !important;
            }

            .hero .subtitle {
                font-size: 0.85rem;
            }

            .section-header h2 {
                font-size: 1.25rem;
            }

            .project-card {
                padding: 1rem;
            }

            .project-icon {
                width: 44px;
                height: 44px;
                font-size: 1.25rem;
            }

            .difficulty-tag {
                font-size: 0.7rem;
                padding: 0.2rem 0.625rem;
            }

            .dataset-tag {
                font-size: 11px;
                padding: 0.25rem 0.5rem;
            }
        }

        /* 大屏幕优化 */
        @media (min-width: 1400px) {
            .projects-grid {
                grid-template-columns: repeat(4, 1fr);
            }

            .hero h1 {
                font-size: 3rem;
            }

            .hero .subtitle {
                font-size: 1.5rem;
            }
        }

        /* 触控优化 */
        @media (hover: none) and (pointer: coarse) {
            /* 移除hover效果，提升触控体验 */
            .project-card:hover {
                transform: none;
            }

            .audience-card:hover,
            .skill-item:hover,
            .service-card:hover,
            .testimonial-card:hover,
            .benefit-card:hover {
                transform: none;
            }

            /* 增加按钮和可点击元素的触控区域 */
            .nav-link {
                padding: 0.75rem 1rem;
            }

            .filter-btn {
                padding: 0.75rem 1.25rem;
            }

            .start-btn {
                padding: 1rem;
            }

            /* 悬浮按钮始终可见 */
            .floating-btn {
                opacity: 1;
            }
        }

        /* 打印样式 */
        @media print {
            .navbar,
            .floating-btn,
            .modal,
            .hero-features {
                display: none !important;
            }

            .hero {
                padding: 2rem;
                background: white;
                color: black;
            }

            .project-card,
            .audience-card,
            .skill-item {
                break-inside: avoid;
                box-shadow: none;
                border: 1px solid #ddd;
            }
        }

        /* 减少动画（无障碍） */
        @media (prefers-reduced-motion: reduce) {
            * {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
        }
    '''
    
    # 在 </style> 之前添加响应式CSS
    content = content.replace('</style>', responsive_css + '\n    </style>')
    
    # 5. 性能优化 - 确保所有图标都是SVG或Font Awesome（已经是轻量的）
    # 添加图片懒加载提示
    performance_tips = '''
    <!-- 性能优化说明：
    1. 所有图标使用 Font Awesome（CDN已优化）
    2. 头像使用 DiceBear API SVG（轻量）
    3. 无大型图片资源
    4. CSS/JS 已内联或使用 CDN
    5. 响应式图片 srcset 优化
    -->'''
    
    # 在 </head> 之前添加
    content = content.replace('</head>', performance_tips + '\n</head>')
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 最终优化完成！")

if __name__ == "__main__":
    final_optimization()
