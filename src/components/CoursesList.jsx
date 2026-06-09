import { Link } from 'react-router-dom';
import { COURSES } from '../data/courses';
export default function CoursesList() {
 const courses = Object.values(COURSES);
 const levelColors = {
 '入门': 'bg-success',
 '初级': 'bg-info',
 '中级': 'bg-warning',
 '高级': 'bg-danger'
 };
 return (<div className="container mt-5">
 <h1 className="h1 mb-6">课程体系</h1>
 
 <div className="row">
 {courses.map(course => (<div key={course.id} className="col-lg-4 col-md-6 mb-4">
 <Link to={`/course/${course.id}`} className="text-decoration-none">
 <div className="card h-100 course-card transition-all duration-300 hover:shadow-lg">
 <div className="card-body">
 <div className="text-4xl mb-3">{course.icon}</div>
 <h3 className="h4 text-dark mb-2">{course.title}</h3>
 <p className="text-muted text-sm mb-3">{course.description}</p>
 <div className="d-flex justify-content-between items-center">
 <span className={`badge ${levelColors[course.level]} text-white`}>
 {course.level}
 </span>
 <span className="text-sm text-muted">{course.duration}</span>
 </div>
 <div className="mt-3 pt-3 border-top">
 <span className="text-sm text-muted">
 {course.chapters.length} 个章节
 </span>
 </div>
 </div>
 </div>
 </Link>
 </div>))}
 </div>
 </div>);
}
