<template>
    <div class="admin-qna-edit">
      <div class="admin-page-header">
        <div class="d-flex align-items-center">
          <router-link :to="`/admins/qna/${questionId}`" class="btn-back">
            <i class="bi bi-arrow-left"></i>
          </router-link>
          <div>
            <h2 class="admin-page-title">Chỉnh sửa câu hỏi</h2>
            <p class="admin-page-description">Cập nhật thông tin câu hỏi</p>
          </div>
        </div>
      </div>
  
      <!-- Loading Indicator -->
      <div v-if="loading" class="loading-container">
        <div class="spinner">
          <div class="bounce1"></div>
          <div class="bounce2"></div>
          <div class="bounce3"></div>
        </div>
        <p class="loading-text">Đang tải thông tin câu hỏi...</p>
      </div>
  
      <!-- Error Message -->
      <div v-else-if="error" class="error-message">
        <i class="bi bi-exclamation-triangle-fill error-icon"></i>
        <span>{{ error }}</span>
      </div>
  
      <!-- Access Denied Message -->
      <div v-else-if="!canEditQuestion" class="access-denied">
        <i class="bi bi-shield-lock error-icon"></i>
        <h4>Không có quyền chỉnh sửa</h4>
        <p>Bạn chỉ có thể chỉnh sửa câu hỏi do chính mình tạo ra.</p>
        <router-link :to="`/admins/qna/${questionId}`" class="btn-back-link">
          <i class="bi bi-arrow-left me-2"></i> Quay lại chi tiết câu hỏi
        </router-link>
      </div>
  
      <div v-else class="admin-card">
        <form @submit.prevent="updateQuestion" class="question-form">
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
  
          <div class="meta-info">
            <div class="meta-item">
              <span class="meta-label">Người tạo:</span>
              <span class="meta-value">{{ question.user?.name || 'N/A' }}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">Ngày tạo:</span>
              <span class="meta-value">{{ formatDate(question.created_at) }}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">Cập nhật:</span>
              <span class="meta-value">{{ formatDate(question.updated_at) }}</span>
            </div>
          </div>
  
          <div v-if="submitError" class="alert alert-danger">
            <i class="bi bi-exclamation-triangle-fill me-2"></i>
            {{ submitError }}
          </div>
  
          <div class="form-actions">
            <button type="submit" class="btn-save" :disabled="isSubmitting">
              <i class="bi bi-check-circle me-2"></i>
              {{ isSubmitting ? 'Đang lưu...' : 'Lưu thay đổi' }}
            </button>
            <router-link :to="`/admins/qna/${questionId}`" class="btn-cancel">
              <i class="bi bi-x-circle me-2"></i>
              Hủy
            </router-link>
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, reactive, computed, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import QnaController from '@/controllers/admins/qnaController'
  
  export default {
    name: 'AdminQnaEdit',
    props: {
      questionId: {
        type: [String, Number],
        required: true
      }
    },
    setup(props) {
      const router = useRouter()
      const question = ref({})
      const loading = ref(true)
      const error = ref(null)
      
      // Lấy thông tin người dùng hiện tại từ session storage
      const currentUser = {
        id: parseInt(sessionStorage.getItem('userId') || '0'),
        role: sessionStorage.getItem('userRole') || 'admin',
        email: sessionStorage.getItem('userEmail') || ''
      }
      
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
      
      // Check if current user can edit the question
      const canEditQuestion = computed(() => {
        // Admin chỉ có thể edit câu hỏi do chính mình tạo ra
        return question.value && 
               question.value.user && 
               (question.value.user.id === currentUser.id && 
                question.value.user.role === 'admin')
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
      
      // Load question data
      const loadQuestionData = async () => {
        try {
          loading.value = true
          error.value = null
          
          const questionData = await QnaController.getQuestionById(props.questionId)
          question.value = questionData
          
          // Set form data
          formData.title = questionData.title
          formData.body_text = questionData.body_text
          
        } catch (err) {
          error.value = `Không thể tải thông tin câu hỏi: ${err.message}`
        } finally {
          loading.value = false
        }
      }
  
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
  
      const updateQuestion = async () => {
        if (!validateForm()) {
          return
        }
        
        // Check if user has permission
        if (!canEditQuestion.value) {
          submitError.value = 'Bạn không có quyền chỉnh sửa câu hỏi này'
          return
        }
  
        try {
          isSubmitting.value = true
          
          await QnaController.updateQuestion(props.questionId, {
            title: formData.title.trim(),
            body_text: formData.body_text.trim()
          })
          
          alert('Cập nhật câu hỏi thành công!')
          router.push(`/admins/qna/${props.questionId}`)
        } catch (error) {
          submitError.value = error.message
        } finally {
          isSubmitting.value = false
        }
      }
      
      onMounted(() => {
        loadQuestionData()
      })
  
      return {
        question,
        formData,
        errors,
        loading,
        error,
        isSubmitting,
        submitError,
        canEditQuestion,
        formatDate,
        updateQuestion
      }
    }
  }
  </script>
  
  <style scoped>
  .admin-qna-edit {
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
  
  .meta-info {
    margin: 1.5rem 0;
    padding: 1rem;
    background-color: #f8f9fa;
    border-radius: 8px;
  }
  
  .meta-item {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.5rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #e9ecef;
  }
  
  .meta-item:last-child {
    margin-bottom: 0;
    padding-bottom: 0;
    border-bottom: none;
  }
  
  .meta-label {
    font-weight: 500;
    color: #6c757d;
  }
  
  .meta-value {
    color: #0B2942;
    font-weight: 500;
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
  .error-message, .access-denied {
    background-color: #f8d7da;
    color: #721c24;
    padding: 2rem;
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    margin-bottom: 1.5rem;
  }
  
  .error-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
  }
  
  .access-denied {
    background-color: #f8f9fa;
    color: #212529;
  }
  
  .access-denied h4 {
    font-size: 1.25rem;
    margin-bottom: 0.5rem;
    color: #0B2942;
  }
  
  .access-denied p {
    color: #6c757d;
    margin-bottom: 1.5rem;
  }
  
  .btn-back-link {
    display: inline-flex;
    align-items: center;
    background-color: #0B2942;
    color: #fff;
    padding: 0.75rem 1.25rem;
    border-radius: 8px;
    text-decoration: none;
    transition: all 0.3s;
  }
  
  .btn-back-link:hover {
    background-color: #4da0ff;
    color: #fff;
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