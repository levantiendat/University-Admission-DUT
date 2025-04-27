<template>
    <div class="admin-major-admission-methods">
      <div class="admin-page-header d-flex justify-content-between align-items-center">
        <div>
          <div class="d-flex align-items-center">
            <router-link :to="`/admins/majors/${majorId}`" class="btn-back">
              <i class="bi bi-arrow-left"></i>
            </router-link>
            <div>
              <h2 class="admin-page-title">Quản lý phương thức tuyển sinh</h2>
              <p class="admin-page-description">
                Danh sách các phương thức tuyển sinh áp dụng cho ngành: 
                <strong>{{ majorName }}</strong>
              </p>
            </div>
          </div>
        </div>
        <button class="btn-create" @click="showAddMethodModal">
          <i class="bi bi-plus-circle me-2"></i>Thêm phương thức tuyển sinh
        </button>
      </div>
  
      <!-- Search and Filter -->
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
                <th>Thao tác</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="method in filteredMethods" :key="method.id" class="data-row">
                <td><span class="id-badge">#{{ method.admission_methods_id }}</span></td>
                <td><span class="name-text">{{ getMethodName(method.admission_methods_id) }}</span></td>
                <td>{{ getMethodMinScore(method.admission_methods_id) }}</td>
                <td>{{ getMethodMaxScore(method.admission_methods_id) }}</td>
                <td>
                  <div class="action-buttons">
                    <router-link 
                      :to="`/admins/admission-methods/${method.admission_methods_id}`" 
                      class="btn-action view" 
                      title="Xem chi tiết phương thức tuyển sinh"
                    >
                      <i class="bi bi-eye"></i>
                    </router-link>
                    <button 
                      class="btn-action delete"
                      @click="confirmRemoveMethod(method)"
                      title="Xóa phương thức tuyển sinh khỏi ngành"
                    >
                      <i class="bi bi-x-circle"></i>
                    </button>
                  </div>
                </td>
              </tr>
  
              <!-- Empty State -->
              <tr v-if="filteredMethods.length === 0">
                <td colspan="5">
                  <div class="empty-state">
                    <i class="bi bi-clipboard-x empty-icon"></i>
                    <h4>Không tìm thấy phương thức tuyển sinh</h4>
                    <p v-if="searchQuery">Thử thay đổi từ khóa tìm kiếm</p>
                    <p v-else>Chưa có phương thức tuyển sinh nào được áp dụng cho ngành này</p>
                    <button @click="showAddMethodModal" class="btn-create-empty">
                      <i class="bi bi-plus-circle me-2"></i>Thêm phương thức tuyển sinh
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
  
      <!-- Add Method Modal -->
      <div v-if="showAddModal" class="modal-overlay" @click="cancelAddMethod">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h4 class="modal-title">Thêm phương thức tuyển sinh</h4>
            <button type="button" class="btn-close" @click="cancelAddMethod"></button>
          </div>
          <div class="modal-body">
            <div class="form-group">
              <label for="method-select">Chọn phương thức tuyển sinh <span class="required">*</span></label>
              <select 
                id="method-select" 
                v-model="selectedMethodId" 
                class="form-control" 
                :class="{ 'is-invalid': addError }"
              >
                <option value="" disabled selected>Chọn phương thức tuyển sinh</option>
                <option v-for="method in availableMethods" :key="method.id" :value="method.id">
                  {{ method.name }} ({{ method.min_score !== null ? `${method.min_score} - ${method.max_score} điểm` : 'Không giới hạn điểm' }})
                </option>
              </select>
              <div v-if="addError" class="invalid-feedback">{{ addError }}</div>
            </div>
            <p class="text-info" v-if="availableMethods.length === 0">
              <i class="bi bi-info-circle me-1"></i>
              Tất cả phương thức tuyển sinh đã được áp dụng cho ngành này.
            </p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn-cancel" @click="cancelAddMethod">Hủy</button>
            <button 
              type="button" 
              class="btn-add" 
              @click="addMethodToMajor" 
              :disabled="isAdding || !selectedMethodId"
            >
              <span v-if="isAdding">Đang thêm...</span>
              <span v-else>Thêm phương thức</span>
            </button>
          </div>
        </div>
      </div>
  
      <!-- Remove Confirmation Modal -->
      <div v-if="showRemoveModal" class="modal-overlay" @click="cancelRemoveMethod">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h4 class="modal-title">Xác nhận xóa</h4>
            <button type="button" class="btn-close" @click="cancelRemoveMethod"></button>
          </div>
          <div class="modal-body">
            <p>Bạn có chắc chắn muốn xóa phương thức tuyển sinh <strong>{{ getMethodName(methodToRemove?.admission_methods_id) }}</strong> khỏi ngành này?</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn-cancel" @click="cancelRemoveMethod">Hủy</button>
            <button type="button" class="btn-delete" @click="removeMethodFromMajor" :disabled="isRemoving">
              <span v-if="isRemoving">Đang xóa...</span>
              <span v-else>Xác nhận xóa</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue'
  import MajorController from '@/controllers/admins/MajorController'
  import AdmissionMethodController from '@/controllers/admins/AdmissionMethodController'
  import AdmissionMethodMajorController from '@/controllers/admins/AdmissionMethodMajorController'
  
  export default {
    name: 'AdminMajorAdmissionMethods',
    props: {
      majorId: {
        type: [String, Number],
        required: true
      }
    },
    setup(props) {
      const methods = ref([])
      const filteredMethods = ref([])
      const allMethods = ref([])
      const availableMethods = ref([])
      const majorName = ref('')
      const loading = ref(true)
      const error = ref(null)
      const searchQuery = ref('')
      
      // Add method modal state
      const showAddModal = ref(false)
      const selectedMethodId = ref('')
      const isAdding = ref(false)
      const addError = ref('')
      
      // Remove method modal state
      const showRemoveModal = ref(false)
      const methodToRemove = ref(null)
      const isRemoving = ref(false)
  
      // Get method details by ID
      const getMethodName = (methodId) => {
        const method = allMethods.value.find(m => m.id === methodId)
        return method ? method.name : 'Không xác định'
      }
      
      const getMethodMinScore = (methodId) => {
        const method = allMethods.value.find(m => m.id === methodId)
        return method ? method.min_score : 'N/A'
      }
      
      const getMethodMaxScore = (methodId) => {
        const method = allMethods.value.find(m => m.id === methodId)
        return method ? method.max_score : 'N/A'
      }
  
      // Filter methods based on search query
      const filterMethods = () => {
        if (!methods.value.length) return
        
        filteredMethods.value = methods.value.filter(method => {
          const methodName = getMethodName(method.admission_methods_id)
          const matchesQuery = !searchQuery.value || 
            methodName.toLowerCase().includes(searchQuery.value.toLowerCase())
          
          return matchesQuery
        })
      }
  
      // Load major details and methods
      const loadData = async () => {
        try {
          loading.value = true
          error.value = null
          
          // Get major name
          const major = await MajorController.getMajorById(props.majorId)
          majorName.value = major.name
          
          // Get all admission methods (for reference)
          const methodsData = await AdmissionMethodController.getAllAdmissionMethods()
          allMethods.value = methodsData
          
          // Get methods applied to this major
          const majorMethodsData = await AdmissionMethodMajorController.getAdmissionMethodsByMajor(props.majorId)
          methods.value = majorMethodsData
          filteredMethods.value = [...majorMethodsData]
          
          // Get available methods (all methods not applied to this major)
          await loadAvailableMethods()
        } catch (err) {
          error.value = `Không thể tải danh sách phương thức tuyển sinh: ${err.message}`
        } finally {
          loading.value = false
        }
      }
      
      // Load methods available to add
      const loadAvailableMethods = async () => {
        try {
          // Filter out methods that are already applied to this major
          const currentMethodIds = methods.value.map(m => m.admission_methods_id)
          availableMethods.value = allMethods.value.filter(method => !currentMethodIds.includes(method.id))
        } catch (err) {
          console.error('Error loading available methods:', err)
          availableMethods.value = []
        }
      }
      
      // Show add method modal
      const showAddMethodModal = () => {
        selectedMethodId.value = ''
        addError.value = ''
        showAddModal.value = true
      }
      
      // Cancel add method
      const cancelAddMethod = () => {
        showAddModal.value = false
        selectedMethodId.value = ''
        addError.value = ''
      }
      
      // Add method to major
      const addMethodToMajor = async () => {
        if (!selectedMethodId.value) {
          addError.value = 'Vui lòng chọn phương thức tuyển sinh'
          return
        }
        
        try {
          isAdding.value = true
          addError.value = ''
          
          await AdmissionMethodMajorController.createAdmissionMethodMajor({
            major_id: props.majorId,
            admission_methods_id: selectedMethodId.value
          })
          
          // Reload data
          await loadData()
          
          // Close modal
          showAddModal.value = false
          selectedMethodId.value = ''
          
          alert('Thêm phương thức tuyển sinh thành công')
        } catch (err) {
          addError.value = `Không thể thêm phương thức tuyển sinh: ${err.message}`
        } finally {
          isAdding.value = false
        }
      }
      
      // Show remove confirmation modal
      const confirmRemoveMethod = (method) => {
        methodToRemove.value = method
        showRemoveModal.value = true
      }
      
      // Cancel remove method
      const cancelRemoveMethod = () => {
        showRemoveModal.value = false
        methodToRemove.value = null
      }
      
      // Remove method from major
      const removeMethodFromMajor = async () => {
        if (!methodToRemove.value) return
        
        try {
          isRemoving.value = true
          
          await AdmissionMethodMajorController.deleteAdmissionMethodMajor(methodToRemove.value.id)
          
          // Remove from lists
          methods.value = methods.value.filter(m => m.id !== methodToRemove.value.id)
          filterMethods()
          
          // Close modal
          showRemoveModal.value = false
          methodToRemove.value = null
          
          // Reload available methods
          await loadAvailableMethods()
          
          alert('Xóa phương thức tuyển sinh thành công')
        } catch (err) {
          alert(`Lỗi: ${err.message}`)
        } finally {
          isRemoving.value = false
        }
      }
  
      onMounted(() => {
        loadData()
      })
  
      return {
        methods,
        filteredMethods,
        availableMethods,
        majorName,
        loading,
        error,
        searchQuery,
        showAddModal,
        selectedMethodId,
        isAdding,
        addError,
        showRemoveModal,
        methodToRemove,
        isRemoving,
        getMethodName,
        getMethodMinScore,
        getMethodMaxScore,
        filterMethods,
        showAddMethodModal,
        cancelAddMethod,
        addMethodToMajor,
        confirmRemoveMethod,
        cancelRemoveMethod,
        removeMethodFromMajor
      }
    }
  }
  </script>
  
  <style scoped>
  .admin-major-admission-methods {
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
  
  .btn-back {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: #f8f9fa;
    color: #0B2942;
    text-decoration: none;
    margin-right: 1rem;
    transition: all 0.2s ease;
  }
  
  .btn-back:hover {
    background-color: #e9ecef;
    transform: translateX(-2px);
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
    border: none;
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
  
  .form-group {
    margin-bottom: 1rem;
  }
  
  .form-group label {
    display: block;
    font-weight: 500;
    margin-bottom: 0.5rem;
    color: #0B2942;
  }
  
  .required {
    color: #dc3545;
  }
  
  .form-control {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    font-size: 0.95rem;
    transition: all 0.3s;
  }
  
  .form-control:focus {
    outline: none;
    border-color: #4da0ff;
    box-shadow: 0 0 0 3px rgba(77, 160, 255, 0.25);
  }
  
  .form-control.is-invalid {
    border-color: #dc3545;
  }
  
  .invalid-feedback {
    color: #dc3545;
    font-size: 0.875em;
    margin-top: 0.25rem;
  }
  
  .text-info {
    color: #17a2b8;
    margin-top: 1rem;
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
  
  .btn-add {
    padding: 0.5rem 1rem;
    background-color: #0B2942;
    color: #fff;
    border: none;
    border-radius: 6px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s;
  }
  
  .btn-add:hover:not(:disabled) {
    background-color: #4da0ff;
  }
  
  .btn-add:disabled {
    background-color: #e9ecef;
    color: #6c757d;
    cursor: not-allowed;
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