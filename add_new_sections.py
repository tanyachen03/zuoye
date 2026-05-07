#!/usr/bin/env python3
import os

def add_new_sections():
    html_path = "/workspace/data-analytics-platform/index.html"
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 新的内容区块HTML
    new_sections = '''
    <!-- 课程定位区域 -->
    <section class="path-section" id="path">
        <div class="container">
            <div class="section-header">
                <h2>从零基础到数据分析实战高手</h2>
                <p>系统化学习路径，循序渐进掌握核心技能</p>
            </div>
            
            <div class="path-timeline">
                <div class="path-item">
                    <div class="path-icon">
                        <i class="fas fa-seedling"></i>
                    </div>
                    <div class="path-content">
                        <h3>零基础</h3>
                        <p>从Python基础开始，<br>无门槛入门</p>
                    </div>
                </div>
                
                <div class="path-arrow">
                    <i class="fas fa-arrow-right"></i>
                </div>
                
                <div class="path-item">
                    <div class="path-icon">
                        <i class="fas fa-gem"></i>
                    </div>
                    <div class="path-content">
                        <h3>Pandas核心</h3>
                        <p>掌握数据分析<br>核心工具</p>
                    </div>
                </div>
                
                <div class="path-arrow">
                    <i class="fas fa-arrow-right"></i>
                </div>
                
                <div class="path-item">
                    <div class="path-icon">
                        <i class="fas fa-laptop-code"></i>
                    </div>
                    <div class="path-content">
                        <h3>10大项目实战</h3>
                        <p>真实业务场景<br>边学边练</p>
                    </div>
                </div>
                
                <div class="path-arrow">
                    <i class="fas fa-arrow-right"></i>
                </div>
                
                <div class="path-item">
                    <div class="path-icon">
                        <i class="fas fa-briefcase"></i>
                    </div>
                    <div class="path-content">
                        <h3>可写进简历</h3>
                        <p>获得真实项目经验<br>和证书认证</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- 适合人群区域 -->
    <section class="audience-section" id="audience">
        <div class="container">
            <div class="section-header">
                <h2>适合人群</h2>
                <p>无论你是谁，都能在这里找到成长路径</p>
            </div>
            
            <div class="audience-grid">
                <div class="audience-card">
                    <div class="audience-icon">
                        <i class="fas fa-exchange-alt"></i>
                    </div>
                    <h3>转行数据分析者</h3>
                    <p>想要进入数据分析领域<br>缺乏系统学习方法</p>
                </div>
                
                <div class="audience-card">
                    <div class="audience-icon">
                        <i class="fas fa-chart-bar"></i>
                    </div>
                    <h3>业务/运营/产品人员</h3>
                    <p>需要数据分析能力<br>提升日常工作效率</p>
                </div>
                
                <div class="audience-card">
                    <div class="audience-icon">
                        <i class="fas fa-graduation-cap"></i>
                    </div>
                    <h3>在校学生</h3>
                    <p>想要提前学习技能<br>为就业增加竞争力</p>
                </div>
                
                <div class="audience-card">
                    <div class="audience-icon">
                        <i class="fas fa-chart-line"></i>
                    </div>
                    <h3>职场提升者</h3>
                    <p>想要提升数据能力<br>获得职场晋升机会</p>
                </div>
            </div>
        </div>
    </section>

    <!-- 学习收获区域 -->
    <section class="skills-section" id="skills">
        <div class="container">
            <div class="section-header">
                <h2>学习收获</h2>
                <p>6大核心技能，覆盖数据分析全流程</p>
            </div>
            
            <div class="skills-grid">
                <div class="skill-item">
                    <div class="skill-icon">
                        <i class="fas fa-broom"></i>
                    </div>
                    <h3>数据清洗</h3>
                    <p>处理缺失值、异常值、<br>格式统一等</p>
                </div>
                
                <div class="skill-item">
                    <div class="skill-icon">
                        <i class="fas fa-layer-group"></i>
                    </div>
                    <h3>分组聚合</h3>
                    <p>groupby聚合、透视表、<br>多维度分析</p>
                </div>
                
                <div class="skill-item">
                    <div class="skill-icon">
                        <i class="fas fa-chart-area"></i>
                    </div>
                    <h3>数据可视化</h3>
                    <p>Matplotlib、Seaborn<br>专业图表制作</p>
                </div>
                
                <div class="skill-item">
                    <div class="skill-icon">
                        <i class="fas fa-flask"></i>
                    </div>
                    <h3>AB测试</h3>
                    <p>实验设计、显著性检验<br>转化率分析</p>
                </div>
                
                <div class="skill-item">
                    <div class="skill-icon">
                        <i class="fas fa-chart-line"></i>
                    </div>
                    <h3>时间序列</h3>
                    <p>趋势分析、移动平均<br>预测模型</p>
                </div>
                
                <div class="skill-item">
                    <div class="skill-icon">
                        <i class="fas fa-magic"></i>
                    </div>
                    <h3>特征工程</h3>
                    <p>特征构建、编码转换<br>数据预处理</p>
                </div>
            </div>
        </div>
    </section>

    <!-- 服务说明区域 -->
    <section class="service-section" id="service">
        <div class="container">
            <div class="section-header">
                <h2>服务说明</h2>
                <p>完善的学习支持，让你学习无忧</p>
            </div>
            
            <div class="service-grid">
                <div class="service-card">
                    <div class="service-icon">
                        <i class="fas fa-browser"></i>
                    </div>
                    <h3>浏览器在线运行</h3>
                    <p>无需安装任何软件<br>打开浏览器即可开始编程</p>
                </div>
                
                <div class="service-card">
                    <div class="service-icon">
                        <i class="fas fa-infinity"></i>
                    </div>
                    <h3>永久回看</h3>
                    <p>课程内容永久有效<br>随时复习巩固知识</p>
                </div>
                
                <div class="service-card">
                    <div class="service-icon">
                        <i class="fas fa-comments"></i>
                    </div>
                    <h3>答疑支持</h3>
                    <p>遇到问题可提交咨询<br>专业团队为你解答</p>
                </div>
                
                <div class="service-card">
                    <div class="service-icon">
                        <i class="fas fa-award"></i>
                    </div>
                    <h3>证书与徽章</h3>
                    <p>完成项目获得成就徽章<br>积累可写进简历的经验</p>
                </div>
            </div>
        </div>
    </section>
'''
    
    # 在项目列表区域之后插入新内容
    # 找到 </section> (项目列表的结束标签) 并在其后插入
    old_section_end = '''        </div>
    </section>

    <!-- 学习收获区域 -->'''
    
    new_section_with_old = '''        </div>
    </section>
''' + new_sections + '''
    <!-- 学习收获区域（已迁移到上方skills-section） -->
    <!-- 
    <section class="benefits-section" id="benefits">
        <div class="section-header">
            <h2>学习收获</h2>
            <p>系统掌握数据分析核心技能，提升职场竞争力</p>
        </div>
        
        <div class="benefits-grid">
            <div class="benefit-card">
                <div class="benefit-icon">
                    <i class="fas fa-check"></i>
                </div>
                <h3>数据处理能力</h3>
                <p>熟练使用 Pandas 进行数据清洗、转换、合并等操作</p>
            </div>
            
            <div class="benefit-card">
                <div class="benefit-icon">
                    <i class="fas fa-chart-pie"></i>
                </div>
                <h3>可视化技能</h3>
                <p>掌握 Matplotlib、Seaborn 等工具制作专业图表</p>
            </div>
            
            <div class="benefit-card">
                <div class="benefit-icon">
                    <i class="fas fa-brain"></i>
                </div>
                <h3>业务分析思维</h3>
                <p>学会从数据中发现业务问题，提出解决方案</p>
            </div>
            
            <div class="benefit-card">
                <div class="benefit-icon">
                    <i class="fas fa-briefcase"></i>
                </div>
                <h3>实战项目经验</h3>
                <p>10个真实业务场景项目，可写入简历的作品集</p>
            </div>
        </div>
    </section>
    -->'''
    
    content = content.replace(old_section_end, new_section_with_old)
    
    # 添加新的CSS样式
    css_styles = '''
        /* 容器 */
        .container {
            max-width: var(--max-width);
            margin: 0 auto;
            padding: 0 2rem;
        }

        /* 课程定位区域 */
        .path-section {
            padding: 5rem 2rem;
            background: white;
        }

        .path-timeline {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1.5rem;
            flex-wrap: wrap;
            margin-top: 3rem;
        }

        .path-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            flex: 1;
            min-width: 200px;
            max-width: 250px;
        }

        .path-icon {
            width: 80px;
            height: 80px;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 1rem;
            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);
        }

        .path-icon i {
            font-size: 2rem;
            color: white;
        }

        .path-content h3 {
            font-size: 1.125rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 0.5rem;
        }

        .path-content p {
            font-size: 14px;
            color: var(--text-secondary);
            line-height: 1.6;
        }

        .path-arrow {
            color: var(--primary-color);
            font-size: 1.5rem;
        }

        /* 适合人群区域 */
        .audience-section {
            padding: 5rem 2rem;
            background: var(--bg-light);
        }

        .audience-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            max-width: var(--max-width);
            margin: 3rem auto 0;
        }

        .audience-card {
            background: white;
            border-radius: var(--border-radius);
            padding: 2rem;
            text-align: center;
            box-shadow: var(--shadow-md);
            border: 2px solid transparent;
            transition: all 0.3s ease;
        }

        .audience-card:hover {
            transform: translateY(-5px);
            box-shadow: var(--shadow-xl);
            border-color: var(--primary-light);
        }

        .audience-icon {
            width: 64px;
            height: 64px;
            background: linear-gradient(135deg, #10b981, #34d399);
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 1.25rem;
        }

        .audience-icon i {
            font-size: 1.75rem;
            color: white;
        }

        .audience-card h3 {
            font-size: 1.125rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 0.625rem;
        }

        .audience-card p {
            font-size: 14px;
            color: var(--text-secondary);
            line-height: 1.6;
        }

        /* 学习收获区域 */
        .skills-section {
            padding: 5rem 2rem;
            background: white;
        }

        .skills-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.5rem;
            max-width: var(--max-width);
            margin: 3rem auto 0;
        }

        .skill-item {
            background: var(--bg-light);
            border-radius: var(--border-radius);
            padding: 2rem;
            text-align: center;
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }

        .skill-item:hover {
            background: white;
            transform: translateY(-5px);
            box-shadow: var(--shadow-lg);
            border-color: var(--primary-light);
        }

        .skill-icon {
            width: 64px;
            height: 64px;
            background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 1.25rem;
        }

        .skill-icon i {
            font-size: 1.75rem;
            color: white;
        }

        .skill-item h3 {
            font-size: 1.125rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 0.625rem;
        }

        .skill-item p {
            font-size: 14px;
            color: var(--text-secondary);
            line-height: 1.6;
        }

        /* 服务说明区域 */
        .service-section {
            padding: 5rem 2rem;
            background: linear-gradient(135deg, #eff6ff 0%, #f8fafc 100%);
        }

        .service-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            max-width: var(--max-width);
            margin: 3rem auto 0;
        }

        .service-card {
            background: white;
            border-radius: var(--border-radius);
            padding: 2rem;
            text-align: center;
            box-shadow: var(--shadow-md);
            border: 2px solid transparent;
            transition: all 0.3s ease;
        }

        .service-card:hover {
            transform: translateY(-5px);
            box-shadow: var(--shadow-xl);
            border-color: var(--success-color);
        }

        .service-icon {
            width: 64px;
            height: 64px;
            background: linear-gradient(135deg, #10b981, #06b6d4);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 1.25rem;
        }

        .service-icon i {
            font-size: 1.75rem;
            color: white;
        }

        .service-card h3 {
            font-size: 1.125rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 0.625rem;
        }

        .service-card p {
            font-size: 14px;
            color: var(--text-secondary);
            line-height: 1.6;
        }
'''
    
    # 在 </style> 之前插入新样式
    content = content.replace('</style>', css_styles + '\n    </style>')
    
    # 更新导航栏，添加新链接
    old_nav = '''<nav class="navbar-menu">
                <a href="#hero" class="nav-link active">首页</a>
                <a href="#projects" class="nav-link">项目列表</a>
                <a href="#benefits" class="nav-link">学习收获</a>
                <a href="#faq" class="nav-link">常见问题</a>
            </nav>'''
    
    new_nav = '''<nav class="navbar-menu">
                <a href="#hero" class="nav-link active">首页</a>
                <a href="#projects" class="nav-link">项目列表</a>
                <a href="#path" class="nav-link">学习路径</a>
                <a href="#audience" class="nav-link">适合人群</a>
                <a href="#skills" class="nav-link">学习收获</a>
                <a href="#service" class="nav-link">服务说明</a>
                <a href="#faq" class="nav-link">常见问题</a>
            </nav>'''
    
    content = content.replace(old_nav, new_nav)
    
    # 更新footer的快速链接
    old_footer_links = '''<ul>
                    <li><a href="#hero">首页</a></li>
                    <li><a href="#projects">项目列表</a></li>
                    <li><a href="#benefits">学习收获</a></li>
                    <li><a href="#faq">常见问题</a></li>
                </ul>'''
    
    new_footer_links = '''<ul>
                    <li><a href="#hero">首页</a></li>
                    <li><a href="#projects">项目列表</a></li>
                    <li><a href="#path">学习路径</a></li>
                    <li><a href="#audience">适合人群</a></li>
                    <li><a href="#skills">学习收获</a></li>
                    <li><a href="#service">服务说明</a></li>
                    <li><a href="#faq">常见问题</a></li>
                </ul>'''
    
    content = content.replace(old_footer_links, new_footer_links)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 新增内容区块完成！")

if __name__ == "__main__":
    add_new_sections()
