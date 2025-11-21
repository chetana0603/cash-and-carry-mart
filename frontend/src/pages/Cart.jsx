import { useState, useEffect } from 'react'
import { toast } from 'react-toastify'
import api from '../services/api'
import { useAuth } from '../context/AuthContext'
import Modal from '../components/Modal'
import './Page.css'
import './Cart.css'

const Cart = () => {
  const [cartItems, setCartItems] = useState([])
  const [customers, setCustomers] = useState([])
  const [products, setProducts] = useState([])
  const [stores, setStores] = useState([])
  const [employees, setEmployees] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedCustomer, setSelectedCustomer] = useState(null)
  const [checkoutModalOpen, setCheckoutModalOpen] = useState(false)
  const [addItemModalOpen, setAddItemModalOpen] = useState(false)
  const [formData, setFormData] = useState({
    customer_id: '',
    product_id: '',
    quantity: 1
  })
  const [checkoutData, setCheckoutData] = useState({
    customer_id: '',
    store_id: '',
    employee_id: ''
  })
  const { isEmployee } = useAuth()

  useEffect(() => {
    if (selectedCustomer) {
      fetchCartItems()
    }
  }, [selectedCustomer])

  useEffect(() => {
    fetchInitialData()
  }, [])

  const fetchInitialData = async () => {
    try {
      const [customersRes, productsRes, storesRes, employeesRes] = await Promise.allSettled([
        api.get('/customers'),
        api.get('/products'),
        api.get('/stores'),
        api.get('/employees')
      ])
      
      // Handle each response, set empty array on error (empty data is OK)
      if (customersRes.status === 'fulfilled') {
        setCustomers(customersRes.value.data.customers || [])
      } else {
        setCustomers([])
      }
      
      if (productsRes.status === 'fulfilled') {
        setProducts(productsRes.value.data.products || [])
      } else {
        setProducts([])
      }
      
      if (storesRes.status === 'fulfilled') {
        setStores(storesRes.value.data.stores || [])
      } else {
        setStores([])
      }
      
      if (employeesRes.status === 'fulfilled') {
        setEmployees(employeesRes.value.data.employees || [])
      } else {
        setEmployees([])
      }
      
      // Only show error if all requests failed
      const allFailed = [customersRes, productsRes, storesRes, employeesRes].every(r => r.status === 'rejected')
      if (allFailed) {
        toast.error('Failed to load data. Please check database connection.')
      }
    } catch (error) {
      console.error('Error loading data:', error)
      // Set empty arrays so page still renders
      setCustomers([])
      setProducts([])
      setStores([])
      setEmployees([])
    } finally {
      setLoading(false)
    }
  }

  const fetchCartItems = async () => {
    if (!selectedCustomer) return
    try {
      const response = await api.get(`/cart/customer/${selectedCustomer}`)
      setCartItems(response.data.cart)
    } catch (error) {
      toast.error('Failed to load cart items')
    }
  }

  const handleAddItem = () => {
    if (!selectedCustomer) {
      toast.error('Please select a customer first')
      return
    }
    setFormData({ customer_id: selectedCustomer, product_id: '', quantity: 1 })
    setAddItemModalOpen(true)
  }

  const handleAddItemSubmit = async (e) => {
    e.preventDefault()
    try {
      await api.post('/cart', {
        customer_id: selectedCustomer,
        product_id: formData.product_id,
        quantity: parseInt(formData.quantity)
      })
      toast.success('Item added to cart')
      setAddItemModalOpen(false)
      fetchCartItems()
    } catch (error) {
      toast.error(error.response?.data?.message || 'Failed to add item')
    }
  }

  const handleUpdateQuantity = async (cartId, newQuantity) => {
    if (newQuantity <= 0) {
      handleRemoveItem(cartId)
      return
    }
    try {
      await api.put(`/cart/${cartId}`, { quantity: newQuantity })
      toast.success('Quantity updated')
      fetchCartItems()
    } catch (error) {
      toast.error('Failed to update quantity')
    }
  }

  const handleRemoveItem = async (cartId) => {
    try {
      await api.delete(`/cart/${cartId}`)
      toast.success('Item removed from cart')
      fetchCartItems()
    } catch (error) {
      toast.error('Failed to remove item')
    }
  }

  const handleCheckout = () => {
    if (cartItems.length === 0) {
      toast.error('Cart is empty')
      return
    }
    setCheckoutData({
      customer_id: selectedCustomer,
      store_id: '',
      employee_id: ''
    })
    setCheckoutModalOpen(true)
  }

  const handleCheckoutSubmit = async (e) => {
    e.preventDefault()
    try {
      const items = cartItems.map(item => ({
        product_id: item.product_id,
        quantity: item.quantity,
        unit_price: item.price
      }))

      await api.post('/orders', {
        customer_id: checkoutData.customer_id,
        store_id: checkoutData.store_id,
        employee_id: checkoutData.employee_id || null,
        items: items
      })

      toast.success('Order created successfully!')
      setCheckoutModalOpen(false)
      setCartItems([])
      setSelectedCustomer(null)
    } catch (error) {
      toast.error(error.response?.data?.message || 'Failed to create order')
    }
  }

  const totalAmount = cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0)

  if (loading) return <div className="spinner"></div>

  return (
    <div className="page">
      <h1 className="page-title">Cart Management</h1>
      
      <div className="cart-container">
        <div className="cart-sidebar">
          <h2>Select Customer</h2>
          <select
            className="input"
            value={selectedCustomer || ''}
            onChange={(e) => setSelectedCustomer(e.target.value ? parseInt(e.target.value) : null)}
            style={{ marginBottom: '16px' }}
          >
            <option value="">-- Select Customer --</option>
            {customers.map((customer) => (
              <option key={customer.customer_id} value={customer.customer_id}>
                {customer.first_name} {customer.last_name} - {customer.phone}
              </option>
            ))}
          </select>

          {selectedCustomer && (
            <>
              <button className="btn btn-primary" onClick={handleAddItem} style={{ width: '100%', marginBottom: '16px' }}>
                ➕ Add Item
              </button>
              {cartItems.length > 0 && (
                <button className="btn btn-success" onClick={handleCheckout} style={{ width: '100%' }}>
                  🛒 Checkout
                </button>
              )}
            </>
          )}
        </div>

        <div className="cart-main">
          {!selectedCustomer ? (
            <div className="empty-state">
              <p>Please select a customer to view their cart</p>
            </div>
          ) : cartItems.length === 0 ? (
            <div className="empty-state">
              <p>Cart is empty. Add items to get started!</p>
            </div>
          ) : (
            <>
              <table className="table">
                <thead>
                  <tr>
                    <th>Product</th>
                    <th>Price</th>
                    <th>Quantity</th>
                    <th>Subtotal</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {cartItems.map((item) => (
                    <tr key={item.cart_id}>
                      <td>{item.product_name}</td>
                      <td>₹{item.price?.toLocaleString()}</td>
                      <td>
                        <div className="quantity-controls">
                          <button
                            className="btn-icon"
                            onClick={() => handleUpdateQuantity(item.cart_id, item.quantity - 1)}
                          >
                            ➖
                          </button>
                          <span>{item.quantity}</span>
                          <button
                            className="btn-icon"
                            onClick={() => handleUpdateQuantity(item.cart_id, item.quantity + 1)}
                          >
                            ➕
                          </button>
                        </div>
                      </td>
                      <td>₹{(item.price * item.quantity).toLocaleString()}</td>
                      <td>
                        <button
                          className="btn-icon btn-icon-danger"
                          onClick={() => handleRemoveItem(item.cart_id)}
                        >
                          🗑️
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
                <tfoot>
                  <tr>
                    <td colSpan="3" style={{ textAlign: 'right', fontWeight: 'bold' }}>Total:</td>
                    <td style={{ fontWeight: 'bold', fontSize: '18px' }}>₹{totalAmount.toLocaleString()}</td>
                    <td></td>
                  </tr>
                </tfoot>
              </table>
            </>
          )}
        </div>
      </div>

      <Modal
        isOpen={addItemModalOpen}
        onClose={() => setAddItemModalOpen(false)}
        title="Add Item to Cart"
      >
        <form onSubmit={handleAddItemSubmit}>
          <div className="form-group">
            <label>Product *</label>
            <select
              className="input"
              value={formData.product_id}
              onChange={(e) => setFormData({ ...formData, product_id: e.target.value })}
              required
            >
              <option value="">Select Product</option>
              {products.filter(p => p.availability).map((product) => (
                <option key={product.product_id} value={product.product_id}>
                  {product.name} - ₹{product.price?.toLocaleString()}
                </option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label>Quantity *</label>
            <input
              type="number"
              className="input"
              value={formData.quantity}
              onChange={(e) => setFormData({ ...formData, quantity: e.target.value })}
              required
              min="1"
            />
          </div>
          <div className="form-actions">
            <button type="button" className="btn btn-secondary" onClick={() => setAddItemModalOpen(false)}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary">
              Add to Cart
            </button>
          </div>
        </form>
      </Modal>

      <Modal
        isOpen={checkoutModalOpen}
        onClose={() => setCheckoutModalOpen(false)}
        title="Checkout"
      >
        <form onSubmit={handleCheckoutSubmit}>
          <div className="form-group">
            <label>Store *</label>
            <select
              className="input"
              value={checkoutData.store_id}
              onChange={(e) => setCheckoutData({ ...checkoutData, store_id: e.target.value })}
              required
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
            <label>Employee</label>
            <select
              className="input"
              value={checkoutData.employee_id}
              onChange={(e) => setCheckoutData({ ...checkoutData, employee_id: e.target.value || null })}
            >
              <option value="">Select Employee (Optional)</option>
              {employees.map((employee) => (
                <option key={employee.employee_id} value={employee.employee_id}>
                  {employee.name}
                </option>
              ))}
            </select>
          </div>
          <div className="checkout-summary">
            <h3>Order Summary</h3>
            {cartItems.map((item) => (
              <div key={item.cart_id} className="checkout-item">
                <span>{item.product_name} x {item.quantity}</span>
                <span>₹{(item.price * item.quantity).toLocaleString()}</span>
              </div>
            ))}
            <div className="checkout-total">
              <strong>Total: ₹{totalAmount.toLocaleString()}</strong>
            </div>
          </div>
          <div className="form-actions">
            <button type="button" className="btn btn-secondary" onClick={() => setCheckoutModalOpen(false)}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary">
              Create Order
            </button>
          </div>
        </form>
      </Modal>
    </div>
  )
}

export default Cart

