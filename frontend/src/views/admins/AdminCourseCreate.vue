<template>
    <div class="admin-course-create">
      <div class="admin-page-header">
        <div class="d-flex align-items-center">
          <router-link to="/admins/courses" class="btn-back">
            <i class="bi bi-arrow-left"></i>
          </router-link>
          <div>
            <h2 class="admin-page-title">Thêm lớp học phần mới</h2>
            <p class="admin-page-description">Tạo lớp học phần mới cho chương trình đào tạo</p>
          </div>
        </div>
      </div>
  
      <div class="admin-card">
        <form @submit.prevent="createCourse" class="create-form">
          <div class="row">
            <div class="col-md-6 mb-4">
              <div class="form-group">
                <label for="course-code">Mã học phần <span class="required">*</span></label>
                <input 
                  type="text" 
                  id="course-code" 
                  v-model="formData.course_code" 
                  class="form-control" 
                  required
                  :class="{ 'is-invalid': errors.course_code }"
                  placeholder="Ví dụ: 3190111"
                >
                <div v-if="errors.course_code" class="invalid-feedback">{{ errors.course_code }}</div>
                <small class="form-text text-muted">Mã học phần phải là duy nhất trong hệ thống</small>
              </div>
            </div>
            
            <div class="col-md-6 mb-4">
              <div class="form-group">
                <label for="credits">Số tín chỉ <span class="required">*</span></label>
                <input 
                  type="number" 
                  id="credits" 
                  v-model="formData.credits" 
                  class="form-control" 
                  required
                  :class="{ 'is-invalid': errors.credits }"
                  step="0.5"
                  min="0.5"
                  placeholder="Ví dụ: 3"
                >
                <div v-if="errors.credits" class="invalid-feedback">{{ errors.credits }}</div>
                <small class="form-text text-muted">Số tín chỉ có thể là số nguyên hoặc số thập phân (tối đa 1 chữ số thập phân)</small>
              </div>
            </div>
          </div>
  
          <div class="row">
            <div class="col-md-12 mb-4">
              <div class="form-group">
                <label for="name">Tên học phần <span class="required">*</span></label>
                <input 
                  type="text" 
                  id="name" 
                  v-model="formData.name" 
                  class="form-control" 
                  required
                  :class="{ 'is-invalid': errors.name }"
                  placeholder="Nhập tên đầy đủ của học phần"
                >
                <div v-if="errors.name" class="invalid-feedback">{{ errors.name }}</div>
              </div>
            </div>
          </div>
  
          <div class="alert alert-warning" v-if="isDuplicate">
            <i class="bi bi-exclamation-triangle-fill me-2"></i>
            <strong>Cảnh báo:</strong> Đã tồn tại học phần có mã <strong>{{ formData.course_code }}</strong> trong hệ thống. Vui lòng kiểm tra lại.
          </div>
  
          <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>
  
          <div class="form-actions">
            <button type="submit" class="btn-create" :disabled="isCreating || isDuplicate">
              <i class="bi bi-plus-circle me-2"></i>
              {{ isCreating ? 'Đang lưu...' : 'Thêm học phần' }}
            </button>
            <button type="reset" class="btn-reset" @click="resetForm">
              <i class="bi bi-arrow-repeat me-2"></i>
              Nhập lại
            </button>
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import { reactive, ref, computed, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import CourseController from '@/controllers/admins/CourseController'
  
  export default {
    name: 'AdminCourseCreate',
    setup() {
      const router = useRouter()
      const formData = reactive({
        course_code: '',
        name: '',
        credits: ''
      })
      
      const existingCourses = ref([])
      
      const isCreating = ref(false)
      const errorMessage = ref('')
      const errors = reactive({
        course_code: '',
        name: '',
        credits: ''
      })
      
      // Check if there's a duplicate course code
      const isDuplicate = computed(() => {
        if (!formData.course_code.trim()) {
          return false
        }
        
        return existingCourses.value.some(course => 
          course.course_code.toLowerCase() === formData.course_code.trim().toLowerCase()
        )
      })
  
      // Reset form
      const resetForm = () => {
        formData.course_code = ''
        formData.name = ''
        formData.credits = ''
        
        // Clear errors
        Object.keys(errors).forEach(key => {
          errors[key] = ''
        })
        errorMessage.value = ''
      }
  
      // Validate form
      const validateForm = () => {
        let isValid = true
        
        // Clear previous errors
        Object.keys(errors).forEach(key => {
          errors[key] = ''
        })
        errorMessage.value = ''
        
        if (!formData.course_code.trim()) {
          errors.course_code = 'Vui lòng nhập mã học phần'
          isValid = false
        }
        
        if (!formData.name.trim()) {
          errors.name = 'Vui lòng nhập tên học phần'
          isValid = false
        }
        
        if (!formData.credits) {
          errors.credits = 'Vui lòng nhập số tín chỉ'
          isValid = false
        } else if (isNaN(parseFloat(formData.credits)) || parseFloat(formData.credits) <= 0) {
          errors.credits = 'Số tín chỉ phải là số dương'
          isValid = false
        }
        
        if (isDuplicate.value) {
          errors.course_code = 'Mã học phần đã tồn tại trong hệ thống'
          isValid = false
        }
        
        return isValid
      }
  
      // Create course
      const createCourse = async () => {
        try {
          // Validate form
          if (!validateForm()) {
            return
          }
          
          isCreating.value = true
          
          const data = {
            course_code: formData.course_code.trim(),
            name: formData.name.trim(),
            credits: parseFloat(formData.credits)
          }
          
          await CourseController.createCourse(data)
          
          alert('Thêm lớp học phần thành công')
          router.push('/admins/courses')
        } catch (err) {
          errorMessage.value = `Không thể thêm lớp học phần: ${err.message}`
        } finally {
          isCreating.value = false
        }
      }
      
      // Load existing courses for duplicate check
      const loadExistingCourses = async () => {
        try {
          const courses = await CourseController.getAllCourses()
          existingCourses.value = courses
        } catch (err) {
          errorMessage.value = `Không thể tải danh sách học phần: ${err.message}`
        }
      }
  
      onMounted(() => {
        loadExistingCourses()
      })
  
      return {
        formData,
        isCreating,
        errorMessage,
        errors,
        isDuplicate,
        resetForm,
        createCourse
      }
    }
  }
  </script>
  
  <style scoped>
  .admin-course-create {
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
    padding: 2rem;
    transition: all 0.3s ease;
  }
  
  .admin-card:hover {
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
  }
  
  /* Form Styling */
  .create-form {
    width: 100%;
    max-width: 900px;
    margin: 0 auto;
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
  
  .btn-create {
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
  
  .btn-create:hover:not(:disabled) {
    background-color: #4da0ff;
  }
  
  .btn-create:disabled {
    background-color: #e9ecef;
    color: #6c757d;
    cursor: not-allowed;
  }
  
  .btn-reset {
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
  
  .btn-reset:hover {
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
  
  @media (max-width: 768px) {
    .form-actions {
      flex-direction: column;
    }
    
    .btn-create, .btn-reset {
      width: 100%;
    }
  }
  </style>