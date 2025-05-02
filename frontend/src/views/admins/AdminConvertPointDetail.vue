<template>
    <div class="admin-convert-point-detail">
      <div class="admin-page-header">
        <div class="d-flex align-items-center">
          <router-link to="/admins/convert-points" class="btn-back">
            <i class="bi bi-arrow-left"></i>
          </router-link>
          <div>
            <h2 class="admin-page-title">Chi tiết quy đổi điểm</h2>
            <p class="admin-page-description">Xem và chỉnh sửa thông tin quy đổi điểm</p>
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
        <p class="loading-text">Đang tải thông tin quy đổi điểm...</p>
      </div>
  
      <!-- Error State -->
      <div v-else-if="error" class="error-message">
        <i class="bi bi-exclamation-triangle-fill error-icon"></i>
        <span>{{ error }}</span>
      </div>
  
      <div v-else class="row">
        <!-- Convert Point Info Card -->
        <div class="col-md-4 mb-4">
          <div class="admin-card info-card">
            <div class="info-header">
              <div class="convert-point-badge">
                <i class="bi bi-calculator"></i>
              </div>
              <h3 class="method-name">{{ getMethodName(convertPoint.admission_methods_id) }}</h3>
              <div class="score-ranges">
                <div class="origin-score">
                  <span class="score-label">Điểm gốc:</span>
                  <span class="score-value">{{ formatNumber(convertPoint.origin_min) }} - {{ formatNumber(convertPoint.origin_max) }}</span>
                </div>
                <div class="convert-score">
                  <span class="score-label">Điểm quy đổi:</span>
                  <span class="score-value">{{ formatNumber(convertPoint.convert_score_min) }} - {{ formatNumber(convertPoint.convert_score_max) }}</span>
                </div>
              </div>
            </div>
            
            <div class="info-meta">
              <div class="info-item">
                <span class="info-label">ID:</span>
                <span class="info-value">#{{ convertPoint.id }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Ngày tạo:</span>
                <span class="info-value">{{ formatDate(convertPoint.created_at) }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Cập nhật:</span>
                <span class="info-value">{{ formatDate(convertPoint.updated_at) }}</span>
              </div>
            </div>
  
            <div class="info-actions">
              <button 
                class="btn-delete"
                @click="confirmDelete"
              >
                <i class="bi bi-trash me-2"></i>
                Xóa quy đổi điểm
              </button>
            </div>
          </div>
        </div>
  
        <!-- Edit Form -->
        <div class="col-md-8">
          <div class="admin-card">
            <h3 class="section-title">Chỉnh sửa thông tin</h3>
  
            <form @submit.prevent="updateConvertPoint" class="edit-form">
              <div class="form-group">
                <label for="admission-method-id">Phương thức xét tuyển</label>
                <select 
                  id="admission-method-id" 
                  v-model="formData.admission_methods_id" 
                  class="form-select" 
                  disabled
                >
                  <option v-for="method in admissionMethods" :key="method.id" :value="method.id">
                    {{ method.name }}
                  </option>
                </select>
                <small class="form-text text-muted">Không thể thay đổi phương thức xét tuyển</small>
              </div>
  
              <div class="card mb-4 p-3 border-info">
                <h5 class="card-title mb-3">Điểm gốc (theo thang điểm của phương thức xét tuyển)</h5>
                <div class="row">
                  <div class="col-md-6">
                    <div class="form-group">
                      <label for="origin-min">Điểm gốc tối thiểu <span class="required">*</span></label>
                      <input 
                        type="number" 
                        id="origin-min" 
                        v-model="formData.origin_min" 
                        class="form-control" 
                        required
                        :class="{ 'is-invalid': errors.origin_min }"
                        step="0.01"
                      >
                      <div v-if="errors.origin_min" class="invalid-feedback">{{ errors.origin_min }}</div>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="form-group">
                      <label for="origin-max">Điểm gốc tối đa <span class="required">*</span></label>
                      <input 
                        type="number" 
                        id="origin-max" 
                        v-model="formData.origin_max" 
                        class="form-control" 
                        required
                        :class="{ 'is-invalid': errors.origin_max }"
                        step="0.01"
                      >
                      <div v-if="errors.origin_max" class="invalid-feedback">{{ errors.origin_max }}</div>
                    </div>
                  </div>
                </div>
              </div>
  
              <div class="card mb-4 p-3 border-success">
                <h5 class="card-title mb-3">Điểm quy đổi (từ 0 đến 30)</h5>
                <div class="row">
                  <div class="col-md-6">
                    <div class="form-group">
                      <label for="convert-score-min">Điểm quy đổi tối thiểu <span class="required">*</span></label>
                      <input 
                        type="number" 
                        id="convert-score-min" 
                        v-model="formData.convert_score_min" 
                        class="form-control" 
                        required
                        :class="{ 'is-invalid': errors.convert_score_min }"
                        min="0" 
                        max="30"
                        step="0.01"
                      >
                      <div v-if="errors.convert_score_min" class="invalid-feedback">{{ errors.convert_score_min }}</div>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="form-group">
                      <label for="convert-score-max">Điểm quy đổi tối đa <span class="required">*</span></label>
                      <input 
                        type="number" 
                        id="convert-score-max" 
                        v-model="formData.convert_score_max" 
                        class="form-control" 
                        required
                        :class="{ 'is-invalid': errors.convert_score_max }"
                        min="0" 
                        max="30"
                        step="0.01"
                      >
                      <div v-if="errors.convert_score_max" class="invalid-feedback">{{ errors.convert_score_max }}</div>
                    </div>
                  </div>
                </div>
              </div>
  
              <div class="alert alert-info mb-4">
                <i class="bi bi-info-circle me-2"></i>
                <span>Điểm quy đổi phải nằm trong khoảng từ 0 đến 30.</span>
              </div>
  
              <div v-if="updateError" class="alert alert-danger">{{ updateError }}</div>
  
              <div class="form-actions">
                <button type="submit" class="btn-save" :disabled="isUpdating">
                  <i class="bi bi-check-circle me-2"></i>
                  {{ isUpdating ? 'Đang lưu...' : 'Lưu thay đổi' }}
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
            <h4 class="modal-title">Xác nhận xóa quy đổi điểm</h4>
            <button type="button" class="btn-close" @click="cancelDelete"></button>
          </div>
          <div class="modal-body">
            <p>Bạn có chắc chắn muốn xóa quy đổi điểm này?</p>
            <div class="convert-point-details">
              <p><strong>Phương thức xét tuyển:</strong> {{ getMethodName(convertPoint.admission_methods_id) }}</p>
              <p><strong>Điểm gốc:</strong> {{ formatNumber(convertPoint.origin_min) }} - {{ formatNumber(convertPoint.origin_max) }}</p>
              <p><strong>Điểm quy đổi:</strong> {{ formatNumber(convertPoint.convert_score_min) }} - {{ formatNumber(convertPoint.convert_score_max) }}</p>
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
  import { ref, reactive, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import ConvertPointController from '@/controllers/admins/ConvertPointController'
  import AdmissionMethodController from '@/controllers/admins/AdmissionMethodController'
  
  export default {
    name: 'AdminConvertPointDetail',
    props: {
      convertPointId: {
        type: [String, Number],
        required: true
      }
    },
    setup(props) {
      const router = useRouter()
      const convertPoint = ref({})
      const formData = reactive({
        admission_methods_id: '',
        origin_min: '',
        origin_max: '',
        convert_score_min: '',
        convert_score_max: ''
      })
      
      const admissionMethods = ref([])
      
      const loading = ref(true)
      const error = ref(null)
      const updateError = ref(null)
      const isUpdating = ref(false)
      const errors = reactive({
        origin_min: '',
        origin_max: '',
        convert_score_min: '',
        convert_score_max: ''
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
      
      // Format number with 2 decimal places if needed
      const formatNumber = (value) => {
        if (value === null || value === undefined) return 'N/A'
        
        const num = parseFloat(value)
        return Number.isInteger(num) ? num : num.toFixed(2)
      }
      
      // Get method name by ID
      const getMethodName = (methodId) => {
        const method = admissionMethods.value.find(m => m.id === methodId)
        return method ? method.name : 'Không xác định'
      }
      
      // Fetch convert point details
      const fetchConvertPointDetails = async () => {
        try {
          loading.value = true
          error.value = null
          
          // Load all data in parallel
          const [convertPointData, methodsData] = await Promise.all([
            ConvertPointController.getConvertPointById(props.convertPointId),
            AdmissionMethodController.getAllAdmissionMethods()
          ])
          
          convertPoint.value = convertPointData
          admissionMethods.value = methodsData
          
          // Set form data
          formData.admission_methods_id = convertPointData.admission_methods_id
          formData.origin_min = convertPointData.origin_min
          formData.origin_max = convertPointData.origin_max
          formData.convert_score_min = convertPointData.convert_score_min
          formData.convert_score_max = convertPointData.convert_score_max
        } catch (err) {
          error.value = `Không thể tải thông tin quy đổi điểm: ${err.message}`
        } finally {
          loading.value = false
        }
      }
      
      // Reset form
      const resetForm = () => {
        // Reset to original values
        formData.origin_min = convertPoint.value.origin_min
        formData.origin_max = convertPoint.value.origin_max
        formData.convert_score_min = convertPoint.value.convert_score_min
        formData.convert_score_max = convertPoint.value.convert_score_max
        
        // Clear errors
        Object.keys(errors).forEach(key => {
          errors[key] = ''
        })
        updateError.value = null
      }
      
      // Validate form
      const validateForm = () => {
        let isValid = true
        
        // Clear previous errors
        Object.keys(errors).forEach(key => {
          errors[key] = ''
        })
        updateError.value = null
        
        if (formData.origin_min === '' || isNaN(parseFloat(formData.origin_min))) {
          errors.origin_min = 'Vui lòng nhập điểm gốc tối thiểu hợp lệ'
          isValid = false
        }
        
        if (formData.origin_max === '' || isNaN(parseFloat(formData.origin_max))) {
          errors.origin_max = 'Vui lòng nhập điểm gốc tối đa hợp lệ'
          isValid = false
        }
        
        if (parseFloat(formData.origin_min) >= parseFloat(formData.origin_max)) {
          errors.origin_max = 'Điểm gốc tối đa phải lớn hơn điểm gốc tối thiểu'
          isValid = false
        }
        
        if (formData.convert_score_min === '' || isNaN(parseFloat(formData.convert_score_min))) {
          errors.convert_score_min = 'Vui lòng nhập điểm quy đổi tối thiểu hợp lệ'
          isValid = false
        }
        
        if (parseFloat(formData.convert_score_min) < 0 || parseFloat(formData.convert_score_min) > 30) {
          errors.convert_score_min = 'Điểm quy đổi tối thiểu phải từ 0 đến 30'
          isValid = false
        }
        
        if (formData.convert_score_max === '' || isNaN(parseFloat(formData.convert_score_max))) {
          errors.convert_score_max = 'Vui lòng nhập điểm quy đổi tối đa hợp lệ'
          isValid = false
        }
        
        if (parseFloat(formData.convert_score_max) < 0 || parseFloat(formData.convert_score_max) > 30) {
          errors.convert_score_max = 'Điểm quy đổi tối đa phải từ 0 đến 30'
          isValid = false
        }
        
        if (parseFloat(formData.convert_score_min) >= parseFloat(formData.convert_score_max)) {
          errors.convert_score_max = 'Điểm quy đổi tối đa phải lớn hơn điểm quy đổi tối thiểu'
          isValid = false
        }
        
        return isValid
      }
      
      // Update convert point
      const updateConvertPoint = async () => {
        try {
          // Validate form
          if (!validateForm()) {
            return
          }
          
          isUpdating.value = true
          
          const updatedData = {
            origin_min: parseFloat(formData.origin_min),
            origin_max: parseFloat(formData.origin_max),
            convert_score_min: parseFloat(formData.convert_score_min),
            convert_score_max: parseFloat(formData.convert_score_max)
          }
          
          await ConvertPointController.updateConvertPoint(props.convertPointId, updatedData)
          
          // Update local state
          Object.assign(convertPoint.value, updatedData, { updated_at: new Date().toISOString() })
          
          alert('Cập nhật quy đổi điểm thành công')
        } catch (err) {
          updateError.value = `Không thể cập nhật quy đổi điểm: ${err.message}`
        } finally {
          isUpdating.value = false
        }
      }
      
      // Confirm delete
      const confirmDelete = () => {
        showDeleteModal.value = true
      }
      
      // Cancel delete
      const cancelDelete = () => {
        showDeleteModal.value = false
      }
      
      // Delete convert point
      const deleteConvertPoint = async () => {
        try {
          isDeleting.value = true
          
          await ConvertPointController.deleteConvertPoint(props.convertPointId)
          
          alert('Xóa quy đổi điểm thành công')
          router.push('/admins/convert-points')
        } catch (err) {
          alert(`Lỗi: ${err.message}`)
        } finally {
          isDeleting.value = false
          showDeleteModal.value = false
        }
      }
  
      onMounted(() => {
        fetchConvertPointDetails()
      })
  
      return {
        convertPoint,
        formData,
        admissionMethods,
        loading,
        error,
        updateError,
        isUpdating,
        errors,
        showDeleteModal,
        isDeleting,
        formatDate,
        formatNumber,
        getMethodName,
        resetForm,
        updateConvertPoint,
        confirmDelete,
        cancelDelete,
        deleteConvertPoint
      }
    }
  }
  </script>
  
  <style scoped>
  .admin-convert-point-detail {
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
  
  .convert-point-badge {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background-color: #f1f8ff;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1rem;
    color: #1e88e5;
    font-size: 2.5rem;
  }
  
  .method-name {
    font-size: 1.3rem;
    font-weight: 600;
    color: #0B2942;
    margin-bottom: 1rem;
    padding: 0.35rem 0.75rem;
    border-radius: 50px;
    background-color: #e3f2fd;
  }
  
  .score-ranges {
    background-color: #f8f9fa;
    border-radius: 8px;
    padding: 1rem;
    width: 100%;
  }
  
  .origin-score, .convert-score {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.5rem;
  }
  
  .convert-score {
    margin-bottom: 0;
    color: #198754;
    font-weight: 500;
  }
  
  .score-label {
    font-weight: 500;
    color: #6c757d;
  }
  
  .score-value {
    font-weight: 500;
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
  
  .info-actions {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    margin-top: auto;
  }
  
  .btn-delete {
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
  
  .btn-delete:hover {
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
  
  .form-control, .form-select {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    font-size: 0.95rem;
    transition: all 0.3s;
  }
  
  .form-control:focus, .form-select:focus {
    outline: none;
    border-color: #4da0ff;
    box-shadow: 0 0 0 3px rgba(77, 160, 255, 0.25);
  }
  
  .form-control:disabled, .form-select:disabled {
    background-color: #f8f9fa;
    cursor: not-allowed;
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
  
  .form-text {
    font-size: 0.85rem;
    margin-top: 0.25rem;
  }
  
  .text-muted {
    color: #6c757d;
  }
  
  .card {
    border-radius: 8px;
  }
  
  .border-info {
    border-color: #0dcaf0;
  }
  
  .border-success {
    border-color: #198754;
  }
  
  .card-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #0B2942;
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
  
  .alert-info {
    background-color: #cff4fc;
    color: #055160;
    border: 1px solid #b6effb;
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