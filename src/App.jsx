import { useState, useEffect } from 'react';
import { Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Home from './components/Home';
import CoursesList from './components/CoursesList';
import CourseDetail from './components/CourseDetail';
import ChapterPage from './components/ChapterPage';
import ProjectsList from './components/ProjectsList';
import Login from './components/Login';
import Register from './components/Register';

function App() {
  const [currentUser, setCurrentUser] = useState(null);
  const [completedChapters, setCompletedChapters] = useState([]);
  const [completedProjects, setCompletedProjects] = useState([]);

  useEffect(() => {
    const savedUser = localStorage.getItem('currentUser');
    const savedChapters = localStorage.getItem('completedChapters');
    const savedProjects = localStorage.getItem('completedProjects');
    
    if (savedUser) {
      setCurrentUser(JSON.parse(savedUser));
    }
    if (savedChapters) {
      setCompletedChapters(JSON.parse(savedChapters));
    }
    if (savedProjects) {
      setCompletedProjects(JSON.parse(savedProjects));
    }
  }, []);

  useEffect(() => {
    localStorage.setItem('currentUser', JSON.stringify(currentUser));
    localStorage.setItem('completedChapters', JSON.stringify(completedChapters));
    localStorage.setItem('completedProjects', JSON.stringify(completedProjects));
  }, [currentUser, completedChapters, completedProjects]);

  const handleLogin = (user) => {
    setCurrentUser(user);
  };

  const handleLogout = () => {
    setCurrentUser(null);
  };

  const handleRegister = (user) => {
    console.log('Registered:', user);
  };

  const handleCompleteChapter = (chapterId) => {
    if (!completedChapters.includes(chapterId)) {
      setCompletedChapters(prev => [...prev, chapterId]);
    }
  };

  return (
    <div className="min-h-screen bg-light">
      <Header currentUser={currentUser} onLogout={handleLogout} />
      <main>
        <Routes>
          <Route
            path="/"
            element={
              <Home
                completedChapters={completedChapters}
                completedProjects={completedProjects}
              />
            }
          />
          <Route path="/courses" element={<CoursesList />} />
          <Route
            path="/course/:courseId"
            element={
              <CourseDetail
                completedChapters={completedChapters}
                onCompleteChapter={handleCompleteChapter}
              />
            }
          />
          <Route
            path="/chapter/:chapterId"
            element={
              <ChapterPage
                completedChapters={completedChapters}
                onCompleteChapter={handleCompleteChapter}
              />
            }
          />
          <Route path="/projects" element={<ProjectsList />} />
          <Route
            path="/login"
            element={<Login onLogin={handleLogin} />}
          />
          <Route
            path="/register"
            element={<Register onRegister={handleRegister} />}
          />
        </Routes>
      </main>
      <footer className="bg-dark text-white py-4 mt-8">
        <div className="container text-center">
          <p>© 2024 数析学院 - 商务数据分析在线教育平台</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
