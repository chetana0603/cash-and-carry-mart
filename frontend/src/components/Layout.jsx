import { Outlet, useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import './Layout.css'

const Layout = () => {
  const { user, logout, isAdmin } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  const menuItems = [
    { path: '/dashboard', label: 'Dashboard', icon: '📊' },
    { path: '/customers', label: 'Customers', icon: '👥' },
    { path: '/employees', label: 'Employees', icon: '👔' },
    { path: '/stores', label: 'Stores', icon: '🏪' },
    { path: '/products', label: 'Products', icon: '📦' },
    { path: '/inventory', label: 'Inventory', icon: '📋' },
    { path: '/orders', label: 'Orders', icon: '🛒' },
    { path: '/suppliers', label: 'Suppliers', icon: '🚚' },
    { path: '/cart', label: 'Cart', icon: '🛍️' }
  ]

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="layout">
      <aside className="sidebar">
        <div className="sidebar-header">
          <h2>💰 Cash & Carry</h2>
          <p>Management System</p>
        </div>
        <nav className="sidebar-nav">
          {menuItems.map((item) => (
            <button
              key={item.path}
              className={`nav-item ${location.pathname === item.path ? 'active' : ''}`}
              onClick={() => navigate(item.path)}
            >
              <span className="nav-icon">{item.icon}</span>
              <span className="nav-label">{item.label}</span>
            </button>
          ))}
        </nav>
        <div className="sidebar-footer">
          <div className="user-info">
            <p className="user-name">{user?.username}</p>
            <p className="user-role">{user?.role}</p>
          </div>
          <button className="btn btn-danger" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </aside>
      <main className="main-content">
        <Outlet />
      </main>
    </div>
  )
}

export default Layout

