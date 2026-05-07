#!/usr/bin/env python3
import os

def add_final_sections():
    html_path = "/workspace/data-analytics-platform/index.html"
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 新的内容区块HTML
    new_sections = '''
    <!-- 学员评价区域 -->
    <section class="testimonials-section" id="testimonials">
        <div class="container">
            <div class="section-header">
                <h2>学员评价</h2>
                <p>听听已经学习的同学怎么说</p>
            </div>
            
            <div class="testimonials-grid">
                <div class="testimonial-card">
                    <div class="testimonial-header">
                        <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=student1" alt="学员头像" class="testimonial-avatar">
                        <div class="testimonial-info">
                            <h4>张同学</h4>
                            <span class="testimonial-tag">转行成功者</span>
                        </div>
                    </div>
                    <div class="testimonial-rating">
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                    </div>
                    <p class="testimonial-quote">"从一个完全不懂代码的小白，到现在能够独立完成数据分析项目，这个课程帮了我大忙！老师讲得很细致，项目也很实用。"</p>
                </div>
                
                <div class="testimonial-card">
                    <div class="testimonial-header">
                        <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=student2" alt="学员头像" class="testimonial-avatar">
                        <div class="testimonial-info">
                            <h4>李运营</h4>
                            <span class="testimonial-tag">运营专员</span>
                        </div>
                    </div>
                    <div class="testimonial-rating">
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star-half-alt"></i>
                    </div>
                    <p class="testimonial-quote">"之前每次做报表都要花很长时间，现在用学到的Pandas技能，效率提升了至少3倍！而且浏览器就能跑代码，太方便了！"</p>
                </div>
                
                <div class="testimonial-card">
                    <div class="testimonial-header">
                        <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=student3" alt="学员头像" class="testimonial-avatar">
                        <div class="testimonial-info">
                            <h4>王学生</h4>
                            <span class="testimonial-tag">应届毕业生</span>
                        </div>
                    </div>
                    <div class="testimonial-rating">
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                    </div>
                    <p class="testimonial-quote">"秋招的时候，这份项目经验帮了大忙！面试官对我做过的项目很感兴趣，最终拿到了心仪的offer，真的很感谢这个课程！"</p>
                </div>
            </div>
        </div>
    </section>

    <!-- 师资简介区域 -->
    <section class="instructor-section" id="instructor">
        <div class="container">
            <div class="instructor-wrapper">
                <div class="instructor-image">
                    <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=instructor" alt="讲师头像">
                </div>
                <div class="instructor-content">
                    <div class="instructor-badge">
                        <i class="fas fa-user-tie"></i>
                        主讲讲师
                    </div>
                    <h2>讲师简介</h2>
                    <h3>数据分析师 | 行业专家</h3>
                    <div class="instructor-bio">
                        <p><strong>5年+数据分析经验</strong>，曾服务于某知名互联网公司，负责用户增长数据分析</p>
                        <p><strong>主导过多个大型数据分析项目</strong>，涵盖电商、金融、教育等多个行业</p>
                        <p><strong>擅长使用Python、Pandas进行数据处理</strong>，精通数据可视化与业务分析</p>
                        <p><strong>曾培养学员1000+</strong>，帮助多名学员成功转型数据分析岗位</p>
                    </div>
                    <div class="instructor-tags">
                        <span><i class="fas fa-check"></i> Python专家</span>
                        <span><i class="fas fa-check"></i> Pandas高手</span>
                        <span><i class="fas fa-check"></i> 数据可视化</span>
                        <span><i class="fas fa-check"></i> 业务分析</span>
                    </div>
                </div>
            </div>
        </div>
    </section>
'''
    
    # 在底部之前插入新内容
    content = content.replace('</footer>\n\n    <!-- 登录弹窗 -->', new_sections + '\n</footer>\n\n    <!-- 登录弹窗 -->')
    
    # 添加CSS样式
    css_styles = '''
        /* 学员评价区域 */
        .testimonials-section {
            padding: 5rem 2rem;
            background: white;
        }

        .testimonials-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 2rem;
            max-width: var(--max-width);
            margin: 3rem auto 0;
        }

        .testimonial-card {
            background: var(--bg-light);
            border-radius: var(--border-radius);
            padding: 2rem;
            box-shadow: var(--shadow-md);
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }

        .testimonial-card:hover {
            transform: translateY(-5px);
            box-shadow: var(--shadow-xl);
            border-color: var(--primary-light);
        }

        .testimonial-header {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1rem;
        }

        .testimonial-avatar {
            width: 56px;
            height: 56px;
            border-radius: 50%;
            border: 3px solid var(--primary-color);
        }

        .testimonial-info h4 {
            font-size: 1rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 0.25rem;
        }

        .testimonial-tag {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            font-size: 0.75rem;
            font-weight: 600;
            border-radius: 9999px;
        }

        .testimonial-rating {
            margin-bottom: 1rem;
        }

        .testimonial-rating i {
            color: #fbbf24;
            font-size: 1rem;
            margin-right: 0.125rem;
        }

        .testimonial-quote {
            font-size: 14px;
            color: var(--text-secondary);
            line-height: 1.7;
            font-style: italic;
        }

        .testimonial-quote::before {
            content: '"';
            font-size: 3rem;
            color: var(--primary-light);
            opacity: 0.3;
            line-height: 0;
            vertical-align: -1.5rem;
            margin-right: 0.5rem;
        }

        /* 师资简介区域 */
        .instructor-section {
            padding: 5rem 2rem;
            background: linear-gradient(135deg, #eff6ff 0%, #f8fafc 100%);
        }

        .instructor-wrapper {
            display: flex;
            align-items: center;
            gap: 3rem;
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 3rem;
            box-shadow: var(--shadow-xl);
        }

        .instructor-image {
            flex-shrink: 0;
        }

        .instructor-image img {
            width: 180px;
            height: 180px;
            border-radius: 50%;
            border: 5px solid var(--primary-color);
            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);
        }

        .instructor-content {
            flex: 1;
        }

        .instructor-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            font-size: 0.875rem;
            font-weight: 600;
            border-radius: 9999px;
            margin-bottom: 1rem;
        }

        .instructor-content h2 {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 0.5rem;
        }

        .instructor-content h3 {
            font-size: 1.125rem;
            font-weight: 600;
            color: var(--primary-color);
            margin-bottom: 1.5rem;
        }

        .instructor-bio {
            margin-bottom: 1.5rem;
        }

        .instructor-bio p {
            font-size: 14px;
            color: var(--text-secondary);
            line-height: 1.7;
            margin-bottom: 0.75rem;
            padding-left: 1.5rem;
            position: relative;
        }

        .instructor-bio p::before {
            content: '•';
            position: absolute;
            left: 0;
            color: var(--primary-color);
            font-weight: bold;
        }

        .instructor-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 0.75rem;
        }

        .instructor-tags span {
            display: inline-flex;
            align-items: center;
            gap: 0.375rem;
            padding: 0.5rem 1rem;
            background: rgba(59, 130, 246, 0.08);
            color: var(--primary-color);
            font-size: 0.875rem;
            font-weight: 500;
            border-radius: 9999px;
        }

        .instructor-tags span i {
            font-size: 0.75rem;
        }

        /* 响应式 */
        @media (max-width: 768px) {
            .instructor-wrapper {
                flex-direction: column;
                text-align: center;
                padding: 2rem;
            }

            .instructor-image img {
                width: 140px;
                height: 140px;
            }

            .instructor-bio p {
                text-align: left;
            }

            .instructor-tags {
                justify-content: center;
            }

            .testimonials-grid {
                grid-template-columns: 1fr;
            }
        }
'''
    
    # 在 </style> 之前插入CSS
    content = content.replace('</style>', css_styles + '\n    </style>')
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 新增底部内容完成！")

if __name__ == "__main__":
    add_final_sections()
