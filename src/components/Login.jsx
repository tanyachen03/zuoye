import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';

export default function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!username || !password) {
      setError('请填写用户名和密码');
      return;
    }

    const mockUsers = [
      { username: 'admin', password: '123456' },
      { username: 'user', password: 'password' }
    ];

    const user = mockUsers.find(u => u.username === username && u.password === password);
    
    if (user) {
      onLogin(user);
      navigate('/');
    } else {
      setError('用户名或密码错误');
    }
  };

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-6">
          <div className="card">
            <div className="card-header bg-primary text-white text-center">
              <h2>用户登录</h2>
            </div>
            <div className="card-body">
              {error && (
                <div className="alert alert-danger">{error}</div>
              )}
              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label className="form-label">用户名</label>
                  <input
                    type="text"
                    className="form-control"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="请输入用户名"
                  />
                </div>
                <div className="mb-3">
                  <label className="form-label">密码</label>
                  <input
                    type="password"
                    className="form-control"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="请输入密码"
                  />
                </div>
                <button type="submit" className="btn btn-primary w-100">
                  登录
                </button>
              </form>
              <p className="text-center mt-3">
                还没有账号？<Link to="/register">立即注册</Link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
