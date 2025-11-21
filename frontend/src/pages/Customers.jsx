import { useState, useEffect } from 'react'
import { toast } from 'react-toastify'
import api from '../services/api'
import { useAuth } from '../context/AuthContext'
import DataTable from '../components/DataTable'
import Modal from '../components/Modal'
import './Page.css'

const Customers = () => {
  const [customers, setCustomers] = useState([])
  const [loading, setLoading] = useState(true)
  const [modalOpen, setModalOpen] = useState(false)
  const [editingCustomer, setEditingCustomer] = useState(null)
  const [formData, setFormData] = useState({
    first_name: '',
    middle_name: '',
    last_name: '',
    phone: '',
    email: '',
    address: ''
  })
  const { isAdmin, isEmployee } = useAuth()

  useEffect(() => {
    fetchCustomers()
  }, [])

  const fetchCustomers = async () => {
    try {
      const response = await api.get('/customers')
      setCustomers(response.data.customers || [])
    } catch (error) {
      // Only show error for real failures, not empty data
      const errorCode = error.response?.status
      if (errorCode && errorCode >= 500) {
        toast.error('Failed to load customers. Please check database connection.')
      } else {
        // Empty data is OK, just set empty array
        setCustomers([])
      }
    } finally {
      setLoading(false)
    }
  }

  const handleAdd = () => {
    setEditingCustomer(null)
    setFormData({
      first_name: '',
      middle_name: '',
      last_name: '',
      phone: '',
      email: '',
      address: ''
    })
    setModalOpen(true)
  }

  const handleEdit = (customer) => {
    setEditingCustomer(customer)
    setFormData({
      first_name: customer.first_name || '',
      middle_name: customer.middle_name || '',
      last_name: customer.last_name || '',
      phone: customer.phone || '',
      email: customer.email || '',
      address: customer.address || ''
    })
    setModalOpen(true)
  }

  const handleDelete = async (customer) => {
    if (!window.confirm(`Delete customer ${customer.first_name} ${customer.last_name}?`)) return
    
    try {
      await api.delete(`/customers/${customer.customer_id}`)
      toast.success('Customer deleted successfully')
      fetchCustomers()
    } catch (error) {
      toast.error(error.response?.data?.message || 'Failed to delete customer')
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      if (editingCustomer) {
        await api.put(`/customers/${editingCustomer.customer_id}`, formData)
        toast.success('Customer updated successfully')
      } else {
        await api.post('/customers', formData)
        toast.success('Customer created successfully')
      }
      setModalOpen(false)
      setFormData({
        first_name: '',
        middle_name: '',
        last_name: '',
        phone: '',
        email: '',
        address: ''
      })
      setEditingCustomer(null)
      fetchCustomers()
    } catch (error) {
      toast.error(error.response?.data?.message || 'Operation failed')
    }
  }

  const columns = [
    { key: 'customer_id', label: 'ID' },
    { key: 'first_name', label: 'First Name' },
    { key: 'last_name', label: 'Last Name' },
    { key: 'phone', label: 'Phone' },
    { key: 'email', label: 'Email' },
    { key: 'address', label: 'Address' }
  ]

  if (loading) {
    return <div className="spinner"></div>
  }

  return (
    <div className="page">
      <h1 className="page-title">Customers</h1>
      <DataTable
        data={customers}
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
            first_name: '',
            middle_name: '',
            last_name: '',
            phone: '',
            email: '',
            address: ''
          })
          setEditingCustomer(null)
        }}
        title={editingCustomer ? 'Edit Customer' : 'Add Customer'}
      >
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>First Name *</label>
            <input
              type="text"
              className="input"
              value={formData.first_name}
              onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
              required
            />
          </div>
          <div className="form-group">
            <label>Middle Name</label>
            <input
              type="text"
              className="input"
              value={formData.middle_name}
              onChange={(e) => setFormData({ ...formData, middle_name: e.target.value })}
            />
          </div>
          <div className="form-group">
            <label>Last Name</label>
            <input
              type="text"
              className="input"
              value={formData.last_name}
              onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
            />
          </div>
          <div className="form-group">
            <label>Phone *</label>
            <input
              type="tel"
              className="input"
              value={formData.phone}
              onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
              required
            />
          </div>
          <div className="form-group">
            <label>Email *</label>
            <input
              type="email"
              className="input"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              required
            />
          </div>
          <div className="form-group">
            <label>Address *</label>
            <input
              type="text"
              className="input"
              value={formData.address}
              onChange={(e) => setFormData({ ...formData, address: e.target.value })}
              required
            />
          </div>
          <div className="form-actions">
            <button type="button" className="btn btn-secondary" onClick={() => setModalOpen(false)}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary">
              {editingCustomer ? 'Update' : 'Create'}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  )
}

export default Customers

