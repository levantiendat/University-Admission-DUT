<template>
    <div class="admin-subject-create">
      <div class="admin-page-header">
        <div class="d-flex align-items-center">
          <router-link to="/admins/subjects" class="btn-back">
            <i class="bi bi-arrow-left"></i>
          </router-link>
          <div>
            <h2 class="admin-page-title">Tạo môn thi mới</h2>
            <p class="admin-page-description">Thêm môn thi mới vào hệ thống</p>
          </div>
        </div>
      </div>
  
      <div class="admin-card">
        <form @submit.prevent="createSubject" class="create-form">
          <div class="form-group">
            <label for="name">Tên môn thi <span class="required">*</span></label>
            <input 
              type="text" 
              id="name" 
              v-model="formData.name" 
              class="form-control" 
              required
              :class="{ 'is-invalid': errors.name }"
              placeholder="Ví dụ: Toán, Ngữ Văn, Tiếng Anh..."
            >
            <div v-if="errors.name" class="invalid-feedback">{{ errors.name }}</div>
          </div>
  
          <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>
  
          <div class="form-actions">
            <button type="submit" class="btn-create" :disabled="isCreating">
              <i class="bi bi-plus-circle me-2"></i>
              {{ isCreating ? 'Đang tạo...' : 'Tạo môn thi' }}
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
  import { reactive, ref } from 'vue'
  import { useRouter } from 'vue-router'
  import SubjectController from '@/controllers/admins/SubjectController'
  
  export default {
    name: 'AdminSubjectCreate',
    setup() {
      const router = useRouter()
      const formData = reactive({
        name: ''
      })
      
      const isCreating = ref(false)
      const errorMessage = ref('')
      const errors = reactive({
        name: ''
      })
  
      // Reset form
      const resetForm = () => {
        formData.name = ''
        
        // Clear errors
        errors.name = ''
        errorMessage.value = ''
      }
  
      // Validate form
      const validateForm = () => {
        let isValid = true
        
        // Name validation
        if (!formData.name.trim()) {
          errors.name = 'Tên môn thi không được để trống'
          isValid = false
        }
        
        return isValid
      }
  
      // Create subject
      const createSubject = async () => {
        try {
          // Validate form
          if (!validateForm()) {
            return
          }
          
          isCreating.value = true
          errorMessage.value = ''
          
          await SubjectController.createSubject(formData)
          
          alert('Tạo môn thi mới thành công')
          router.push('/admins/subjects')
        } catch (err) {
          errorMessage.value = `Không thể tạo môn thi: ${err.message}`
        } finally {
          isCreating.value = false
        }
      }
  
      return {
        formData,
        isCreating,
        errorMessage,
        errors,
        resetForm,
        createSubject
      }
    }
  }
  </script>
  
  <style scoped>
  .admin-subject-create {
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
    max-width: 700px;
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
  
  @media (max-width: 768px) {
    .form-actions {
      flex-direction: column;
    }
    
    .btn-create, .btn-reset {
      width: 100%;
    }
  }
  </style>