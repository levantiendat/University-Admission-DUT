<template>
    <div class="qa-container">
      <h1 class="qa-title">Q&A - Câu hỏi và giải đáp</h1>
      
      <div class="qa-actions">
        <button @click="navigateToCreate" class="create-btn">
          <i class="fas fa-plus"></i> Create new question
        </button>
      </div>
  
      <div class="qa-list">
        <div v-if="loading" class="loading">
          <div class="spinner"></div>
          <p>Đang tải dữ liệu...</p>
        </div>
        <div v-else-if="error" class="error-message">
          {{ error }}
        </div>
        <div v-else-if="questions.length === 0" class="no-data">
          Chưa có câu hỏi nào. Hãy tạo câu hỏi đầu tiên!
        </div>
        <div v-else class="question-items">
          <div 
            v-for="question in questions" 
            :key="question.id"
            class="question-item"
            @click="viewQuestionDetail(question.id)"
          >
            <div class="question-content">
              <h3 class="question-title">{{ question.title }}</h3>
              <p class="question-info">
                <span 
                  class="question-author"
                  :class="{ 'expert-author': isExpert(question.user.role) }"
                >
                  {{ question.user.name }}
                  <span v-if="isExpert(question.user.role)" class="expert-label">Expert</span>
                </span>
                <span class="question-date">{{ formatDate(question.created_at) }}</span>
              </p>
            </div>
            <div class="question-arrow">
              <i class="fas fa-chevron-right"></i>
            </div>
          </div>
        </div>
      </div>
  
      <button @click="navigateToCreate" class="floating-create-btn">
        <i class="bi bi-plus-lg"></i>
      </button>
    </div>
  </template>
  
  <script>
  import qnaListController from '@/controllers/qnaListController'
  import userController from '@/controllers/userController'
  
  export default {
    name: 'QAList',
    data() {
      return {
        questions: [],
        loading: true,
        error: null,
        currentUser: null
      }
    },
    async created() {
      try {
        // Lấy thông tin người dùng hiện tại từ API
        this.currentUser = await userController.getCurrentUser()
        
        // Lấy danh sách câu hỏi
        this.questions = await qnaListController.getQuestions()
        this.loading = false
      } catch (error) {
        if (error.response && error.response.status === 401) {
          this.error = 'Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.'
          // Redirect to login page
          setTimeout(() => {
            this.$router.push({ name: 'Login' })
          }, 2000)
        } else {
          this.error = 'Không thể tải danh sách câu hỏi. Vui lòng thử lại sau.'
        }
        this.loading = false
        console.error('Error in QAList component:', error)
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
      viewQuestionDetail(questionId) {
        this.$router.push({ name: 'QADetail', params: { question_id: questionId } })
      },
      navigateToCreate() {
        this.$router.push({ name: 'QACreate' })
      }
    }
  }
  </script>
  
  <style scoped>
  .qa-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
    position: relative;
    min-height: 80vh;
  }
  
  .qa-title {
    color: #0056b3;
    font-size: 2rem;
    margin-bottom: 1.5rem;
    text-align: center;
  }
  
  .qa-actions {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 1.5rem;
  }
  
  .create-btn {
    background-color: #0056b3;
    color: white;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 4px;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.3s;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .create-btn:hover {
    background-color: #003d82;
  }
  
  .qa-list {
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 1rem;
  }
  
  .question-items {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .question-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    border-radius: 6px;
    background: #f8f9fa;
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s;
  }
  
  .question-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    background-color: #e9f0f8;
  }
  
  .question-content {
    flex: 1;
  }
  
  .question-title {
    color: #0056b3;
    margin-bottom: 0.5rem;
    font-size: 1.2rem;
  }
  
  .question-info {
    display: flex;
    gap: 1rem;
    align-items: center;
    color: #6c757d;
    font-size: 0.9rem;
  }
  
  .question-author {
    font-weight: 600;
    color: #0056b3;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .question-author.expert-author {
    color: #856404;
  }
  
  .expert-label {
    background-color: #ffd700;
    color: #000;
    font-size: 0.7rem;
    padding: 0.1rem 0.3rem;
    border-radius: 3px;
    font-weight: bold;
  }
  
  .question-arrow {
    color: #0056b3;
  }
  
  .floating-create-btn {
    position: fixed;
    bottom: 2rem;
    right: 2rem;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background-color: #0056b3;
    color: white;
    border: none;
    font-size: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 10px rgba(0, 86, 179, 0.3);
    cursor: pointer;
    transition: transform 0.2s, background-color 0.3s;
  }
  
  .floating-create-btn:hover {
    transform: scale(1.05);
    background-color: #003d82;
  }
  
  .loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
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
  }
  
  .no-data {
    text-align: center;
    color: #6c757d;
    padding: 2rem;
  }
  </style>