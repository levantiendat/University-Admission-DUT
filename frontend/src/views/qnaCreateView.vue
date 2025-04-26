<template>
    <div class="qa-create-container">
      <div class="back-link">
        <a @click="$router.push({ name: 'QAList' })">
          <i class="fas fa-arrow-left"></i> Quay lại danh sách câu hỏi
        </a>
      </div>
  
      <h1 class="page-title">
        {{ isUpdateMode ? 'Cập nhật câu hỏi' : 'Tạo câu hỏi mới' }}
      </h1>
  
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>Đang tải dữ liệu...</p>
      </div>
      
      <div v-else-if="error" class="error-message">
        {{ error }}
      </div>
      
      <form v-else @submit.prevent="handleSubmit" class="question-form">
        <div class="form-group">
          <label for="question-title">Tiêu đề câu hỏi</label>
          <input
            id="question-title"
            v-model="form.title"
            type="text"
            class="form-control"
            placeholder="Nhập tiêu đề câu hỏi"
            required
          />
        </div>
        
        <div class="form-group">
          <label for="question-body">Nội dung câu hỏi</label>
          <textarea
            id="question-body"
            v-model="form.body_text"
            class="form-control"
            placeholder="Nhập nội dung chi tiết của câu hỏi..."
            rows="6"
            required
          ></textarea>
        </div>
        
        <div class="form-actions">
          <button 
            type="button" 
            @click="cancel" 
            class="cancel-btn"
          >
            Hủy
          </button>
          <button 
            type="submit" 
            class="submit-btn"
            :disabled="isSubmitting"
          >
            {{ isSubmitting ? 'Đang xử lý...' : (isUpdateMode ? 'Cập nhật' : 'Gửi câu hỏi') }}
          </button>
        </div>
      </form>
    </div>
  </template>
  
  <script>
  import qnaCreateController from '@/controllers/qnaCreateController'
  import userController from '@/controllers/userController'
  
  export default {
    name: 'QACreate',
    data() {
      return {
        form: {
          title: '',
          body_text: ''
        },
        loading: false,
        error: null,
        isSubmitting: false,
        questionId: null,
        isUpdateMode: false,
        currentUser: null
      }
    },
    async created() {
      this.loading = true;
      
      try {
        // Lấy thông tin người dùng hiện tại từ API
        this.currentUser = await userController.getCurrentUser()
        
        // Kiểm tra có phải là chế độ update không
        if (this.$route.name === 'QAUpdate') {
          this.questionId = this.$route.params.question_id
          this.isUpdateMode = true
          
          try {
            // Lấy thông tin câu hỏi cần cập nhật
            const question = await qnaCreateController.getQuestionForUpdate(this.questionId)
            
            // Kiểm tra quyền chỉnh sửa
            if (question.user.id !== this.currentUser.id) {
              this.error = 'Bạn không có quyền chỉnh sửa câu hỏi này.'
              setTimeout(() => {
                this.$router.push({ name: 'QADetail', params: { question_id: this.questionId } })
              }, 2000)
              return
            }
            
            this.form.title = question.title
            this.form.body_text = question.body_text
          } catch (error) {
            this.error = 'Không thể tải thông tin câu hỏi. Vui lòng thử lại sau.'
            console.error('Error fetching question for update:', error)
          }
        }
      } catch (error) {
        if (error.response && error.response.status === 401) {
          this.error = 'Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.'
          // Redirect to login page
          setTimeout(() => {
            this.$router.push({ name: 'Login' })
          }, 2000)
        } else {
          this.error = 'Có lỗi xảy ra. Vui lòng thử lại sau.'
        }
        console.error('Error in QACreate component:', error)
      } finally {
        this.loading = false
      }
    },
    methods: {
      async handleSubmit() {
        if (!this.form.title.trim() || !this.form.body_text.trim()) return
        
        this.isSubmitting = true
        
        try {
          if (this.isUpdateMode) {
            // Cập nhật câu hỏi
            await qnaCreateController.updateQuestion(this.questionId, this.form)
            this.$router.push({ name: 'QADetail', params: { question_id: this.questionId } })
          } else {
            // Tạo câu hỏi mới
            const newQuestion = await qnaCreateController.createQuestion(this.form)
            this.$router.push({ name: 'QADetail', params: { question_id: newQuestion.id } })
          }
        } catch (error) {
          const action = this.isUpdateMode ? 'cập nhật' : 'tạo'
          alert(`Không thể ${action} câu hỏi. Vui lòng thử lại sau.`)
          console.error(`Error ${this.isUpdateMode ? 'updating' : 'creating'} question:`, error)
        } finally {
          this.isSubmitting = false
        }
      },
      cancel() {
        if (this.isUpdateMode && this.questionId) {
          this.$router.push({ name: 'QADetail', params: { question_id: this.questionId } })
        } else {
          this.$router.push({ name: 'QAList' })
        }
      }
    }
  }
  </script>
  
  <style scoped>
  /* Giữ nguyên CSS như trong file gốc */
  </style>
  
  <style scoped>
  .qa-create-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
  }
  
  .back-link {
    margin-bottom: 1.5rem;
  }
  
  .back-link a {
    color: #0056b3;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 500;
    cursor: pointer;
    text-decoration: none;
  }
  
  .back-link a:hover {
    text-decoration: underline;
  }
  
  .page-title {
    color: #0056b3;
    font-size: 1.8rem;
    margin-bottom: 1.5rem;
    text-align: center;
  }
  
  .question-form {
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 2rem;
  }
  
  .form-group {
    margin-bottom: 1.5rem;
  }
  
  .form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 600;
    color: #333;
  }
  
  .form-control {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #ced4da;
    border-radius: 4px;
    font-family: inherit;
    font-size: 1rem;
  }
  
  .form-control:focus {
    border-color: #0056b3;
    outline: none;
    box-shadow: 0 0 0 2px rgba(0, 86, 179, 0.25);
  }
  
  textarea.form-control {
    resize: vertical;
  }
  
  .form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    margin-top: 2rem;
  }
  
  .submit-btn, .cancel-btn {
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 4px;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .submit-btn {
    background-color: #0056b3;
    color: white;
  }
  
  .submit-btn:hover {
    background-color: #003d82;
  }
  
  .submit-btn:disabled {
    background-color: #6c757d;
    cursor: not-allowed;
  }
  
  .cancel-btn {
    background-color: #6c757d;
    color: white;
  }
  
  .cancel-btn:hover {
    background-color: #5a6268;
  }
  
  /* Loading and Error styles */
  .loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem;
  }
  
  .spinner {
    border: 4px solid #f3f3f3;
    border-top: 4px solid #0056b3;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    margin-bottom: 1rem;
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  
  .error-message {
    color: #dc3545;
    text-align: center;
    padding: 2rem;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }
  </style>