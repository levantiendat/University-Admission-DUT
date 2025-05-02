<template>
    <div class="admin-convert-points">
      <div class="admin-page-header d-flex justify-content-between align-items-center">
        <div>
          <h2 class="admin-page-title">Quản lý quy đổi điểm</h2>
          <p class="admin-page-description">Quản lý cách quy đổi điểm giữa các phương thức xét tuyển</p>
        </div>
        <router-link to="/admins/convert-points/create" class="btn-create">
          <i class="bi bi-plus-circle me-2"></i>Thêm quy đổi điểm
        </router-link>
      </div>
  
      <!-- Search and Filter -->
      <div class="admin-card mb-4">
        <div class="row">
          <div class="col-md-6 mb-3">
            <div class="form-group">
              <label for="method-filter">Lọc theo phương thức xét tuyển</label>
              <select id="method-filter" v-model="filters.methodId" class="form-select" @change="applyFilters">
                <option value="">Tất cả phương thức</option>
                <option v-for="method in admissionMethods" :key="method.id" :value="method.id">
                  {{ method.name }}
                </option>
              </select>
            </div>
          </div>
          <div class="col-md-6 mb-3">
            <div class="form-group">
              <label for="search-input">Tìm kiếm</label>
              <div class="search-box">
                <i class="bi bi-search search-icon"></i>
                <input 
                  type="text" 
                  id="search-input"
                  v-model="searchQuery" 
                  class="search-input" 
                  placeholder="Tìm kiếm..." 
                  @input="applyFilters"
                >
              </div>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Loading Indicator -->
      <div v-if="loading" class="loading-container">
        <div class="spinner">
          <div class="bounce1"></div>
          <div class="bounce2"></div>
          <div class="bounce3"></div>
        </div>
        <p class="loading-text">Đang tải danh sách quy đổi điểm...</p>
      </div>
  
      <!-- Error Message -->
      <div v-else-if="error" class="error-message">
        <i class="bi bi-exclamation-triangle-fill error-icon"></i>
        <span>{{ error }}</span>
      </div>
  
      <!-- Convert Points Table -->
      <div v-else class="admin-card">
        <div class="table-responsive">
          <table class="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Phương thức xét tuyển</th>
                <th>Điểm gốc (min-max)</th>
                <th>Điểm quy đổi (min-max)</th>
                <th>Thao tác</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="convertPoint in filteredConvertPoints" :key="convertPoint.id" class="data-row">
                <td><span class="id-badge">#{{ convertPoint.id }}</span></td>
                <td>
                  <span class="method-name">{{ getMethodName(convertPoint.admission_methods_id) }}</span>
                </td>
                <td>
                  <span class="score-range">
                    {{ formatNumber(convertPoint.origin_min) }} - {{ formatNumber(convertPoint.origin_max) }}
                  </span>
                </td>
                <td>
                  <span class="score-range convert-score">
                    {{ formatNumber(convertPoint.convert_score_min) }} - {{ formatNumber(convertPoint.convert_score_max) }}
                  </span>
                </td>
                <td>
                  <div class="action-buttons">
                    <router-link :to="`/admins/convert-points/${convertPoint.id}`" class="btn-action edit" title="Xem và chỉnh sửa">
                      <i class="bi bi-pencil-square"></i>
                    </router-link>
                    <button 
                      class="btn-action delete"
                      @click="confirmDelete(convertPoint)"
                      title="Xóa quy đổi điểm"
                    >
                      <i class="bi bi-trash"></i>
                    </button>
                  </div>
                </td>
              </tr>
  
              <!-- Empty State -->
              <tr v-if="filteredConvertPoints.length === 0">
                <td colspan="5">
                  <div class="empty-state">
                    <i class="bi bi-calculator empty-icon"></i>
                    <h4>Không tìm thấy quy đổi điểm nào</h4>
                    <p v-if="hasFilters">Thử thay đổi các bộ lọc</p>
                    <p v-else>Chưa có dữ liệu quy đổi điểm trong hệ thống</p>
                    <router-link to="/admins/convert-points/create" class="btn-create-empty">
                      <i class="bi bi-plus-circle me-2"></i>Thêm quy đổi điểm
                    </router-link>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
  
      <!-- Delete Confirmation Modal -->
      <div v-if="showDeleteModal" class="modal-overlay" @click="cancelDelete">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h4 class="modal-title">Xác nhận xóa quy đổi điểm</h4>
            <button type="button" class="btn-close" @click="cancelDelete"></button>
          </div>
          <div class="modal-body">
            <p>Bạn có chắc chắn muốn xóa quy đổi điểm này?</p>
            <div class="convert-point-details">
              <p><strong>Phương thức xét tuyển:</strong> {{ getMethodName(convertPointToDelete?.admission_methods_id) }}</p>
              <p><strong>Điểm gốc:</strong> {{ formatNumber(convertPointToDelete?.origin_min) }} - {{ formatNumber(convertPointToDelete?.origin_max) }}</p>
              <p><strong>Điểm quy đổi:</strong> {{ formatNumber(convertPointToDelete?.convert_score_min) }} - {{ formatNumber(convertPointToDelete?.convert_score_max) }}</p>
            </div>
            <p class="text-danger">
              <i class="bi bi-exclamation-triangle me-2"></i>
              Thao tác này không thể khôi phục lại!
            </p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn-cancel" @click="cancelDelete">Hủy</button>
            <button type="button" class="btn-delete" @click="deleteConvertPoint" :disabled="isDeleting">
              <span v-if="isDeleting">Đang xóa...</span>
              <span v-else>Xác nhận xóa</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, reactive, computed, onMounted } from 'vue'
  import ConvertPointController from '@/controllers/admins/ConvertPointController'
  import AdmissionMethodController from '@/controllers/admins/AdmissionMethodController'
  
  export default {
    name: 'AdminConvertPoints',
    setup() {
      const convertPoints = ref([])
      const filteredConvertPoints = ref([])
      const loading = ref(true)
      const error = ref(null)
      const searchQuery = ref('')
      
      const admissionMethods = ref([])
      
      // Delete modal state
      const showDeleteModal = ref(false)
      const convertPointToDelete = ref(null)
      const isDeleting = ref(false)
  
      // Filters
      const filters = reactive({
        methodId: '',
      })
      
      // Check if any filters are applied
      const hasFilters = computed(() => {
        return filters.methodId || searchQuery.value
      })
      
      // Get method name by ID
      const getMethodName = (methodId) => {
        const method = admissionMethods.value.find(m => m.id === methodId)
        return method ? method.name : 'Không xác định'
      }
      
      // Format number with 2 decimal places if needed
      const formatNumber = (value) => {
        if (value === null || value === undefined) return 'N/A'
        
        const num = parseFloat(value)
        return Number.isInteger(num) ? num : num.toFixed(2)
      }
  
      // Apply filters and search
      const applyFilters = () => {
        filteredConvertPoints.value = convertPoints.value.filter(convertPoint => {
          // Apply method filter
          if (filters.methodId && convertPoint.admission_methods_id !== parseInt(filters.methodId)) {
            return false
          }
          
          // Apply search query
          if (searchQuery.value) {
            const methodName = getMethodName(convertPoint.admission_methods_id).toLowerCase()
            const query = searchQuery.value.toLowerCase()
            
            return methodName.includes(query)
          }
          
          return true
        })
      }
  
      // Show delete confirmation modal
      const confirmDelete = (convertPoint) => {
        convertPointToDelete.value = convertPoint
        showDeleteModal.value = true
      }
  
      // Cancel delete action
      const cancelDelete = () => {
        showDeleteModal.value = false
        convertPointToDelete.value = null
      }
  
      // Delete convert point
      const deleteConvertPoint = async () => {
        if (!convertPointToDelete.value) return
        
        try {
          isDeleting.value = true
          await ConvertPointController.deleteConvertPoint(convertPointToDelete.value.id)
          
          // Remove from lists
          convertPoints.value = convertPoints.value.filter(cp => cp.id !== convertPointToDelete.value.id)
          applyFilters() // Update filtered list
          
          // Close modal and reset
          showDeleteModal.value = false
          convertPointToDelete.value = null
          
          alert('Xóa quy đổi điểm thành công!')
        } catch (err) {
          alert(`Lỗi: ${err.message}`)
        } finally {
          isDeleting.value = false
        }
      }
  
      // Load convert points and admission methods
      const loadData = async () => {
        try {
          loading.value = true
          error.value = null
          
          // Load all data in parallel
          const [convertPointsData, methodsData] = await Promise.all([
            ConvertPointController.getAllConvertPoints(),
            AdmissionMethodController.getAllAdmissionMethods()
          ])
          
          convertPoints.value = convertPointsData
          admissionMethods.value = methodsData
          
          // Apply initial filtering
          applyFilters()
        } catch (err) {
          error.value = `Không thể tải dữ liệu: ${err.message}`
        } finally {
          loading.value = false
        }
      }
  
      onMounted(() => {
        loadData()
      })
  
      return {
        convertPoints,
        filteredConvertPoints,
        loading,
        error,
        searchQuery,
        admissionMethods,
        showDeleteModal,
        convertPointToDelete,
        isDeleting,
        filters,
        hasFilters,
        getMethodName,
        formatNumber,
        applyFilters,
        confirmDelete,
        cancelDelete,
        deleteConvertPoint
      }
    }
  }
  </script>
  
  <style scoped>
  .admin-convert-points {
    width: 100%;
  }
  
  .admin-page-header {
    margin-bottom: 2rem;
  }
  
  .admin-page-title {
    font-size: 1.75rem;
    font-weight: 600;
    color: #0B2942;
    margin-bottom: 0.5rem;
  }
  
  .admin-page-description {
    color: #6c757d;
    font-size: 0.95rem;
  }
  
  .admin-card {
    background-color: #fff;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    transition: all 0.3s ease;
  }
  
  .admin-card:hover {
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
  }
  
  .btn-create {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background-color: #0B2942;
    color: #fff;
    font-weight: 500;
    padding: 0.75rem 1.25rem;
    border-radius: 8px;
    text-decoration: none;
    transition: all 0.3s;
    border: none;
    cursor: pointer;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  .btn-create:hover, .btn-create:focus {
    background-color: #4da0ff;
    color: #fff;
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
  }
  
  /* Filter and Search Styles */
  .form-group {
    margin-bottom: 1rem;
  }
  
  .form-group label {
    display: block;
    font-weight: 500;
    margin-bottom: 0.5rem;
    color: #0B2942;
  }
  
  .form-select {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    font-size: 0.95rem;
    transition: all 0.3s;
    background-color: #fff;
  }
  
  .form-select:focus {
    outline: none;
    border-color: #4da0ff;
    box-shadow: 0 0 0 3px rgba(77, 160, 255, 0.25);
  }
  
  .search-box {
    position: relative;
  }
  
  .search-icon {
    position: absolute;
    left: 15px;
    top: 50%;
    transform: translateY(-50%);
    color: #95a5a6;
  }
  
  .search-input {
    width: 100%;
    padding: 0.75rem 0.75rem 0.75rem 40px;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    font-size: 0.95rem;
    transition: all 0.3s;
  }
  
  .search-input:focus {
    outline: none;
    border-color: #4da0ff;
    box-shadow: 0 0 0 3px rgba(77, 160, 255, 0.25);
  }
  
  /* Loading Animation */
  .loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem 0;
  }
  
  .spinner {
    margin: 0 auto;
    width: 70px;
    text-align: center;
  }
  
  .spinner > div {
    width: 18px;
    height: 18px;
    background-color: #0B2942;
    border-radius: 100%;
    display: inline-block;
    animation: sk-bouncedelay 1.4s infinite ease-in-out both;
    margin: 0 3px;
  }
  
  .spinner .bounce1 {
    animation-delay: -0.32s;
  }
  
  .spinner .bounce2 {
    animation-delay: -0.16s;
  }
  
  @keyframes sk-bouncedelay {
    0%, 80%, 100% { transform: scale(0); }
    40% { transform: scale(1.0); }
  }
  
  .loading-text {
    margin-top: 1rem;
    color: #6c757d;
    font-size: 1rem;
  }
  
  /* Error Message */
  .error-message {
    background-color: #f8d7da;
    color: #721c24;
    padding: 1rem;
    border-radius: 8px;
    display: flex;
    align-items: center;
    margin-bottom: 1.5rem;
  }
  
  .error-icon {
    font-size: 1.25rem;
    margin-right: 0.75rem;
  }
  
  /* Table Styling */
  .data-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
  }
  
  .data-table th {
    background-color: #f8f9fa;
    color: #0B2942;
    font-weight: 600;
    padding: 1rem;
    text-align: left;
    border-bottom: 2px solid #dee2e6;
    position: sticky;
    top: 0;
    z-index: 10;
  }
  
  .data-table td {
    padding: 1rem;
    vertical-align: middle;
    border-bottom: 1px solid #edf2f7;
  }
  
  .data-row {
    transition: background-color 0.3s;
  }
  
  .data-row:hover {
    background-color: rgba(77, 160, 255, 0.05);
  }
  
  .id-badge {
    font-weight: 600;
    color: #6c757d;
  }
  
  .method-name {
    display: inline-block;
    padding: 0.35rem 0.75rem;
    border-radius: 50px;
    font-size: 0.85rem;
    font-weight: 500;
    background-color: #e3f2fd;
    color: #0d6efd;
  }
  
  .score-range {
    font-weight: 500;
    color: #0B2942;
    font-size: 1rem;
  }
  
  .convert-score {
    color: #198754;
  }
  
  .action-buttons {
    display: flex;
    gap: 0.5rem;
  }
  
  .btn-action {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    border-radius: 8px;
    border: none;
    background-color: transparent;
    transition: all 0.3s ease;
  }
  
  .btn-action.edit {
    color: #0B2942;
  }
  
  .btn-action.delete {
    color: #dc3545;
  }
  
  .btn-action:hover {
    background-color: #f8f9fa;
    transform: translateY(-2px);
  }
  
  .btn-action.edit:hover {
    color: #0B2942;
    background-color: rgba(11, 41, 66, 0.1);
  }
  
  .btn-action.delete:hover {
    color: #dc3545;
    background-color: rgba(220, 53, 69, 0.1);
  }
  
  /* Empty State */
  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem 0;
    text-align: center;
  }
  
  .empty-icon {
    font-size: 3rem;
    color: #6c757d;
    margin-bottom: 1rem;
  }
  
  .empty-state h4 {
    font-size: 1.25rem;
    color: #0B2942;
    margin-bottom: 0.5rem;
  }
  
  .empty-state p {
    color: #6c757d;
    margin-bottom: 1.5rem;
  }
  
  .btn-create-empty {
    display: inline-flex;
    align-items: center;
    background-color: #0B2942;
    color: #fff;
    padding: 0.75rem 1.25rem;
    border-radius: 8px;
    text-decoration: none;
    transition: all 0.3s;
  }
  
  .btn-create-empty:hover {
    background-color: #4da0ff;
    color: #fff;
  }
  
  /* Convert Point Details in Modal */
  .convert-point-details {
    background-color: #f8f9fa;
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
  }
  
  .convert-point-details p {
    margin-bottom: 0.5rem;
  }
  
  .convert-point-details p:last-child {
    margin-bottom: 0;
  }
  
  /* Modal Styling */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1050;
  }
  
  .modal-content {
    background-color: #fff;
    border-radius: 12px;
    width: 90%;
    max-width: 500px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
    overflow: hidden;
  }
  
  .modal-header {
    padding: 1rem 1.5rem;
    border-bottom: 1px solid #e9ecef;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  
  .modal-title {
    font-size: 1.25rem;
    color: #0B2942;
    margin: 0;
  }
  
  .btn-close {
    background: transparent;
    border: none;
    font-size: 1.5rem;
    line-height: 1;
    color: #6c757d;
    cursor: pointer;
  }
  
  .modal-body {
    padding: 1.5rem;
  }
  
  .modal-footer {
    padding: 1rem 1.5rem;
    border-top: 1px solid #e9ecef;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 0.5rem;
  }
  
  .btn-cancel {
    padding: 0.5rem 1rem;
    background-color: #f8f9fa;
    color: #6c757d;
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s;
  }
  
  .btn-cancel:hover {
    background-color: #e9ecef;
    color: #0B2942;
  }
  
  .btn-delete {
    padding: 0.5rem 1rem;
    background-color: #dc3545;
    color: #fff;
    border: none;
    border-radius: 6px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s;
  }
  
  .btn-delete:hover:not(:disabled) {
    background-color: #c82333;
  }
  
  .btn-delete:disabled {
    background-color: #e9ecef;
    color: #6c757d;
    cursor: not-allowed;
  }
  
  .text-danger {
    color: #dc3545;
  }
  
  @media (max-width: 768px) {
    .admin-page-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 1rem;
    }
    
    .btn-create {
      width: 100%;
    }
  }
  </style>