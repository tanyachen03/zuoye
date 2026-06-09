const Store = {
    data: {
        courseProgress: {},
        projectProgress: {},
        codeRunCount: 0,
        studyStreak: {
            current: 0,
            lastStudyDate: null
        },
        achievements: [],
        isLoggedIn: false,
        user: null
    },

    init() {
        const saved = localStorage.getItem('shuxi_store');
        if (saved) {
            try {
                this.data = JSON.parse(saved);
            } catch (e) {
                console.error('Failed to load store:', e);
            }
        }
    },

    save() {
        try {
            localStorage.setItem('shuxi_store', JSON.stringify(this.data));
        } catch (e) {
            console.error('Failed to save store:', e);
        }
    },

    getCourseProgress(courseId) {
        return this.data.courseProgress[courseId] || {
            completedLessons: [],
            currentLesson: null,
            lastAccessed: null
        };
    },

    setCurrentLesson(courseId, lessonId) {
        if (!this.data.courseProgress[courseId]) {
            this.data.courseProgress[courseId] = {
                completedLessons: [],
                currentLesson: null,
                lastAccessed: null
            };
        }
        this.data.courseProgress[courseId].currentLesson = lessonId;
        this.data.courseProgress[courseId].lastAccessed = new Date().toISOString();
        this.updateStudyStreak();
        this.save();
        this.checkCourseAchievements();
    },

    markLessonComplete(courseId, lessonId) {
        if (!this.data.courseProgress[courseId]) {
            this.data.courseProgress[courseId] = {
                completedLessons: [],
                currentLesson: null,
                lastAccessed: null
            };
        }
        if (!this.data.courseProgress[courseId].completedLessons.includes(lessonId)) {
            this.data.courseProgress[courseId].completedLessons.push(lessonId);
        }
        this.data.courseProgress[courseId].lastAccessed = new Date().toISOString();
        this.updateStudyStreak();
        this.save();
        this.checkCourseAchievements();
    },

    unmarkLessonComplete(courseId, lessonId) {
        if (!this.data.courseProgress[courseId]) {
            return;
        }
        const index = this.data.courseProgress[courseId].completedLessons.indexOf(lessonId);
        if (index > -1) {
            this.data.courseProgress[courseId].completedLessons.splice(index, 1);
        }
        this.save();
    },

    isLessonCompleted(courseId, lessonId) {
        const progress = this.getCourseProgress(courseId);
        return progress.completedLessons.includes(lessonId);
    },

    getCourseCompletionRate(courseId, totalLessons) {
        const progress = this.getCourseProgress(courseId);
        return Math.round((progress.completedLessons.length / totalLessons) * 100);
    },

    isCourseCompleted(courseId, totalLessons) {
        const progress = this.getCourseProgress(courseId);
        return progress.completedLessons.length >= totalLessons;
    },

    getProjectProgress(projectId) {
        return this.data.projectProgress[projectId] || {
            completed: false,
            lastAccessed: null
        };
    },

    markProjectComplete(projectId) {
        this.data.projectProgress[projectId] = {
            completed: true,
            lastAccessed: new Date().toISOString()
        };
        this.updateStudyStreak();
        this.save();
        this.checkProjectAchievements();
    },

    isProjectCompleted(projectId) {
        return this.data.projectProgress[projectId]?.completed || false;
    },

    incrementCodeRunCount() {
        this.data.codeRunCount++;
        this.save();
        this.checkCodeAchievements();
    },

    updateStudyStreak() {
        const today = new Date().toDateString();
        const lastDate = this.data.studyStreak.lastStudyDate;

        if (lastDate === today) {
            return;
        }

        const yesterday = new Date();
        yesterday.setDate(yesterday.getDate() - 1);

        if (lastDate === yesterday.toDateString()) {
            this.data.studyStreak.current++;
        } else if (lastDate !== today) {
            this.data.studyStreak.current = 1;
        }

        this.data.studyStreak.lastStudyDate = today;
        this.checkStreakAchievements();
    },

    getCompletedCoursesCount() {
        return Object.keys(this.data.courseProgress).filter(id => {
            const course = COURSES_DATA.find(c => c.id === id);
            return course && this.isCourseCompleted(id, course.lessons.length);
        }).length;
    },

    getCompletedProjectsCount() {
        return Object.keys(this.data.projectProgress).filter(id => {
            return this.data.projectProgress[id].completed;
        }).length;
    },

    checkCourseAchievements() {
        const completedCourses = this.getCompletedCoursesCount();

        if (completedCourses >= 1 && !this.data.achievements.includes('first-course')) {
            this.unlockAchievement('first-course');
        }
        if (completedCourses >= 5 && !this.data.achievements.includes('five-courses')) {
            this.unlockAchievement('five-courses');
        }
        if (completedCourses >= 12 && !this.data.achievements.includes('all-courses')) {
            this.unlockAchievement('all-courses');
        }
    },

    checkProjectAchievements() {
        const completedProjects = this.getCompletedProjectsCount();

        if (completedProjects >= 1 && !this.data.achievements.includes('first-project')) {
            this.unlockAchievement('first-project');
        }
        if (completedProjects >= 5 && !this.data.achievements.includes('five-projects')) {
            this.unlockAchievement('five-projects');
        }
        if (completedProjects >= 10 && !this.data.achievements.includes('all-projects')) {
            this.unlockAchievement('all-projects');
        }
    },

    checkStreakAchievements() {
        const streak = this.data.studyStreak.current;

        if (streak >= 3 && !this.data.achievements.includes('streak-3')) {
            this.unlockAchievement('streak-3');
        }
        if (streak >= 7 && !this.data.achievements.includes('streak-7')) {
            this.unlockAchievement('streak-7');
        }
        if (streak >= 30 && !this.data.achievements.includes('streak-30')) {
            this.unlockAchievement('streak-30');
        }
    },

    checkCodeAchievements() {
        const count = this.data.codeRunCount;

        if (count >= 50 && !this.data.achievements.includes('run-50')) {
            this.unlockAchievement('run-50');
        }
        if (count >= 100 && !this.data.achievements.includes('run-100')) {
            this.unlockAchievement('run-100');
        }
        if (count >= 500 && !this.data.achievements.includes('run-500')) {
            this.unlockAchievement('run-500');
        }
    },

    unlockAchievement(achievementId) {
        if (!this.data.achievements.includes(achievementId)) {
            this.data.achievements.push(achievementId);
            this.save();
            const achievement = ACHIEVEMENTS_DATA.find(a => a.id === achievementId);
            if (achievement) {
                App.showToast(`🎉 解锁成就：${achievement.title}`);
            }
        }
    },

    isAchievementUnlocked(achievementId) {
        return this.data.achievements.includes(achievementId);
    },

    login(email) {
        this.data.isLoggedIn = true;
        this.data.user = { email };
        this.save();
    },

    logout() {
        this.data.isLoggedIn = false;
        this.data.user = null;
        this.save();
    },

    reset() {
        this.data = {
            courseProgress: {},
            projectProgress: {},
            codeRunCount: 0,
            studyStreak: {
                current: 0,
                lastStudyDate: null
            },
            achievements: [],
            isLoggedIn: false,
            user: null
        };
        this.save();
    }
};

Store.init();
