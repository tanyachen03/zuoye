document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    setupEventListeners();
    initLearningModule();
    initAchievementSystem();
});

function setupEventListeners() {
    const loginBtn = document.getElementById('login-btn');
    const registerBtn = document.getElementById('register-btn');
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const logoutBtn = document.getElementById('logout-btn');
    const hamburgerMenu = document.getElementById('hamburger-menu');
    const navbarMenu = document.querySelector('.navbar-menu');

    if (loginBtn) {
        loginBtn.addEventListener('click', () => openModal('login-modal'));
    }

    if (registerBtn) {
        registerBtn.addEventListener('click', () => openModal('register-modal'));
    }

    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }

    if (logoutBtn) {
        logoutBtn.addEventListener('click', handleLogout);
    }

    if (hamburgerMenu && navbarMenu) {
        hamburgerMenu.addEventListener('click', () => {
            navbarMenu.classList.toggle('active');
        });
    }
}

function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('hidden');
        document.body.style.overflow = '';
    }
}

function switchModal(targetModalId) {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => modal.classList.add('hidden'));
    openModal(targetModalId);
}

function checkAuth() {
    const user = JSON.parse(localStorage.getItem('currentUser'));
    const userProfile = document.getElementById('user-profile');
    const loginBtn = document.getElementById('login-btn');
    const registerBtn = document.getElementById('register-btn');

    if (user) {
        if (userProfile) {
            userProfile.classList.remove('hidden');
            document.getElementById('user-name').textContent = user.name;
        }
        if (loginBtn) loginBtn.classList.add('hidden');
        if (registerBtn) registerBtn.classList.add('hidden');
    } else {
        if (userProfile) userProfile.classList.add('hidden');
        if (loginBtn) loginBtn.classList.remove('hidden');
        if (registerBtn) registerBtn.classList.remove('hidden');
    }
}

function handleLogin(e) {
    e.preventDefault();
    
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    
    const users = JSON.parse(localStorage.getItem('users')) || [];
    const user = users.find(u => u.email === email && u.password === password);
    
    if (user) {
        localStorage.setItem('currentUser', JSON.stringify(user));
        closeModal('login-modal');
        checkAuth();
        showNotification('登录成功！', 'success');
    } else {
        showNotification('邮箱或密码错误', 'error');
    }
}

function handleRegister(e) {
    e.preventDefault();
    
    const name = document.getElementById('register-name').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    
    const users = JSON.parse(localStorage.getItem('users')) || [];
    
    if (users.find(u => u.email === email)) {
        showNotification('该邮箱已被注册', 'error');
        return;
    }
    
    const newUser = {
        id: Date.now().toString(),
        name,
        email,
        password
    };
    
    users.push(newUser);
    localStorage.setItem('users', JSON.stringify(users));
    localStorage.setItem('currentUser', JSON.stringify(newUser));
    
    closeModal('register-modal');
    checkAuth();
    showNotification('注册成功！', 'success');
}

function handleLogout() {
    localStorage.removeItem('currentUser');
    checkAuth();
    showNotification('已退出登录', 'info');
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    notification.style.cssText = `
        position: fixed;
        top: 90px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 0.5rem;
        color: white;
        font-weight: 500;
        z-index: 3000;
        animation: slideIn 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    `;
    
    const colors = {
        success: '#10b981',
        error: '#ef4444',
        info: '#3b82f6'
    };
    
    notification.style.backgroundColor = colors[type] || colors.info;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(100%);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideOut {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(100%);
        }
    }
`;
document.head.appendChild(style);

// ==================== 学习模块核心功能 ====================

function initLearningModule() {
    loadQuizProgress();
    initQuizEvents();
    initCodeChallenges();
}

// localStorage存储相关
function getQuizKey(quizId) {
    const pageName = window.location.pathname.split('/').pop() || 'index.html';
    return `quiz_${pageName}_${quizId}`;
}

function saveQuizAnswer(quizId, answer, isCorrect) {
    const key = getQuizKey(quizId);
    const data = { answer, isCorrect, timestamp: Date.now() };
    localStorage.setItem(key, JSON.stringify(data));
}

function getQuizAnswer(quizId) {
    const key = getQuizKey(quizId);
    const data = localStorage.getItem(key);
    return data ? JSON.parse(data) : null;
}

function saveChapterTest(chapter, answers, score) {
    const key = `chapter_test_${chapter}`;
    const data = { answers, score, timestamp: Date.now() };
    localStorage.setItem(key, JSON.stringify(data));
}

function getChapterTest(chapter) {
    const key = `chapter_test_${chapter}`;
    const data = localStorage.getItem(key);
    return data ? JSON.parse(data) : null;
}

// 知识点测验相关
function initQuizEvents() {
    document.querySelectorAll('.quiz-container').forEach(container => {
        const quizId = container.dataset.quizId;
        const savedAnswer = getQuizAnswer(quizId);
        
        if (savedAnswer) {
            showQuizResult(container, savedAnswer.answer, savedAnswer.isCorrect);
        }
        
        container.querySelectorAll('.quiz-option').forEach(option => {
            option.addEventListener('click', () => {
                if (!savedAnswer) {
                    const isCorrect = option.dataset.correct === 'true';
                    const answer = option.textContent.trim();
                    saveQuizAnswer(quizId, answer, isCorrect);
                    showQuizResult(container, answer, isCorrect);
                }
            });
        });
    });
}

function showQuizResult(container, answer, isCorrect) {
    const options = container.querySelectorAll('.quiz-option');
    const explanation = container.querySelector('.quiz-explanation');
    
    options.forEach(option => {
        if (option.dataset.correct === 'true') {
            option.classList.add('quiz-correct');
        } else if (option.textContent.trim() === answer && !isCorrect) {
            option.classList.add('quiz-incorrect');
        }
        option.style.pointerEvents = 'none';
    });
    
    if (explanation) {
        explanation.classList.remove('hidden');
    }
    
    setTimeout(() => {
        const quizId = container.dataset.quizId;
        checkAchievements('quiz_complete', { quizId, isCorrect });
    }, 500);
}

function loadQuizProgress() {
}

// 综合测评相关
function submitChapterTest(chapter) {
    const container = document.querySelector(`[data-chapter-test="${chapter}"]`);
    const answers = [];
    let score = 0;
    const questions = container.querySelectorAll('.test-question');
    
    questions.forEach((q, index) => {
        const selected = q.querySelector('input[type="radio"]:checked');
        const correctAnswer = q.dataset.correct;
        let isCorrect = false;
        
        if (selected) {
            isCorrect = selected.value === correctAnswer;
            answers.push({ question: index, answer: selected.value, isCorrect, correctAnswer });
            if (isCorrect) score++;
        } else {
            answers.push({ question: index, answer: null, isCorrect: false, correctAnswer });
        }
    });
    
    const percentage = Math.round((score / questions.length) * 100);
    saveChapterTest(chapter, answers, percentage);
    showChapterTestResult(container, score, questions.length, answers);
}

function showChapterTestResult(container, score, total, answers) {
    const resultDiv = container.querySelector('.test-result');
    const questionsDiv = container.querySelector('.test-questions');
    
    resultDiv.classList.remove('hidden');
    resultDiv.innerHTML = `
        <div class="test-score">
            <h3>🎉 测评完成！</h3>
            <div class="score-display">
                <span class="score-number">${score}/${total}</span>
                <span class="score-percentage">${Math.round((score / total) * 100)}%</span>
            </div>
            <p class="score-message">${getScoreMessage(score, total)}</p>
        </div>
    `;
    
    const wrongAnswersDiv = document.createElement('div');
    wrongAnswersDiv.className = 'wrong-answers';
    wrongAnswersDiv.innerHTML = '<h4>📚 错题回顾</h4>';
    
    answers.forEach((a, i) => {
        if (!a.isCorrect) {
            const questionDiv = document.createElement('div');
            questionDiv.className = 'wrong-answer-item';
            const questionText = questionsDiv.querySelectorAll('.test-question')[i].querySelector('.question-text').textContent;
            questionDiv.innerHTML = `
                <p class="wrong-question">${questionText}</p>
                <p class="wrong-answer-text">你的答案: ${a.answer || '未作答'}</p>
                <p class="correct-answer-text">正确答案: ${a.correctAnswer}</p>
            `;
            wrongAnswersDiv.appendChild(questionDiv);
        }
    });
    
    if (wrongAnswersDiv.querySelectorAll('.wrong-answer-item').length > 0) {
        resultDiv.appendChild(wrongAnswersDiv);
    }
    
    questionsDiv.style.display = 'none';
    container.querySelector('.submit-test-btn').style.display = 'none';
    
    setTimeout(() => {
        const chapterMatch = container.dataset.chapterTest.match(/chapter(\d+)/);
        if (chapterMatch) {
            checkAchievements('chapter_test', { 
                chapter: chapterMatch[1],
                score: Math.round((score / total) * 100)
            });
        }
    }, 500);
}

function getScoreMessage(score, total) {
    const percentage = (score / total) * 100;
    if (percentage >= 90) return '太棒了！你是学习达人！';
    if (percentage >= 70) return '不错哦，继续加油！';
    if (percentage >= 50) return '还需要加强学习哦！';
    return '建议重新学习本章内容！';
}

// 代码挑战相关
function initCodeChallenges() {
    document.querySelectorAll('.code-challenge').forEach((challenge, index) => {
        const runBtn = challenge.querySelector('.run-code-btn');
        if (runBtn) {
            runBtn.addEventListener('click', () => runCodeChallenge(challenge));
        }
        
        const resetBtn = challenge.querySelector('.reset-code-btn');
        if (resetBtn) {
            resetBtn.addEventListener('click', () => resetCodeChallenge(challenge));
        }
    });
}

function runCodeChallenge(challenge) {
    const codeEditor = challenge.querySelector('.code-editor');
    const outputDiv = challenge.querySelector('.code-output');
    const code = codeEditor.value;
    
    outputDiv.innerHTML = '<div class="output-loading">⌛ 正在运行...</div>';
    
    // 使用Skulpt运行Python代码
    try {
        Sk.configure({
            output: function(text) {
                const output = outputDiv.querySelector('.output-text');
                if (!output) {
                    outputDiv.innerHTML = '<pre class="output-text"></pre>';
                }
                outputDiv.querySelector('.output-text').textContent += text;
            },
            read: function(filename) {
                if (Sk.builtinFiles === undefined || Sk.builtinFiles['files'][filename] === undefined) {
                    throw 'File not found: ' + filename;
                }
                return Sk.builtinFiles['files'][filename];
            }
        });
        
        Sk.misceval.asyncToPromise(function() {
            return Sk.importMainWithBody('<stdin>', false, code, true);
        }).then(function(mod) {
            outputDiv.classList.remove('output-error');
            outputDiv.classList.add('output-success');
        }, function(err) {
            outputDiv.innerHTML = `<pre class="output-text output-error">❌ 运行错误: ${err.toString()}</pre>`;
        });
    } catch (e) {
        outputDiv.innerHTML = `<pre class="output-text output-error">❌ 运行错误: ${e.toString()}</pre>`;
    }
}

function resetCodeChallenge(challenge) {
    const codeEditor = challenge.querySelector('.code-editor');
    const outputDiv = challenge.querySelector('.code-output');
    const originalCode = codeEditor.dataset.originalCode;
    
    codeEditor.value = originalCode || '';
    outputDiv.innerHTML = '<div class="output-placeholder">点击"运行"按钮执行代码</div>';
}

// ==================== 成就激励系统 ====================

const ACHIEVEMENTS = {
    newcomer: {
        id: 'newcomer',
        name: '初出茅庐',
        description: '完成第一章节学习',
        icon: 'fa-star',
        color: '#f59e0b',
        condition: (data) => data.chaptersCompleted >= 1
    },
    pythonMaster: {
        id: 'pythonMaster',
        name: 'Python达人',
        description: '完成Python基础章节',
        icon: 'fab fa-python',
        color: '#3b82f6',
        condition: (data) => data.chaptersCompleted >= 2
    },
    scholar: {
        id: 'scholar',
        name: '学霸',
        description: '章节测评正确率达到90%以上',
        icon: 'fa-graduation-cap',
        color: '#10b981',
        condition: (data) => data.bestScore >= 90
    },
    dataExplorer: {
        id: 'dataExplorer',
        name: '数据探险家',
        description: '完成3个章节学习',
        icon: 'fa-compass',
        color: '#8b5cf6',
        condition: (data) => data.chaptersCompleted >= 3
    },
    lifelongLearner: {
        id: 'lifelongLearner',
        name: '终身学习',
        description: '完成5个章节学习',
        icon: 'fa-book',
        color: '#ec4899',
        condition: (data) => data.chaptersCompleted >= 5
    },
    quizMaster: {
        id: 'quizMaster',
        name: '答题王',
        description: '完成10道知识点测验',
        icon: 'fa-award',
        color: '#f97316',
        condition: (data) => data.quizzesCompleted >= 10
    },
    earlyBird: {
        id: 'earlyBird',
        name: '早起鸟',
        description: '在早上6-9点之间完成学习',
        icon: 'fa-sun',
        color: '#fbbf24',
        condition: (data) => data.earlyMorningStudy
    },
    perfectAttendance: {
        id: 'perfectAttendance',
        name: '全勤奖',
        description: '连续7天学习',
        icon: 'fa-calendar-check',
        color: '#06b6d4',
        condition: (data) => data.streakDays >= 7
    },
    projectMaster: {
        id: 'projectMaster',
        name: '项目达人',
        description: '完成5个实战项目',
        icon: 'fa-rocket',
        color: '#ef4444',
        condition: (data) => data.projectsCompleted >= 5
    },
    dataCleaner: {
        id: 'dataCleaner',
        name: '数据清洗专家',
        description: '完成销售数据清洗项目',
        icon: 'fa-broom',
        color: '#10b981',
        condition: (data) => data.completedProjectIds.includes('project1')
    },
    analystPro: {
        id: 'analystPro',
        name: '分析高手',
        description: '完成RFM用户分层项目',
        icon: 'fa-chart-line',
        color: '#3b82f6',
        condition: (data) => data.completedProjectIds.includes('project4')
    }
};

function initAchievementSystem() {
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    if (!currentUser) return;

    updateUserAchievementData();
    
    if (typeof updateProgressDisplay === 'function') {
        updateProgressDisplay();
    }
}

function getUserAchievementData() {
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    if (!currentUser) return null;

    const userData = JSON.parse(localStorage.getItem(`achievement_data_${currentUser.id}`)) || {
        chaptersCompleted: 0,
        quizzesCompleted: 0,
        bestScore: 0,
        earlyMorningStudy: false,
        streakDays: 0,
        lastStudyDate: null,
        codeChallengesCompleted: 0,
        unlockedAchievements: []
    };

    return userData;
}

function saveUserAchievementData(data) {
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    if (!currentUser) return;

    localStorage.setItem(`achievement_data_${currentUser.id}`, JSON.stringify(data));
}

function updateUserAchievementData() {
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    if (!currentUser) return;

    let data = getUserAchievementData();

    const chapters = ['chapter1', 'chapter2', 'chapter3', 'chapter4', 'chapter5', 'chapter6'];
    let completedChapters = 0;
    let maxScore = 0;

    chapters.forEach(chapter => {
        const test = getChapterTest(chapter);
        if (test) {
            completedChapters++;
            if (test.score > maxScore) {
                maxScore = test.score;
            }
        }
    });

    const quizKeys = Object.keys(localStorage).filter(key => key.startsWith('quiz_'));
    let completedQuizzes = 0;
    quizKeys.forEach(key => {
        const quizData = JSON.parse(localStorage.getItem(key));
        if (quizData && quizData.isCorrect) {
            completedQuizzes++;
        }
    });

    const hour = new Date().getHours();
    const earlyMorning = hour >= 6 && hour < 9;

    const today = new Date().toDateString();
    const lastStudy = data.lastStudyDate;
    let streakDays = data.streakDays;

    if (lastStudy !== today) {
        const yesterday = new Date();
        yesterday.setDate(yesterday.getDate() - 1);
        if (lastStudy === yesterday.toDateString()) {
            streakDays++;
        } else if (lastStudy !== today) {
            streakDays = 1;
        }
        data.lastStudyDate = today;
    }

    data.chaptersCompleted = completedChapters;
    data.quizzesCompleted = completedQuizzes;
    data.bestScore = maxScore;
    data.earlyMorningStudy = data.earlyMorningStudy || earlyMorning;
    data.streakDays = streakDays;

    saveUserAchievementData(data);
}

function checkAchievements(type, data) {
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    if (!currentUser) return;

    updateUserAchievementData();
    
    const userData = getUserAchievementData();
    const unlocked = loadAchievement();

    Object.values(ACHIEVEMENTS).forEach(achievement => {
        if (!unlocked.includes(achievement.id) && achievement.condition(userData)) {
            unlockAchievement(achievement.id);
        }
    });
}

function unlockAchievement(achievementId) {
    const achievement = ACHIEVEMENTS[achievementId];
    if (!achievement) return;

    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    if (!currentUser) return;

    let unlocked = loadAchievement();
    
    if (unlocked.includes(achievementId)) return;

    unlocked.push(achievementId);
    saveAchievement(achievementId);

    const userData = getUserAchievementData();
    userData.unlockedAchievements = unlocked;
    saveUserAchievementData(userData);

    showAchievementUnlock(achievement);
}

function showAchievementUnlock(achievement) {
    const existingPopup = document.querySelector('.achievement-popup');
    if (existingPopup) return;

    const popup = document.createElement('div');
    popup.className = 'achievement-popup';
    popup.innerHTML = `
        <div class="achievement-popup-icon" style="background: linear-gradient(135deg, ${achievement.color}, ${achievement.color}88);">
            <i class="fas ${achievement.icon}"></i>
        </div>
        <div class="achievement-popup-content">
            <div class="achievement-popup-badge">🎉 新成就解锁</div>
            <h3 class="achievement-popup-title">${achievement.name}</h3>
            <p class="achievement-popup-desc">${achievement.description}</p>
        </div>
        <button class="achievement-popup-close" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;

    document.body.appendChild(popup);

    requestAnimationFrame(() => {
        popup.classList.add('achievement-popup-show');
    });

    setTimeout(() => {
        popup.classList.remove('achievement-popup-show');
        setTimeout(() => popup.remove(), 300);
    }, 4000);
}

function saveAchievement(achievementId) {
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    if (!currentUser) return;

    const key = `achievements_${currentUser.id}`;
    const achievements = JSON.parse(localStorage.getItem(key)) || [];
    
    if (!achievements.includes(achievementId)) {
        achievements.push(achievementId);
        localStorage.setItem(key, JSON.stringify(achievements));
    }
}

function loadAchievement() {
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    if (!currentUser) return [];

    const key = `achievements_${currentUser.id}`;
    return JSON.parse(localStorage.getItem(key)) || [];
}

function getAllAchievements() {
    return Object.values(ACHIEVEMENTS).map(achievement => {
        const unlocked = loadAchievement();
        return {
            ...achievement,
            unlocked: unlocked.includes(achievement.id)
        };
    });
}

function getLearningProgress() {
    const userData = getUserAchievementData();
    if (!userData) return 0;

    const totalChapters = 6;
    const chapterWeight = 60;
    const quizWeight = 20;
    const streakWeight = 10;
    const scoreWeight = 10;

    const chapterProgress = (userData.chaptersCompleted / totalChapters) * chapterWeight;
    const quizProgress = Math.min(userData.quizzesCompleted / 10, 1) * quizWeight;
    const streakProgress = Math.min(userData.streakDays / 7, 1) * streakWeight;
    const scoreProgress = (userData.bestScore / 100) * scoreWeight;

    const totalProgress = chapterProgress + quizProgress + streakProgress + scoreProgress;
    
    return Math.round(Math.min(totalProgress, 100));
}

function getChapterProgress(chapterNum) {
    const test = getChapterTest(`chapter${chapterNum}`);
    return test ? test.score : 0;
}

function renderAchievementsPage() {
    const achievements = getAllAchievements();
    const container = document.getElementById('achievements-grid');
    if (!container) return;

    container.innerHTML = achievements.map(achievement => `
        <div class="achievement-card ${achievement.unlocked ? 'unlocked' : 'locked'}">
            <div class="achievement-icon" style="${achievement.unlocked ? `background: linear-gradient(135deg, ${achievement.color}, ${achievement.color}88);` : ''}">
                <i class="fas ${achievement.unlocked ? achievement.icon : 'fa-lock'}"></i>
            </div>
            <h3 class="achievement-name">${achievement.name}</h3>
            <p class="achievement-desc">${achievement.description}</p>
            ${achievement.unlocked ? 
                '<div class="achievement-badge unlocked-badge"><i class="fas fa-check"></i> 已解锁</div>' : 
                '<div class="achievement-badge locked-badge"><i class="fas fa-lock"></i> 未解锁</div>'
            }
        </div>
    `).join('');

    const progressBar = document.getElementById('progress-bar');
    const progressText = document.getElementById('progress-text');
    const progressPercent = document.getElementById('progress-percent');
    
    if (progressBar) {
        const progress = getLearningProgress();
        progressBar.style.width = `${progress}%`;
        progressBar.setAttribute('data-progress', progress);
    }
    if (progressText) {
        progressText.textContent = getLearningProgress() + '%';
    }
    if (progressPercent) {
        const progress = getLearningProgress();
        progressPercent.textContent = `${progress}%`;
    }
}

if (typeof window !== 'undefined') {
    window.checkAchievements = checkAchievements;
    window.getLearningProgress = getLearningProgress;
    window.getAllAchievements = getAllAchievements;
    window.renderAchievementsPage = renderAchievementsPage;
    window.updateUserAchievementData = updateUserAchievementData;
}

// ==================== 项目系统功能 ====================

function initProjectSystem() {
    initProjectFilters();
}

function initProjectFilters() {
    const filterBtns = document.querySelectorAll('.filter-btn');
    const projectCards = document.querySelectorAll('.project-detail-card');

    if (filterBtns.length === 0 || projectCards.length === 0) return;

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const filter = btn.dataset.filter;

            projectCards.forEach(card => {
                if (filter === 'all' || card.dataset.difficulty === filter) {
                    card.style.display = 'flex';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
}

function saveProjectProgress(projectId, code, result) {
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    if (!currentUser) return;

    const key = `project_progress_${currentUser.id}_${projectId}`;
    const data = { code, result, timestamp: Date.now() };
    localStorage.setItem(key, JSON.stringify(data));

    checkAchievements('project_complete', { projectId });
}

function getProjectProgress(projectId) {
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    if (!currentUser) return null;

    const key = `project_progress_${currentUser.id}_${projectId}`;
    const data = localStorage.getItem(key);
    return data ? JSON.parse(data) : null;
}

if (typeof window !== 'undefined') {
    window.initProjectSystem = initProjectSystem;
    window.saveProjectProgress = saveProjectProgress;
    window.getProjectProgress = getProjectProgress;
}

document.addEventListener('DOMContentLoaded', () => {
    initProjectSystem();
});