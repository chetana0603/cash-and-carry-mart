import { useState, useEffect } from 'react'
import { toast } from 'react-toastify'
import api from '../services/api'
import { useAuth } from '../context/AuthContext'
import DataTable from '../components/DataTable'
import Modal from '../components/Modal'
import './Page.css'

const Employees = () => {
  const [employees, setEmployees] = useState([])
  const [stores, setStores] = useState([])
  const [loading, setLoading] = useState(true)
  const [modalOpen, setModalOpen] = useState(false)
  const [editingEmployee, setEditingEmployee] = useState(null)
  const [formData, setFormData] = useState({
    name: '',
    job_title: '',
    hire_date: '',
    salary: '',
    store_id: '',
    email: ''
  })
  const { isAdmin, isEmployee } = useAuth()

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const [employeesRes, storesRes] = await Promise.all([
        api.get('/employees'),
        api.get('/stores')
      ])
      setEmployees(employeesRes.data.employees || [])
      setStores(storesRes.data.stores || [])
    } catch (error) {
      const errorCode = error.response?.status
      if (errorCode && errorCode >= 500) {
        toast.error('Failed to load data. Please check database connection.')
      } else {
        setEmployees([])
        setStores([])
      }
    } finally {
      setLoading(false)
    }
  }

  const handleAdd = () => {
    setEditingEmployee(null)
    setFormData({
      name: '',
      job_title: '',
      hire_date: '',
      salary: '',
      store_id: '',
      email: ''
    })
    setModalOpen(true)
  }

  const handleEdit = (employee) => {
    setEditingEmployee(employee)
    setFormData({
      name: employee.name || '',
      job_title: employee.job_title || '',
      hire_date: employee.hire_date || '',
      salary: employee.salary || '',
      store_id: employee.store_id || '',
      email: employee.email || ''
    })
    setModalOpen(true)
  }

  const handleDelete = async (employee) => {
    if (!window.confirm(`Delete employee ${employee.name}?`)) return
    
    try {
      await api.delete(`/employees/${employee.employee_id}`)
      toast.success('Employee deleted successfully')
      fetchData()
    } catch (error) {
      toast.error(error.response?.data?.message || 'Failed to delete employee')
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const data = { ...formData, salary: formData.salary ? parseFloat(formData.salary) : null }
      if (editingEmployee) {
        await api.put(`/employees/${editingEmployee.employee_id}`, data)
        toast.success('Employee updated successfully')
      } else {
        await api.post('/employees', data)
        toast.success('Employee created successfully')
      }
      setModalOpen(false)
      // Reset form data immediately
      setFormData({
        name: '',
        job_title: '',
        hire_date: '',
        salary: '',
        store_id: '',
        email: ''
      })
      setEditingEmployee(null)
      fetchData()
    } catch (error) {
      toast.error(error.response?.data?.message || 'Operation failed')
    }
  }

  const columns = [
    { key: 'employee_id', label: 'ID' },
    { key: 'name', label: 'Name' },
    { key: 'job_title', label: 'Job Title' },
    { key: 'email', label: 'Email' },
    { key: 'store_name', label: 'Store' },
    { 
      key: 'salary', 
      label: 'Salary',
      render: (value) => value ? `₹${value.toLocaleString()}` : '-'
    }
  ]

  if (loading) return <div className="spinner"></div>

  return (
    <div className="page">
      <h1 className="page-title">Employees</h1>
      <DataTable
        data={employees}
        columns={columns}
        onAdd={isEmployee() ? handleAdd : null}
        onEdit={isEmployee() ? handleEdit : null}
        onDelete={isEmployee() ? handleDelete : null}
        canAdd={isEmployee()}
        canEdit={isEmployee()}
        canDelete={isEmployee()}
      />
      <Modal
        isOpen={modalOpen}
        onClose={() => {
          setModalOpen(false)
          setFormData({
            name: '',
            job_title: '',
            hire_date: '',
            salary: '',
            store_id: '',
            email: ''
          })
          setEditingEmployee(null)
        }}
        title={editingEmployee ? 'Edit Employee' : 'Add Employee'}
      >
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Name *</label>
            <input
              type="text"
              className="input"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              required
            />
          </div>
          <div className="form-group">
            <label>Job Title</label>
            <input
              type="text"
              className="input"
              value={formData.job_title}
              onChange={(e) => setFormData({ ...formData, job_title: e.target.value })}
            />
          </div>
          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              className="input"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
            />
          </div>
          <div className="form-group">
            <label>Hire Date</label>
            <input
              type="date"
              className="input"
              value={formData.hire_date}
              onChange={(e) => setFormData({ ...formData, hire_date: e.target.value })}
            />
          </div>
          <div className="form-group">
            <label>Salary</label>
            <input
              type="number"
              className="input"
              value={formData.salary}
              onChange={(e) => setFormData({ ...formData, salary: e.target.value })}
              min="0"
              step="0.01"
            />
          </div>
          <div className="form-group">
            <label>Store</label>
            <select
              className="input"
              value={formData.store_id}
              onChange={(e) => setFormData({ ...formData, store_id: e.target.value || null })}
            >
              <option value="">Select Store</option>
              {stores.map((store) => (
                <option key={store.store_id} value={store.store_id}>
                  {store.name}
                </option>
              ))}
            </select>
          </div>
          <div className="form-actions">
            <button type="button" className="btn btn-secondary" onClick={() => setModalOpen(false)}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary">
              {editingEmployee ? 'Update' : 'Create'}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  )
}

export default Employees

