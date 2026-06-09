import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

export default function Header({ currentUser, onLogout }) {
  const navigate = useNavigate()

  return (
    <header className="bg-primary text-white">
      <div className="container">
        <nav className="navbar navbar-expand-lg navbar-dark">
          <div className="container-fluid">
            <Link className="navbar-brand" to="/">
              <span className="fs-4">📊 数析学院</span>
            </Link>
            <button
              className="navbar-toggler"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#navbarNav"
              aria-controls="navbarNav"
              aria-expanded="false"
              aria-label="Toggle navigation"
            >
              <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarNav">
              <ul className="navbar-nav me-auto">
                <li className="nav-item">
                  <Link className="nav-link" to="/">首页</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/courses">课程体系</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/projects">项目实战</Link>
                </li>
              </ul>
              <div className="d-flex align-items-center">
                {currentUser ? (
                  <div className="d-flex align-items-center gap-3">
                    <span className="text-light">欢迎, {currentUser.username}</span>
                    <button
                      onClick={onLogout}
                      className="btn btn-light btn-sm"
                    >
                      退出登录
                    </button>
                  </div>
                ) : (
                  <div className="d-flex gap-2">
                    <button
                      onClick={() => navigate('/login')}
                      className="btn btn-light btn-sm"
                    >
                      登录
                    </button>
                    <button
                      onClick={() => navigate('/register')}
                      className="btn btn-outline-light btn-sm"
                    >
                      注册
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        </nav>
      </div>
    </header>
  )
}
