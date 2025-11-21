import { useState } from 'react'
import './DataTable.css'

const DataTable = ({ 
  data, 
  columns, 
  onEdit, 
  onDelete, 
  onAdd,
  canEdit = true,
  canDelete = true,
  canAdd = true,
  searchable = true,
  searchPlaceholder = "Search..."
}) => {
  const [searchTerm, setSearchTerm] = useState('')
  const [currentPage, setCurrentPage] = useState(1)
  const itemsPerPage = 10

  const filteredData = data.filter((item) => {
    if (!searchTerm) return true
    return columns.some((col) => {
      const value = item[col.key]
      return value?.toString().toLowerCase().includes(searchTerm.toLowerCase())
    })
  })

  const totalPages = Math.ceil(filteredData.length / itemsPerPage)
  const startIndex = (currentPage - 1) * itemsPerPage
  const paginatedData = filteredData.slice(startIndex, startIndex + itemsPerPage)

  return (
    <div className="data-table-container">
      <div className="table-header">
        {searchable && (
          <input
            type="text"
            className="input search-input"
            placeholder={searchPlaceholder}
            value={searchTerm}
            onChange={(e) => {
              setSearchTerm(e.target.value)
              setCurrentPage(1)
            }}
          />
        )}
        {canAdd && onAdd && (
          <button className="btn btn-primary" onClick={onAdd}>
            ➕ Add New
          </button>
        )}
      </div>
      <div className="table-wrapper">
        <table className="table">
          <thead>
            <tr>
              {columns.map((col) => (
                <th key={col.key}>{col.label}</th>
              ))}
              {(canEdit || canDelete) && <th>Actions</th>}
            </tr>
          </thead>
          <tbody>
            {paginatedData.length === 0 ? (
              <tr>
                <td colSpan={columns.length + (canEdit || canDelete ? 1 : 0)} className="text-center">
                  No data available
                </td>
              </tr>
            ) : (
              paginatedData.map((row, index) => (
                <tr key={row.id || index}>
                  {columns.map((col) => (
                    <td key={col.key}>
                      {col.render ? col.render(row[col.key], row) : row[col.key]}
                    </td>
                  ))}
                  {(canEdit || canDelete) && (
                    <td>
                      <div className="action-buttons">
                        {canEdit && onEdit && (
                          <button
                            className="btn-icon"
                            onClick={() => onEdit(row)}
                            title="Edit"
                          >
                            ✏️
                          </button>
                        )}
                        {canDelete && onDelete && (
                          <button
                            className="btn-icon btn-icon-danger"
                            onClick={() => onDelete(row)}
                            title="Delete"
                          >
                            🗑️
                          </button>
                        )}
                      </div>
                    </td>
                  )}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
      {totalPages > 1 && (
        <div className="pagination">
          <button
            className="btn btn-secondary"
            onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
            disabled={currentPage === 1}
          >
            Previous
          </button>
          <span>
            Page {currentPage} of {totalPages}
          </span>
          <button
            className="btn btn-secondary"
            onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
            disabled={currentPage === totalPages}
          >
            Next
          </button>
        </div>
      )}
    </div>
  )
}

export default DataTable

