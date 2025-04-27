<template>
    <div class="admin-major-detail">
      <div class="admin-page-header">
        <div class="d-flex align-items-center">
          <router-link to="/admins/majors" class="btn-back">
            <i class="bi bi-arrow-left"></i>
          </router-link>
          <div>
            <h2 class="admin-page-title">Chi tiết ngành</h2>
            <p class="admin-page-description">Xem và chỉnh sửa thông tin ngành đào tạo</p>
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
        <p class="loading-text">Đang tải thông tin ngành...</p>
      </div>
  
      <!-- Error State -->
      <div v-else-if="error" class="error-message">
        <i class="bi bi-exclamation-triangle-fill error-icon"></i>
        <span>{{ error }}</span>
      </div>
  
      <div v-else class="row">
        <!-- Major Info Card -->
        <div class="col-md-4 mb-4">
          <div class="admin-card info-card">
            <div class="info-header">
              <div class="major-badge">
                <i class="bi bi-book"></i>
              </div>
              <h3 class="major-name">{{ major.name }}</h3>
              <div class="major-code">{{ major.major_code }}</div>
            </div>
            
            <div class="info-meta">
              <div class="info-item">
                <span class="info-label">ID:</span>
                <span class="info-value">#{{ major.id }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Khoa:</span>
                <span class="info-value">
                  <router-link :to="`/admins/faculties/${major.faculty_id}`" class="faculty-link">
                    {{ facultyName }}
                  </router-link>
                </span>
              </div>
              <div class="info-item">
                <span class="info-label">Chỉ tiêu:</span>
                <span class="info-value seats">{{ major.seats || 0 }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Ngày tạo:</span>
                <span class="info-value">{{ formatDate(major.created_at) }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Cập nhật:</span>
                <span class="info-value">{{ formatDate(major.updated_at) }}</span>
              </div>
            </div>
  
            <div class="info-actions">
              <button 
                class="btn-delete-major"
                @click="confirmDelete"
              >
                <i class="bi bi-trash me-2"></i>
                Xóa ngành
              </button>
              <router-link :to="`/admins/majors/${major.id}/admission-methods`" class="btn-view-admission-methods">
                <i class="bi bi-clipboard-check me-2"></i>
                Quản lý phương thức tuyển sinh
              </router-link>
            </div>
            
          </div>
        </div>
  
        <!-- Edit Form -->
        <div class="col-md-8">
          <div class="admin-card">
            <h3 class="section-title">Chỉnh sửa thông tin</h3>
  
            <form @submit.prevent="updateMajor" class="edit-form">
              <div class="form-group">
                <label for="faculty">Khoa <span class="required">*</span></label>
                <select 
                  id="faculty" 
                  v-model="formData.faculty_id" 
                  class="form-control"
                  required
                  :class="{ 'is-invalid': errors.faculty_id }"
                >
                  <option value="" disabled>Chọn khoa</option>
                  <option v-for="faculty in faculties" :key="faculty.id" :value="faculty.id">
                    {{ faculty.name }}
                  </option>
                </select>
                <div v-if="errors.faculty_id" class="invalid-feedback">{{ errors.faculty_id }}</div>
              </div>
  
              <div class="form-group">
                <label for="major_code">Mã ngành <span class="required">*</span></label>
                <input 
                  type="text" 
                  id="major_code" 
                  v-model="formData.major_code" 
                  class="form-control" 
                  required
                  :class="{ 'is-invalid': errors.major_code }"
                >
                <div v-if="errors.major_code" class="invalid-feedback">{{ errors.major_code }}</div>
              </div>
  
              <div class="form-group">
                <label for="name">Tên ngành <span class="required">*</span></label>
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
  
              <div class="form-group">
                <label for="seats">Chỉ tiêu</label>
                <input 
                  type="number" 
                  id="seats" 
                  v-model="formData.seats" 
                  class="form-control"
                  min="0" 
                  :class="{ 'is-invalid': errors.seats }"
                >
                <div v-if="errors.seats" class="invalid-feedback">{{ errors.seats }}</div>
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
            <h4 class="modal-title">Xác nhận xóa ngành</h4>
            <button type="button" class="btn-close" @click="cancelDelete"></button>
          </div>
          <div class="modal-body">
            <p>Bạn có chắc chắn muốn xóa ngành <strong>{{ major.name }}</strong>?</p>
            <p class="text-danger">
              <i class="bi bi-exclamation-triangle me-2"></i>
              Thao tác này không thể khôi phục lại!
            </p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn-cancel" @click="cancelDelete">Hủy</button>
            <button type="button" class="btn-delete" @click="deleteMajor" :disabled="isDeleting">
              <span v-if="isDeleting">Đang xóa...</span>
              <span v-else>Xác nhận xóa</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, reactive, onMounted, computed } from 'vue'
  import { useRouter } from 'vue-router'
  import MajorController from '@/controllers/admins/MajorController'
  import FacultyController from '@/controllers/admins/FacultyController'
  
  export default {
    name: 'AdminMajorDetail',
    props: {
      majorId: {
        type: [String, Number],
        required: true
      }
    },
    setup(props) {
      const router = useRouter()
      const major = ref({})
      const faculties = ref([])
      const formData = reactive({
        name: '',
        major_code: '',
        faculty_id: '',
        seats: '',
        description: ''
      })
      const loading = ref(true)
      const error = ref(null)
      const updateError = ref(null)
      const isSaving = ref(false)
      const errors = reactive({
        name: '',
        major_code: '',
        faculty_id: '',
        seats: ''
      })
      
      // Delete modal state
      const showDeleteModal = ref(false)
      const isDeleting = ref(false)
      
      // Get faculty name for display
      const facultyName = computed(() => {
        const faculty = faculties.value.find(f => f.id === major.value.faculty_id)
        return faculty ? faculty.name : 'N/A'
      })
  
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
  
      // Load faculties for dropdown
      const loadFaculties = async () => {
        try {
          const data = await FacultyController.getAllFaculties()
          faculties.value = data
        } catch (err) {
          console.error('Error loading faculties:', err)
        }
      }
  
      // Fetch major details
      const fetchMajorDetails = async () => {
        try {
          loading.value = true
          error.value = null
          
          const data = await MajorController.getMajorById(props.majorId)
          major.value = data
          
          // Set form data
          formData.name = data.name || ''
          formData.major_code = data.major_code || ''
          formData.faculty_id = data.faculty_id || ''
          formData.seats = data.seats || 0
          formData.description = data.description || ''
        } catch (err) {
          error.value = `Không thể tải thông tin ngành: ${err.message}`
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
        
        // Faculty validation
        if (!formData.faculty_id) {
          errors.faculty_id = 'Vui lòng chọn khoa'
          isValid = false
        }
        
        // Major code validation
        if (!formData.major_code.trim()) {
          errors.major_code = 'Mã ngành không được để trống'
          isValid = false
        }
        
        // Name validation
        if (!formData.name.trim()) {
          errors.name = 'Tên ngành không được để trống'
          isValid = false
        }
        
        // Seats validation - should be a number
        if (formData.seats && isNaN(parseInt(formData.seats))) {
          errors.seats = 'Chỉ tiêu phải là số'
          isValid = false
        }
        
        return isValid
      }
  
      // Reset form
      const resetForm = () => {
        formData.name = major.value.name || ''
        formData.major_code = major.value.major_code || ''
        formData.faculty_id = major.value.faculty_id || ''
        formData.seats = major.value.seats || 0
        formData.description = major.value.description || ''
        
        // Clear errors
        Object.keys(errors).forEach(key => {
          errors[key] = ''
        })
        updateError.value = null
      }
  
      // Update major
      const updateMajor = async () => {
        try {
          // Validate form
          if (!validateForm()) {
            return
          }
          
          isSaving.value = true
          updateError.value = null
          
          // Convert seats to number
          const majorData = { ...formData }
          if (majorData.seats) {
            majorData.seats = parseInt(majorData.seats)
          } else {
            majorData.seats = 0
          }
          
          await MajorController.updateMajor(props.majorId, majorData)
          
          // Update local major object
          major.value = { ...major.value, ...majorData }
          
          alert('Cập nhật thông tin ngành thành công')
        } catch (err) {
          updateError.value = `Không thể cập nhật thông tin ngành: ${err.message}`
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
  
      // Delete major
      const deleteMajor = async () => {
        try {
          isDeleting.value = true
          
          await MajorController.deleteMajor(props.majorId)
          
          alert('Xóa ngành thành công')
          
          // Redirect to majors list or back to faculty detail if we know the faculty
          if (major.value.faculty_id) {
            router.push(`/admins/majors/faculty/${major.value.faculty_id}`)
          } else {
            router.push('/admins/majors')
          }
        } catch (err) {
          alert(`Lỗi: ${err.message}`)
        } finally {
          isDeleting.value = false
          showDeleteModal.value = false
        }
      }
  
      onMounted(async () => {
        await loadFaculties()
        await fetchMajorDetails()
      })
  
      return {
        major,
        formData,
        faculties,
        facultyName,
        loading,
        error,
        updateError,
        isSaving,
        errors,
        showDeleteModal,
        isDeleting,
        formatDate,
        resetForm,
        updateMajor,
        confirmDelete,
        cancelDelete,
        deleteMajor
      }
    }
  }
  </script>
  
  <style scoped>
  .admin-major-detail {
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
  
  .major-badge {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background-color: #e3f2fd;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1rem;
    color: #0d6efd;
    font-size: 2.5rem;
  }
  
  .major-name {
    font-size: 1.5rem;
    font-weight: 600;
    color: #0B2942;
    margin-bottom: 0.5rem;
  }
  
  .major-code {
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
  
  .info-value.seats {
    display: inline-block;
    padding: 0.25rem 0.5rem;
    border-radius: 50px;
    font-size: 0.85rem;
    background-color: #e3faeb;
    color: #198754;
  }
  
  .faculty-link {
    color: #0B2942;
    text-decoration: none;
    transition: all 0.3s;
  }
  
  .faculty-link:hover {
    color: #4da0ff;
    text-decoration: underline;
  }
  
  .info-actions {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    margin-top: auto;
  }
  
  .btn-delete-major {
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
  
  .btn-delete-major:hover {
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
  
  select.form-control {
    appearance: none;
    background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3e%3cpath fill='none' stroke='%23343a40' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M2 5l6 6 6-6'/%3e%3c/svg%3e");
    background-repeat: no-repeat;
    background-position: right 0.75rem center;
    background-size: 16px 12px;
    padding-right: 2.5rem;
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

  .btn-view-admission-methods {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem 1rem;
  background-color: #8c54ff;
  color: white;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-view-admission-methods:hover {
  background-color: #7540e0;
  color: white;
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