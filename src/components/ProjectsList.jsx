import { PROJECTS } from '../data/courses';
export default function ProjectsList() {
 const difficultyColors = {
 '初级': 'bg-success',
 '中级': 'bg-warning',
 '高级': 'bg-danger'
 };
 return (<div className="container mt-5">
 <h1 className="h1 mb-6">项目实战</h1>
 
 <div className="row">
 {PROJECTS.map(project => (<div key={project.id} className="col-lg-4 col-md-6 mb-4">
 <div className="card h-100">
 <div className="card-body">
 <h3 className="h4 mb-2">{project.title}</h3>
 <p className="text-muted text-sm mb-3">{project.description}</p>
 <div className="d-flex justify-content-between items-center mb-3">
 <span className={`badge ${difficultyColors[project.difficulty]} text-white`}>
 {project.difficulty}
 </span>
 <span className="text-sm text-muted">{project.duration}</span>
 </div>
 <div className="flex-wrap gap-1">
 {project.skills.map((skill, idx) => (<span key={idx} className="badge bg-light text-dark text-sm">
 {skill}
 </span>))}
 </div>
 </div>
 </div>
 </div>))}
 </div>
 </div>);
}
