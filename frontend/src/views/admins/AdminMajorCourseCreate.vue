<template>
    <div class="admin-major-course-create">
      <div class="admin-page-header">
        <div class="d-flex align-items-center">
          <router-link to="/admins/major-courses" class="btn-back">
            <i class="bi bi-arrow-left"></i>
          </router-link>
          <div>
            <h2 class="admin-page-title">Thêm khung chương trình đào tạo mới</h2>
            <p class="admin-page-description">Tạo khung chương trình đào tạo cho ngành học</p>
          </div>
        </div>
      </div>
  
      <div class="admin-card">
        <form @submit.prevent="createMajorCourse" class="create-form">
          <div class="row">
            <div class="col-md-12 mb-4">
              <div class="form-group">
                <label for="major-id">Ngành học <span class="required">*</span></label>
                <select 
                  id="major-id" 
                  v-model="formData.major_id" 
                  class="form-select" 
                  required
                  :class="{ 'is-invalid': errors.major_id }"
                >
                  <option value="" disabled selected>Chọn ngành học</option>
                  <option v-for="major in majors" :key="major.id" :value="major.id">
                    {{ major.name }}
                  </option>
                </select>
                <div v-if="errors.major_id" class="invalid-feedback">{{ errors.major_id }}</div>
              </div>
            </div>
  
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
                  <option value="" disabled selected>Chọn năm</option>
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
                  <option value="" disabled selected>Chọn loại chương trình</option>
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
  
          <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>
  
          <div class="form-actions">
            <button type="submit" class="btn-create" :disabled="isCreating || isDuplicate">
              <i class="bi bi-plus-circle me-2"></i>
              {{ isCreating ? 'Đang lưu...' : 'Tạo khung chương trình' }}
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
  import MajorCourseController from '@/controllers/admins/MajorCourseController'
  import MajorController from '@/controllers/admins/MajorController'
  
  export default {
    name: 'AdminMajorCourseCreate',
    setup() {
      const router = useRouter()
      const formData = reactive({
        major_id: '',
        year: '',
        type: ''
      })
      
      const existingMajorCourses = ref([])
      const majors = ref([])
      
      const isCreating = ref(false)
      const errorMessage = ref('')
      const errors = reactive({
        major_id: '',
        year: '',
        type: ''
      })
      
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
        
        return existingMajorCourses.value.some(course => 
          parseInt(course.major_id) === parseInt(formData.major_id) &&
          parseInt(course.year) === parseInt(formData.year) &&
          course.type === formData.type
        )
      })
  
      // Reset form
      const resetForm = () => {
        formData.major_id = ''
        formData.year = ''
        formData.type = ''
        
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
        
        if (!formData.major_id) {
          errors.major_id = 'Vui lòng chọn ngành học'
          isValid = false
        }
        
        if (!formData.year) {
          errors.year = 'Vui lòng chọn năm'
          isValid = false
        }
        
        if (!formData.type) {
          errors.type = 'Vui lòng chọn loại chương trình đào tạo'
          isValid = false
        }
        
        if (isDuplicate.value) {
          errorMessage.value = 'Đã tồn tại khung chương trình này'
          isValid = false
        }
        
        return isValid
      }
  
      // Create major course
      const createMajorCourse = async () => {
        try {
          // Validate form
          if (!validateForm()) {
            return
          }
          
          isCreating.value = true
          
          const data = {
            major_id: parseInt(formData.major_id),
            year: parseInt(formData.year),
            type: formData.type
          }
          
          await MajorCourseController.createMajorCourse(data)
          
          alert('Thêm khung chương trình thành công')
          router.push('/admins/major-courses')
        } catch (err) {
          errorMessage.value = `Không thể tạo khung chương trình: ${err.message}`
        } finally {
          isCreating.value = false
        }
      }
      
      // Load data
      const loadData = async () => {
        try {
          // Load all data in parallel
          const [coursesData, majorsData] = await Promise.all([
            MajorCourseController.getAllMajorCourses(),
            MajorController.getAllMajors()
          ])
          
          existingMajorCourses.value = coursesData
          majors.value = majorsData
        } catch (err) {
          errorMessage.value = `Không thể tải dữ liệu: ${err.message}`
        }
      }
  
      onMounted(() => {
        loadData()
      })
  
      return {
        formData,
        majors,
        isCreating,
        errorMessage,
        errors,
        availableYears,
        isDuplicate,
        resetForm,
        createMajorCourse
      }
    }
  }
  </script>
  
  <style scoped>
  .admin-major-course-create {
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