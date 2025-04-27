<template>
    <div class="admin-admission-methods">
      <div class="admin-page-header d-flex justify-content-between align-items-center">
        <div>
          <h2 class="admin-page-title">Quản lý phương thức tuyển sinh</h2>
          <p class="admin-page-description">Quản lý tất cả phương thức xét tuyển trong hệ thống</p>
        </div>
        <router-link to="/admins/admission-methods/create" class="btn-create">
          <i class="bi bi-plus-circle me-2"></i>Thêm phương thức mới
        </router-link>
      </div>
  
      <!-- Search -->
      <div class="admin-card mb-4">
        <div class="row align-items-center">
          <div class="col-md-12">
            <div class="search-box">
              <i class="bi bi-search search-icon"></i>
              <input 
                type="text" 
                v-model="searchQuery" 
                class="search-input" 
                placeholder="Tìm kiếm phương thức tuyển sinh theo tên..." 
                @input="filterMethods"
              >
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
        <p class="loading-text">Đang tải danh sách phương thức tuyển sinh...</p>
      </div>
  
      <!-- Error Message -->
      <div v-else-if="error" class="error-message">
        <i class="bi bi-exclamation-triangle-fill error-icon"></i>
        <span>{{ error }}</span>
      </div>
  
      <!-- Methods Table -->
      <div v-else class="admin-card">
        <div class="table-responsive">
          <table class="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Tên phương thức</th>
                <th>Điểm tối thiểu</th>
                <th>Điểm tối đa</th>
                <th>Ngành áp dụng</th>
                <th>Ngày tạo</th>
                <th>Thao tác</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="method in filteredMethods" :key="method.id" class="data-row">
                <td><span class="id-badge">#{{ method.id }}</span></td>
                <td><span class="name-text">{{ method.name }}</span></td>
                <td>{{ method.min_score }}</td>
                <td>{{ method.max_score }}</td>
                <td>
                  <router-link :to="`/admins/admission-methods/${method.id}/majors`" class="badge major-count-badge">
                    {{ getMajorCount(method.id) }} ngành
                  </router-link>
                </td>
                <td>{{ formatDate(method.created_at) }}</td>
                <td>
                  <div class="action-buttons">
                    <router-link :to="`/admins/admission-methods/${method.id}`" class="btn-action edit" title="Xem và chỉnh sửa thông tin">
                      <i class="bi bi-pencil-square"></i>
                    </router-link>
                    <router-link :to="`/admins/admission-methods/${method.id}/majors`" class="btn-action view" title="Xem danh sách ngành áp dụng">
                      <i class="bi bi-list-ul"></i>
                    </router-link>
                    <button 
                      class="btn-action delete"
                      @click="confirmDelete(method)"
                      title="Xóa phương thức tuyển sinh"
                    >
                      <i class="bi bi-trash"></i>
                    </button>
                  </div>
                </td>
              </tr>
  
              <!-- Empty State -->
              <tr v-if="filteredMethods.length === 0">
                <td colspan="7">
                  <div class="empty-state">
                    <i class="bi bi-clipboard-x empty-icon"></i>
                    <h4>Không tìm thấy phương thức tuyển sinh</h4>
                    <p v-if="searchQuery">Thử thay đổi từ khóa tìm kiếm</p>
                    <p v-else>Chưa có phương thức tuyển sinh nào trong hệ thống</p>
                    <router-link to="/admins/admission-methods/create" class="btn-create-empty">
                      <i class="bi bi-plus-circle me-2"></i>Thêm phương thức mới
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
            <h4 class="modal-title">Xác nhận xóa phương thức tuyển sinh</h4>
            <button type="button" class="btn-close" @click="cancelDelete"></button>
          </div>
          <div class="modal-body">
            <p>Bạn có chắc chắn muốn xóa phương thức tuyển sinh <strong>{{ methodToDelete?.name }}</strong>?</p>
            <p class="text-danger">
              <i class="bi bi-exclamation-triangle me-2"></i>
              Thao tác này sẽ xóa tất cả mối quan hệ giữa phương thức này và các ngành đào tạo, và không thể khôi phục lại!
            </p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn-cancel" @click="cancelDelete">Hủy</button>
            <button type="button" class="btn-delete" @click="deleteMethod" :disabled="isDeleting">
              <span v-if="isDeleting">Đang xóa...</span>
              <span v-else>Xác nhận xóa</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue'
  import AdmissionMethodController from '@/controllers/admins/AdmissionMethodController'
  import AdmissionMethodMajorController from '@/controllers/admins/AdmissionMethodMajorController'
  
  export default {
    name: 'AdminAdmissionMethods',
    setup() {
      const methods = ref([])
      const filteredMethods = ref([])
      const methodMajors = ref({}) // Object to store method-major relationships by method ID
      const loading = ref(true)
      const error = ref(null)
      const searchQuery = ref('')
      
      // Delete modal state
      const showDeleteModal = ref(false)
      const methodToDelete = ref(null)
      const isDeleting = ref(false)
  
      // Format date
      const formatDate = (dateString) => {
        const date = new Date(dateString)
        return new Intl.DateTimeFormat('vi-VN', { 
          day: '2-digit', 
          month: '2-digit', 
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        }).format(date)
      }
  
      // Get count of majors using a method
      const getMajorCount = (methodId) => {
        return methodMajors.value[methodId]?.length || 0
      }
  
      // Filter methods based on search query
      const filterMethods = () => {
        if (!methods.value.length) return
        
        filteredMethods.value = methods.value.filter(method => {
          const matchesQuery = !searchQuery.value || 
            method.name.toLowerCase().includes(searchQuery.value.toLowerCase())
          
          return matchesQuery
        })
      }
  
      // Load methods and method-major relationships
      const loadMethodsAndMajors = async () => {
        try {
          loading.value = true
          error.value = null
          
          // Load all admission methods
          const methodsData = await AdmissionMethodController.getAllAdmissionMethods()
          methods.value = methodsData
          filteredMethods.value = [...methodsData]
          
          // Load method-major relationships for each method
          for (const method of methodsData) {
            try {
              const majors = await AdmissionMethodMajorController.getMajorsByAdmissionMethod(method.id)
              methodMajors.value[method.id] = majors
            } catch (err) {
              console.error(`Error loading majors for method ${method.id}:`, err)
              methodMajors.value[method.id] = []
            }
          }
        } catch (err) {
          error.value = `Không thể tải danh sách phương thức tuyển sinh: ${err.message}`
        } finally {
          loading.value = false
        }
      }
  
      // Show delete confirmation modal
      const confirmDelete = (method) => {
        methodToDelete.value = method
        showDeleteModal.value = true
      }
  
      // Cancel delete action
      const cancelDelete = () => {
        showDeleteModal.value = false
        methodToDelete.value = null
      }
  
      // Delete admission method
      const deleteMethod = async () => {
        if (!methodToDelete.value) return
        
        try {
          isDeleting.value = true
          await AdmissionMethodController.deleteAdmissionMethod(methodToDelete.value.id)
          
          // Remove from lists
          methods.value = methods.value.filter(m => m.id !== methodToDelete.value.id)
          delete methodMajors.value[methodToDelete.value.id]
          filterMethods() // Update filtered list
          
          // Close modal and reset
          showDeleteModal.value = false
          methodToDelete.value = null
          
          alert('Xóa phương thức tuyển sinh thành công!')
        } catch (err) {
          alert(`Lỗi: ${err.message}`)
        } finally {
          isDeleting.value = false
        }
      }
  
      onMounted(() => {
        loadMethodsAndMajors()
      })
  
      return {
        methods,
        filteredMethods,
        loading,
        error,
        searchQuery,
        showDeleteModal,
        methodToDelete,
        isDeleting,
        formatDate,
        getMajorCount,
        filterMethods,
        confirmDelete,
        cancelDelete,
        deleteMethod
      }
    }
  }
  </script>
  
  <style scoped>
  .admin-admission-methods {
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
  
  /* Search Box */
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
  
  .name-text {
    font-weight: 500;
    color: #0B2942;
  }
  
  .major-count-badge {
    display: inline-block;
    padding: 0.35rem 0.75rem;
    border-radius: 50px;
    font-size: 0.85rem;
    font-weight: 500;
    background-color: #e3f2fd;
    color: #0d6efd;
    text-decoration: none;
    transition: all 0.3s;
  }
  
  .major-count-badge:hover {
    background-color: #0d6efd;
    color: #fff;
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
  
  .btn-action.view {
    color: #17a2b8;
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
  
  .btn-action.view:hover {
    color: #17a2b8;
    background-color: rgba(23, 162, 184, 0.1);
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