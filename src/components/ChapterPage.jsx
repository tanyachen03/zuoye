import { useState, useRef, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { COURSES, CHAPTERS } from '../data/courses';
export default function ChapterPage({ completedChapters, onCompleteChapter }) {
 const { chapterId } = useParams();
 const navigate = useNavigate();
 const chapter = CHAPTERS[chapterId];
 const [code, setCode] = useState('');
 const [output, setOutput] = useState('');
 const [showAnswer, setShowAnswer] = useState({});
 const [selectedAnswers, setSelectedAnswers] = useState({});
 const [exerciseResults, setExerciseResults] = useState({});
 const codeRef = useRef(null);
 if (!chapter) {
 return <div className="container mt-5">章节不存在</div>;
 }
 const course = COURSES[chapter.course_id];
 const chapters = course.chapters.map(chId => CHAPTERS[chId]);
 const currentIndex = chapters.findIndex(ch => ch.id === chapter.id);
 const prevChapter = currentIndex > 0 ? chapters[currentIndex - 1] : null;
 const nextChapter = currentIndex < chapters.length - 1 ? chapters[currentIndex + 1] : null;
 useEffect(() => {
 setCode(chapter.starter_code);
 }, [chapter]);
 const handleRunCode = () => {
 try {
 const logs = [];
 const originalLog = console.log;
 console.log = (...args) => logs.push(args.map(a => 
 typeof a === 'object' ? JSON.stringify(a, null, 2) : String(a)).join(' '));
 try {
 new Function(code)();
 }
 catch (e) {
 logs.push(`错误: ${e.message}`);
 }
 console.log = originalLog;
 setOutput(logs.join('\n'));
 }
 catch (e) {
 setOutput(`执行错误: ${e.message}`);
 }
 };
 const handleCopyCode = () => {
 navigator.clipboard.writeText(chapter.code_example);
 };
 const handlePasteCode = () => {
 setCode(chapter.code_example);
 };
 const handleCheckAnswer = (index) => {
 const userAnswer = selectedAnswers[index];
 const correctAnswer = chapter.exercises[index].answer;
 const isCorrect = userAnswer && userAnswer.toLowerCase().includes(correctAnswer.toLowerCase());
 setExerciseResults(prev => ({ ...prev, [index]: isCorrect }));
 setShowAnswer(prev => ({ ...prev, [index]: true }));
 };
 const handleCompleteChapter = () => {
 onCompleteChapter(chapter.id);
 navigate(`/course/${chapter.course_id}`);
 };
 const isCompleted = completedChapters.includes(chapter.id);
 return (<div className="container mt-5">
 <div className="d-flex justify-content-between items-center mb-4">
 <div>
 <Link to={`/course/${chapter.course_id}`} className="text-muted text-sm">← 返回课程</Link>
 <h1 className="h1 mt-2">{chapter.title}</h1>
 </div>
 <div className="d-flex gap-2">
 <Link to="/projects" className="btn btn-secondary">项目实战</Link>
 <Link to="/courses" className="btn btn-secondary">课程体系</Link>
 <Link to="/" className="btn btn-primary">首页</Link>
 </div>
 </div>

 <div className="row">
 <div className="col-lg-8">
 <div className="card mb-4">
 <div className="card-header bg-primary text-white">📖 理论知识</div>
 <div className="card-body">
 <div className="theory-content" dangerouslySetInnerHTML={{ __html: chapter.theory }}></div>
 </div>
 </div>

 <div className="card mb-4">
 <div className="card-header bg-info text-white">💻 代码示例</div>
 <div className="card-body">
 <div className="d-flex justify-content-between mb-3">
 <span>点击下方按钮复制代码</span>
 <button onClick={handleCopyCode} className="btn btn-sm btn-primary">复制代码</button>
 </div>
 <pre className="bg-dark text-light p-3 rounded"><code>{chapter.code_example}</code></pre>
 </div>
 </div>

 <div className="card mb-4">
 <div className="card-header bg-success text-white">🎯 动手实践</div>
 <div className="card-body">
 <div className="d-flex justify-content-between mb-3">
 <span>在下方编辑器中编写代码</span>
 <div className="d-flex gap-2">
 <button onClick={handlePasteCode} className="btn btn-sm btn-secondary">粘贴示例</button>
 <button onClick={handleRunCode} className="btn btn-sm btn-success">运行代码</button>
 </div>
 </div>
 <textarea ref={codeRef} value={code} onChange={(e) => setCode(e.target.value)} className="form-control font-mono text-sm" rows={10} style={{ resize: 'vertical' }}></textarea>
 {output && (<div className="mt-3 p-3 bg-dark text-light rounded" style={{ maxHeight: '200px', overflowY: 'auto' }}>
 <pre>{output}</pre>
 </div>)}
 </div>
 </div>

 <div className="card mb-4">
 <div className="card-header bg-warning text-white">📝 课后习题</div>
 <div className="card-body">
 {chapter.exercises.map((exercise, index) => (<div key={index} className="mb-4 p-3 bg-light rounded">
 <p className="font-weight-bold mb-2">{index + 1}. {exercise.question}</p>
 <input type="text" placeholder="请输入答案" value={selectedAnswers[index] || ''} onChange={(e) => setSelectedAnswers(prev => ({ ...prev, [index]: e.target.value }))} className="form-control mb-2"/>
 <div className="d-flex gap-2">
 <button onClick={() => handleCheckAnswer(index)} className="btn btn-sm btn-primary">
 提交答案
 </button>
 <button onClick={() => setShowAnswer(prev => ({ ...prev, [index]: !prev[index] }))} className="btn btn-sm btn-secondary">
 {showAnswer[index] ? '隐藏答案' : '查看答案'}
 </button>
 </div>
 {showAnswer[index] && (<div className={`mt-2 p-2 rounded ${exerciseResults[index] ? 'bg-success text-white' : 'bg-danger text-white'}`}>
 {exerciseResults[index] ? '✓ 回答正确！' : `✗ 正确答案: ${exercise.answer}`}
 </div>)}
 </div>))}
 </div>
 </div>

 <button onClick={handleCompleteChapter} className={`btn w-100 py-3 mb-4 ${isCompleted ? 'btn-secondary' : 'btn-primary'}`}>
 {isCompleted ? '✓ 已完成本章节' : '完成本章节'}
 </button>
 </div>

 <div className="col-lg-4">
 <div className="card mb-4">
 <div className="card-header bg-dark text-white">📚 课程目录</div>
 <div className="card-body p-0">
 <div className="list-group">
 {chapters.map((ch, idx) => (<Link key={ch.id} to={`/chapter/${ch.id}`} className={`list-group-item list-group-item-action ${ch.id === chapter.id ? 'active' : ''}`}>
 <div className="d-flex justify-content-between align-items-center">
 <span>{idx + 1}. {ch.title}</span>
 {completedChapters.includes(ch.id) && <span className="text-success">✓</span>}
 </div>
 </Link>))}
 </div>
 </div>
 </div>

 <div className="card">
 <div className="card-header bg-dark text-white">🔄 章节导航</div>
 <div className="card-body">
 {prevChapter && (<Link to={`/chapter/${prevChapter.id}`} className="d-block mb-2 btn btn-secondary w-full">
 ← 上一章节
 </Link>)}
 {nextChapter && (<Link to={`/chapter/${nextChapter.id}`} className="d-block btn btn-primary w-full">
 下一章节 →
 </Link>)}
 </div>
 </div>
 </div>
 </div>
 </div>);
}
