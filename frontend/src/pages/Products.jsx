import { useState, useEffect } from 'react'
import { toast } from 'react-toastify'
import api from '../services/api'
import { useAuth } from '../context/AuthContext'
import DataTable from '../components/DataTable'
import Modal from '../components/Modal'
import './Page.css'

const Products = () => {
  const [products, setProducts] = useState([])
  const [categories, setCategories] = useState([])
  const [suppliers, setSuppliers] = useState([])
  const [loading, setLoading] = useState(true)
  const [modalOpen, setModalOpen] = useState(false)
  const [editingProduct, setEditingProduct] = useState(null)
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    price: '',
    availability: true,
    category_id: '',
    supplier_id: ''
  })
  const { isAdmin, isEmployee } = useAuth()

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const [productsRes, categoriesRes, suppliersRes] = await Promise.all([
        api.get('/products'),
        api.get('/categories'),
        api.get('/suppliers')
      ])
      setProducts(productsRes.data.products || [])
      setCategories(categoriesRes.data.categories || [])
      setSuppliers(suppliersRes.data.suppliers || [])
    } catch (error) {
      const errorCode = error.response?.status
      if (errorCode && errorCode >= 500) {
        toast.error('Failed to load data. Please check database connection.')
      } else {
        setProducts([])
        setCategories([])
        setSuppliers([])
      }
    } finally {
      setLoading(false)
    }
  }

  const handleAdd = () => {
    setEditingProduct(null)
    setFormData({
      name: '',
      description: '',
      price: '',
      availability: true,
      category_id: '',
      supplier_id: ''
    })
    setModalOpen(true)
  }

  const handleEdit = (product) => {
    setEditingProduct(product)
    setFormData({
      name: product.name || '',
      description: product.description || '',
      price: product.price || '',
      availability: product.availability !== undefined ? product.availability : true,
      category_id: product.category_id || '',
      supplier_id: product.supplier_id || ''
    })
    setModalOpen(true)
  }

  const handleDelete = async (product) => {
    if (!window.confirm(`Delete product ${product.name}?`)) return
    try {
      await api.delete(`/products/${product.product_id}`)
      toast.success('Product deleted successfully')
      fetchData()
    } catch (error) {
      toast.error(error.response?.data?.message || 'Failed to delete product')
    }
  }

  const handleToggleAvailability = async (product) => {
    try {
      const payload = {
        name: product.name,
        description: product.description,
        price: parseFloat(product.price),
        availability: !product.availability,
        category_id: product.category_id,
        supplier_id: product.supplier_id
      }
      await api.put(`/products/${product.product_id}`, payload)
      toast.success(`Product marked as ${payload.availability ? 'available' : 'unavailable'}`)
      fetchData()
    } catch (error) {
      toast.error(error.response?.data?.message || 'Failed to update availability')
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const data = {
        ...formData,
        price: parseFloat(formData.price),
        category_id: formData.category_id || null,
        supplier_id: formData.supplier_id || null
      }
      if (editingProduct) {
        await api.put(`/products/${editingProduct.product_id}`, data)
        toast.success('Product updated successfully')
      } else {
        await api.post('/products', data)
        toast.success('Product created successfully')
      }
      setModalOpen(false)
      setFormData({
        name: '',
        description: '',
        price: '',
        availability: true,
        category_id: '',
        supplier_id: ''
      })
      setEditingProduct(null)
      fetchData()
    } catch (error) {
      toast.error(error.response?.data?.message || 'Operation failed')
    }
  }

  const columns = [
    { key: 'product_id', label: 'ID' },
    { key: 'name', label: 'Name' },
    { key: 'category_name', label: 'Category' },
    { key: 'supplier_name', label: 'Supplier' },
    { 
      key: 'price', 
      label: 'Price',
      render: (value) => `₹${value?.toLocaleString() || 0}`
    },
    { 
      key: 'availability', 
      label: 'Available',
      render: (value, row) => (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
          <span>{value ? '✅ Available' : '❌ Unavailable'}</span>
          {isEmployee() && (
            <button
              type="button"
              className="btn btn-secondary"
              style={{ padding: '4px 8px', fontSize: '12px' }}
              onClick={() => handleToggleAvailability(row)}
            >
              {value ? 'Mark Unavailable' : 'Mark Available'}
            </button>
          )}
        </div>
      )
    }
  ]

  if (loading) return <div className="spinner"></div>

  return (
    <div className="page">
      <h1 className="page-title">Products</h1>
      <DataTable
        data={products}
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
            description: '',
            price: '',
            availability: true,
            category_id: '',
            supplier_id: ''
          })
          setEditingProduct(null)
        }}
        title={editingProduct ? 'Edit Product' : 'Add Product'}
        size="large"
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
            <label>Description</label>
            <textarea
              className="input"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              rows="3"
            />
          </div>
          <div className="form-group">
            <label>Price *</label>
            <input
              type="number"
              className="input"
              value={formData.price}
              onChange={(e) => setFormData({ ...formData, price: e.target.value })}
              required
              min="0"
              step="0.01"
            />
          </div>
          <div className="form-group">
            <label>Category</label>
            <select
              className="input"
              value={formData.category_id}
              onChange={(e) => setFormData({ ...formData, category_id: e.target.value || null })}
            >
              <option value="">Select Category</option>
              {categories.map((cat) => (
                <option key={cat.category_id} value={cat.category_id}>
                  {cat.name}
                </option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label>Supplier</label>
            <select
              className="input"
              value={formData.supplier_id}
              onChange={(e) => setFormData({ ...formData, supplier_id: e.target.value || null })}
            >
              <option value="">Select Supplier</option>
              {suppliers.map((sup) => (
                <option key={sup.supplier_id} value={sup.supplier_id}>
                  {sup.name}
                </option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label>
              <input
                type="checkbox"
                checked={formData.availability}
                onChange={(e) => setFormData({ ...formData, availability: e.target.checked })}
              />
              {' '}Available
            </label>
          </div>
          <div className="form-actions">
            <button type="button" className="btn btn-secondary" onClick={() => setModalOpen(false)}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary">
              {editingProduct ? 'Update' : 'Create'}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  )
}

export default Products

