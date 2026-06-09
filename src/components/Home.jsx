import { Link } from 'react-router-dom'
import { COURSES, PROJECTS } from '../data/courses'

export default function Home({ completedChapters, completedProjects }) {
  const totalCourses = Object.keys(COURSES).length
  const totalChapters = Object.keys(COURSES).reduce((sum, cid) => sum + COURSES[cid].chapters.length, 0)
  const totalProjects = PROJECTS.length
  
  const chapterProgress = totalChapters > 0 ? Math.round((completedChapters.length / totalChapters) * 100) : 0
  const projectProgress = totalProjects > 0 ? Math.round((completedProjects.length / totalProjects) * 100) : 0

  const featuredCourses = Object.values(COURSES).slice(0, 4)
  const featuredProjects = PROJECTS.slice(0, 3)

  return (
    <div className="container mt-5">
      <section className="mb-8">
        <h1 className="display-4 text-center mb-4">欢迎来到数析学院</h1>
        <p className="text-center text-muted mb-8">
          掌握商务数据分析技能，开启数据驱动决策之旅
        </p>
        
        <div className="row">
          <div className="col-md-4">
            <div className="card text-center p-4 bg-primary text-white">
              <div className="text-4xl mb-2">📚</div>
              <div className="text-3xl font-bold">{totalCourses}</div>
              <div className="text-sm opacity-80">门课程</div>
            </div>
          </div>
          <div className="col-md-4">
            <div className="card text-center p-4 bg-success text-white">
              <div className="text-4xl mb-2">📖</div>
              <div className="text-3xl font-bold">{totalChapters}</div>
              <div className="text-sm opacity-80">章节</div>
            </div>
          </div>
          <div className="col-md-4">
            <div className="card text-center p-4 bg-warning text-white">
              <div className="text-4xl mb-2">🎯</div>
              <div className="text-3xl font-bold">{totalProjects}</div>
              <div className="text-sm opacity-80">个项目</div>
            </div>
          </div>
        </div>
      </section>

      <section className="mb-8">
        <h2 className="h2 mb-4">我的学习进度</h2>
        <div className="card p-4">
          <div className="mb-4">
            <div className="d-flex justify-content-between mb-2">
              <span>课程学习进度</span>
              <span>{chapterProgress}%</span>
            </div>
            <div className="progress">
              <div
                className="progress-bar bg-primary"
                style={{ width: `${chapterProgress}%` }}
              ></div>
            </div>
          </div>
          <div>
            <div className="d-flex justify-content-between mb-2">
              <span>项目完成进度</span>
              <span>{projectProgress}%</span>
            </div>
            <div className="progress">
              <div
                className="progress-bar bg-success"
                style={{ width: `${projectProgress}%` }}
              ></div>
            </div>
          </div>
        </div>
      </section>

      <section className="mb-8">
        <div className="d-flex justify-content-between items-center mb-4">
          <h2 className="h2">热门课程</h2>
          <Link to="/courses" className="text-primary">查看全部 →</Link>
        </div>
        <div className="row">
          {featuredCourses.map(course => (
            <div key={course.id} className="col-md-3 mb-4">
              <Link to={`/course/${course.id}`} className="text-decoration-none">
                <div className="card h-100 course-card transition-all duration-300 hover:shadow-lg">
                  <div className="card-body">
                    <div className="text-3xl mb-3">{course.icon}</div>
                    <h3 className="h5 text-dark">{course.title}</h3>
                    <p className="text-muted text-sm">{course.description}</p>
                    <div className="mt-3 d-flex justify-content-between text-sm">
                      <span className="badge bg-info text-white">{course.level}</span>
                      <span className="text-muted">{course.duration}</span>
                    </div>
                  </div>
                </div>
              </Link>
            </div>
          ))}
        </div>
      </section>

      <section>
        <div className="d-flex justify-content-between items-center mb-4">
          <h2 className="h2">实战项目</h2>
          <Link to="/projects" className="text-primary">查看全部 →</Link>
        </div>
        <div className="row">
          {featuredProjects.map(project => (
            <div key={project.id} className="col-md-4 mb-4">
              <div className="card h-100">
                <div className="card-body">
                  <h3 className="h5 text-dark">{project.title}</h3>
                  <p className="text-muted text-sm mb-3">{project.description}</p>
                  <div className="d-flex justify-content-between items-center">
                    <span className={`badge ${
                      project.difficulty === '初级' ? 'bg-success' :
                      project.difficulty === '中级' ? 'bg-warning' : 'bg-danger'
                    } text-white`}>
                      {project.difficulty}
                    </span>
                    <span className="text-sm text-muted">{project.duration}</span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}
