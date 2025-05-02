<template>
    <div class="admin-major-course-detail">
      <div class="admin-page-header">
        <div class="d-flex align-items-center">
          <router-link to="/admins/major-courses" class="btn-back">
            <i class="bi bi-arrow-left"></i>
          </router-link>
          <div>
            <h2 class="admin-page-title">Chi tiết khung chương trình đào tạo</h2>
            <p class="admin-page-description">Xem và chỉnh sửa thông tin khung chương trình</p>
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
        <p class="loading-text">Đang tải thông tin khung chương trình...</p>
      </div>
  
      <!-- Error State -->
      <div v-else-if="error" class="error-message">
        <i class="bi bi-exclamation-triangle-fill error-icon"></i>
        <span>{{ error }}</span>
      </div>
  
      <div v-else class="row">
        <!-- Major Course Info Card -->
        <div class="col-md-4 mb-4">
          <div class="admin-card info-card">
            <div class="info-header">
              <div 
                class="course-badge"
                :class="{
                  'bachelor': majorCourse.type === 'Cử nhân',
                  'engineer': majorCourse.type === 'Kỹ sư',
                  'architect': majorCourse.type === 'Kiến trúc sư'
                }"
              >
                <i class="bi bi-mortarboard-fill"></i>
              </div>
              <h3 class="major-name">{{ getMajorName(majorCourse.major_id) }}</h3>
              <div class="course-type">
                <span 
                  class="type-badge" 
                  :class="{
                    'bachelor': majorCourse.type === 'Cử nhân',
                    'engineer': majorCourse.type === 'Kỹ sư',
                    'architect': majorCourse.type === 'Kiến trúc sư'
                  }"
                >
                  {{ majorCourse.type }} ({{ majorCourse.year }})
                </span>
              </div>
            </div>
            
            <div class="info-meta">
              <div class="info-item">
                <span class="info-label">ID:</span>
                <span class="info-value">#{{ majorCourse.id }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Năm:</span>
                <span class="info-value">{{ majorCourse.year }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Ngày tạo:</span>
                <span class="info-value">{{ formatDate(majorCourse.created_at) }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Cập nhật:</span>
                <span class="info-value">{{ formatDate(majorCourse.updated_at) }}</span>
              </div>
            </div>
  
            <div class="info-actions">
              <button 
                class="btn-delete"
                @click="confirmDelete"
              >
                <i class="bi bi-trash me-2"></i>
                Xóa khung chương trình
              </button>
            </div>
          </div>
        </div>
  
        <!-- Edit Form -->
        <div class="col-md-8">
          <div class="admin-card">
            <h3 class="section-title">Chỉnh sửa thông tin</h3>
  
            <form @submit.prevent="updateMajorCourse" class="edit-form">
              <div class="form-group">
                <label for="major-id">Ngành học</label>
                <select 
                  id="major-id" 
                  v-model="formData.major_id" 
                  class="form-select" 
                  disabled
                >
                  <option v-for="major in majors" :key="major.id" :value="major.id">
                    {{ major.name }}
                  </option>
                </select>
                <small class="form-text text-muted">Không thể thay đổi ngành học</small>
              </div>
  
              <div class="row">
                <div class="col-md-6">
                  <div class="form-group">
                    <label for="year">Năm <span class="required">*</span></label>
                    <select 
                      id="year" 
                      v-model="formData.year" 
                      class="form-select" 
                      required
                      :class="{ 'is-invalid': errors.year }"
                    >
                      <option v-for="year in availableYears" :key="year" :value="year">
                        {{ year }}
                      </option>
                    </select>
                    <div v-if="errors.year" class="invalid-feedback">{{ errors.year }}</div>
                  </div>
                </div>
  
                <div class="col-md-6">
                  <div class="form-group">
                    <label for="type">Loại chương trình đào tạo <span class="required">*</span></label>
                    <select 
                      id="type" 
                      v-model="formData.type" 
                      class="form-select" 
                      required
                      :class="{ 'is-invalid': errors.type }"
                    >
                      <option value="Cử nhân">Cử nhân</option>
                      <option value="Kỹ sư">Kỹ sư</option>
                      <option value="Kiến trúc sư">Kiến trúc sư</option>
                    </select>
                    <div v-if="errors.type" class="invalid-feedback">{{ errors.type }}</div>
                  </div>
                </div>
              </div>
  
              <div class="alert alert-warning" v-if="isDuplicate">
                <i class="bi bi-exclamation-triangle-fill me-2"></i>
                <strong>Cảnh báo:</strong> Đã tồn tại khung chương trình {{ formData.type }} cho ngành này trong năm {{ formData.year }}. Vui lòng kiểm tra lại.
              </div>
  
              <div v-if="updateError" class="alert alert-danger">{{ updateError }}</div>
  
              <div class="form-actions">
                <button type="submit" class="btn-save" :disabled="isUpdating || isDuplicate">
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
            <h4 class="modal-title">Xác nhận xóa khung chương trình</h4>
            <button type="button" class="btn-close" @click="cancelDelete"></button>
          </div>
          <div class="modal-body">
            <p>Bạn có chắc chắn muốn xóa khung chương trình <strong>{{ majorCourse.type }}</strong> của ngành <strong>{{ getMajorName(majorCourse.major_id) }}</strong> năm <strong>{{ majorCourse.year }}</strong>?</p>
            <p class="text-danger">
              <i class="bi bi-exclamation-triangle me-2"></i>
              Thao tác này không thể khôi phục lại!
            </p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn-cancel" @click="cancelDelete">Hủy</button>
            <button type="button" class="btn-delete" @click="deleteMajorCourse" :disabled="isDeleting">
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
  import { useRouter } from 'vue-router'
  import MajorCourseController from '@/controllers/admins/MajorCourseController'
  import MajorController from '@/controllers/admins/MajorController'
  
  export default {
    name: 'AdminMajorCourseDetail',
    props: {
      majorCourseId: {
        type: [String, Number],
        required: true
      }
    },
    setup(props) {
      const router = useRouter()
      const majorCourse = ref({})
      const formData = reactive({
        major_id: '',
        year: '',
        type: ''
      })
      
      const existingMajorCourses = ref([])
      const majors = ref([])
      
      const loading = ref(true)
      const error = ref(null)
      const updateError = ref(null)
      const isUpdating = ref(false)
      const errors = reactive({
        year: '',
        type: ''
      })
      
      // Delete modal state
      const showDeleteModal = ref(false)
      const isDeleting = ref(false)
      
      // Generate a list of years (current year - 5 to current year + 5)
      const availableYears = computed(() => {
        const currentYear = new Date().getFullYear()
        const years = []
        for (let i = -5; i <= 5; i++) {
          years.push(currentYear + i)
        }
        return years.sort((a, b) => b - a) // Sort years in descending order
      })
      
      // Check if there's a duplicate entry
      const isDuplicate = computed(() => {
        if (!formData.major_id || !formData.year || !formData.type) {
          return false
        }
        
        // Check if values changed from original
        if (
          parseInt(formData.year) === majorCourse.value.year &&
          formData.type === majorCourse.value.type
        ) {
          return false // Not changed, so no duplicate
        }
        
        return existingMajorCourses.value.some(course => 
          parseInt(course.major_id) === parseInt(formData.major_id) &&
          parseInt(course.year) === parseInt(formData.year) &&
          course.type === formData.type &&
          course.id !== parseInt(props.majorCourseId) // Exclude current course
        )
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
      
      // Get major name by ID
      const getMajorName = (majorId) => {
        const major = majors.value.find(m => m.id === majorId)
        return major ? major.name : 'Không xác định'
      }
      
      // Fetch major course details
      const fetchMajorCourseDetails = async () => {
        try {
          loading.value = true
          error.value = null
          
          // Load all data in parallel
          const [courseData, coursesData, majorsData] = await Promise.all([
            MajorCourseController.getMajorCourseById(props.majorCourseId),
            MajorCourseController.getAllMajorCourses(),
            MajorController.getAllMajors()
          ])
          
          majorCourse.value = courseData
          existingMajorCourses.value = coursesData
          majors.value = majorsData
          
          // Set form data
          formData.major_id = courseData.major_id
          formData.year = courseData.year
          formData.type = courseData.type
        } catch (err) {
          error.value = `Không thể tải thông tin khung chương trình: ${err.message}`
        } finally {
          loading.value = false
        }
      }
      
      // Reset form
      const resetForm = () => {
        // Reset to original values
        formData.year = majorCourse.value.year
        formData.type = majorCourse.value.type
        
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
        
        if (!formData.year) {
          errors.year = 'Vui lòng chọn năm'
          isValid = false
        }
        
        if (!formData.type) {
          errors.type = 'Vui lòng chọn loại chương trình đào tạo'
          isValid = false
        }
        
        if (isDuplicate.value) {
          updateError.value = 'Đã tồn tại khung chương trình này'
          isValid = false
        }
        
        return isValid
      }
      
      // Update major course
      const updateMajorCourse = async () => {
        try {
          // Validate form
          if (!validateForm()) {
            return
          }
          
          isUpdating.value = true
          
          const updatedData = {
            year: parseInt(formData.year),
            type: formData.type
          }
          
          await MajorCourseController.updateMajorCourse(props.majorCourseId, updatedData)
          
          // Update local state
          Object.assign(majorCourse.value, updatedData, { updated_at: new Date().toISOString() })
          
          alert('Cập nhật khung chương trình thành công')
        } catch (err) {
          updateError.value = `Không thể cập nhật khung chương trình: ${err.message}`
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
      
      // Delete major course
      const deleteMajorCourse = async () => {
        try {
          isDeleting.value = true
          
          await MajorCourseController.deleteMajorCourse(props.majorCourseId)
          
          alert('Xóa khung chương trình thành công')
          router.push('/admins/major-courses')
        } catch (err) {
          alert(`Lỗi: ${err.message}`)
        } finally {
          isDeleting.value = false
          showDeleteModal.value = false
        }
      }
  
      onMounted(() => {
        fetchMajorCourseDetails()
      })
  
      return {
        majorCourse,
        formData,
        majors,
        loading,
        error,
        updateError,
        isUpdating,
        errors,
        showDeleteModal,
        isDeleting,
        availableYears,
        isDuplicate,
        formatDate,
        getMajorName,
        resetForm,
        updateMajorCourse,
        confirmDelete,
        cancelDelete,
        deleteMajorCourse
      }
    }
  }
  </script>
  
  <style scoped>
  .admin-major-course-detail {
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
  
  .course-badge {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1rem;
    font-size: 2.5rem;
  }
  
  .course-badge.bachelor {
    background-color: #e3f2fd;
    color: #0d6efd;
  }
  
  .course-badge.engineer {
    background-color: #e8f5e9;
    color: #28a745;
  }
  
  .course-badge.architect {
    background-color: #fff8e1;
    color: #ffc107;
  }
  
  .major-name {
    font-size: 1.3rem;
    font-weight: 600;
    color: #0B2942;
    margin-bottom: 1rem;
  }
  
  .course-type {
    margin-bottom: 0.5rem;
  }
  
  .type-badge {
    display: inline-block;
    padding: 0.35rem 0.75rem;
    border-radius: 50px;
    font-size: 0.85rem;
    font-weight: 500;
  }
  
  .type-badge.bachelor {
    background-color: #e3f2fd;
    color: #0d6efd;
  }
  
  .type-badge.engineer {
    background-color: #e8f5e9;
    color: #28a745;
  }
  
  .type-badge.architect {
    background-color: #fff8e1;
    color: #ffc107;
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
  
  .form-control.is-invalid, .form-select.is-invalid {
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
  
  .alert-warning {
    background-color: #fff3cd;
    color: #664d03;
    border: 1px solid #ffecb5;
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