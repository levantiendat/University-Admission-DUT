<template>
    <div class="admin-previous-admission-create">
      <div class="admin-page-header">
        <div class="d-flex align-items-center">
          <router-link to="/admins/previous-admissions" class="btn-back">
            <i class="bi bi-arrow-left"></i>
          </router-link>
          <div>
            <h2 class="admin-page-title">Thêm điểm chuẩn mới</h2>
            <p class="admin-page-description">Thêm thông tin điểm chuẩn của năm trước</p>
          </div>
        </div>
      </div>
  
      <div class="admin-card">
        <form @submit.prevent="createPreviousAdmission" class="create-form">
          <div class="row">
            <div class="col-md-6">
              <div class="form-group">
                <label for="major-id">Ngành <span class="required">*</span></label>
                <select 
                  id="major-id" 
                  v-model="formData.major_id" 
                  class="form-select" 
                  required
                  :class="{ 'is-invalid': errors.major_id }"
                >
                  <option value="" disabled selected>Chọn ngành</option>
                  <option v-for="major in majors" :key="major.id" :value="major.id">
                    {{ major.name }}
                  </option>
                </select>
                <div v-if="errors.major_id" class="invalid-feedback">{{ errors.major_id }}</div>
              </div>
            </div>
  
            <div class="col-md-6">
              <div class="form-group">
                <label for="admission-method-id">Phương thức xét tuyển <span class="required">*</span></label>
                <select 
                  id="admission-method-id" 
                  v-model="formData.admission_methods_id" 
                  class="form-select" 
                  required
                  :class="{ 'is-invalid': errors.admission_methods_id }"
                >
                  <option value="" disabled selected>Chọn phương thức xét tuyển</option>
                  <option v-for="method in admissionMethods" :key="method.id" :value="method.id">
                    {{ method.name }}
                  </option>
                </select>
                <div v-if="errors.admission_methods_id" class="invalid-feedback">{{ errors.admission_methods_id }}</div>
              </div>
            </div>
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
                <label for="score">Điểm chuẩn <span class="required">*</span></label>
                <input 
                  type="number" 
                  id="score" 
                  v-model="formData.score" 
                  class="form-control" 
                  min="0" 
                  step="0.01"
                  placeholder="Ví dụ: 25.75"
                  required
                  :class="{ 'is-invalid': errors.score }"
                >
                <div v-if="errors.score" class="invalid-feedback">{{ errors.score }}</div>
              </div>
            </div>
          </div>
  
          <div class="alert alert-warning" v-if="isDuplicate">
            <i class="bi bi-exclamation-triangle-fill me-2"></i>
            <strong>Cảnh báo:</strong> Đã tồn tại điểm chuẩn cho ngành và phương thức xét tuyển này trong năm đã chọn. Tạo mới sẽ cập nhật dữ liệu hiện có.
          </div>
  
          <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>
  
          <div class="form-actions">
            <button type="submit" class="btn-create" :disabled="isCreating">
              <i class="bi bi-plus-circle me-2"></i>
              {{ isCreating ? 'Đang lưu...' : 'Lưu điểm chuẩn' }}
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
  import PreviousAdmissionController from '@/controllers/admins/PreviousAdmissionController'
  import MajorController from '@/controllers/admins/MajorController'
  import AdmissionMethodController from '@/controllers/admins/AdmissionMethodController'
  
  export default {
    name: 'AdminPreviousAdmissionCreate',
    setup() {
      const router = useRouter()
      const formData = reactive({
        major_id: '',
        admission_methods_id: '',
        year: '',
        score: ''
      })
      
      const existingAdmissions = ref([])
      const majors = ref([])
      const admissionMethods = ref([])
      
      const isCreating = ref(false)
      const errorMessage = ref('')
      const errors = reactive({
        major_id: '',
        admission_methods_id: '',
        year: '',
        score: ''
      })
  
      // Generate a list of years (current year - 10 to current year)
      const availableYears = computed(() => {
        const currentYear = new Date().getFullYear()
        const years = []
        for (let i = 0; i <= 10; i++) {
          years.push(currentYear - i)
        }
        return years
      })
      
      // Check if there's a duplicate entry
      const isDuplicate = computed(() => {
        if (!formData.major_id || !formData.admission_methods_id || !formData.year) {
          return false
        }
        
        return existingAdmissions.value.some(admission => 
          parseInt(admission.major_id) === parseInt(formData.major_id) &&
          parseInt(admission.admission_methods_id) === parseInt(formData.admission_methods_id) &&
          parseInt(admission.year) === parseInt(formData.year)
        )
      })
  
      // Reset form
      const resetForm = () => {
        formData.major_id = ''
        formData.admission_methods_id = ''
        formData.year = ''
        formData.score = ''
        
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
          errors.major_id = 'Vui lòng chọn ngành'
          isValid = false
        }
        
        if (!formData.admission_methods_id) {
          errors.admission_methods_id = 'Vui lòng chọn phương thức xét tuyển'
          isValid = false
        }
        
        if (!formData.year) {
          errors.year = 'Vui lòng chọn năm'
          isValid = false
        }
        
        if (!formData.score && formData.score !== 0) {
          errors.score = 'Vui lòng nhập điểm chuẩn'
          isValid = false
        } else if (isNaN(parseFloat(formData.score)) || parseFloat(formData.score) < 0) {
          errors.score = 'Điểm chuẩn phải là số và không được âm'
          isValid = false
        }
        
        return isValid
      }
  
      // Create previous admission record
      const createPreviousAdmission = async () => {
        try {
          // Validate form
          if (!validateForm()) {
            return
          }
          
          isCreating.value = true
          
          const data = {
            major_id: parseInt(formData.major_id),
            admission_methods_id: parseInt(formData.admission_methods_id),
            year: parseInt(formData.year),
            score: parseFloat(formData.score)
          }
          
          await PreviousAdmissionController.createPreviousAdmission(data)
          
          alert('Thêm điểm chuẩn thành công')
          router.push('/admins/previous-admissions')
        } catch (err) {
          errorMessage.value = `Không thể thêm điểm chuẩn: ${err.message}`
        } finally {
          isCreating.value = false
        }
      }
      
      // Load data
      const loadData = async () => {
        try {
          // Load all data in parallel
          const [admissionsData, majorsData, methodsData] = await Promise.all([
            PreviousAdmissionController.getAllPreviousAdmissions(),
            MajorController.getAllMajors(),
            AdmissionMethodController.getAllAdmissionMethods()
          ])
          
          existingAdmissions.value = admissionsData
          majors.value = majorsData
          admissionMethods.value = methodsData
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
        admissionMethods,
        isCreating,
        errorMessage,
        errors,
        availableYears,
        isDuplicate,
        resetForm,
        createPreviousAdmission
      }
    }
  }
  </script>
  
  <style scoped>
  .admin-previous-admission-create {
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