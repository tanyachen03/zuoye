// 全局变量
let currentUser = null;
let pyodideReady = false;
let pyodideInstance = null;
let currentDataset = null;

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    initAuth();
    initNavigation();
    if (document.getElementById('code-editor-container')) {
        initCodeEditor();
    }
});

// 认证初始化
function initAuth() {
    const storedUser = localStorage.getItem('currentUser');
    if (storedUser) {
        currentUser = JSON.parse(storedUser);
        updateNavUser();
    }
    
    const loginBtn = document.getElementById('login-btn');
    const logoutBtn = document.getElementById('logout-btn');
    const userMenu = document.getElementById('user-menu');
    
    if (loginBtn) {
        loginBtn.addEventListener('click', showLoginModal);
    }
    if (logoutBtn) {
        logoutBtn.addEventListener('click', logout);
    }
    if (userMenu) {
        userMenu.addEventListener('click', (e) => {
            if (e.target.id === 'logout-btn') {
                logout();
            }
        });
    }
}

function showLoginModal() {
    const modal = new bootstrap.Modal(document.getElementById('loginModal'));
    modal.show();
}

function login() {
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    
    // 模拟登录验证
    if (username && password) {
        currentUser = {
            id: Date.now(),
            username: username,
            email: `${username}@example.com`,
            joinedAt: new Date().toISOString(),
            progress: {},
            badges: [],
            streak: 1
        };
        localStorage.setItem('currentUser', JSON.stringify(currentUser));
        localStorage.setItem('lastLogin', new Date().toISOString());
        
        updateNavUser();
        bootstrap.Modal.getInstance(document.getElementById('loginModal')).hide();
        showToast('success', '登录成功！欢迎回来');
    } else {
        showToast('error', '请输入用户名和密码');
    }
}

function logout() {
    currentUser = null;
    localStorage.removeItem('currentUser');
    updateNavUser();
    showToast('info', '已退出登录');
}

function updateNavUser() {
    const loginBtn = document.getElementById('login-btn');
    const logoutBtn = document.getElementById('logout-btn');
    const userMenu = document.getElementById('user-menu');
    const usernameSpan = document.getElementById('username-span');
    
    if (currentUser) {
        if (loginBtn) loginBtn.style.display = 'none';
        if (logoutBtn) logoutBtn.style.display = 'block';
        if (userMenu) userMenu.style.display = 'block';
        if (usernameSpan) usernameSpan.textContent = currentUser.username;
    } else {
        if (loginBtn) loginBtn.style.display = 'block';
        if (logoutBtn) logoutBtn.style.display = 'none';
        if (userMenu) userMenu.style.display = 'none';
    }
}

// 导航初始化
function initNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    const currentPath = window.location.pathname;
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath || 
            (currentPath === '/' && link.getAttribute('href') === '/index.html')) {
            link.classList.add('active');
        }
    });
}

// Toast 提示
function showToast(type, message) {
    const toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'position-fixed bottom-4 right-4 z-50';
        document.body.appendChild(container);
    }
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white border-0 ${type === 'success' ? 'bg-success' : type === 'error' ? 'bg-danger' : 'bg-info'}`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    document.getElementById('toast-container').appendChild(toast);
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    setTimeout(() => toast.remove(), 3000);
}

// 数据集加载成功弹窗
function showDatasetLoadedModal(datasetName) {
    const modalElement = document.getElementById('datasetLoadedModal');
    if (!modalElement) {
        showToast('success', `✅ ${datasetName} 已加载到在线编程区域，可以去试一试啦！`);
        return;
    }
    
    const messageEl = document.getElementById('dataset-loaded-message');
    if (messageEl) {
        messageEl.textContent = `${datasetName} 已加载到在线编程区域，可以去试一试啦 🚀`;
    }
    
    try {
        const modal = new bootstrap.Modal(modalElement);
        modal.show();
    } catch (err) {
        console.error('Modal show error:', err);
        showToast('success', `✅ ${datasetName} 已加载到在线编程区域，可以去试一试啦！`);
    }
}

// 工具函数
function getProgress(type, id) {
    if (!currentUser?.progress[type]) return null;
    return currentUser.progress[type][id];
}

// 进度保存
function saveProgress(type, id, completed = false) {
    if (!currentUser) return;
    
    if (!currentUser.progress[type]) {
        currentUser.progress[type] = {};
    }
    
    if (completed) {
        currentUser.progress[type][id] = {
            completed: true,
            completedAt: new Date().toISOString()
        };
    } else {
        currentUser.progress[type][id] = {
            completed: false,
            lastVisited: new Date().toISOString()
        };
    }
    
    localStorage.setItem('currentUser', JSON.stringify(currentUser));
    checkBadges();
}

function getProgress(type, id) {
    if (!currentUser || !currentUser.progress[type]) return null;
    return currentUser.progress[type][id];
}

// 徽章系统
function checkBadges() {
    if (!currentUser) return;
    
    const completedCourses = Object.keys(currentUser.progress['courses'] || {}).filter(
        id => currentUser.progress['courses'][id]?.completed
    ).length;
    
    const completedProjects = Object.keys(currentUser.progress['projects'] || {}).filter(
        id => currentUser.progress['projects'][id]?.completed
    ).length;
    
    // 代码初体验徽章
    if (!currentUser.badges.includes('first_code') && hasRunCode()) {
        unlockBadge('first_code');
    }
    
    // 课程完成徽章
    if (!currentUser.badges.includes('course_complete') && completedCourses >= 1) {
        unlockBadge('course_complete');
    }
    
    // 项目实战徽章
    if (!currentUser.badges.includes('project_complete') && completedProjects >= 1) {
        unlockBadge('project_complete');
    }
    
    // 分析大师徽章
    if (!currentUser.badges.includes('master_analyst') && 
        completedCourses >= 5 && completedProjects >= 10) {
        unlockBadge('master_analyst');
    }
    
    localStorage.setItem('currentUser', JSON.stringify(currentUser));
}

function hasRunCode() {
    return localStorage.getItem('hasRunCode') === 'true';
}

function markCodeRun() {
    localStorage.setItem('hasRunCode', 'true');
}

function unlockBadge(badgeId) {
    if (!currentUser.badges.includes(badgeId)) {
        currentUser.badges.push(badgeId);
        showToast('success', `🎉 获得徽章: ${badgesData[badgeId]?.name || badgeId}`);
    }
}

function isBadgeUnlocked(badgeId) {
    return currentUser?.badges.includes(badgeId) || false;
}

// 代码编辑器初始化
async function initCodeEditor() {
    try {
        const statusEl = document.getElementById('py-status');
        const statusText = document.getElementById('py-status-text');
        
        statusEl.textContent = '⏳ 加载中';
        statusEl.className = 'status-badge';
        
        pyodideInstance = await loadPyodide({
            indexURL: "https://cdn.jsdelivr.net/pyodide/v0.26.1/full/"
        });
        
        await pyodideInstance.loadPackage(['pandas', 'numpy']);
        
        pyodideReady = true;
        statusEl.textContent = '✅ 就绪';
        statusEl.className = 'status-badge ready';
        statusText.textContent = 'Python 环境已准备就绪，可以运行代码';
        
        // 添加快捷键支持
        const codeInput = document.getElementById('main-code-input');
        if (codeInput) {
            codeInput.addEventListener('keydown', (e) => {
                if (e.ctrlKey && e.key === 'Enter') {
                    e.preventDefault();
                    runCode();
                }
            });
        }
        
        // 添加按钮事件
        const runBtn = document.querySelector('.btn-editor.run');
        const clearBtn = document.querySelector('.btn-editor.clear');
        const clearOutputBtn = document.querySelector('.btn-editor.clear-output');
        
        if (runBtn) runBtn.addEventListener('click', runCode);
        if (clearBtn) clearBtn.addEventListener('click', clearCode);
        if (clearOutputBtn) clearOutputBtn.addEventListener('click', clearOutput);
        
    } catch (err) {
        console.error('Pyodide 初始化失败:', err);
        const statusEl = document.getElementById('py-status');
        const statusText = document.getElementById('py-status-text');
        if (statusEl) {
            statusEl.textContent = '✗ 失败';
            statusEl.className = 'status-badge error';
        }
        if (statusText) {
            statusText.textContent = '⚠️ Python 环境加载失败，请刷新页面重试';
        }
        showToast('error', 'Python环境加载失败，请检查网络连接');
    }
}

async function runCode() {
    if (!pyodideReady) {
        showToast('error', 'Python环境还未准备好，请稍等');
        return;
    }
    
    const codeInput = document.getElementById('main-code-input');
    const outputEl = document.getElementById('main-code-output');
    const statusEl = document.getElementById('py-status');
    
    if (!codeInput || !outputEl) return;
    
    const code = codeInput.value;
    
    statusEl.textContent = '⏳ 运行中';
    statusEl.className = 'status-badge';
    outputEl.textContent = '运行中...';
    
    try {
        const result = await pyodideInstance.runPythonAsync(code);
        
        let output = '';
        if (result !== undefined && result !== null) {
            output = String(result);
        }
        
        // 获取print输出
        const capturedOutput = await pyodideInstance.runPythonAsync(`
import io
import sys
cap = io.StringIO()
sys.stdout = cap
${code}
sys.stdout = sys.__stdout__
cap.getvalue()
        `);
        
        output = capturedOutput || output || "(代码执行完成 - 如无输出请添加 print 语句)";
        outputEl.textContent = output;
        
        markCodeRun();
        checkBadges();
        
    } catch (err) {
        outputEl.textContent = `错误: ${err.message}`;
    } finally {
        statusEl.textContent = '✅ 就绪';
        statusEl.className = 'status-badge ready';
    }
}

function clearCode() {
    const codeInput = document.getElementById('main-code-input');
    if (codeInput) {
        codeInput.value = '# 在此输入Python代码\nimport pandas as pd\nimport numpy as np\n\n# 数据集已加载到 df 变量\n';
    }
}

function clearOutput() {
    const outputEl = document.getElementById('main-code-output');
    if (outputEl) {
        outputEl.textContent = '等待代码执行...';
    }
}

async function loadDataset(datasetId) {
    if (!pyodideReady) {
        showToast('error', 'Python环境还未准备好，请稍等');
        return;
    }
    
    const dataset = datasetsData[datasetId];
    if (!dataset) return;
    
    const codeInput = document.getElementById('main-code-input');
    const outputEl = document.getElementById('main-code-output');
    
    outputEl.textContent = `正在加载 ${dataset.name}...`;
    
    try {
        // 读取CSV数据
        const response = await fetch(dataset.file);
        const csvText = await response.text();
        
        // 将CSV数据加载到Python环境
        await pyodideInstance.runPythonAsync(`
import pandas as pd
import io
csv_data = '''${csvText}'''
df = pd.read_csv(io.StringIO(csv_data))
        `);
        
        currentDataset = datasetId;
        
        codeInput.value = `# ============================================
# 📊 数据集: ${dataset.name}
# ${dataset.desc}
# 数据已加载到变量 df，可以直接使用！
# ============================================

import pandas as pd
import numpy as np

# 查看数据基本信息
print("=== 数据预览 ===")
print(df.head())

print("\\n=== 数据信息 ===")
print(df.info())

print("\\n=== 统计摘要 ===")
print(df.describe())`;
        
        outputEl.textContent = `✅ ${dataset.name} 已加载！\n数据已存储在变量 df 中，可以直接使用。`;
        
        // 显示加载成功弹窗
        showDatasetLoadedModal(dataset.name);
        
    } catch (err) {
        outputEl.textContent = `加载失败: ${err.message}`;
        showToast('error', '数据集加载失败');
    }
}

// 测评系统
let assessmentAnswers = {};
let assessmentSubmitted = false;

function initAssessment() {
    const questions = document.querySelectorAll('.question-card');
    questions.forEach((card, index) => {
        const options = card.querySelectorAll('.option');
        options.forEach((option, optIndex) => {
            option.addEventListener('click', () => {
                if (assessmentSubmitted) return;
                
                // 清除其他选项的选中状态
                card.querySelectorAll('.option').forEach(opt => opt.classList.remove('selected'));
                option.classList.add('selected');
                
                assessmentAnswers[index] = optIndex;
            });
        });
    });
    
    const submitBtn = document.getElementById('submit-assessment');
    if (submitBtn) {
        submitBtn.addEventListener('click', submitAssessment);
    }
}

function submitAssessment() {
    const questions = document.querySelectorAll('.question-card');
    let score = 0;
    let total = questions.length;
    
    questions.forEach((card, index) => {
        const options = card.querySelectorAll('.option');
        const correctAnswer = parseInt(card.dataset.answer);
        const userAnswer = assessmentAnswers[index];
        
        options.forEach((option, optIndex) => {
            option.classList.add('disabled');
            if (optIndex === correctAnswer) {
                option.classList.add('correct');
                option.classList.remove('selected');
            } else if (optIndex === userAnswer && userAnswer !== correctAnswer) {
                option.classList.add('incorrect');
            }
        });
        
        if (userAnswer === correctAnswer) {
            score++;
        }
    });
    
    assessmentSubmitted = true;
    
    const resultDiv = document.getElementById('assessment-result');
    const percentage = Math.round((score / total) * 100);
    
    resultDiv.innerHTML = `
        <div class="card bg-gradient-to-br from-success/20 to-success/5 border-success/30 p-6 text-center">
            <div class="text-6xl mb-4">${percentage >= 60 ? '🎉' : '💪'}</div>
            <h3 class="text-2xl font-bold mb-2">测评完成！</h3>
            <p class="text-xl mb-4">得分: ${score} / ${total} (${percentage}%)</p>
            <p class="text-secondary">${percentage >= 60 ? '恭喜通过测评！' : '继续努力，再接再厉！'}</p>
        </div>
    `;
    
    if (percentage >= 60 && !isBadgeUnlocked('assessment_pass')) {
        unlockBadge('assessment_pass');
    }
    
    if (currentUser) {
        currentUser.assessmentScore = {
            score,
            total,
            percentage,
            submittedAt: new Date().toISOString()
        };
        localStorage.setItem('currentUser', JSON.stringify(currentUser));
    }
}

// 页面初始化函数
function initPage(page) {
    switch(page) {
        case 'index':
            initIndex();
            break;
        case 'course':
            initCourse();
            break;
        case 'chapter':
            initChapter();
            break;
        case 'project':
            initProject();
            break;
        case 'dashboard':
            initDashboard();
            break;
        case 'assessment':
            initAssessment();
            break;
    }
}

function initIndex() {
    // 数据集卡片点击事件
    const datasetCards = document.querySelectorAll('.dataset-card');
    datasetCards.forEach(card => {
        card.addEventListener('click', () => {
            const datasetId = card.dataset.datasetId;
            loadDataset(datasetId);
        });
    });
}

function initCourse() {
    const courseId = new URLSearchParams(window.location.search).get('id');
    const course = coursesData[courseId];
    
    if (!course) {
        document.getElementById('course-content').innerHTML = '<p class="text-center text-secondary">课程不存在</p>';
        return;
    }
    
    // 渲染课程信息
    document.getElementById('course-title').textContent = course.title;
    document.getElementById('course-desc').textContent = course.description;
    document.getElementById('course-level').textContent = course.level;
    document.getElementById('course-duration').textContent = course.duration;
    
    // 渲染章节列表
    const chapterList = document.getElementById('chapter-list');
    chapterList.innerHTML = '';
    
    course.chapters.forEach((chapter, index) => {
        const progress = getProgress('chapters', `${courseId}-${chapter.id}`);
        const status = progress?.completed ? 'completed' : 
                      (index === 0 && !progress) ? 'in-progress' : 'pending';
        
        const icon = progress?.completed ? '✓' : index === 0 && !progress ? '▶' : '○';
        
        const li = document.createElement('li');
        li.className = `chapter-item ${status}`;
        li.innerHTML = `
            <span class="chapter-icon">${icon}</span>
            <div class="chapter-info">
                <h4>${chapter.title}</h4>
                <p>${chapter.duration}</p>
            </div>
            <span class="chapter-status">${progress?.completed ? '已完成' : '未开始'}</span>
        `;
        
        li.addEventListener('click', () => {
            window.location.href = `chapter.html?course=${courseId}&chapter=${chapter.id}`;
        });
        
        chapterList.appendChild(li);
    });
}

function initChapter() {
    const params = new URLSearchParams(window.location.search);
    const courseId = params.get('course');
    const chapterId = params.get('chapter');
    
    const course = coursesData[courseId];
    if (!course) return;
    
    const chapter = course.chapters.find(c => c.id === chapterId);
    if (!chapter) return;
    
    // 渲染章节信息
    const courseLink = document.getElementById('course-link');
    if (courseLink) {
        courseLink.textContent = course.title;
        courseLink.href = `course.html?id=${courseId}`;
    }
    const chapterTitle = document.getElementById('chapter-title');
    if (chapterTitle) chapterTitle.textContent = chapter.title;
    const chapterTitleH1 = document.getElementById('chapter-title-h1');
    if (chapterTitleH1) chapterTitleH1.textContent = chapter.title;
    const chapterDuration = document.getElementById('chapter-duration');
    if (chapterDuration) chapterDuration.textContent = chapter.duration;
    
    // 渲染理论内容
    const theoryDiv = document.getElementById('theory-content');
    theoryDiv.innerHTML = marked.parse(chapter.theory);
    
    // 渲染小贴士
    const tipsList = document.getElementById('tips-list');
    tipsList.innerHTML = chapter.tips.map(tip => `<li>${tip}</li>`).join('');
    
    // 渲染代码示例
    const codeInput = document.getElementById('main-code-input');
    if (codeInput) {
        codeInput.value = chapter.code;
    }
    
    // 渲染数据集列表
    const datasetsList = document.getElementById('datasets-list');
    if (datasetsList) {
        datasetsList.innerHTML = '';
        Object.values(datasetsData).forEach(dataset => {
            const datasetCard = document.createElement('div');
            datasetCard.className = 'dataset-card';
            datasetCard.dataset.id = dataset.id;
            datasetCard.innerHTML = `
                <div class="dataset-header">
                    <span class="dataset-icon">📊</span>
                    <div>
                        <h5>${dataset.name}</h5>
                        <p class="text-sm text-secondary">${dataset.desc}</p>
                    </div>
                </div>
                <div class="dataset-columns">
                    <span class="text-xs text-secondary">列：${dataset.columns.join(', ')}</span>
                </div>
                <div class="dataset-buttons">
                    <button class="btn-load-dataset">加载数据</button>
                    <button class="btn-download-dataset" data-id="${dataset.id}">
                        <i class="bi bi-download"></i> 下载
                    </button>
                </div>
            `;
            datasetsList.appendChild(datasetCard);

            // 添加加载按钮事件
            datasetCard.querySelector('.btn-load-dataset').addEventListener('click', () => {
                loadDataset(dataset.id);
            });

            // 添加下载按钮事件
            datasetCard.querySelector('.btn-download-dataset').addEventListener('click', (e) => {
                e.stopPropagation();
                downloadDataset(dataset.id);
            });
        });
    }
    
    // 渲染练习题
    const exercisesContainer = document.getElementById('exercises-container');
    if (chapter.exercises && chapter.exercises.length > 0) {
        chapter.exercises.forEach((exercise, index) => {
            const questionCard = document.createElement('div');
            questionCard.className = 'question-card';
            questionCard.dataset.answer = exercise.answer;
            questionCard.dataset.explanation = exercise.explanation || '';
            questionCard.innerHTML = `
                <div class="question">${index + 1}. ${exercise.question}</div>
                <ul class="options">
                    ${exercise.options.map((option, optIndex) => `
                        <li class="option" data-index="${optIndex}">
                            <span class="option-indicator">${String.fromCharCode(65 + optIndex)}</span>
                            <span>${option}</span>
                        </li>
                    `).join('')}
                </ul>
                <div class="explanation" style="display: none;">
                    <strong>💡 解析：</strong>${exercise.explanation}
                </div>
            `;
            exercisesContainer.appendChild(questionCard);
        });
        
        // 添加练习题点击事件
        const options = exercisesContainer.querySelectorAll('.option');
        options.forEach(option => {
            option.addEventListener('click', () => {
                const card = option.closest('.question-card');
                const answer = parseInt(card.dataset.answer);
                const selectedIndex = parseInt(option.dataset.index);
                const explanation = card.dataset.explanation;
                
                card.querySelectorAll('.option').forEach(opt => {
                    opt.classList.remove('selected', 'correct', 'incorrect');
                });
                
                const explanationDiv = card.querySelector('.explanation');
                
                if (selectedIndex === answer) {
                    option.classList.add('correct');
                    explanationDiv.style.display = 'none';
                    showToast('success', '回答正确！');
                } else {
                    option.classList.add('incorrect');
                    card.querySelector(`.option[data-index="${answer}"]`).classList.add('correct');
                    explanationDiv.style.display = 'block';
                    showToast('error', '回答错误，查看解析了解更多');
                }
            });
        });
    } else {
        exercisesContainer.innerHTML = '<p class="text-center text-secondary py-4">本章节暂无练习题</p>';
    }
    
    // 保存进度
    saveProgress('chapters', `${courseId}-${chapterId}`);
    
    // 完成按钮
    const completeBtn = document.getElementById('complete-chapter');
    if (completeBtn) {
        completeBtn.addEventListener('click', () => {
            saveProgress('chapters', `${courseId}-${chapterId}`, true);
            saveProgress('courses', courseId, checkCourseComplete(courseId));
            showToast('success', '章节已完成！');
            completeBtn.textContent = '已完成';
            completeBtn.disabled = true;
        });
    }
    
    // 回到首页按钮
    const backToHomeBtn = document.getElementById('back-to-home');
    if (backToHomeBtn) {
        backToHomeBtn.addEventListener('click', () => {
            window.location.href = 'index.html';
        });
    }
    
    // 下一章节按钮
    const nextChapterBtn = document.getElementById('next-chapter');
    if (nextChapterBtn) {
        const currentIndex = course.chapters.findIndex(c => c.id === chapterId);
        const hasNext = currentIndex < course.chapters.length - 1;
        
        if (hasNext) {
            const nextChapter = course.chapters[currentIndex + 1];
            nextChapterBtn.addEventListener('click', () => {
                window.location.href = `chapter.html?course=${courseId}&chapter=${nextChapter.id}`;
            });
        } else {
            nextChapterBtn.disabled = true;
            nextChapterBtn.textContent = '已是最后一章';
            nextChapterBtn.classList.remove('btn-outline-primary');
            nextChapterBtn.classList.add('btn-secondary', 'opacity-50');
        }
    }
}

function checkCourseComplete(courseId) {
    const course = coursesData[courseId];
    if (!course) return false;
    
    return course.chapters.every(chapter => {
        const progress = getProgress('chapters', `${courseId}-${chapter.id}`);
        return progress?.completed;
    });
}

function initProject() {
    const params = new URLSearchParams(window.location.search);
    const projectId = params.get('id');
    
    const project = projectsData[projectId];
    if (!project) {
        document.getElementById('project-content').innerHTML = '<p class="text-center text-secondary">项目不存在</p>';
        return;
    }
    
    // 渲染项目信息
    document.getElementById('project-title').textContent = project.title;
    document.getElementById('project-desc').textContent = project.description;
    document.getElementById('project-level').textContent = project.level;
    document.getElementById('project-duration').textContent = project.duration;
    
    // 渲染背景
    document.getElementById('project-background').textContent = project.background;
    
    // 渲染目标
    const goalsList = document.getElementById('project-goals');
    goalsList.innerHTML = project.goals.map(goal => `<li>${goal}</li>`).join('');
    
    // 渲染小贴士
    const tipsList = document.getElementById('tips-list');
    tipsList.innerHTML = project.tips.map(tip => `<li>${tip}</li>`).join('');
    
    // 渲染代码
    const codeInput = document.getElementById('main-code-input');
    if (codeInput) {
        codeInput.value = project.code;
    }
    
    // 渲染常见错误
    const errorsList = document.getElementById('errors-list');
    errorsList.innerHTML = project.errors.map(error => `<li>${error}</li>`).join('');
    
    // 数据集加载和下载按钮
    if (project.dataset && datasetsData[project.dataset]) {
        const datasetBtn = document.getElementById('load-dataset-btn');
        const downloadBtn = document.getElementById('download-dataset-btn');
        if (datasetBtn) {
            datasetBtn.style.display = 'inline-block';
            datasetBtn.addEventListener('click', () => {
                loadDataset(project.dataset);
            });
        }
        if (downloadBtn) {
            downloadBtn.style.display = 'inline-block';
            downloadBtn.addEventListener('click', () => {
                downloadDataset(project.dataset);
            });
        }
    }
    
    // 保存进度
    saveProgress('projects', projectId);
    
    // 完成按钮
    const completeBtn = document.getElementById('complete-project');
    if (completeBtn) {
        completeBtn.addEventListener('click', () => {
            saveProgress('projects', projectId, true);
            showToast('success', '项目已完成！');
            completeBtn.textContent = '已完成';
            completeBtn.disabled = true;
        });
    }
}

function initDashboard() {
    if (!currentUser) {
        document.getElementById('dashboard-content').innerHTML = `
            <div class="text-center py-12">
                <div class="text-6xl mb-4">🔐</div>
                <h3 class="text-xl mb-2">请先登录</h3>
                <p class="text-secondary mb-4">登录后可以查看学习进度和成就</p>
                <button class="btn-primary" onclick="showLoginModal()">立即登录</button>
            </div>
        `;
        return;
    }
    
    // 统计数据
    const totalCourses = Object.keys(coursesData).length;
    const completedCourses = Object.keys(currentUser.progress['courses'] || {}).filter(
        id => currentUser.progress['courses'][id]?.completed
    ).length;
    
    const totalProjects = Object.keys(projectsData).length;
    const completedProjects = Object.keys(currentUser.progress['projects'] || {}).filter(
        id => currentUser.progress['projects'][id]?.completed
    ).length;
    
    const totalBadges = Object.keys(badgesData).length;
    const unlockedBadges = currentUser.badges.length;
    
    // 更新统计卡片
    document.getElementById('stat-courses').textContent = `${completedCourses}/${totalCourses}`;
    document.getElementById('stat-projects').textContent = `${completedProjects}/${totalProjects}`;
    document.getElementById('stat-badges').textContent = `${unlockedBadges}/${totalBadges}`;
    document.getElementById('stat-streak').textContent = currentUser.streak || 1;
    
    // 渲染进度条
    const courseProgress = Math.round((completedCourses / totalCourses) * 100);
    const projectProgress = Math.round((completedProjects / totalProjects) * 100);
    
    document.getElementById('course-progress-fill').style.width = `${courseProgress}%`;
    document.getElementById('course-progress-text').textContent = `${courseProgress}%`;
    document.getElementById('project-progress-fill').style.width = `${projectProgress}%`;
    document.getElementById('project-progress-text').textContent = `${projectProgress}%`;
    
    // 渲染徽章
    const badgesContainer = document.getElementById('badges-container');
    badgesContainer.innerHTML = '';
    
    Object.values(badgesData).forEach(badge => {
        const unlocked = isBadgeUnlocked(badge.id);
        const card = document.createElement('div');
        card.className = `badge-card ${unlocked ? 'unlocked' : 'locked'}`;
        card.innerHTML = `
            <div class="badge-icon">${unlocked ? badge.name.split(' ')[0] : '🔒'}</div>
            <h4>${unlocked ? badge.name.split(' ').slice(1).join(' ') : '???'}</h4>
            <p>${unlocked ? badge.desc : '尚未解锁'}</p>
        `;
        badgesContainer.appendChild(card);
    });
    
    // 渲染学习记录
    const recentActivity = document.getElementById('recent-activity');
    const activities = [];
    
    // 收集最近完成的章节和项目
    if (currentUser.progress['chapters']) {
        Object.entries(currentUser.progress['chapters']).forEach(([id, progress]) => {
            if (progress.completed) {
                activities.push({
                    type: 'chapter',
                    id,
                    date: progress.completedAt,
                    completed: true
                });
            }
        });
    }
    
    if (currentUser.progress['projects']) {
        Object.entries(currentUser.progress['projects']).forEach(([id, progress]) => {
            if (progress.completed) {
                activities.push({
                    type: 'project',
                    id,
                    date: progress.completedAt,
                    completed: true
                });
            }
        });
    }
    
    // 按日期排序
    activities.sort((a, b) => new Date(b.date) - new Date(a.date));
    
    if (activities.length > 0) {
        recentActivity.innerHTML = activities.slice(0, 5).map(activity => {
            const icon = activity.type === 'chapter' ? '📚' : '🎯';
            const date = new Date(activity.date).toLocaleDateString('zh-CN');
            return `<li>${icon} 完成${activity.type === 'chapter' ? '章节' : '项目'} - ${date}</li>`;
        }).join('');
    } else {
        recentActivity.innerHTML = '<li class="text-secondary">暂无学习记录</li>';
    }
}

// 导出函数供HTML调用
window.login = login;
window.runCode = runCode;
window.clearCode = clearCode;
// 下载数据集到本地
function downloadDataset(datasetId) {
    const dataset = datasetsData[datasetId];
    if (!dataset) {
        showToast('error', '未找到数据集');
        return;
    }

    const fileName = dataset.file.split('/').pop();

    fetch(dataset.file)
        .then(response => {
            if (!response.ok) throw new Error('网络请求失败');
            return response.blob();
        })
        .then(blob => {
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = fileName;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            showToast('success', `✅ ${dataset.name} 已下载到本地（${fileName}）`);
        })
        .catch(err => {
            console.error('Download error:', err);
            // 如果 fetch 失败，则使用预览数据生成 CSV 作为兜底方案
            if (dataset.preview && dataset.preview.length > 0) {
                try {
                    let csvContent = dataset.columns.join(',') + '\n';
                    dataset.preview.forEach(row => {
                        csvContent += row.map(cell => {
                            const str = String(cell ?? '');
                            if (str.includes(',') || str.includes('"') || str.includes('\n')) {
                                return '"' + str.replace(/"/g, '""') + '"';
                            }
                            return str;
                        }).join(',') + '\n';
                    });
                    const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = fileName;
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                    URL.revokeObjectURL(url);
                    showToast('success', `✅ ${dataset.name} 已下载到本地（${fileName}）`);
                } catch (e) {
                    showToast('error', '下载失败，请重试');
                }
            } else {
                showToast('error', '下载失败，请重试');
            }
        });
}

window.clearOutput = clearOutput;
window.loadDataset = loadDataset;
window.downloadDataset = downloadDataset;
window.showLoginModal = showLoginModal;
window.initPage = initPage;
