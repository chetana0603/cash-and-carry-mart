import { useState, useEffect } from 'react'
import { toast } from 'react-toastify'
import api from '../services/api'
import { useAuth } from '../context/AuthContext'
import DataTable from '../components/DataTable'
import Modal from '../components/Modal'
import './Page.css'

const Orders = () => {
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedOrder, setSelectedOrder] = useState(null)
  const [modalOpen, setModalOpen] = useState(false)
  const { isAdmin } = useAuth()

  useEffect(() => {
    fetchOrders()
  }, [])

  const fetchOrders = async () => {
    try {
      const response = await api.get('/orders')
      setOrders(response.data.orders)
    } catch (error) {
      toast.error('Failed to load orders')
    } finally {
      setLoading(false)
    }
  }

  const handleView = async (order) => {
    try {
      const response = await api.get(`/orders/${order.order_id}`)
      setSelectedOrder(response.data.order)
      setModalOpen(true)
    } catch (error) {
      toast.error('Failed to load order details')
    }
  }

  const handleStatusUpdate = async (order, newStatus) => {
    try {
      await api.put(`/orders/${order.order_id}/status`, { status: newStatus })
      toast.success('Order status updated')
      fetchOrders()
    } catch (error) {
      toast.error(error.response?.data?.message || 'Failed to update status')
    }
  }

  const handleDelete = async (order) => {
    if (!window.confirm(`Delete order #${order.order_id}?`)) return
    try {
      await api.delete(`/orders/${order.order_id}`)
      toast.success('Order deleted successfully')
      fetchOrders()
    } catch (error) {
      toast.error(error.response?.data?.message || 'Failed to delete order')
    }
  }

  const columns = [
    { key: 'order_id', label: 'Order ID' },
    { 
      key: 'customer_id', 
      label: 'Customer',
      render: (value, row) => `${row.first_name || ''} ${row.last_name || ''}`.trim() || `Customer #${value}`
    },
    { 
      key: 'total_amount', 
      label: 'Amount',
      render: (value) => `₹${value?.toLocaleString() || 0}`
    },
    { 
      key: 'status', 
      label: 'Status',
      render: (value) => (
        <span className={`status-badge status-${value?.toLowerCase()}`}>
          {value}
        </span>
      )
    },
    { 
      key: 'order_date', 
      label: 'Date',
      render: (value) => new Date(value).toLocaleDateString()
    }
  ]

  if (loading) return <div className="spinner"></div>

  return (
    <div className="page">
      <h1 className="page-title">Orders</h1>
      <DataTable
        data={orders}
        columns={columns}
        onEdit={handleView}
        onDelete={isAdmin() ? handleDelete : null}
        canAdd={false}
        canEdit={true}
        canDelete={isAdmin()}
        searchPlaceholder="Search orders..."
      />
      <Modal
        isOpen={modalOpen}
        onClose={() => {
          setModalOpen(false)
          setSelectedOrder(null)
        }}
        title={`Order #${selectedOrder?.order_id}`}
        size="large"
      >
        {selectedOrder && (
          <div>
            <div style={{ marginBottom: '24px' }}>
              <p><strong>Customer:</strong> {selectedOrder.first_name} {selectedOrder.last_name}</p>
              <p><strong>Date:</strong> {new Date(selectedOrder.order_date).toLocaleString()}</p>
              <p><strong>Status:</strong> 
                <span className={`status-badge status-${selectedOrder.status?.toLowerCase()}`} style={{ marginLeft: '8px' }}>
                  {selectedOrder.status}
                </span>
              </p>
              <p><strong>Total:</strong> ₹{selectedOrder.total_amount?.toLocaleString()}</p>
            </div>
            <h3>Items:</h3>
            <table className="table">
              <thead>
                <tr>
                  <th>Product</th>
                  <th>Quantity</th>
                  <th>Unit Price</th>
                  <th>Subtotal</th>
                </tr>
              </thead>
              <tbody>
                {selectedOrder.items?.map((item) => (
                  <tr key={item.order_item_id}>
                    <td>{item.product_name}</td>
                    <td>{item.quantity}</td>
                    <td>₹{item.unit_price?.toLocaleString()}</td>
                    <td>₹{item.subtotal?.toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            {isAdmin() && (
              <div className="form-actions" style={{ marginTop: '24px' }}>
                <button
                  className="btn btn-primary"
                  onClick={() => handleStatusUpdate(selectedOrder, 'PAID')}
                  disabled={selectedOrder.status === 'PAID'}
                >
                  Mark as Paid
                </button>
                <button
                  className="btn btn-secondary"
                  onClick={() => handleStatusUpdate(selectedOrder, 'SHIPPED')}
                  disabled={selectedOrder.status === 'SHIPPED' || selectedOrder.status === 'CANCELLED'}
                >
                  Mark as Shipped
                </button>
                <button
                  className="btn btn-danger"
                  onClick={() => handleStatusUpdate(selectedOrder, 'CANCELLED')}
                  disabled={selectedOrder.status === 'CANCELLED'}
                >
                  Cancel Order
                </button>
              </div>
            )}
          </div>
        )}
      </Modal>
    </div>
  )
}

export default Orders

