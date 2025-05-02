<template>
    <div class="admin-admission-description-create">
      <div class="admin-page-header">
        <div class="d-flex align-items-center">
          <router-link to="/admins/admission-descriptions" class="btn-back">
            <i class="bi bi-arrow-left"></i>
          </router-link>
          <div>
            <h2 class="admin-page-title">Thêm lĩnh vực/môn học xét tuyển mới</h2>
            <p class="admin-page-description">Thêm lĩnh vực hoặc môn học đạt giải cho phương thức xét tuyển</p>
          </div>
        </div>
      </div>
  
      <div class="admin-card">
        <form @submit.prevent="createAdmissionDescription" class="create-form">
          <div class="row">
            <div class="col-md-12">
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
          </div>
  
          <div class="row">
            <div class="col-md-12">
              <div class="form-group">
                <label for="field-or-subject-name">Tên lĩnh vực hoặc môn học <span class="required">*</span></label>
                <input 
                  type="text" 
                  id="field-or-subject-name" 
                  v-model="formData.field_or_subject_name" 
                  class="form-control" 
                  required
                  :class="{ 'is-invalid': errors.field_or_subject_name }"
                  placeholder="Ví dụ: Toán, Vật Lý, Tin Học, Khoa học kỹ thuật..."
                >
                <div v-if="errors.field_or_subject_name" class="invalid-feedback">{{ errors.field_or_subject_name }}</div>
                <small class="form-text text-muted">Nhập tên lĩnh vực hoặc môn học học sinh giỏi, khoa học kỹ thuật cho phương thức xét tuyển</small>
              </div>
            </div>
          </div>
  
          <div class="alert alert-warning" v-if="isDuplicate">
            <i class="bi bi-exclamation-triangle-fill me-2"></i>
            <strong>Cảnh báo:</strong> Đã tồn tại lĩnh vực/môn học tương tự cho ngành đã chọn. Vui lòng kiểm tra lại.
          </div>
  
          <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>
  
          <div class="form-actions">
            <button type="submit" class="btn-create" :disabled="isCreating">
              <i class="bi bi-plus-circle me-2"></i>
              {{ isCreating ? 'Đang lưu...' : 'Lưu thông tin' }}
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
  import AdmissionDescriptionController from '@/controllers/admins/AdmissionDescriptionController'
  import MajorController from '@/controllers/admins/MajorController'
  
  export default {
    name: 'AdminAdmissionDescriptionCreate',
    setup() {
      const router = useRouter()
      const formData = reactive({
        major_id: '',
        field_or_subject_name: ''
      })
      
      const existingDescriptions = ref([])
      const majors = ref([])
      
      const isCreating = ref(false)
      const errorMessage = ref('')
      const errors = reactive({
        major_id: '',
        field_or_subject_name: ''
      })
      
      // Check if there's a duplicate entry
      const isDuplicate = computed(() => {
        if (!formData.major_id || !formData.field_or_subject_name) {
          return false
        }
        
        return existingDescriptions.value.some(desc => 
          parseInt(desc.major_id) === parseInt(formData.major_id) &&
          desc.field_or_subject_name.toLowerCase() === formData.field_or_subject_name.toLowerCase()
        )
      })
  
      // Reset form
      const resetForm = () => {
        formData.major_id = ''
        formData.field_or_subject_name = ''
        
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
        
        if (!formData.field_or_subject_name || formData.field_or_subject_name.trim() === '') {
          errors.field_or_subject_name = 'Vui lòng nhập tên lĩnh vực hoặc môn học'
          isValid = false
        }
        
        return isValid
      }
  
      // Create admission description
      const createAdmissionDescription = async () => {
        try {
          // Validate form
          if (!validateForm()) {
            return
          }
          
          isCreating.value = true
          
          const data = {
            major_id: parseInt(formData.major_id),
            field_or_subject_name: formData.field_or_subject_name.trim()
          }
          
          await AdmissionDescriptionController.createAdmissionDescription(data)
          
          alert('Thêm lĩnh vực/môn học thành công')
          router.push('/admins/admission-descriptions')
        } catch (err) {
          errorMessage.value = `Không thể thêm lĩnh vực/môn học: ${err.message}`
        } finally {
          isCreating.value = false
        }
      }
      
      // Load data
      const loadData = async () => {
        try {
          // Load all data in parallel
          const [descriptionsData, majorsData] = await Promise.all([
            AdmissionDescriptionController.getAllAdmissionDescriptions(),
            MajorController.getAllMajors()
          ])
          
          existingDescriptions.value = descriptionsData
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
        isDuplicate,
        resetForm,
        createAdmissionDescription
      }
    }
  }
  </script>
  
  <style scoped>
  .admin-admission-description-create {
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