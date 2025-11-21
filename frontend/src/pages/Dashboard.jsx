import { useState, useEffect } from 'react'
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import api from '../services/api'
import { toast } from 'react-toastify'
import './Dashboard.css'

const COLORS = ['#A8E6CF', '#FFD3B6', '#FFAAA5', '#FF8B85', '#7FD3B8']

const Dashboard = () => {
  const [stats, setStats] = useState(null)
  const [bestSelling, setBestSelling] = useState([])
  const [recentOrders, setRecentOrders] = useState([])
  const [lowStock, setLowStock] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      setLoading(true)
      
      // Fetch data with better error handling
      const [statsRes, bestSellingRes, recentRes, lowStockRes] = await Promise.allSettled([
        api.get('/dashboard/stats'),
        api.get('/dashboard/best-selling?limit=5'),
        api.get('/dashboard/recent-orders?limit=5'),
        api.get('/inventory/low-stock?threshold=10').catch(() => ({ data: { items: [] } })) // Fallback if endpoint doesn't exist
      ])

      // Handle stats - this is critical, show error only if it fails
      if (statsRes.status === 'fulfilled') {
        setStats(statsRes.value.data.stats)
      } else {
        console.error('Stats error:', statsRes.reason)
        // Only show error if it's a real error (not just empty data)
        const errorCode = statsRes.reason?.response?.status
        if (errorCode && errorCode >= 500) {
          toast.error('Failed to load statistics. Please check database connection.')
        }
        // Set default stats for empty database
        setStats({
          total_customers: 0,
          total_products: 0,
          total_stores: 0,
          total_employees: 0,
          total_orders: 0,
          total_revenue: 0,
          today_revenue: 0,
          month_revenue: 0,
          low_stock_count: 0
        })
      }

      // Handle best selling - empty is OK, don't show error
      if (bestSellingRes.status === 'fulfilled') {
        setBestSelling(bestSellingRes.value.data.products || [])
      } else {
        console.warn('Best selling products:', bestSellingRes.reason?.response?.data?.message || 'No data')
        setBestSelling([])
      }

      // Handle recent orders - empty is OK, don't show error
      if (recentRes.status === 'fulfilled') {
        setRecentOrders(recentRes.value.data.orders || [])
      } else {
        console.warn('Recent orders:', recentRes.reason?.response?.data?.message || 'No data')
        setRecentOrders([])
      }

      // Handle low stock - empty is OK, don't show error
      if (lowStockRes.status === 'fulfilled') {
        setLowStock(lowStockRes.value.data?.items || [])
      } else {
        console.warn('Low stock items:', lowStockRes.reason?.response?.data?.message || 'No data')
        setLowStock([])
      }
    } catch (error) {
      toast.error('Failed to load dashboard data')
      console.error('Dashboard error:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
        <div className="spinner"></div>
      </div>
    )
  }

  // Show message if stats failed to load (only for real errors, not empty data)
  if (!stats) {
    return (
      <div className="dashboard">
        <h1 className="page-title">Dashboard</h1>
        <div style={{ textAlign: 'center', padding: '40px' }}>
          <p style={{ fontSize: '18px', color: 'var(--text-light)' }}>
            Unable to load dashboard data. This might be because:
          </p>
          <ul style={{ textAlign: 'left', display: 'inline-block', marginTop: '20px' }}>
            <li>Database connection issue</li>
            <li>Check browser console (F12) for detailed errors</li>
            <li>Check backend server is running</li>
          </ul>
          <button 
            onClick={fetchDashboardData} 
            className="btn btn-primary"
            style={{ marginTop: '20px' }}
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  const statCards = [
    { label: 'Total Revenue', value: `₹${stats?.total_revenue?.toLocaleString() || 0}`, color: 'primary', icon: '💰' },
    { label: 'Today\'s Revenue', value: `₹${stats?.today_revenue?.toLocaleString() || 0}`, color: 'success', icon: '📈' },
    { label: 'Total Orders', value: stats?.total_orders || 0, color: 'secondary', icon: '🛒' },
    { label: 'Total Customers', value: stats?.total_customers || 0, color: 'accent', icon: '👥' },
    { label: 'Total Products', value: stats?.total_products || 0, color: 'primary', icon: '📦' },
    { label: 'Low Stock Items', value: stats?.low_stock_count || 0, color: 'warning', icon: '⚠️' }
  ]

  return (
    <div className="dashboard">
      <h1 className="page-title">Dashboard</h1>
      
      <div className="stats-grid">
        {statCards.map((stat, index) => (
          <div key={index} className={`stat-card stat-${stat.color}`}>
            <div className="stat-icon">{stat.icon}</div>
            <div className="stat-content">
              <p className="stat-label">{stat.label}</p>
              <h3 className="stat-value">{stat.value}</h3>
            </div>
          </div>
        ))}
      </div>

      <div className="dashboard-grid">
        <div className="dashboard-card">
          <h2>Best Selling Products</h2>
          {bestSelling.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={bestSelling}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="total_sold" fill="#A8E6CF" name="Units Sold" />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-center">No data available</p>
          )}
        </div>

        <div className="dashboard-card">
          <h2>Revenue Distribution</h2>
          {bestSelling.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={bestSelling}
                  dataKey="total_revenue"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  label
                >
                  {bestSelling.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-center">No data available</p>
          )}
        </div>
      </div>

      <div className="dashboard-grid">
        <div className="dashboard-card">
          <h2>Recent Orders</h2>
          {recentOrders.length > 0 ? (
            <table className="table">
              <thead>
                <tr>
                  <th>Order ID</th>
                  <th>Customer</th>
                  <th>Amount</th>
                  <th>Status</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                {recentOrders.map((order) => (
                  <tr key={order.order_id}>
                    <td>#{order.order_id}</td>
                    <td>{order.customer_name}</td>
                    <td>₹{order.total_amount?.toLocaleString()}</td>
                    <td>
                      <span className={`status-badge status-${order.status?.toLowerCase()}`}>
                        {order.status}
                      </span>
                    </td>
                    <td>{new Date(order.order_date).toLocaleDateString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p className="text-center">No recent orders</p>
          )}
        </div>

        <div className="dashboard-card">
          <h2>Low Stock Alerts</h2>
          {lowStock.length > 0 ? (
            <div className="low-stock-list">
              {lowStock.map((item) => (
                <div key={item.inventory_id} className="low-stock-item">
                  <div>
                    <strong>{item.product_name}</strong>
                    <p>{item.store_name}</p>
                  </div>
                  <span className="stock-badge">{item.quantity_in_stock} left</span>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-center">All items are well stocked! ✅</p>
          )}
        </div>
      </div>
    </div>
  )
}

export default Dashboard

