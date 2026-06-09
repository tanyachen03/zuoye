const App = {
    pyodide: null,
    pyodideReady: false,
    pyodideLoading: false,

    async init() {
        Router.init();
        this.setupRoutes();
        this.setupEventListeners();
        this.bindCourseCardEvents();
    },

    setupRoutes() {
        Router.register('home', () => this.renderHome());
        Router.register('courses', () => this.renderCourses());
        Router.register('course', (id) => this.renderCourseDetail(id));
        Router.register('projects', () => this.renderProjects());
        Router.register('project', (id) => this.renderProjectDetail(id));
        Router.register('achievements', () => this.renderAchievements());
    },

    setupEventListeners() {
        document.getElementById('mobileMenuBtn')?.addEventListener('click', () => {
            document.getElementById('navMenu').classList.toggle('show');
        });

        document.getElementById('loginBtn')?.addEventListener('click', () => {
            document.getElementById('loginModal').classList.add('show');
        });

        document.getElementById('closeLoginModal')?.addEventListener('click', () => {
            document.getElementById('loginModal').classList.remove('show');
        });

        document.getElementById('cancelLogin')?.addEventListener('click', () => {
            document.getElementById('loginModal').classList.remove('show');
        });

        document.getElementById('confirmLogin')?.addEventListener('click', () => {
            Store.login('learner@datacademy.cn');
            document.getElementById('loginModal').classList.remove('show');
            this.showToast('登录成功！');
            this.updateLoginButton();
        });

        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                document.getElementById('navMenu').classList.remove('show');
            });
        });
    },

    bindCourseCardEvents() {
        setTimeout(() => {
            document.querySelectorAll('.course-card').forEach(card => {
                card.addEventListener('click', (e) => {
                    const index = card.getAttribute('data-index');
                    const courseId = card.getAttribute('data-course-id');
                    this.toggleCourseExpand(parseInt(index), courseId);
                });
            });

            document.querySelectorAll('.complete-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    const courseId = btn.getAttribute('data-course-id');
                    const lessonId = btn.getAttribute('data-lesson-id');
                    this.toggleLessonComplete(courseId, lessonId);
                });
            });

            document.querySelectorAll('.start-course-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    const courseId = btn.getAttribute('data-course-id');
                    Router.navigate('course', courseId);
                });
            });

            document.querySelectorAll('.lesson-list-item').forEach(item => {
                item.addEventListener('click', (e) => {
                    if (e.target.tagName !== 'BUTTON') {
                        const courseId = item.getAttribute('data-lesson-id') ? 
                            document.querySelector('.complete-btn[data-lesson-id="' + item.getAttribute('data-lesson-id') + '"]')?.getAttribute('data-course-id') : null;
                        const lessonId = item.querySelector('.complete-btn')?.getAttribute('data-lesson-id');
                        if (courseId) {
                            Router.navigate('course', courseId);
                        }
                    }
                });
            });
        }, 100);
    },

    updateLoginButton() {
        const btn = document.getElementById('loginBtn');
        if (btn) {
            if (Store.data.isLoggedIn) {
                btn.textContent = '已登录';
                btn.disabled = true;
            }
        }
    },

    showToast(message) {
        const toast = document.getElementById('toast');
        const toastMessage = document.getElementById('toastMessage');
        if (toast && toastMessage) {
            toastMessage.textContent = message;
            toast.classList.add('show');
            setTimeout(() => toast.classList.remove('show'), 3000);
        }
    },

    renderHome() {
        const app = document.getElementById('app');
        const completedCourses = Store.getCompletedCoursesCount();
        const completedProjects = Store.getCompletedProjectsCount();
        const totalCodeRuns = Store.data.codeRunCount;

        app.innerHTML = `
            <section class="hero">
                <h1 class="hero-title">数析学院</h1>
                <p class="hero-subtitle">专业的Python数据分析在线学习平台，从入门到实战，让你掌握数据分析核心技能</p>
                <a href="#courses" class="hero-btn">开始学习</a>
            </section>

            <section class="stats-section">
                <div class="stat-card">
                    <div class="stat-number">${COURSES_DATA.length}</div>
                    <div class="stat-label">精品课程</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${PROJECTS_DATA.length}</div>
                    <div class="stat-label">实战项目</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">10,000+</div>
                    <div class="stat-label">学员总数</div>
                </div>
            </section>

            <section class="section">
                <h2 class="section-title">📚 推荐课程</h2>
                <div class="card-grid">
                    ${COURSES_DATA.slice(0, 3).map((course, index) => this.renderCourseCard(course, index)).join('')}
                </div>
            </section>

            <section class="section">
                <h2 class="section-title">🛠️ 热门项目</h2>
                <div class="card-grid">
                    ${PROJECTS_DATA.slice(0, 3).map(project => this.renderProjectCard(project)).join('')}
                </div>
            </section>
        `;

        document.getElementById('footer').style.display = 'block';
        this.bindCourseCardEvents();
    },

    renderCourseCard(course, index) {
        const progress = Store.getCourseProgress(course.id);
        const completionRate = Store.getCourseCompletionRate(course.id, course.lessons.length);

        return `
            <div class="course-card-wrapper" id="course-wrapper-${index}">
                <div class="card course-card" data-index="${index}" data-course-id="${course.id}" style="cursor: pointer;">
                    <div class="card-icon">${course.icon}</div>
                    <h3 class="card-title">${course.title}</h3>
                    <p class="card-desc">${course.description}</p>
                    <div class="card-meta">
                        <span>${course.difficulty}</span>
                        <span>${course.lessons.length}个小节</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${completionRate}%"></div>
                    </div>
                    <div style="color: var(--text-muted); font-size: 12px; margin-top: 8px; display: flex; justify-content: space-between; align-items: center;">
                        <span class="completion-text-${index}">已完成 ${progress.completedLessons.length}/${course.lessons.length} 小节</span>
                        <span class="expand-icon" id="expand-icon-${index}" style="font-size: 16px;">▼</span>
                    </div>
                </div>
                <div class="course-lessons-list" id="lessons-${index}" style="display: none;">
                    <div style="padding: 16px; background: var(--bg-tertiary); border-radius: 0 0 12px 12px; border: 1px solid var(--border-color); border-top: none;">
                        <div style="margin-bottom: 12px; color: var(--text-secondary); font-weight: bold;">📚 课程小节</div>
                        ${course.lessons.map(lesson => `
                            <div class="lesson-list-item" style="display: flex; align-items: center; justify-content: space-between; padding: 10px 12px; margin-bottom: 8px; border-radius: 6px; background: var(--bg-secondary); cursor: pointer;" 
                                 data-course-id="${course.id}" data-lesson-id="${lesson.id}">
                                <div style="display: flex; align-items: center; gap: 10px;">
                                    <span class="lesson-icon-${lesson.id}" style="font-size: 14px;">${Store.isLessonCompleted(course.id, lesson.id) ? '✓' : '📚'}</span>
                                    <div>
                                        <div class="lesson-title-text-${lesson.id}" style="font-size: 14px; ${Store.isLessonCompleted(course.id, lesson.id) ? 'color: var(--text-muted); text-decoration: line-through;' : 'color: var(--text-primary);'}">${lesson.id} ${lesson.title}</div>
                                        <div style="font-size: 12px; color: var(--text-muted);">${lesson.duration} · ${lesson.type}</div>
                                    </div>
                                </div>
                                <button class="btn ${Store.isLessonCompleted(course.id, lesson.id) ? 'btn-secondary' : 'btn-primary'} complete-btn" 
                                        data-course-id="${course.id}"
                                        data-lesson-id="${lesson.id}"
                                        style="padding: 6px 12px; font-size: 12px; border-radius: 4px;">
                                    ✓
                                </button>
                            </div>
                        `).join('')}
                        <div style="margin-top: 16px;">
                            <button class="btn btn-primary start-course-btn" data-course-id="${course.id}" style="width: 100%;">
                                🚀 开始学习本课程
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    },

    renderProjectCard(project) {
        return `
            <div class="card" onclick="Router.navigate('project', '${project.id}')">
                <div class="card-icon">${project.icon}</div>
                <h3 class="card-title">${project.title}</h3>
                <p class="card-desc">${project.description}</p>
                <div class="card-meta">
                    <span class="card-tag ${project.difficulty === '入门' ? 'tag-easy' : project.difficulty === '进阶' ? 'tag-medium' : 'tag-hard'}">${project.difficulty}</span>
                    <span>${project.duration}</span>
                </div>
                ${Store.isProjectCompleted(project.id) ? '<div style="color: var(--accent-green); font-size: 12px; margin-top: 8px;">✓ 已完成</div>' : ''}
            </div>
        `;
    },

    renderCourses() {
        const app = document.getElementById('app');
        document.getElementById('footer').style.display = 'none';

        app.innerHTML = `
            <div style="max-width: 1200px; margin: 0 auto; padding: 48px 24px;">
                <h1 class="section-title">📚 课程中心</h1>
                <p style="color: var(--text-secondary); margin-bottom: 32px;">点击课程卡片展开查看小节，点击✓按钮标记已完成</p>
                <div class="card-grid" id="coursesContainer">
                    ${COURSES_DATA.map((course, index) => this.renderCourseCard(course, index)).join('')}
                </div>
            </div>
        `;
        
        this.bindCourseCardEvents();
    },

    toggleCourseExpand(index, courseId) {
        const lessonsDiv = document.getElementById(`lessons-${index}`);
        const expandIcon = document.getElementById(`expand-icon-${index}`);
        
        if (!lessonsDiv || !expandIcon) {
            return;
        }
        
        if (lessonsDiv.style.display === 'none' || lessonsDiv.style.display === '') {
            lessonsDiv.style.display = 'block';
            expandIcon.textContent = '▲';
            expandIcon.style.transform = 'rotate(180deg)';
        } else {
            lessonsDiv.style.display = 'none';
            expandIcon.textContent = '▼';
            expandIcon.style.transform = 'rotate(0deg)';
        }
    },

    toggleLessonComplete(courseId, lessonId) {
        if (Store.isLessonCompleted(courseId, lessonId)) {
            Store.unmarkLessonComplete(courseId, lessonId);
        } else {
            Store.markLessonComplete(courseId, lessonId);
        }
        
        const course = COURSES_DATA.find(c => c.id === courseId);
        if (course) {
            const progress = Store.getCourseProgress(courseId);
            const courseIndex = COURSES_DATA.findIndex(c => c.id === courseId);
            
            const completionText = document.querySelector(`.completion-text-${courseIndex}`);
            if (completionText) {
                completionText.textContent = `已完成 ${progress.completedLessons.length}/${course.lessons.length} 小节`;
            }
            
            const lessonIcon = document.querySelector(`.lesson-icon-${lessonId}`);
            if (lessonIcon) {
                lessonIcon.textContent = Store.isLessonCompleted(courseId, lessonId) ? '✓' : '📚';
            }
            
            const lessonTitle = document.querySelector(`.lesson-title-text-${lessonId}`);
            if (lessonTitle) {
                if (Store.isLessonCompleted(courseId, lessonId)) {
                    lessonTitle.style.color = 'var(--text-muted)';
                    lessonTitle.style.textDecoration = 'line-through';
                } else {
                    lessonTitle.style.color = 'var(--text-primary)';
                    lessonTitle.style.textDecoration = 'none';
                }
            }
            
            const btn = document.querySelector(`.complete-btn[data-lesson-id="${lessonId}"]`);
            if (btn) {
                if (Store.isLessonCompleted(courseId, lessonId)) {
                    btn.classList.remove('btn-primary');
                    btn.classList.add('btn-secondary');
                } else {
                    btn.classList.remove('btn-secondary');
                    btn.classList.add('btn-primary');
                }
            }
            
            this.showToast(Store.isLessonCompleted(courseId, lessonId) ? '✓ 已标记为完成' : '○ 已取消完成标记');
        }
    },

    renderCourseDetail(courseId) {
        const course = COURSES_DATA.find(c => c.id === courseId);
        if (!course) {
            Router.navigate('courses');
            return;
        }

        const app = document.getElementById('app');
        document.getElementById('footer').style.display = 'none';
        const progress = Store.getCourseProgress(course.id);
        const currentLesson = progress.currentLesson || course.lessons[0]?.id;
        const firstLesson = course.lessons.find(l => l.id === currentLesson) || course.lessons[0];

        app.innerHTML = `
            <div class="course-detail">
                <aside class="course-sidebar">
                    <button class="back-btn" onclick="Router.navigate('courses')">
                        ← 返回课程列表
                    </button>
                    <h2 class="course-sidebar-title">${course.icon} ${course.title}</h2>
                    <div style="color: var(--text-secondary); margin-bottom: 16px;">
                        ${progress.completedLessons.length}/${course.lessons.length} 小节已完成
                    </div>
                    <div class="progress-bar" style="margin-bottom: 24px;">
                        <div class="progress-fill" style="width: ${Store.getCourseCompletionRate(course.id, course.lessons.length)}%"></div>
                    </div>
                    ${course.lessons.map(lesson => `
                        <div class="lesson-item ${lesson.id === firstLesson.id ? 'active' : ''} ${Store.isLessonCompleted(course.id, lesson.id) ? 'completed' : ''}"
                             onclick="App.selectLesson('${course.id}', '${lesson.id}')">
                            <div class="lesson-info">
                                <span>${Store.isLessonCompleted(course.id, lesson.id) ? '✓' : '📚'}</span>
                                <div>
                                    <div class="lesson-title">${lesson.title}</div>
                                    <div class="lesson-duration">${lesson.duration} · ${lesson.type}</div>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </aside>
                <main class="course-content" id="lessonContent">
                    ${this.renderLessonContent(course, firstLesson)}
                </main>
            </div>
        `;

        Store.setCurrentLesson(course.id, firstLesson.id);
    },

    selectLesson(courseId, lessonId) {
        const course = COURSES_DATA.find(c => c.id === courseId);
        const lesson = course?.lessons.find(l => l.id === lessonId);
        if (!course || !lesson) return;

        document.querySelectorAll('.lesson-item').forEach(item => {
            item.classList.remove('active');
        });
        event.currentTarget.classList.add('active');

        document.getElementById('lessonContent').innerHTML = this.renderLessonContent(course, lesson);
        Store.setCurrentLesson(course.id, lessonId);
    },

    renderLessonContent(course, lesson) {
        return `
            <div class="content-header">
                <h1 class="content-title">${lesson.title}</h1>
                <div class="content-meta">
                    <span>⏱️ ${lesson.duration}</span>
                    <span>📄 ${lesson.type}</span>
                </div>
            </div>
            <div class="content-body">
                <div class="content-section">
                    <h3>📖 内容讲解</h3>
                    <p>${lesson.content.text}</p>
                </div>

                ${lesson.content.codeExamples.map((example, idx) => `
                    <div class="content-section">
                        <h3>💻 代码示例 ${idx + 1}：${example.title}</h3>
                        <div class="code-block">
                            <div class="code-title">Python</div>
                            <pre>${example.code}</pre>
                        </div>
                    </div>
                `).join('')}

                <div class="content-section">
                    <h3>💡 小贴士</h3>
                    ${lesson.content.tips.map(tip => `
                        <div class="tip-box">
                            <div class="tip-content">${tip}</div>
                        </div>
                    `).join('')}
                </div>

                <div class="content-section">
                    <h3>⚠️ 常见错误</h3>
                    ${lesson.content.commonErrors.map(err => `
                        <div class="tip-box warning">
                            <div class="tip-content">${err}</div>
                        </div>
                    `).join('')}
                </div>

                <div style="margin-top: 32px;">
                    ${Store.isLessonCompleted(course.id, lesson.id) ? `
                        <button class="btn btn-secondary" disabled>✓ 已完成</button>
                    ` : `
                        <button class="btn btn-primary" onclick="App.markLessonComplete('${course.id}', '${lesson.id}')">
                            ✓ 标记为已完成
                        </button>
                    `}
                </div>
            </div>
        `;
    },

    markLessonComplete(courseId, lessonId) {
        Store.markLessonComplete(courseId, lessonId);
        const course = COURSES_DATA.find(c => c.id === courseId);
        const lessonIndex = course.lessons.findIndex(l => l.id === lessonId);
        const nextLesson = course.lessons[lessonIndex + 1];

        if (nextLesson) {
            this.selectLesson(courseId, nextLesson.id);
        } else {
            this.selectLesson(courseId, lessonId);
        }
    },

    renderProjects() {
        const app = document.getElementById('app');
        document.getElementById('footer').style.display = 'none';

        app.innerHTML = `
            <div style="max-width: 1200px; margin: 0 auto; padding: 48px 24px;">
                <h1 class="section-title">🛠️ 实战项目</h1>
                <p style="color: var(--text-secondary); margin-bottom: 32px;">通过真实项目提升数据分析能力</p>
                <div class="card-grid">
                    ${PROJECTS_DATA.map(project => `
                        <div class="card" onclick="Router.navigate('project', '${project.id}')">
                            <div class="card-icon">${project.icon}</div>
                            <h3 class="card-title">${project.title}</h3>
                            <p class="card-desc">${project.description}</p>
                            <div class="card-meta">
                                <span class="card-tag ${project.difficulty === '入门' ? 'tag-easy' : project.difficulty === '进阶' ? 'tag-medium' : 'tag-hard'}">${project.difficulty}</span>
                                <span>⏱️ ${project.duration}</span>
                            </div>
                            <div style="color: var(--text-muted); font-size: 12px; margin-top: 8px;">
                                数据集：${project.dataset}
                            </div>
                            ${Store.isProjectCompleted(project.id) ? '<div style="color: var(--accent-green); font-size: 12px; margin-top: 8px;">✓ 已完成</div>' : ''}
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    },

    async renderProjectDetail(projectId) {
        const project = PROJECTS_DATA.find(p => p.id === projectId);
        if (!project) {
            Router.navigate('projects');
            return;
        }

        const app = document.getElementById('app');
        document.getElementById('footer').style.display = 'none';

        app.innerHTML = `
            <div class="project-detail">
                <aside class="project-docs">
                    <button class="back-btn" onclick="Router.navigate('projects')">
                        ← 返回项目列表
                    </button>
                    <h2>${project.icon} ${project.title}</h2>
                    <div class="card-meta" style="margin-bottom: 24px;">
                        <span class="card-tag ${project.difficulty === '入门' ? 'tag-easy' : project.difficulty === '进阶' ? 'tag-medium' : 'tag-hard'}">${project.difficulty}</span>
                        <span>⏱️ ${project.duration}</span>
                        <span>📁 ${project.dataset}</span>
                    </div>

                    <div class="docs-section">
                        <h3>🎯 项目目标</h3>
                        <ul>
                            ${project.content.objectives.map(obj => `<li>${obj}</li>`).join('')}
                        </ul>
                    </div>

                    <div class="docs-section">
                        <h3>📊 数据集说明</h3>
                        <p>${project.content.datasetInfo}</p>
                    </div>

                    <div class="docs-section">
                        <h3>📝 分步骤指引</h3>
                        ${project.content.steps.map((step, idx) => `
                            <div class="step-item">
                                <div class="step-number">${idx + 1}</div>
                                <div class="step-content">
                                    <div class="step-title">${step.title}</div>
                                    <div class="step-desc">${step.description}</div>
                                </div>
                            </div>
                        `).join('')}
                    </div>

                    <div class="docs-section">
                        <h3>💡 小贴士</h3>
                        ${project.content.tips.map(tip => `<p>• ${tip}</p>`).join('')}
                    </div>

                    <div class="docs-section">
                        <h3>⚠️ 常见错误</h3>
                        ${project.content.commonErrors.map(err => `<p>• ${err}</p>`).join('')}
                    </div>

                    ${Store.isProjectCompleted(project.id) ? `
                        <div style="color: var(--accent-green); margin-top: 24px; font-weight: bold;">
                            ✓ 项目已完成
                        </div>
                    ` : ''}
                </aside>

                <div class="project-editor">
                    <div class="editor-header">
                        <div class="editor-title">
                            <span>🐍</span>
                            <span>Python 编辑器</span>
                        </div>
                        <div class="editor-tabs">
                            <span class="editor-tab">main.py</span>
                        </div>
                    </div>
                    <div class="editor-area" id="editorArea">
                        <textarea class="code-editor" id="codeEditor" spellcheck="false">${project.starterCode}</textarea>
                    </div>
                    <div class="editor-footer">
                        <button class="run-btn" id="runBtn" onclick="App.runCode()">
                            ▶ 运行代码
                        </button>
                        <div class="output-area" id="outputArea">
                            <div class="output-header">输出</div>
                            <div class="output-content" id="outputContent">
                                点击"运行代码"查看结果...
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        await this.initPyodide();
    },

    async initPyodide() {
        if (this.pyodideReady) return;

        if (this.pyodideLoading) {
            return;
        }

        this.pyodideLoading = true;

        try {
            this.pyodide = await loadPyodide({
                indexURL: "https://cdn.jsdelivr.net/pyodide/v0.24.1/full/"
            });

            await this.pyodide.loadPackage(["pandas", "numpy", "matplotlib"]);
            this.pyodideReady = true;
            this.pyodideLoading = false;

            const currentProject = Router.getParam();
            const datasetName = PROJECTS_DATA.find(p => p.id === currentProject)?.dataset;
            if (datasetName) {
                const csvData = getDataset(datasetName);
                if (csvData) {
                    this.pyodide.FS.writeFile(datasetName, csvData);
                }
            }

        } catch (error) {
            console.error('Failed to initialize Pyodide:', error);
            this.showToast('Python环境加载失败，请刷新重试');
            this.pyodideLoading = false;
        }
    },

    async runCode() {
        if (!this.pyodideReady) {
            const btn = document.getElementById('runBtn');
            btn.disabled = true;
            btn.innerHTML = '<span class="loading-spinner"></span> 加载中...';
            await this.initPyodide();
        }

        const code = document.getElementById('codeEditor').value;
        const outputContent = document.getElementById('outputContent');
        const btn = document.getElementById('runBtn');

        btn.disabled = true;
        btn.innerHTML = '<span class="loading-spinner"></span> 运行中...';
        outputContent.textContent = '';
        outputContent.classList.remove('error', 'success');

        try {
            const currentProject = Router.getParam();
            const datasetName = PROJECTS_DATA.find(p => p.id === currentProject)?.dataset;

            if (datasetName) {
                const csvData = getDataset(datasetName);
                if (csvData) {
                    this.pyodide.FS.writeFile(datasetName, csvData);
                }
            }

            let result = await this.pyodide.runPythonAsync(code);

            if (result !== undefined && result !== null) {
                outputContent.textContent = String(result);
            } else {
                outputContent.textContent = '代码执行完成';
            }

            outputContent.classList.add('success');
            Store.incrementCodeRunCount();

            if (currentProject && !Store.isProjectCompleted(currentProject)) {
                this.showToast('代码运行成功！');
            }

        } catch (error) {
            outputContent.textContent = `错误: ${error.message}`;
            outputContent.classList.add('error');
        } finally {
            btn.disabled = false;
            btn.innerHTML = '▶ 运行代码';
        }
    },

    renderAchievements() {
        const app = document.getElementById('app');
        document.getElementById('footer').style.display = 'none';

        const unlockedCount = Store.data.achievements.length;
        const totalCount = ACHIEVEMENTS_DATA.length;

        app.innerHTML = `
            <div style="max-width: 1200px; margin: 0 auto; padding: 48px 24px;">
                <h1 class="section-title">🏆 成就殿堂</h1>
                <p style="color: var(--text-secondary); margin-bottom: 16px;">
                    已解锁 ${unlockedCount}/${totalCount} 个成就
                </p>
                <div class="progress-bar" style="margin-bottom: 32px; max-width: 400px;">
                    <div class="progress-fill" style="width: ${(unlockedCount / totalCount) * 100}%"></div>
                </div>
                <div class="achievement-grid">
                    ${ACHIEVEMENTS_DATA.map(achievement => {
                        const isUnlocked = Store.isAchievementUnlocked(achievement.id);
                        return `
                            <div class="achievement-card ${isUnlocked ? 'unlocked' : 'locked'}">
                                <div class="achievement-icon">${achievement.icon}</div>
                                <h3 class="achievement-name">${achievement.title}</h3>
                                <p class="achievement-desc">${achievement.description}</p>
                                <span class="achievement-status">${isUnlocked ? '已解锁' : '未解锁'}</span>
                                <div class="achievement-tooltip">
                                    解锁条件：${achievement.condition}
                                </div>
                            </div>
                        `;
                    }).join('')}
                </div>
            </div>
        `;
    }
};

document.addEventListener('DOMContentLoaded', () => App.init());
