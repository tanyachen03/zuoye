const ACHIEVEMENTS_DATA = [
    {
        id: "first-course",
        title: "初学者",
        icon: "🎓",
        description: "完成第1门课程",
        condition: "完成任意1门课程"
    },
    {
        id: "five-courses",
        title: "五门课程",
        icon: "📚",
        description: "完成5门课程",
        condition: "完成5门课程"
    },
    {
        id: "all-courses",
        title: "全能分析师",
        icon: "🏆",
        description: "完成所有课程",
        condition: "完成全部12门课程"
    },
    {
        id: "first-project",
        title: "实战新手",
        icon: "🛠️",
        description: "完成第1个项目",
        condition: "完成任意1个项目"
    },
    {
        id: "five-projects",
        title: "项目达人",
        icon: "💼",
        description: "完成5个项目",
        condition: "完成5个项目"
    },
    {
        id: "all-projects",
        title: "项目大师",
        icon: "👑",
        description: "完成所有项目",
        condition: "完成全部10个项目"
    },
    {
        id: "streak-3",
        title: "三天学习",
        icon: "🔥",
        description: "连续学习3天",
        condition: "连续3天有学习记录"
    },
    {
        id: "streak-7",
        title: "一周坚持",
        icon: "⭐",
        description: "连续学习7天",
        condition: "连续7天有学习记录"
    },
    {
        id: "streak-30",
        title: "一个月坚持",
        icon: "🌟",
        description: "连续学习30天",
        condition: "连续30天有学习记录"
    },
    {
        id: "run-50",
        title: "代码新手",
        icon: "💻",
        description: "累计运行代码50次",
        condition: "运行代码50次"
    },
    {
        id: "run-100",
        title: "代码达人",
        icon: "⚡",
        description: "累计运行代码100次",
        condition: "运行代码100次"
    },
    {
        id: "run-500",
        title: "代码大师",
        icon: "🚀",
        description: "累计运行代码500次",
        condition: "运行代码500次"
    }
];

if (typeof module !== 'undefined' && module.exports) {
    module.exports = ACHIEVEMENTS_DATA;
}
