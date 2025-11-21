import { useState, useEffect } from 'react'
import { toast } from 'react-toastify'
import api from '../services/api'
import { useAuth } from '../context/AuthContext'
import DataTable from '../components/DataTable'
import Modal from '../components/Modal'
import './Page.css'

const Suppliers = () => {
  const [suppliers, setSuppliers] = useState([])
  const [loading, setLoading] = useState(true)
  const [modalOpen, setModalOpen] = useState(false)
  const [editingSupplier, setEditingSupplier] = useState(null)
  const [formData, setFormData] = useState({ name: '', contact: '', address: '' })
  const { isAdmin, isEmployee } = useAuth()

  useEffect(() => {
    fetchSuppliers()
  }, [])

  const fetchSuppliers = async () => {
    try {
      const response = await api.get('/suppliers')
      setSuppliers(response.data.suppliers || [])
    } catch (error) {
      const errorCode = error.response?.status
      if (errorCode && errorCode >= 500) {
        toast.error('Failed to load suppliers. Please check database connection.')
      } else {
        setSuppliers([])
      }
    } finally {
      setLoading(false)
    }
  }

  const handleAdd = () => {
    setEditingSupplier(null)
    setFormData({ name: '', contact: '', address: '' })
    setModalOpen(true)
  }

  const handleEdit = (supplier) => {
    setEditingSupplier(supplier)
    setFormData({
      name: supplier.name || '',
      contact: supplier.contact || '',
      address: supplier.address || ''
    })
    setModalOpen(true)
  }

  const handleDelete = async (supplier) => {
    if (!window.confirm(`Delete supplier ${supplier.name}?`)) return
    try {
      await api.delete(`/suppliers/${supplier.supplier_id}`)
      toast.success('Supplier deleted successfully')
      fetchSuppliers()
    } catch (error) {
      toast.error(error.response?.data?.message || 'Failed to delete supplier')
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      if (editingSupplier) {
        await api.put(`/suppliers/${editingSupplier.supplier_id}`, formData)
        toast.success('Supplier updated successfully')
      } else {
        await api.post('/suppliers', formData)
        toast.success('Supplier created successfully')
      }
      setModalOpen(false)
      setFormData({ name: '', contact: '', address: '' })
      setEditingSupplier(null)
      fetchSuppliers()
    } catch (error) {
      toast.error(error.response?.data?.message || 'Operation failed')
    }
  }

  const columns = [
    { key: 'supplier_id', label: 'ID' },
    { key: 'name', label: 'Name' },
    { key: 'contact', label: 'Contact' },
    { key: 'address', label: 'Address' }
  ]

  if (loading) return <div className="spinner"></div>

  return (
    <div className="page">
      <h1 className="page-title">Suppliers</h1>
      <DataTable
        data={suppliers}
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
          setFormData({ name: '', contact: '', address: '' })
          setEditingSupplier(null)
        }}
        title={editingSupplier ? 'Edit Supplier' : 'Add Supplier'}
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
            <label>Contact</label>
            <input
              type="text"
              className="input"
              value={formData.contact}
              onChange={(e) => setFormData({ ...formData, contact: e.target.value })}
            />
          </div>
          <div className="form-group">
            <label>Address</label>
            <input
              type="text"
              className="input"
              value={formData.address}
              onChange={(e) => setFormData({ ...formData, address: e.target.value })}
            />
          </div>
          <div className="form-actions">
            <button type="button" className="btn btn-secondary" onClick={() => setModalOpen(false)}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary">
              {editingSupplier ? 'Update' : 'Create'}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  )
}

export default Suppliers

