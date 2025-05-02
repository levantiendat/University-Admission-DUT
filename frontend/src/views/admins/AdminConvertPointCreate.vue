<template>
    <div class="admin-convert-point-create">
      <div class="admin-page-header">
        <div class="d-flex align-items-center">
          <router-link to="/admins/convert-points" class="btn-back">
            <i class="bi bi-arrow-left"></i>
          </router-link>
          <div>
            <h2 class="admin-page-title">Thêm quy đổi điểm mới</h2>
            <p class="admin-page-description">Tạo mới quy đổi điểm giữa các phương thức xét tuyển</p>
          </div>
        </div>
      </div>
  
      <div class="admin-card">
        <form @submit.prevent="createConvertPoint" class="create-form">
          <div class="row">
            <div class="col-md-12">
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
                    placeholder="Nhập điểm gốc tối thiểu"
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
                    placeholder="Nhập điểm gốc tối đa"
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
                    placeholder="0 đến 30"
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
                    placeholder="0 đến 30"
                  >
                  <div v-if="errors.convert_score_max" class="invalid-feedback">{{ errors.convert_score_max }}</div>
                </div>
              </div>
            </div>
          </div>
  
          <div class="alert alert-info mb-4">
            <i class="bi bi-info-circle me-2"></i>
            <span>Điểm quy đổi sẽ được tính theo tỷ lệ tương ứng giữa điểm gốc và điểm quy đổi.</span>
          </div>
  
          <div class="alert alert-warning" v-if="isDuplicate">
            <i class="bi bi-exclamation-triangle-fill me-2"></i>
            <strong>Cảnh báo:</strong> Đã tồn tại quy đổi điểm cho phương thức này trong khoảng điểm gốc tương tự. Vui lòng kiểm tra lại.
          </div>
  
          <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>
  
          <div class="form-actions">
            <button type="submit" class="btn-create" :disabled="isCreating">
              <i class="bi bi-plus-circle me-2"></i>
              {{ isCreating ? 'Đang lưu...' : 'Lưu quy đổi điểm' }}
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
  import ConvertPointController from '@/controllers/admins/ConvertPointController'
  import AdmissionMethodController from '@/controllers/admins/AdmissionMethodController'
  
  export default {
    name: 'AdminConvertPointCreate',
    setup() {
      const router = useRouter()
      const formData = reactive({
        admission_methods_id: '',
        origin_min: '',
        origin_max: '',
        convert_score_min: '',
        convert_score_max: ''
      })
      
      const existingConvertPoints = ref([])
      const admissionMethods = ref([])
      
      const isCreating = ref(false)
      const errorMessage = ref('')
      const errors = reactive({
        admission_methods_id: '',
        origin_min: '',
        origin_max: '',
        convert_score_min: '',
        convert_score_max: ''
      })
      
      // Check if there's a duplicate entry
      const isDuplicate = computed(() => {
        if (!formData.admission_methods_id || !formData.origin_min || !formData.origin_max) {
          return false
        }
        
        const methodId = parseInt(formData.admission_methods_id)
        const originMin = parseFloat(formData.origin_min)
        const originMax = parseFloat(formData.origin_max)
        
        return existingConvertPoints.value.some(cp => {
          if (cp.admission_methods_id !== methodId) return false
          
          // Check if ranges overlap
          return !(originMax < cp.origin_min || originMin > cp.origin_max)
        })
      })
  
      // Reset form
      const resetForm = () => {
        formData.admission_methods_id = ''
        formData.origin_min = ''
        formData.origin_max = ''
        formData.convert_score_min = ''
        formData.convert_score_max = ''
        
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
        
        if (!formData.admission_methods_id) {
          errors.admission_methods_id = 'Vui lòng chọn phương thức xét tuyển'
          isValid = false
        }
        
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
  
      // Create convert point
      const createConvertPoint = async () => {
        try {
          // Validate form
          if (!validateForm()) {
            return
          }
          
          isCreating.value = true
          
          const data = {
            admission_methods_id: parseInt(formData.admission_methods_id),
            origin_min: parseFloat(formData.origin_min),
            origin_max: parseFloat(formData.origin_max),
            convert_score_min: parseFloat(formData.convert_score_min),
            convert_score_max: parseFloat(formData.convert_score_max)
          }
          
          await ConvertPointController.createConvertPoint(data)
          
          alert('Thêm quy đổi điểm thành công')
          router.push('/admins/convert-points')
        } catch (err) {
          errorMessage.value = `Không thể thêm quy đổi điểm: ${err.message}`
        } finally {
          isCreating.value = false
        }
      }
      
      // Load data
      const loadData = async () => {
        try {
          // Load all data in parallel
          const [convertPointsData, methodsData] = await Promise.all([
            ConvertPointController.getAllConvertPoints(),
            AdmissionMethodController.getAllAdmissionMethods()
          ])
          
          existingConvertPoints.value = convertPointsData
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
        admissionMethods,
        isCreating,
        errorMessage,
        errors,
        isDuplicate,
        resetForm,
        createConvertPoint
      }
    }
  }
  </script>
  
  <style scoped>
  .admin-convert-point-create {
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
  
  .alert-info {
    background-color: #cff4fc;
    color: #055160;
    border: 1px solid #b6effb;
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