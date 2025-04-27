<template>
    <div class="admin-admission-method-detail">
      <div class="admin-page-header">
        <div class="d-flex align-items-center">
          <router-link to="/admins/admission-methods" class="btn-back">
            <i class="bi bi-arrow-left"></i>
          </router-link>
          <div>
            <h2 class="admin-page-title">Chi tiết phương thức tuyển sinh</h2>
            <p class="admin-page-description">Xem và chỉnh sửa thông tin phương thức tuyển sinh</p>
          </div>
        </div>
      </div>
  
      <!-- Loading State -->
      <div v-if="loading" class="loading-container">
        <div class="spinner">
          <div class="bounce1"></div>
          <div class="bounce2"></div>
          <div class="bounce3"></div>
        </div>
        <p class="loading-text">Đang tải thông tin phương thức tuyển sinh...</p>
      </div>
  
      <!-- Error State -->
      <div v-else-if="error" class="error-message">
        <i class="bi bi-exclamation-triangle-fill error-icon"></i>
        <span>{{ error }}</span>
      </div>
  
      <div v-else class="row">
        <!-- Method Info Card -->
        <div class="col-md-4 mb-4">
          <div class="admin-card info-card">
            <div class="info-header">
              <div class="method-badge">
                <i class="bi bi-clipboard-check"></i>
              </div>
              <h3 class="method-name">{{ method.name }}</h3>
              <div class="method-score">
                {{ method.min_score !== null ? `${method.min_score} - ${method.max_score} điểm` : 'Không giới hạn điểm' }}
              </div>
            </div>
            
            <div class="info-meta">
              <div class="info-item">
                <span class="info-label">ID:</span>
                <span class="info-value">#{{ method.id }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Ngành áp dụng:</span>
                <span class="info-value">
                  <router-link :to="`/admins/admission-methods/${method.id}/majors`" class="majors-link">
                    {{ majorCount }} ngành
                  </router-link>
                </span>
              </div>
              <div class="info-item">
                <span class="info-label">Ngày tạo:</span>
                <span class="info-value">{{ formatDate(method.created_at) }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Cập nhật:</span>
                <span class="info-value">{{ formatDate(method.updated_at) }}</span>
              </div>
            </div>
  
            <div class="info-actions">
              <router-link :to="`/admins/admission-methods/${method.id}/majors`" class="btn-view-majors">
                <i class="bi bi-list-ul me-2"></i>
                Quản lý ngành áp dụng
              </router-link>
              <button 
                class="btn-delete-method"
                @click="confirmDelete"
              >
                <i class="bi bi-trash me-2"></i>
                Xóa phương thức
              </button>
            </div>
          </div>
        </div>
  
        <!-- Edit Form -->
        <div class="col-md-8">
          <div class="admin-card">
            <h3 class="section-title">Chỉnh sửa thông tin</h3>
  
            <form @submit.prevent="updateMethod" class="edit-form">
              <div class="form-group">
                <label for="name">Tên phương thức tuyển sinh <span class="required">*</span></label>
                <input 
                  type="text" 
                  id="name" 
                  v-model="formData.name" 
                  class="form-control" 
                  required
                  :class="{ 'is-invalid': errors.name }"
                >
                <div v-if="errors.name" class="invalid-feedback">{{ errors.name }}</div>
              </div>
  
              <div class="row">
                <div class="col-md-6">
                  <div class="form-group">
                    <label for="min_score">Điểm tối thiểu</label>
                    <input 
                      type="number" 
                      id="min_score" 
                      v-model="formData.min_score" 
                      class="form-control"
                      step="0.01" 
                      :class="{ 'is-invalid': errors.min_score }"
                    >
                    <div v-if="errors.min_score" class="invalid-feedback">{{ errors.min_score }}</div>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="form-group">
                    <label for="max_score">Điểm tối đa</label>
                    <input 
                      type="number" 
                      id="max_score" 
                      v-model="formData.max_score" 
                      class="form-control"
                      step="0.01" 
                      :class="{ 'is-invalid': errors.max_score }"
                    >
                    <div v-if="errors.max_score" class="invalid-feedback">{{ errors.max_score }}</div>
                  </div>
                </div>
              </div>
  
              <div class="form-group">
                <label for="description">Mô tả</label>
                <textarea 
                  id="description" 
                  v-model="formData.description" 
                  class="form-control" 
                  rows="4"
                ></textarea>
              </div>
  
              <div v-if="updateError" class="alert alert-danger">{{ updateError }}</div>
  
              <div class="form-actions">
                <button type="submit" class="btn-save" :disabled="isSaving">
                  <i class="bi bi-check-circle me-2"></i>
                  {{ isSaving ? 'Đang lưu...' : 'Lưu thay đổi' }}
                </button>
                <button type="button" class="btn-cancel" @click="resetForm">
                  <i class="bi bi-x-circle me-2"></i>
                  Hủy thay đổi
                </button>
              </div>
            </form>
          </div>
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
            <p>Bạn có chắc chắn muốn xóa phương thức tuyển sinh <strong>{{ method.name }}</strong>?</p>
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
  import { ref, reactive, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import AdmissionMethodController from '@/controllers/admins/AdmissionMethodController'
  import AdmissionMethodMajorController from '@/controllers/admins/AdmissionMethodMajorController'
  
  export default {
    name: 'AdminAdmissionMethodDetail',
    props: {
      admissionMethodId: {
        type: [String, Number],
        required: true
      }
    },
    setup(props) {
      const router = useRouter()
      const method = ref({})
      const formData = reactive({
        name: '',
        min_score: '',
        max_score: '',
        description: ''
      })
      const loading = ref(true)
      const error = ref(null)
      const updateError = ref(null)
      const isSaving = ref(false)
      const majorCount = ref(0)
      const errors = reactive({
        name: '',
        min_score: '',
        max_score: ''
      })
      
      // Delete modal state
      const showDeleteModal = ref(false)
      const isDeleting = ref(false)
  
      // Format date
      const formatDate = (dateString) => {
        if (!dateString) return 'N/A'
        
        const date = new Date(dateString)
        return new Intl.DateTimeFormat('vi-VN', { 
          day: '2-digit', 
          month: '2-digit', 
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        }).format(date)
      }
  
      // Fetch method details
      const fetchMethodDetails = async () => {
        try {
          loading.value = true
          error.value = null
          
          const data = await AdmissionMethodController.getAdmissionMethodById(props.admissionMethodId)
          method.value = data
          
          // Set form data
          formData.name = data.name || ''
          formData.min_score = data.min_score !== null ? data.min_score : ''
          formData.max_score = data.max_score !== null ? data.max_score : ''
          formData.description = data.description || ''
          
          // Get count of majors using this method
          try {
            const majors = await AdmissionMethodMajorController.getMajorsByAdmissionMethod(props.admissionMethodId)
            majorCount.value = majors.length
          } catch (err) {
            console.error('Error getting majors count:', err)
            majorCount.value = 0
          }
        } catch (err) {
          error.value = `Không thể tải thông tin phương thức tuyển sinh: ${err.message}`
        } finally {
          loading.value = false
        }
      }
  
      // Validate form
      const validateForm = () => {
        let isValid = true
        
        // Clear previous errors
        Object.keys(errors).forEach(key => {
          errors[key] = ''
        })
        
        // Name validation
        if (!formData.name.trim()) {
          errors.name = 'Tên phương thức tuyển sinh không được để trống'
          isValid = false
        }
        
        // Score validation
        const minScore = parseFloat(formData.min_score)
        const maxScore = parseFloat(formData.max_score)
        
        if (formData.min_score && formData.max_score) {
          if (isNaN(minScore) || isNaN(maxScore)) {
            errors.min_score = 'Điểm số phải là số'
            errors.max_score = 'Điểm số phải là số'
            isValid = false
          } else if (minScore > maxScore) {
            errors.min_score = 'Điểm tối thiểu không thể lớn hơn điểm tối đa'
            isValid = false
          }
        }
        
        return isValid
      }
  
      // Reset form
      const resetForm = () => {
        formData.name = method.value.name || ''
        formData.min_score = method.value.min_score !== null ? method.value.min_score : ''
        formData.max_score = method.value.max_score !== null ? method.value.max_score : ''
        formData.description = method.value.description || ''
        
        // Clear errors
        Object.keys(errors).forEach(key => {
          errors[key] = ''
        })
        updateError.value = null
      }
  
      // Update method
      const updateMethod = async () => {
        try {
          // Validate form
          if (!validateForm()) {
            return
          }
          
          isSaving.value = true
          updateError.value = null
          
          // Convert scores to numbers if provided
          const data = { ...formData }
          if (data.min_score) data.min_score = parseFloat(data.min_score)
          if (data.max_score) data.max_score = parseFloat(data.max_score)
          
          await AdmissionMethodController.updateAdmissionMethod(props.admissionMethodId, data)
          
          // Update local method object
          method.value = { 
            ...method.value, 
            name: data.name,
            min_score: data.min_score,
            max_score: data.max_score,
            description: data.description
          }
          
          alert('Cập nhật thông tin phương thức tuyển sinh thành công')
        } catch (err) {
          updateError.value = `Không thể cập nhật thông tin phương thức tuyển sinh: ${err.message}`
        } finally {
          isSaving.value = false
        }
      }
  
      // Delete confirmation
      const confirmDelete = () => {
        showDeleteModal.value = true
      }
  
      // Cancel delete
      const cancelDelete = () => {
        showDeleteModal.value = false
      }
  
      // Delete method
      const deleteMethod = async () => {
        try {
          isDeleting.value = true
          
          await AdmissionMethodController.deleteAdmissionMethod(props.admissionMethodId)
          
          alert('Xóa phương thức tuyển sinh thành công')
          router.push('/admins/admission-methods')
        } catch (err) {
          alert(`Lỗi: ${err.message}`)
        } finally {
          isDeleting.value = false
          showDeleteModal.value = false
        }
      }
  
      onMounted(() => {
        fetchMethodDetails()
      })
  
      return {
        method,
        formData,
        loading,
        error,
        updateError,
        isSaving,
        majorCount,
        errors,
        showDeleteModal,
        isDeleting,
        formatDate,
        resetForm,
        updateMethod,
        confirmDelete,
        cancelDelete,
        deleteMethod
      }
    }
  }
  </script>
  
  <style scoped>
  .admin-admission-method-detail {
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
  
  .admin-card {
    background-color: #fff;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    padding: 1.5rem;
    height: 100%;
    transition: all 0.3s ease;
  }
  
  .admin-card:hover {
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
  }
  
  /* Info Card Styling */
  .info-card {
    display: flex;
    flex-direction: column;
  }
  
  .info-header {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid #e9ecef;
    margin-bottom: 1.5rem;
  }
  
  .method-badge {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background-color: #e3f2fd;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1rem;
    color: #8c54ff;
    font-size: 2.5rem;
  }
  
  .method-name {
    font-size: 1.5rem;
    font-weight: 600;
    color: #0B2942;
    margin-bottom: 0.5rem;
  }
  
  .method-score {
    display: inline-block;
    padding: 0.35rem 0.75rem;
    border-radius: 50px;
    font-size: 0.9rem;
    font-weight: 500;
    background-color: #e3f2fd;
    color: #0d6efd;
  }
  
  .info-meta {
    margin-bottom: 1.5rem;
  }
  
  .info-item {
    display: flex;
    justify-content: space-between;
    padding: 0.75rem 0;
    border-bottom: 1px solid #f1f1f1;
  }
  
  .info-item:last-child {
    border-bottom: none;
  }
  
  .info-label {
    color: #6c757d;
    font-weight: 500;
  }
  
  .info-value {
    color: #0B2942;
    font-weight: 500;
  }
  
  .majors-link {
    color: #4da0ff;
    text-decoration: none;
    transition: all 0.3s;
  }
  
  .majors-link:hover {
    text-decoration: underline;
  }
  
  .info-actions {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    margin-top: auto;
  }
  
  .btn-view-majors {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0.75rem 1rem;
    background-color: #0B2942;
    color: white;
    border-radius: 8px;
    text-decoration: none;
    font-weight: 500;
    transition: all 0.3s ease;
  }
  
  .btn-view-majors:hover {
    background-color: #4da0ff;
    color: white;
  }
  
  .btn-delete-method {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0.75rem 1rem;
    background-color: #f8f9fa;
    border: 1px solid #dc3545;
    color: #dc3545;
    border-radius: 8px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .btn-delete-method:hover {
    background-color: #dc3545;
    color: white;
  }
  
  /* Form Styling */
  .section-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: #0B2942;
    margin-bottom: 1.5rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid #e9ecef;
  }
  
  .edit-form {
    width: 100%;
  }
  
  .form-group {
    margin-bottom: 1.5rem;
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
    background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 12' width='12' height='12' fill='none' stroke='%23dc3545'%3e%3ccircle cx='6' cy='6' r='4.5'/%3e%3cpath stroke-linejoin='round' d='M5.8 3.6h.4L6 6.5z'/%3e%3ccircle cx='6' cy='8.2' r='.6' fill='%23dc3545' stroke='none'/%3e%3c/svg%3e");
    background-repeat: no-repeat;
    background-position: right calc(0.375em + 0.1875rem) center;
    background-size: calc(0.75em + 0.375rem) calc(0.75em + 0.375rem);
  }
  
  .invalid-feedback {
    color: #dc3545;
    font-size: 0.875em;
    margin-top: 0.25rem;
  }
  
  .form-actions {
    display: flex;
    gap: 1rem;
    margin-top: 2rem;
  }
  
  .btn-save {
    padding: 0.75rem 1.5rem;
    background-color: #0B2942;
    border: none;
    border-radius: 8px;
    color: #fff;
    font-weight: 500;
    transition: all 0.3s;
    display: inline-flex;
    align-items: center;
  }
  
  .btn-save:hover:not(:disabled) {
    background-color: #4da0ff;
  }
  
  .btn-save:disabled {
    background-color: #e9ecef;
    color: #6c757d;
    cursor: not-allowed;
  }
  
  .btn-cancel {
    padding: 0.75rem 1.5rem;
    background-color: #f8f9fa;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    color: #6c757d;
    font-weight: 500;
    transition: all 0.3s;
    display: inline-flex;
    align-items: center;
  }
  
  .btn-cancel:hover {
    background-color: #e9ecef;
    color: #0B2942;
  }
  
  /* Alert */
  .alert {
    padding: 1rem;
    margin-bottom: 1rem;
    border-radius: 8px;
  }
  
  .alert-danger {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c2c7;
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
  
  .btn-delete {
    padding: 0.5rem 1rem;
    background-color: #dc3545;
    color: #fff;
    border: none;
    border-radius: 6px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
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
  .form-actions {
    flex-direction: column;
  }
  
  .btn-save, .btn-cancel {
    width: 100%;
  }
}
</style>