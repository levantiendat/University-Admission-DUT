<template>
    <div class="admin-user-create">
      <div class="admin-page-header">
        <div class="d-flex align-items-center">
          <router-link to="/admins/users" class="btn-back">
            <i class="bi bi-arrow-left"></i>
          </router-link>
          <div>
            <h2 class="admin-page-title">Tạo người dùng mới</h2>
            <p class="admin-page-description">Thêm người dùng mới vào hệ thống</p>
          </div>
        </div>
      </div>
  
      <div class="admin-card">
        <form @submit.prevent="createUser" class="create-form">
          <div class="form-group">
            <label for="name">Họ tên <span class="required">*</span></label>
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
            <label for="email">Email <span class="required">*</span></label>
            <input 
              type="email" 
              id="email" 
              v-model="formData.email" 
              class="form-control" 
              required
              :class="{ 'is-invalid': errors.email }"
            >
            <div v-if="errors.email" class="invalid-feedback">{{ errors.email }}</div>
          </div>
  
          <div class="form-group">
            <label for="phone_number">Số điện thoại <span class="required">*</span></label>
            <input 
              type="text" 
              id="phone_number" 
              v-model="formData.phone_number" 
              class="form-control" 
              required
              :class="{ 'is-invalid': errors.phone_number }"
            >
            <div v-if="errors.phone_number" class="invalid-feedback">{{ errors.phone_number }}</div>
          </div>
  
          <div class="form-group">
            <label for="password">Mật khẩu <span class="required">*</span></label>
            <div class="password-input-container">
              <input 
                :type="showPassword ? 'text' : 'password'" 
                id="password" 
                v-model="formData.password" 
                class="form-control" 
                required
                :class="{ 'is-invalid': errors.password }"
              >
              <button type="button" class="btn-toggle-password" @click="togglePasswordVisibility">
                <i class="bi" :class="showPassword ? 'bi-eye-slash' : 'bi-eye'"></i>
              </button>
            </div>
            <div v-if="errors.password" class="invalid-feedback">{{ errors.password }}</div>
            <small class="form-text text-muted">Mật khẩu phải có ít nhất 6 ký tự.</small>
          </div>
  
          <div class="form-group">
            <label>Vai trò <span class="required">*</span></label>
            <div class="role-options">
              <div class="role-option">
                <input 
                  type="radio" 
                  id="role-user" 
                  name="role" 
                  value="user" 
                  v-model="selectedRole" 
                  checked
                >
                <label for="role-user" class="role-label user-role">
                  <span class="role-icon"><i class="bi bi-person"></i></span>
                  <span class="role-name">User</span>
                  <span class="role-desc">Người dùng thông thường</span>
                </label>
              </div>
              <div class="role-option">
                <input 
                  type="radio" 
                  id="role-instructor" 
                  name="role" 
                  value="instructor" 
                  v-model="selectedRole"
                >
                <label for="role-instructor" class="role-label instructor-role">
                  <span class="role-icon"><i class="bi bi-person-check"></i></span>
                  <span class="role-name">Instructor</span>
                  <span class="role-desc">Có thể trả lời câu hỏi tư vấn</span>
                </label>
              </div>
            </div>
          </div>
  
          <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>
  
          <div class="form-actions">
            <button type="submit" class="btn-create" :disabled="isCreating">
              <i class="bi bi-person-plus-fill me-2"></i>
              {{ isCreating ? 'Đang tạo...' : 'Tạo người dùng' }}
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
  import UserController from '@/controllers/admins/UserController'
  
  export default {
    name: 'AdminUserCreate',
    setup() {
      const router = useRouter()
      const formData = reactive({
        name: '',
        email: '',
        phone_number: '',
        password: ''
      })
      
      const selectedRole = ref('user')
      const showPassword = ref(false)
      const isCreating = ref(false)
      const errorMessage = ref('')
      const errors = reactive({
        name: '',
        email: '',
        phone_number: '',
        password: ''
      })
  
      // Toggle password visibility
      const togglePasswordVisibility = () => {
        showPassword.value = !showPassword.value
      }
  
      // Reset form
      const resetForm = () => {
        formData.name = ''
        formData.email = ''
        formData.phone_number = ''
        formData.password = ''
        selectedRole.value = 'user'
        
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
        
        // Name validation
        if (!formData.name.trim()) {
          errors.name = 'Họ tên không được để trống'
          isValid = false
        }
        
        // Email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
        if (!formData.email.trim()) {
          errors.email = 'Email không được để trống'
          isValid = false
        } else if (!emailRegex.test(formData.email)) {
          errors.email = 'Email không hợp lệ'
          isValid = false
        }
        
        // Phone validation
        const phoneRegex = /^[0-9]{10,12}$/
        if (!formData.phone_number.trim()) {
          errors.phone_number = 'Số điện thoại không được để trống'
          isValid = false
        } else if (!phoneRegex.test(formData.phone_number)) {
          errors.phone_number = 'Số điện thoại không hợp lệ (cần 10-12 chữ số)'
          isValid = false
        }
        
        // Password validation
        if (!formData.password) {
          errors.password = 'Mật khẩu không được để trống'
          isValid = false
        } else if (formData.password.length < 6) {
          errors.password = 'Mật khẩu phải có ít nhất 6 ký tự'
          isValid = false
        }
        
        return isValid
      }
  
      // Create user
      const createUser = async () => {
        try {
          // Validate form
          if (!validateForm()) {
            return
          }
          
          isCreating.value = true
          errorMessage.value = ''
          
          const userData = {
            name: formData.name,
            email: formData.email,
            phone_number: formData.phone_number,
            password: formData.password
          }
          
          await UserController.createUser(userData, selectedRole.value)
          
          alert('Tạo người dùng mới thành công')
          router.push('/admins/users')
        } catch (err) {
          errorMessage.value = `Không thể tạo người dùng: ${err.message}`
        } finally {
          isCreating.value = false
        }
      }
  
      return {
        formData,
        selectedRole,
        showPassword,
        isCreating,
        errorMessage,
        errors,
        togglePasswordVisibility,
        resetForm,
        createUser
      }
    }
  }
  </script>
  
  <style scoped>
  .admin-user-create {
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
  
  .form-text {
    display: block;
    margin-top: 0.5rem;
    font-size: 0.875rem;
  }
  
  /* Password Input */
  .password-input-container {
    position: relative;
  }
  
  .btn-toggle-password {
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    background: none;
    border: none;
    color: #6c757d;
    cursor: pointer;
  }
  
  .btn-toggle-password:hover {
    color: #0B2942;
  }
  
  /* Role Selection */
  .role-options {
    display: flex;
    gap: 1rem;
    margin-top: 0.5rem;
  }
  
  .role-option {
    flex: 1;
  }
  
  .role-option input[type="radio"] {
    display: none;
  }
  
  .role-label {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 1.5rem;
    border: 2px solid #e0e0e0;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s;
  }
  
  .role-icon {
    font-size: 2rem;
    margin-bottom: 1rem;
  }
  
  .role-name {
    font-weight: 600;
    font-size: 1.1rem;
    margin-bottom: 0.5rem;
  }
  
  .role-desc {
    font-size: 0.85rem;
    color: #6c757d;
    text-align: center;
  }
  
  .user-role .role-icon {
    color: #0d6efd;
  }
  
  .instructor-role .role-icon {
    color: #198754;
  }
  
  /* Selected Role */
  input[type="radio"]:checked + .role-label {
    border-color: #0B2942;
    background-color: rgba(11, 41, 66, 0.05);
  }
  
  input[type="radio"]:checked + .user-role {
    border-color: #0d6efd;
  }
  
  input[type="radio"]:checked + .instructor-role {
    border-color: #198754;
  }
  
  /* Form Actions */
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
    .role-options {
      flex-direction: column;
      gap: 1rem;
    }
  
    .form-actions {
      flex-direction: column;
    }
    
    .btn-create, .btn-reset {
      width: 100%;
    }
  }
  </style>