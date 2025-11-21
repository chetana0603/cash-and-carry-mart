import { useState, useEffect } from 'react'
import { toast } from 'react-toastify'
import api from '../services/api'
import { useAuth } from '../context/AuthContext'
import DataTable from '../components/DataTable'
import Modal from '../components/Modal'
import './Page.css'

const Inventory = () => {
  const [inventory, setInventory] = useState([])
  const [products, setProducts] = useState([])
  const [stores, setStores] = useState([])
  const [loading, setLoading] = useState(true)
  const [modalOpen, setModalOpen] = useState(false)
  const [editingItem, setEditingItem] = useState(null)
  const [formData, setFormData] = useState({
    product_id: '',
    store_id: '',
    quantity_in_stock: ''
  })
  const { isAdmin, isEmployee } = useAuth()

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const [inventoryRes, productsRes, storesRes] = await Promise.all([
        api.get('/inventory'),
        api.get('/products'),
        api.get('/stores')
      ])
      setInventory(inventoryRes.data.inventory || [])
      setProducts(productsRes.data.products || [])
      setStores(storesRes.data.stores || [])
    } catch (error) {
      const errorCode = error.response?.status
      if (errorCode && errorCode >= 500) {
        toast.error('Failed to load data. Please check database connection.')
      } else {
        setInventory([])
        setProducts([])
        setStores([])
      }
    } finally {
      setLoading(false)
    }
  }

  const handleAdd = () => {
    setEditingItem(null)
    setFormData({ product_id: '', store_id: '', quantity_in_stock: '' })
    setModalOpen(true)
  }

  const handleEdit = (item) => {
    setEditingItem(item)
    setFormData({
      product_id: item.product_id,
      store_id: item.store_id,
      quantity_in_stock: item.quantity_in_stock
    })
    setModalOpen(true)
  }

  const handleDelete = async (item) => {
    if (!window.confirm(`Delete inventory record?`)) return
    try {
      await api.delete(`/inventory/${item.inventory_id}`)
      toast.success('Inventory record deleted successfully')
      fetchData()
    } catch (error) {
      toast.error(error.response?.data?.message || 'Failed to delete')
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const data = {
        ...formData,
        quantity_in_stock: parseInt(formData.quantity_in_stock)
      }
      if (editingItem) {
        await api.put(`/inventory/${editingItem.inventory_id}`, data)
        toast.success('Inventory updated successfully')
      } else {
        await api.post('/inventory', data)
        toast.success('Inventory record created successfully')
      }
      setModalOpen(false)
      setFormData({ product_id: '', store_id: '', quantity_in_stock: '' })
      setEditingItem(null)
      fetchData()
    } catch (error) {
      toast.error(error.response?.data?.message || 'Operation failed')
    }
  }

  const columns = [
    { key: 'inventory_id', label: 'ID' },
    { key: 'product_name', label: 'Product' },
    { key: 'store_name', label: 'Store' },
    { key: 'quantity_in_stock', label: 'Quantity' },
    {
      key: 'quantity_in_stock',
      label: 'Status',
      render: (value) => {
        if (value <= 10) return <span style={{ color: 'var(--accent)', fontWeight: 'bold' }}>⚠️ Low Stock</span>
        if (value <= 50) return <span style={{ color: 'var(--warning)' }}>⚠️ Medium</span>
        return <span style={{ color: 'var(--success)' }}>✅ Good</span>
      }
    }
  ]

  if (loading) return <div className="spinner"></div>

  return (
    <div className="page">
      <h1 className="page-title">Inventory</h1>
      <DataTable
        data={inventory}
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
          setFormData({ product_id: '', store_id: '', quantity_in_stock: '' })
          setEditingItem(null)
        }}
        title={editingItem ? 'Edit Inventory' : 'Add Inventory'}
      >
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Product *</label>
            <select
              className="input"
              value={formData.product_id}
              onChange={(e) => setFormData({ ...formData, product_id: e.target.value })}
              required
              disabled={!!editingItem}
            >
              <option value="">Select Product</option>
              {products.map((product) => (
                <option key={product.product_id} value={product.product_id}>
                  {product.name}
                </option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label>Store *</label>
            <select
              className="input"
              value={formData.store_id}
              onChange={(e) => setFormData({ ...formData, store_id: e.target.value })}
              required
              disabled={!!editingItem}
            >
              <option value="">Select Store</option>
              {stores.map((store) => (
                <option key={store.store_id} value={store.store_id}>
                  {store.name} - {store.location}
                </option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label>Quantity in Stock *</label>
            <input
              type="number"
              className="input"
              value={formData.quantity_in_stock}
              onChange={(e) => setFormData({ ...formData, quantity_in_stock: e.target.value })}
              required
              min="0"
            />
          </div>
          <div className="form-actions">
            <button type="button" className="btn btn-secondary" onClick={() => setModalOpen(false)}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary">
              {editingItem ? 'Update' : 'Create'}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  )
}

export default Inventory

