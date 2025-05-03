<template>
    <div class="admin-qna-create">
      <div class="admin-page-header">
        <div class="d-flex align-items-center">
          <router-link to="/admins/qna" class="btn-back">
            <i class="bi bi-arrow-left"></i>
          </router-link>
          <div>
            <h2 class="admin-page-title">Tạo câu hỏi mới</h2>
            <p class="admin-page-description">Tạo câu hỏi mới trong hệ thống hỏi đáp</p>
          </div>
        </div>
      </div>
  
      <div class="admin-card">
        <form @submit.prevent="createQuestion" class="question-form">
          <div class="form-group">
            <label for="title">Tiêu đề câu hỏi <span class="required">*</span></label>
            <input 
              type="text" 
              id="title" 
              v-model="formData.title" 
              class="form-control" 
              :class="{ 'is-invalid': errors.title }"
              placeholder="Nhập tiêu đề câu hỏi" 
              required
            >
            <div v-if="errors.title" class="invalid-feedback">
              {{ errors.title }}
            </div>
          </div>
  
          <div class="form-group">
            <label for="body_text">Nội dung câu hỏi <span class="required">*</span></label>
            <textarea 
              id="body_text" 
              v-model="formData.body_text" 
              class="form-control" 
              :class="{ 'is-invalid': errors.body_text }" 
              placeholder="Nhập nội dung chi tiết câu hỏi" 
              rows="6"
              required
            ></textarea>
            <div v-if="errors.body_text" class="invalid-feedback">
              {{ errors.body_text }}
            </div>
          </div>
  
          <div class="alert alert-info" role="alert">
            <i class="bi bi-info-circle me-2"></i>
            <span>Câu hỏi sẽ được đăng với tư cách người quản trị.</span>
          </div>
  
          <div v-if="submitError" class="alert alert-danger">
            <i class="bi bi-exclamation-triangle-fill me-2"></i>
            {{ submitError }}
          </div>
  
          <div class="form-actions">
            <button type="submit" class="btn-save" :disabled="isSubmitting">
              <i class="bi bi-check-circle me-2"></i>
              {{ isSubmitting ? 'Đang tạo...' : 'Tạo câu hỏi' }}
            </button>
            <router-link to="/admins/qna" class="btn-cancel">
              <i class="bi bi-x-circle me-2"></i>
              Hủy
            </router-link>
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, reactive } from 'vue'
  import { useRouter } from 'vue-router'
  import QnaController from '@/controllers/admins/qnaController'
  
  export default {
    name: 'AdminQnaCreate',
    setup() {
      const router = useRouter()
      const formData = reactive({
        title: '',
        body_text: ''
      })
  
      const errors = reactive({
        title: '',
        body_text: ''
      })
  
      const isSubmitting = ref(false)
      const submitError = ref('')
  
      const validateForm = () => {
        let isValid = true
        
        // Reset errors
        errors.title = ''
        errors.body_text = ''
        submitError.value = ''
  
        // Validate title
        if (!formData.title || formData.title.trim() === '') {
          errors.title = 'Vui lòng nhập tiêu đề câu hỏi'
          isValid = false
        }
  
        // Validate body_text
        if (!formData.body_text || formData.body_text.trim() === '') {
          errors.body_text = 'Vui lòng nhập nội dung câu hỏi'
          isValid = false
        }
  
        return isValid
      }
  
      const createQuestion = async () => {
        if (!validateForm()) {
          return
        }
  
        try {
          isSubmitting.value = true
          
          const newQuestion = await QnaController.createQuestion({
            title: formData.title.trim(),
            body_text: formData.body_text.trim()
          })
          
          alert('Tạo câu hỏi thành công!')
          router.push(`/admins/qna/${newQuestion.id}`)
        } catch (error) {
          submitError.value = error.message
        } finally {
          isSubmitting.value = false
        }
      }
  
      return {
        formData,
        errors,
        isSubmitting,
        submitError,
        createQuestion
      }
    }
  }
  </script>
  
  <style scoped>
  .admin-qna-create {
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
    transition: all 0.3s ease;
  }
  
  .admin-card:hover {
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
  }
  
  .question-form {
    max-width: 800px;
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
    cursor: pointer;
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
    text-decoration: none;
  }
  
  .btn-cancel:hover {
    background-color: #e9ecef;
    color: #0B2942;
  }
  
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
    background-color: #e1f5fe;
    color: #0c5460;
    border: 1px solid #bee5eb;
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