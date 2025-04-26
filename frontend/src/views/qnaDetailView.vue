<template>
    <div class="qa-detail-container">
      <div class="back-link">
        <a @click="$router.push({ name: 'QAList' })">
          <i class="fas fa-arrow-left"></i> Quay lại danh sách câu hỏi
        </a>
      </div>
  
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>Đang tải dữ liệu...</p>
      </div>
      
      <div v-else-if="error" class="error-message">
        {{ error }}
      </div>
      
      <template v-else>
        <!-- Question Detail -->
        <div class="question-detail">
          <div class="question-header">
            <h1 class="question-title">{{ question.title }}</h1>
            <div class="question-meta">
              <div class="user-info">
                <span 
                  class="user-badge" 
                  :class="{ 
                    'expert-badge': isExpert(question.user.role),
                    'user-badge': !isExpert(question.user.role)
                  }"
                >
                  {{ question.user.name }}
                  <span v-if="isExpert(question.user.role)" class="expert-label">Expert</span>
                </span>
              </div>
              <div class="question-date">
                {{ formatDate(question.created_at) }}
              </div>
            </div>
          </div>
  
          <div class="question-body">
            {{ question.body_text }}
          </div>
  
          <div class="question-actions" v-if="canModifyQuestion">
            <button @click="editQuestion" class="icon-btn edit-icon-btn">
                <i class="bi bi-pencil-square"></i>
            </button>
            <button @click="deleteQuestionConfirm" class="icon-btn delete-icon-btn">
                <i class="bi bi-trash"></i>
            </button>
          </div>
        </div>
  
        <!-- Responses -->
        <div class="responses-section">
          <h2 class="responses-title">Câu trả lời ({{ responses.length }})</h2>
          
          <div v-if="responses.length === 0" class="no-responses">
            Chưa có câu trả lời nào cho câu hỏi này.
          </div>
          
          <div v-else class="responses-list">
            <div v-for="response in responses" :key="response.id" class="response-item">
              <div class="response-header">
                <div class="user-info">
                  <span 
                    class="user-badge" 
                    :class="{ 
                      'expert-badge': isExpert(response.user.role),
                      'user-badge': !isExpert(response.user.role)
                    }"
                  >
                    {{ response.user.name }}
                    <span v-if="isExpert(response.user.role)" class="expert-label">Expert</span>
                  </span>
                </div>
                <div class="response-date">
                  {{ formatDate(response.created_at) }}
                </div>
              </div>
              
              <div class="response-body">
                {{ response.body_text }}
              </div>
              
              <div class="response-actions" v-if="canModifyResponse(response)">
                <button @click="editResponse(response)" class="icon-btn edit-icon-btn">
                    <i class="bi bi-pencil-square"></i>
                </button>
                <button @click="deleteResponseConfirm(response.id)" class="icon-btn delete-icon-btn">
                    <i class="bi bi-trash"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Add New Response -->
        <div class="add-response-section">
          <h3 class="add-response-title">Thêm câu trả lời</h3>
          
          <div class="response-form">
            <textarea 
              v-model="newResponse" 
              placeholder="Nhập câu trả lời của bạn..."
              rows="4"
              class="response-textarea"
            ></textarea>
            
            <div class="form-actions">
              <button @click="submitResponse" :disabled="!newResponse.trim()" class="submit-btn">
                Gửi câu trả lời
              </button>
            </div>
          </div>
        </div>
  
        <!-- Edit Response Modal -->
        <div v-if="showEditResponseModal" class="modal-overlay">
          <div class="modal-content">
            <h3 class="modal-title">Chỉnh sửa câu trả lời</h3>
            
            <div class="modal-body">
              <textarea 
                v-model="editResponseText" 
                class="response-textarea"
                rows="4"
              ></textarea>
            </div>
            
            <div class="modal-actions">
              <button @click="cancelEditResponse" class="cancel-btn">
                Hủy
              </button>
              <button @click="saveEditResponse" :disabled="!editResponseText.trim()" class="submit-btn">
                Lưu
              </button>
            </div>
          </div>
        </div>
      </template>
    </div>
  </template>
  
  <script>
  import qnaDetailController from '@/controllers/qnaDetailController'
  import userController from '@/controllers/userController'
  
  export default {
    name: 'QADetail',
    data() {
      return {
        question: {},
        responses: [],
        loading: true,
        error: null,
        currentUser: null,
        newResponse: '',
        editingResponseId: null,
        editResponseText: '',
        showEditResponseModal: false
      }
    },
    computed: {
      canModifyQuestion() {
        if (!this.currentUser || !this.question.user) return false
        return this.currentUser.id === this.question.user.id
      }
    },
    async created() {
      try {
        // Lấy thông tin người dùng hiện tại từ API
        this.currentUser = await userController.getCurrentUser()
        
        const questionId = this.$route.params.question_id
        
        // Lấy chi tiết câu hỏi
        this.question = await qnaDetailController.getQuestionDetail(questionId)
        
        // Lấy các responses của câu hỏi
        this.responses = await qnaDetailController.getResponses(questionId)
        
        this.loading = false
      } catch (error) {
        if (error.response && error.response.status === 401) {
          this.error = 'Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.'
          // Redirect to login page
          setTimeout(() => {
            this.$router.push({ name: 'Login' })
          }, 2000)
        } else {
          this.error = 'Không thể tải thông tin câu hỏi. Vui lòng thử lại sau.'
        }
        this.loading = false
        console.error('Error in QADetail component:', error)
      }
    },
    methods: {
      formatDate(dateString) {
        const date = new Date(dateString)
        return new Intl.DateTimeFormat('vi-VN', {
          day: '2-digit',
          month: '2-digit',
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        }).format(date)
      },
      isExpert(role) {
        return role === 'instructor' || role === 'admin'
      },
      canModifyResponse(response) {
        if (!this.currentUser || !response.user) return false
        return this.currentUser.id === response.user.id
      },
      async submitResponse() {
        if (!this.newResponse.trim()) return
        
        try {
          const responseData = {
            body_text: this.newResponse.trim(),
            question_id: this.question.id
          }
          
          await qnaDetailController.createResponse(responseData)
          
          // Refresh responses
          this.responses = await qnaDetailController.getResponses(this.question.id)
          this.newResponse = ''
        } catch (error) {
          alert('Không thể gửi câu trả lời. Vui lòng thử lại sau.')
          console.error('Error submitting response:', error)
        }
      },
      editQuestion() {
        this.$router.push({ 
          name: 'QAUpdate', 
          params: { question_id: this.question.id } 
        })
      },
      async deleteQuestionConfirm() {
        if (confirm('Bạn có chắc chắn muốn xóa câu hỏi này không?')) {
          try {
            await qnaDetailController.deleteQuestion(this.question.id)
            this.$router.push({ name: 'QAList' })
          } catch (error) {
            alert('Không thể xóa câu hỏi. Vui lòng thử lại sau.')
            console.error('Error deleting question:', error)
          }
        }
      },
      editResponse(response) {
        this.editingResponseId = response.id
        this.editResponseText = response.body_text
        this.showEditResponseModal = true
      },
      async deleteResponseConfirm(responseId) {
        if (confirm('Bạn có chắc chắn muốn xóa câu trả lời này không?')) {
          try {
            await qnaDetailController.deleteResponse(responseId)
            // Refresh responses
            this.responses = await qnaDetailController.getResponses(this.question.id)
          } catch (error) {
            alert('Không thể xóa câu trả lời. Vui lòng thử lại sau.')
            console.error('Error deleting response:', error)
          }
        }
      },
      cancelEditResponse() {
        this.showEditResponseModal = false
        this.editingResponseId = null
        this.editResponseText = ''
      },
      async saveEditResponse() {
        if (!this.editResponseText.trim()) return
        
        try {
          const responseData = {
            body_text: this.editResponseText.trim(),
            question_id: this.question.id
          }
          
          await qnaDetailController.updateResponse(this.editingResponseId, responseData)
          
          // Refresh responses
          this.responses = await qnaDetailController.getResponses(this.question.id)
          this.cancelEditResponse()
        } catch (error) {
          alert('Không thể cập nhật câu trả lời. Vui lòng thử lại sau.')
          console.error('Error updating response:', error)
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .qa-detail-container {
    max-width: 1000px;
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
  
  .question-detail {
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 1.5rem;
    margin-bottom: 2rem;
    position: relative;
  }
  
  .question-header {
    margin-bottom: 1rem;
  }
  
  .question-title {
    color: #0056b3;
    font-size: 1.8rem;
    margin-bottom: 0.75rem;
  }
  
  .question-meta {
    display: flex;
    justify-content: space-between;
    margin-bottom: 1rem;
  }
  
  .user-badge {
    display: inline-flex;
    align-items: center;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-weight: 600;
  }
  
  .user-badge.expert-badge {
    background-color: #ffd700;
    color: #000;
  }
  
  .user-badge:not(.expert-badge) {
    background-color: #0056b3;
    color: white;
  }
  
  .expert-label {
    margin-left: 0.5rem;
    font-size: 0.8rem;
    padding: 0.1rem 0.4rem;
    border-radius: 10px;
    background-color: #ffffff;
    color: #000;
  }
  
  .question-date {
    color: #6c757d;
    font-size: 0.9rem;
  }
  
  .question-body {
    font-size: 1.1rem;
    line-height: 1.6;
    color: #333;
    white-space: pre-line;
  }
  
  .question-actions {
    position: absolute;
    top: 1.5rem;
    right: 1.5rem;
    display: flex;
    gap: 0.75rem;
  }
  
  .icon-btn {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border: none;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: transform 0.2s, opacity 0.2s;
  }
  
  .icon-btn:hover {
    transform: scale(1.1);
  }
  
  .edit-icon-btn {
    background-color: #0056b3;
    color: white;
  }
  
  .edit-icon-btn:hover {
    background-color: #003d82;
  }
  
  .delete-icon-btn {
    background-color: #dc3545;
    color: white;
  }
  
  .delete-icon-btn:hover {
    background-color: #bd2130;
  }
  
  .responses-section {
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 1.5rem;
    margin-bottom: 2rem;
  }
  
  .responses-title {
    color: #0056b3;
    font-size: 1.4rem;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #e9ecef;
  }
  
  .no-responses {
    text-align: center;
    color: #6c757d;
    padding: 1.5rem;
  }
  
  .responses-list {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }
  
  .response-item {
    padding: 1rem;
    border-radius: 6px;
    background: #f8f9fa;
    position: relative;
  }
  
  .response-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.75rem;
  }
  
  .response-body {
    font-size: 1rem;
    line-height: 1.5;
    color: #333;
    white-space: pre-line;
  }
  
  .response-actions {
    position: absolute;
    top: 3rem;
    right: 1rem;
    display: flex;
    gap: 0.5rem;
  }
  
  .add-response-section {
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 1.5rem;
  }
  
  .add-response-title {
    color: #0056b3;
    font-size: 1.2rem;
    margin-bottom: 1rem;
  }
  
  .response-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .response-textarea {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #ced4da;
    border-radius: 4px;
    font-family: inherit;
    font-size: 1rem;
    resize: vertical;
  }
  
  .response-textarea:focus {
    border-color: #0056b3;
    outline: none;
    box-shadow: 0 0 0 2px rgba(0, 86, 179, 0.25);
  }
  
  .form-actions {
    display: flex;
    justify-content: flex-end;
  }
  
  .submit-btn, .edit-btn, .delete-btn, .cancel-btn {
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
  
  /* Modal styles */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  
  .modal-content {
    background-color: white;
    border-radius: 8px;
    width: 90%;
    max-width: 600px;
    padding: 2rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  }
  
  .modal-title {
    color: #0056b3;
    margin-bottom: 1.5rem;
  }
  
  .modal-body {
    margin-bottom: 1.5rem;
  }
  
  .modal-actions {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
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