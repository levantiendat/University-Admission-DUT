<template>
    <div class="admin-qna-questions">
      <div class="admin-page-header d-flex justify-content-between align-items-center">
        <div>
          <h2 class="admin-page-title">Quản lý hỏi đáp (Q&A)</h2>
          <p class="admin-page-description">Danh sách câu hỏi của người dùng và phản hồi từ nhà tư vấn</p>
        </div>
        <div>
          <router-link to="/admins/qna/create" class="btn-create">
            <i class="bi bi-plus-circle me-2"></i>Tạo câu hỏi mới
          </router-link>
        </div>
      </div>
  
      <!-- Search and Filter -->
      <div class="admin-card mb-4">
        <div class="row">
          <div class="col-md-6">
            <div class="form-group">
              <label for="search-input">Tìm kiếm câu hỏi</label>
              <div class="search-box">
                <i class="bi bi-search search-icon"></i>
                <input 
                  type="text" 
                  id="search-input" 
                  v-model="searchQuery" 
                  class="search-input" 
                  placeholder="Tìm theo tiêu đề hoặc nội dung..." 
                  @input="filterQuestions"
                >
              </div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="form-group">
              <label for="role-filter">Lọc theo vai trò</label>
              <select 
                id="role-filter" 
                v-model="filters.role" 
                class="form-select" 
                @change="filterQuestions"
              >
                <option value="">Tất cả vai trò</option>
                <option value="user">Người dùng</option>
                <option value="instructor">Người hướng dẫn</option>
                <option value="admin">Quản trị viên</option>
              </select>
            </div>
          </div>
          <div class="col-md-3">
            <div class="form-group">
              <label for="sort-by">Sắp xếp theo</label>
              <select 
                id="sort-by" 
                v-model="sortBy" 
                class="form-select" 
                @change="sortQuestions"
              >
                <option value="newest">Mới nhất</option>
                <option value="oldest">Cũ nhất</option>
                <option value="title">Tiêu đề (A-Z)</option>
                <option value="title-desc">Tiêu đề (Z-A)</option>
                <option value="role">Vai trò</option>
              </select>
            </div>
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
        <p class="loading-text">Đang tải danh sách câu hỏi...</p>
      </div>
  
      <!-- Error Message -->
      <div v-else-if="error" class="error-message">
        <i class="bi bi-exclamation-triangle-fill error-icon"></i>
        <span>{{ error }}</span>
      </div>
  
      <!-- Questions List -->
      <div v-else>
        <div class="admin-card mb-3">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h3 class="section-title mb-0">Danh sách câu hỏi</h3>
            <div class="results-count">Hiển thị {{ filteredQuestions.length }} câu hỏi</div>
          </div>
        </div>
  
        <!-- Empty state -->
        <div v-if="filteredQuestions.length === 0" class="admin-card empty-state">
          <i class="bi bi-chat-left-dots empty-icon"></i>
          <h4>Không tìm thấy câu hỏi nào</h4>
          <p v-if="hasFilters">Thử điều chỉnh bộ lọc hoặc từ khóa tìm kiếm</p>
          <p v-else>Hiện chưa có câu hỏi nào trong hệ thống</p>
          <router-link to="/admins/qna/create" class="btn-create-empty">
            <i class="bi bi-plus-circle me-2"></i>Tạo câu hỏi mới
          </router-link>
        </div>
  
        <!-- Questions -->
        <div v-else class="questions-list">
          <div 
            v-for="question in filteredQuestions" 
            :key="question.id" 
            class="admin-card question-card mb-3"
          >
            <div class="d-flex justify-content-between">
              <h4 class="question-title">
                <router-link :to="`/admins/qna/${question.id}`">
                  {{ question.title }}
                </router-link>
              </h4>
              <div class="question-actions">
                <router-link :to="`/admins/qna/${question.id}/edit`" class="btn-action edit" title="Chỉnh sửa">
                  <i class="bi bi-pencil-square"></i>
                </router-link>
                <button @click="confirmDeleteQuestion(question)" class="btn-action delete" title="Xóa">
                  <i class="bi bi-trash"></i>
                </button>
              </div>
            </div>
            <div class="question-content">{{ truncateText(question.body_text, 200) }}</div>
            <div class="question-meta">
              <div class="question-user">
                <span 
                  :class="['user-role-badge', getRoleBadgeClass(question.user.role)]"
                  :title="getRoleTitle(question.user.role)"
                >
                  {{ question.user.role }}
                </span>
                <span class="user-name">{{ question.user.name }}</span>
              </div>
              <div class="question-date">
                {{ formatDate(question.created_at) }}
              </div>
            </div>
            <div class="question-stats">
              <router-link :to="`/admins/qna/${question.id}`" class="view-responses">
                <i class="bi bi-chat-dots me-1"></i> Xem phản hồi
              </router-link>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Delete Question Confirmation Modal -->
      <div v-if="showDeleteModal" class="modal-overlay" @click="cancelDelete">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h4 class="modal-title">Xác nhận xóa câu hỏi</h4>
            <button type="button" class="btn-close" @click="cancelDelete"></button>
          </div>
          <div class="modal-body">
            <p>Bạn có chắc chắn muốn xóa câu hỏi <strong>"{{ questionToDelete?.title }}"</strong>?</p>
            <p class="text-warning">
              <i class="bi bi-exclamation-triangle me-2"></i>
              Việc xóa câu hỏi sẽ xóa tất cả câu trả lời liên quan!
            </p>
            <p class="text-danger">
              <i class="bi bi-exclamation-triangle me-2"></i>
              Thao tác này không thể khôi phục lại!
            </p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn-cancel" @click="cancelDelete">Hủy</button>
            <button type="button" class="btn-delete" @click="deleteQuestion" :disabled="isDeleting">
              <span v-if="isDeleting">Đang xóa...</span>
              <span v-else>Xác nhận xóa</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, reactive, computed, onMounted } from 'vue'
  import QnaController from '@/controllers/admins/qnaController'
  
  export default {
    name: 'AdminQnaQuestions',
    setup() {
      const loading = ref(true)
      const error = ref(null)
      const questions = ref([])
      const filteredQuestions = ref([])
      const searchQuery = ref('')
      const sortBy = ref('newest')
      const filters = reactive({
        role: ''
      })
      
      // Delete modal
      const showDeleteModal = ref(false)
      const questionToDelete = ref(null)
      const isDeleting = ref(false)
  
      // Check if any filters are applied
      const hasFilters = computed(() => {
        return searchQuery.value || filters.role
      })
  
      // Load questions
      const loadQuestions = async () => {
        try {
          loading.value = true
          error.value = null
          
          const questionsData = await QnaController.getAllQuestions()
          questions.value = questionsData
          
          // Sửa lỗi: Khởi tạo filteredQuestions ban đầu với tất cả câu hỏi
          filteredQuestions.value = [...questionsData]
          
          // Initial sort by newest
          sortQuestions()
          
        } catch (err) {
          error.value = `Không thể tải danh sách câu hỏi: ${err.message}`
        } finally {
          loading.value = false
        }
      }
  
      // Filter questions
      const filterQuestions = () => {
        let result = [...questions.value]
        
        // Filter by search query
        if (searchQuery.value) {
          const query = searchQuery.value.toLowerCase()
          result = result.filter(question => {
            return question.title.toLowerCase().includes(query) || 
                   question.body_text.toLowerCase().includes(query)
          })
        }
        
        // Filter by role
        if (filters.role) {
          result = result.filter(question => question.user.role === filters.role)
        }
        
        // Sửa lỗi: Gán kết quả trực tiếp cho filteredQuestions trước khi sắp xếp
        filteredQuestions.value = result
        
        // Apply current sort
        sortQuestions()
      }
  
      // Sort questions
      const sortQuestions = () => {
        const sorted = [...filteredQuestions.value]
        
        switch (sortBy.value) {
          case 'newest':
            sorted.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
            break
          case 'oldest':
            sorted.sort((a, b) => new Date(a.created_at) - new Date(b.created_at))
            break
          case 'title':
            sorted.sort((a, b) => a.title.localeCompare(b.title))
            break
          case 'title-desc':
            sorted.sort((a, b) => b.title.localeCompare(a.title))
            break
          case 'role':
            sorted.sort((a, b) => a.user.role.localeCompare(b.user.role))
            break
        }
        
        filteredQuestions.value = sorted
      }
  
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
  
      // Truncate text
      const truncateText = (text, maxLength) => {
        if (!text) return ''
        if (text.length <= maxLength) return text
        return text.substring(0, maxLength) + '...'
      }
  
      // Get role badge class
      const getRoleBadgeClass = (role) => {
        switch (role) {
          case 'user': return 'user-badge'
          case 'instructor': return 'instructor-badge'
          case 'admin': return 'admin-badge'
          default: return ''
        }
      }
  
      // Get role title
      const getRoleTitle = (role) => {
        switch (role) {
          case 'user': return 'Người dùng'
          case 'instructor': return 'Người hướng dẫn'
          case 'admin': return 'Quản trị viên'
          default: return role
        }
      }
  
      // Delete handlers
      const confirmDeleteQuestion = (question) => {
        questionToDelete.value = question
        showDeleteModal.value = true
      }
      
      const cancelDelete = () => {
        showDeleteModal.value = false
        questionToDelete.value = null
      }
      
      const deleteQuestion = async () => {
        if (!questionToDelete.value) return
        
        try {
          isDeleting.value = true
          await QnaController.deleteQuestion(questionToDelete.value.id)
          
          // Update local state
          questions.value = questions.value.filter(q => q.id !== questionToDelete.value.id)
          filterQuestions() // Re-apply filters
          
          showDeleteModal.value = false
          questionToDelete.value = null
          
          alert('Xóa câu hỏi thành công!')
        } catch (err) {
          alert(`Lỗi: ${err.message}`)
        } finally {
          isDeleting.value = false
        }
      }
  
      onMounted(() => {
        loadQuestions()
      })
  
      return {
        loading,
        error,
        questions,
        filteredQuestions,
        searchQuery,
        sortBy,
        filters,
        showDeleteModal,
        questionToDelete,
        isDeleting,
        hasFilters,
        filterQuestions,
        sortQuestions,
        formatDate,
        truncateText,
        getRoleBadgeClass,
        getRoleTitle,
        confirmDeleteQuestion,
        cancelDelete,
        deleteQuestion
      }
    }
  }
  </script>
  
  <style scoped>
  .admin-qna-questions {
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
  
  .admin-card {
    background-color: #fff;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    padding: 1.5rem;
    transition: all 0.3s ease;
  }
  
  .btn-create {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background-color: #0B2942;
    color: #fff;
    font-weight: 500;
    padding: 0.75rem 1.25rem;
    border-radius: 8px;
    text-decoration: none;
    transition: all 0.3s;
    border: none;
    cursor: pointer;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  .btn-create:hover, .btn-create:focus {
    background-color: #4da0ff;
    color: #fff;
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
  }
  
  .section-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: #0B2942;
  }
  
  /* Filter and Search Styles */
  .form-group {
    margin-bottom: 1rem;
  }
  
  .form-group label {
    display: block;
    font-weight: 500;
    margin-bottom: 0.5rem;
    color: #0B2942;
  }
  
  .form-select {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    font-size: 0.95rem;
    transition: all 0.3s;
    background-color: #fff;
  }
  
  .form-select:focus {
    outline: none;
    border-color: #4da0ff;
    box-shadow: 0 0 0 3px rgba(77, 160, 255, 0.25);
  }
  
  .search-box {
    position: relative;
  }
  
  .search-icon {
    position: absolute;
    left: 15px;
    top: 50%;
    transform: translateY(-50%);
    color: #95a5a6;
  }
  
  .search-input {
    width: 100%;
    padding: 0.75rem 0.75rem 0.75rem 40px;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    font-size: 0.95rem;
    transition: all 0.3s;
  }
  
  .search-input:focus {
    outline: none;
    border-color: #4da0ff;
    box-shadow: 0 0 0 3px rgba(77, 160, 255, 0.25);
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
  .error-message {
    background-color: #f8d7da;
    color: #721c24;
    padding: 1rem;
    border-radius: 8px;
    display: flex;
    align-items: center;
    margin-bottom: 1.5rem;
  }
  
  .error-icon {
    font-size: 1.25rem;
    margin-right: 0.75rem;
  }
  
  /* Results count */
  .results-count {
    color: #6c757d;
    font-size: 0.9rem;
  }
  
  /* Question Card */
  .question-card {
    transition: transform 0.2s;
  }
  
  .question-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
  }
  
  .question-title {
    font-size: 1.25rem;
    margin-bottom: 0.75rem;
  }
  
  .question-title a {
    color: #0B2942;
    text-decoration: none;
    transition: color 0.2s;
  }
  
  .question-title a:hover {
    color: #4da0ff;
  }
  
  .question-content {
    color: #555;
    margin-bottom: 1rem;
    line-height: 1.6;
  }
  
  .question-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid #e9ecef;
  }
  
  .question-user {
    display: flex;
    align-items: center;
  }
  
  .user-role-badge {
    display: inline-block;
    padding: 0.25rem 0.6rem;
    border-radius: 50px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    margin-right: 0.75rem;
  }
  
  .user-badge {
    background-color: #e3f2fd;
    color: #1e88e5;
  }
  
  .instructor-badge {
    background-color: #fff8e1;
    color: #ffa000;
  }
  
  .admin-badge {
    background-color: #ffebee;
    color: #e53935;
  }
  
  .user-name {
    font-weight: 600;
    color: #495057;
  }
  
  .question-date {
    color: #6c757d;
    font-size: 0.85rem;
  }
  
  .question-stats {
    display: flex;
    justify-content: flex-end;
  }
  
  .view-responses {
    display: inline-flex;
    align-items: center;
    color: #4da0ff;
    text-decoration: none;
    font-size: 0.95rem;
    transition: color 0.2s;
  }
  
  .view-responses:hover {
    color: #0B2942;
  }
  
  /* Actions */
  .question-actions {
    display: flex;
    gap: 0.5rem;
  }
  
  .btn-action {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    border-radius: 8px;
    border: none;
    background-color: transparent;
    cursor: pointer;
    transition: all 0.3s ease;
    color: #6c757d;
  }
  
  .btn-action.edit {
    color: #0B2942;
  }
  
  .btn-action.delete {
    color: #dc3545;
  }
  
  .btn-action:hover {
    background-color: #f8f9fa;
    transform: translateY(-2px);
  }
  
  .btn-action.edit:hover {
    background-color: rgba(11, 41, 66, 0.1);
  }
  
  .btn-action.delete:hover {
    background-color: rgba(220, 53, 69, 0.1);
  }
  
  /* Empty State */
  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem 0;
    text-align: center;
  }
  
  .empty-icon {
    font-size: 3rem;
    color: #6c757d;
    margin-bottom: 1.5rem;
  }
  
  .empty-state h4 {
    font-size: 1.25rem;
    color: #0B2942;
    margin-bottom: 0.5rem;
  }
  
  .empty-state p {
    color: #6c757d;
    margin-bottom: 1.5rem;
  }
  
  .btn-create-empty {
    display: inline-flex;
    align-items: center;
    background-color: #0B2942;
    color: #fff;
    padding: 0.75rem 1.25rem;
    border-radius: 8px;
    text-decoration: none;
    transition: all 0.3s;
    border: none;
    cursor: pointer;
  }
  
  .btn-create-empty:hover {
    background-color: #4da0ff;
    color: #fff;
  }
  
  /* Modal Styling */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1050;
  }
  
  .modal-content {
    background-color: #fff;
    border-radius: 12px;
    width: 90%;
    max-width: 500px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
    overflow: hidden;
  }
  
  .modal-header {
    padding: 1rem 1.5rem;
    border-bottom: 1px solid #e9ecef;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  
  .modal-title {
    font-size: 1.25rem;
    color: #0B2942;
    margin: 0;
  }
  
  .btn-close {
    background: transparent;
    border: none;
    font-size: 1.5rem;
    line-height: 1;
    color: #6c757d;
    cursor: pointer;
  }
  
  .modal-body {
    padding: 1.5rem;
  }
  
  .modal-footer {
    padding: 1rem 1.5rem;
    border-top: 1px solid #e9ecef;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 0.5rem;
  }
  
  .btn-delete {
    padding: 0.75rem 1.5rem;
    background-color: #dc3545;
    border: none;
    border-radius: 8px;
    color: #fff;
    font-weight: 500;
    transition: all 0.3s;
    display: inline-flex;
    align-items: center;
  }
  
  .btn-delete:hover:not(:disabled) {
    background-color: #c82333;
  }
  
  .btn-delete:disabled {
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
  }
  
  .btn-cancel:hover {
    background-color: #e9ecef;
    color: #0B2942;
  }
  
  .text-danger {
    color: #dc3545 !important;
  }
  
  .text-warning {
    color: #ffc107 !important;
  }
  
  /* Responsive adjustments */
  @media (max-width: 768px) {
    .admin-page-header {
      flex-direction: column;
      gap: 1rem;
      align-items: flex-start !important;
    }
  
    .btn-create {
      width: 100%;
    }
    
    .question-meta {
      flex-direction: column;
      align-items: flex-start;
      gap: 0.5rem;
    }
  }
  </style>