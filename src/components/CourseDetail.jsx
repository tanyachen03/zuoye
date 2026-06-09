import { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { COURSES, CHAPTERS } from '../data/courses';
export default function CourseDetail({ completedChapters, onCompleteChapter }) {
 const { courseId } = useParams();
 const course = COURSES[courseId];
 const [activeTab, setActiveTab] = useState('chapters');
 if (!course) {
 return <div className="container mt-5">课程不存在</div>;
 }
 const chapters = course.chapters.map(chId => CHAPTERS[chId]);
 const completedCount = chapters.filter(ch => completedChapters.includes(ch.id)).length;
 const progress = Math.round((completedCount / chapters.length) * 100);
 return (<div className="container mt-5">
 <div className="card mb-4">
 <div className="card-body">
 <div className="d-flex align-items-start justify-between">
 <div>
 <div className="text-5xl mb-3">{course.icon}</div>
 <h1 className="h1 mb-2">{course.title}</h1>
 <p className="text-muted">{course.description}</p>
 </div>
 <div className="text-right">
 <span className={`badge ${course.level === '入门' ? 'bg-success' :
 course.level === '初级' ? 'bg-info' :
 course.level === '中级' ? 'bg-warning' : 'bg-danger'} text-white px-3 py-1`}>
 {course.level}
 </span>
 <div className="mt-2 text-muted">{course.duration}</div>
 </div>
 </div>
 </div>
 </div>

 <div className="card mb-4">
 <div className="card-body">
 <div className="d-flex justify-content-between align-items-center mb-2">
 <span>学习进度</span>
 <span>{completedCount}/{chapters.length} 章节</span>
 </div>
 <div className="progress">
 <div className="progress-bar bg-primary" style={{ width: `${progress}%` }}></div>
 </div>
 </div>
 </div>

 <div className="d-flex gap-2 mb-4">
 <button onClick={() => setActiveTab('chapters')} className={`btn ${activeTab === 'chapters' ? 'btn-primary' : 'btn-secondary'}`}>
 课程章节
 </button>
 <button onClick={() => setActiveTab('overview')} className={`btn ${activeTab === 'overview' ? 'btn-primary' : 'btn-secondary'}`}>
 课程概述
 </button>
 </div>

 {activeTab === 'chapters' && (<div className="card">
 <div className="card-body">
 <h3 className="h3 mb-4">课程章节</h3>
 <div className="list-group">
 {chapters.map((chapter, index) => {
 const isCompleted = completedChapters.includes(chapter.id);
 return (<Link key={chapter.id} to={`/chapter/${chapter.id}`} className="list-group-item list-group-item-action chapter-item d-flex justify-content-between align-items-center">
 <div>
 <div className="d-flex align-items-center gap-2">
 <span className="text-muted">#{index + 1}</span>
 <span>{chapter.title}</span>
 {isCompleted && <span className="text-success">✓</span>}
 </div>
 </div>
 <div className="d-flex gap-2">
 {isCompleted && (<span className="badge bg-success text-white">已完成</span>)}
 </div>
 </Link>);
 })}
 </div>
 </div>
 </div>)}

 {activeTab === 'overview' && (<div className="card">
 <div className="card-body">
 <h3 className="h3 mb-3">课程概述</h3>
 <p>{course.description}</p>
 <div className="mt-4">
 <h4 className="h4 mb-2">课程特点</h4>
 <ul className="list-unstyled">
 <li className="mb-2">• 深入浅出的理论讲解</li>
 <li className="mb-2">• 丰富的实战案例</li>
 <li className="mb-2">• 课后练习巩固知识</li>
 <li className="mb-2">• 项目实战提升技能</li>
 </ul>
 </div>
 <div className="mt-4">
 <h4 className="h4 mb-2">学习目标</h4>
 <ul className="list-unstyled">
 <li className="mb-2">• 掌握{course.title}的核心概念</li>
 <li className="mb-2">• 能够独立完成相关数据分析任务</li>
 <li className="mb-2">• 具备解决实际业务问题的能力</li>
 </ul>
 </div>
 </div>
 </div>)}
 </div>);
}
