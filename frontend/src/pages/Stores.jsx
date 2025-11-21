import { useState, useEffect } from 'react'
import { toast } from 'react-toastify'
import api from '../services/api'
import { useAuth } from '../context/AuthContext'
import DataTable from '../components/DataTable'
import Modal from '../components/Modal'
import './Page.css'

const Stores = () => {
  const [stores, setStores] = useState([])
  const [loading, setLoading] = useState(true)
  const [modalOpen, setModalOpen] = useState(false)
  const [editingStore, setEditingStore] = useState(null)
  const [formData, setFormData] = useState({ name: '', location: '' })
  const { isAdmin, isEmployee } = useAuth()

  useEffect(() => {
    fetchStores()
  }, [])

  const fetchStores = async () => {
    try {
      const response = await api.get('/stores')
      setStores(response.data.stores || [])
    } catch (error) {
      const errorCode = error.response?.status
      if (errorCode && errorCode >= 500) {
        toast.error('Failed to load stores. Please check database connection.')
      } else {
        setStores([])
      }
    } finally {
      setLoading(false)
    }
  }

  const handleAdd = () => {
    setEditingStore(null)
    setFormData({ name: '', location: '' })
    setModalOpen(true)
  }

  const handleEdit = (store) => {
    setEditingStore(store)
    setFormData({ name: store.name || '', location: store.location || '' })
    setModalOpen(true)
  }

  const handleDelete = async (store) => {
    if (!window.confirm(`Delete store ${store.name}?`)) return
    try {
      await api.delete(`/stores/${store.store_id}`)
      toast.success('Store deleted successfully')
      fetchStores()
    } catch (error) {
      toast.error(error.response?.data?.message || 'Failed to delete store')
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      if (editingStore) {
        await api.put(`/stores/${editingStore.store_id}`, formData)
        toast.success('Store updated successfully')
      } else {
        await api.post('/stores', formData)
        toast.success('Store created successfully')
      }
      setModalOpen(false)
      setFormData({ name: '', location: '' })
      setEditingStore(null)
      fetchStores()
    } catch (error) {
      toast.error(error.response?.data?.message || 'Operation failed')
    }
  }

  const columns = [
    { key: 'store_id', label: 'ID' },
    { key: 'name', label: 'Name' },
    { key: 'location', label: 'Location' }
  ]

  if (loading) return <div className="spinner"></div>

  return (
    <div className="page">
      <h1 className="page-title">Stores</h1>
      <DataTable
        data={stores}
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
          setFormData({ name: '', location: '' })
          setEditingStore(null)
        }}
        title={editingStore ? 'Edit Store' : 'Add Store'}
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
            <label>Location *</label>
            <input
              type="text"
              className="input"
              value={formData.location}
              onChange={(e) => setFormData({ ...formData, location: e.target.value })}
              required
            />
          </div>
          <div className="form-actions">
            <button type="button" className="btn btn-secondary" onClick={() => setModalOpen(false)}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary">
              {editingStore ? 'Update' : 'Create'}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  )
}

export default Stores

