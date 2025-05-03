<template>
    <div class="admin-qna-detail">
      <div class="admin-page-header">
        <div class="d-flex align-items-center">
          <router-link to="/admins/qna" class="btn-back">
            <i class="bi bi-arrow-left"></i>
          </router-link>
          <div>
            <h2 class="admin-page-title">Chi tiết câu hỏi</h2>
            <p class="admin-page-description">Xem câu hỏi và câu trả lời</p>
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
  
      <div v-else>
        <!-- Question Card -->
        <div class="admin-card mb-4">
          <div class="d-flex justify-content-between align-items-start mb-3">
            <h3 class="question-title">{{ question.title }}</h3>
            <div class="question-actions">
              <router-link 
                v-if="canEditQuestion"
                :to="`/admins/qna/${questionId}/edit`" 
                class="btn-action edit" 
                title="Chỉnh sửa"
              >
                <i class="bi bi-pencil-square"></i>
              </router-link>
              <button @click="confirmDeleteQuestion" class="btn-action delete" title="Xóa">
                <i class="bi bi-trash"></i>
              </button>
            </div>
          </div>
          <div class="question-content">{{ question.body_text }}</div>
          <div class="question-meta">
            <div class="question-user">
              <span 
                :class="['user-role-badge', getRoleBadgeClass(question.user.role)]"
                :title="getRoleTitle(question.user.role)"
              >
                {{ question.user.role }}
              </span>
              <span class="user-name">{{ question.user.name }}</span>
              <span class="user-email">({{ question.user.email }})</span>
            </div>
            <div class="question-date">
              <span class="date-label">Đăng lúc:</span> {{ formatDate(question.created_at) }}
            </div>
          </div>
        </div>
  
        <!-- Responses Section -->
        <h4 class="responses-title">Câu trả lời ({{ responses.length }})</h4>
        
        <!-- Add Response Form -->
        <div class="admin-card mb-4">
          <h5 class="add-response-title">Thêm câu trả lời mới</h5>
          <form @submit.prevent="createResponse" class="response-form">
            <div class="form-group">
              <label for="response-body">Nội dung câu trả lời <span class="required">*</span></label>
              <textarea 
                id="response-body" 
                v-model="newResponse.body_text" 
                class="form-control" 
                :class="{ 'is-invalid': errors.body_text }"
                rows="4" 
                placeholder="Nhập câu trả lời của bạn..." 
                required
              ></textarea>
              <div v-if="errors.body_text" class="invalid-feedback">
                {{ errors.body_text }}
              </div>
            </div>
            <div v-if="submitError" class="alert alert-danger">
              <i class="bi bi-exclamation-triangle-fill me-2"></i>
              {{ submitError }}
            </div>
            <button 
              type="submit" 
              class="btn-submit" 
              :disabled="isSubmitting || !newResponse.body_text.trim()"
            >
              <i class="bi bi-send me-2"></i>
              {{ isSubmitting ? 'Đang gửi...' : 'Gửi câu trả lời' }}
            </button>
          </form>
        </div>
  
        <!-- Response List -->
        <div v-if="responses.length === 0" class="admin-card empty-responses">
          <i class="bi bi-chat-left empty-icon"></i>
          <h4>Chưa có câu trả lời nào</h4>
          <p>Hãy là người đầu tiên trả lời câu hỏi này</p>
        </div>
  
        <div v-else>
          <div 
            v-for="response in sortedResponses" 
            :key="response.id"
            class="admin-card response-card mb-3"
          >
            <div class="d-flex justify-content-between align-items-start mb-2">
              <div class="response-user">
                <span 
                  :class="['user-role-badge', getRoleBadgeClass(response.user.role)]"
                  :title="getRoleTitle(response.user.role)"
                >
                  {{ response.user.role }}
                </span>
                <span class="user-name">{{ response.user.name }}</span>
                <span class="response-date">{{ formatDate(response.created_at) }}</span>
              </div>
              <div class="response-actions">
                <button 
                  v-if="canEditResponse(response)"
                  @click="startEditResponse(response)" 
                  class="btn-action edit" 
                  title="Chỉnh sửa"
                >
                  <i class="bi bi-pencil-square"></i>
                </button>
                <button 
                  @click="confirmDeleteResponse(response)" 
                  class="btn-action delete" 
                  title="Xóa"
                >
                  <i class="bi bi-trash"></i>
                </button>
              </div>
            </div>
  
            <!-- Edit Form (conditionally shown) -->
            <div v-if="editingResponse && editingResponse.id === response.id" class="edit-response-form">
              <textarea 
                v-model="editingResponse.body_text"
                class="form-control"
                rows="3"
              ></textarea>
              <div class="edit-actions">
                <button @click="cancelEditResponse" class="btn-cancel-edit">
                  <i class="bi bi-x-circle me-1"></i> Hủy
                </button>
                <button @click="updateResponse" class="btn-save-edit" :disabled="isUpdating">
                  <i class="bi bi-check-circle me-1"></i> 
                  {{ isUpdating ? 'Đang lưu...' : 'Lưu' }}
                </button>
              </div>
            </div>
            
            <!-- Normal display -->
            <div v-else class="response-content">
              {{ response.body_text }}
            </div>
          </div>
        </div>
      </div>
  
      <!-- Delete Question Confirmation Modal -->
      <div v-if="showDeleteQuestionModal" class="modal-overlay" @click="cancelDeleteQuestion">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h4 class="modal-title">Xác nhận xóa câu hỏi</h4>
            <button type="button" class="btn-close" @click="cancelDeleteQuestion"></button>
          </div>
          <div class="modal-body">
            <p>Bạn có chắc chắn muốn xóa câu hỏi <strong>"{{ question?.title }}"</strong>?</p>
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
            <button type="button" class="btn-cancel" @click="cancelDeleteQuestion">Hủy</button>
            <button type="button" class="btn-delete" @click="deleteQuestion" :disabled="isDeleting">
              <span v-if="isDeleting">Đang xóa...</span>
              <span v-else>Xác nhận xóa</span>
            </button>
          </div>
        </div>
      </div>
  
      <!-- Delete Response Confirmation Modal -->
      <div v-if="showDeleteResponseModal" class="modal-overlay" @click="cancelDeleteResponse">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h4 class="modal-title">Xác nhận xóa câu trả lời</h4>
            <button type="button" class="btn-close" @click="cancelDeleteResponse"></button>
          </div>
          <div class="modal-body">
            <p>Bạn có chắc chắn muốn xóa câu trả lời này?</p>
            <div class="response-preview">{{ responseToDelete?.body_text }}</div>
            <p class="text-danger mt-3">
              <i class="bi bi-exclamation-triangle me-2"></i>
              Thao tác này không thể khôi phục lại!
            </p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn-cancel" @click="cancelDeleteResponse">Hủy</button>
            <button type="button" class="btn-delete" @click="deleteResponse" :disabled="isDeleting">
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
  import { useRouter } from 'vue-router'
  import QnaController from '@/controllers/admins/qnaController'
  
  export default {
    name: 'AdminQnaDetail',
    props: {
      questionId: {
        type: [String, Number],
        required: true
      }
    },
    setup(props) {
      const router = useRouter()
      const question = ref({})
      const responses = ref([])
      const loading = ref(true)
      const error = ref(null)
      
      // Lấy thông tin người dùng hiện tại từ session storage
      const currentUser = {
        id: parseInt(sessionStorage.getItem('userId') || '0'),
        role: sessionStorage.getItem('userRole') || 'admin',
        email: sessionStorage.getItem('userEmail') || ''
      }
      
      // New response
      const newResponse = reactive({
        body_text: '',
        question_id: parseInt(props.questionId)
      })
      const errors = reactive({
        body_text: ''
      })
      const submitError = ref('')
      const isSubmitting = ref(false)
      
      // Edit response
      const editingResponse = ref(null)
      const isUpdating = ref(false)
      
      // Delete modals
      const showDeleteQuestionModal = ref(false)
      const showDeleteResponseModal = ref(false)
      const responseToDelete = ref(null)
      const isDeleting = ref(false)
      
      // Sort responses by date (newest first)
      const sortedResponses = computed(() => {
        return [...responses.value].sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
      })
      
      // Check if current user can edit the question
      const canEditQuestion = computed(() => {
        // Admin chỉ có thể edit câu hỏi do chính mình tạo ra
        return question.value && 
               question.value.user && 
               (question.value.user.id === currentUser.id && 
                question.value.user.role === 'admin')
      })
      
      // Check if current user can edit a response
      const canEditResponse = (response) => {
        // Admin chỉ có thể edit câu trả lời do chính mình tạo ra
        return response && 
               response.user && 
               (response.user.id === currentUser.id && 
                response.user.role === 'admin')
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
      
      // Load question and responses
      const loadQuestionAndResponses = async () => {
        try {
          loading.value = true
          error.value = null
          
          // Load question
          const questionData = await QnaController.getQuestionById(props.questionId)
          question.value = questionData
          
          // Load responses
          const responsesData = await QnaController.getResponsesByQuestionId(props.questionId)
          responses.value = responsesData
          
        } catch (err) {
          error.value = `Không thể tải thông tin câu hỏi: ${err.message}`
        } finally {
          loading.value = false
        }
      }
      
      // Create new response
      const createResponse = async () => {
        // Validate
        errors.body_text = ''
        submitError.value = ''
        
        if (!newResponse.body_text.trim()) {
          errors.body_text = 'Vui lòng nhập nội dung câu trả lời'
          return
        }
        
        try {
          isSubmitting.value = true
          
          const createdResponse = await QnaController.createResponse({
            body_text: newResponse.body_text.trim(),
            question_id: newResponse.question_id
          })
          
          // Add to responses list
          responses.value.unshift(createdResponse)
          
          // Reset form
          newResponse.body_text = ''
          
        } catch (err) {
          submitError.value = `Không thể tạo câu trả lời: ${err.message}`
        } finally {
          isSubmitting.value = false
        }
      }
      
      // Edit response
      const startEditResponse = (response) => {
        editingResponse.value = {
          id: response.id,
          body_text: response.body_text
        }
      }
      
      const cancelEditResponse = () => {
        editingResponse.value = null
      }
      
      const updateResponse = async () => {
        if (!editingResponse.value) return
        
        try {
          isUpdating.value = true
          
          const updatedResponse = await QnaController.updateResponse(editingResponse.value.id, {
            body_text: editingResponse.value.body_text.trim()
          })
          
          // Update responses list
          const index = responses.value.findIndex(r => r.id === editingResponse.value.id)
          if (index !== -1) {
            responses.value[index] = {
              ...responses.value[index],
              body_text: updatedResponse.body_text,
              updated_at: updatedResponse.updated_at
            }
          }
          
          editingResponse.value = null
          
        } catch (err) {
          alert(`Không thể cập nhật câu trả lời: ${err.message}`)
        } finally {
          isUpdating.value = false
        }
      }
      
      // Delete question
      const confirmDeleteQuestion = () => {
        showDeleteQuestionModal.value = true
      }
      
      const cancelDeleteQuestion = () => {
        showDeleteQuestionModal.value = false
      }
      
      const deleteQuestion = async () => {
        try {
          isDeleting.value = true
          
          await QnaController.deleteQuestion(props.questionId)
          
          alert('Xóa câu hỏi thành công!')
          router.push('/admins/qna')
        } catch (err) {
          alert(`Lỗi: ${err.message}`)
        } finally {
          isDeleting.value = false
          showDeleteQuestionModal.value = false
        }
      }
      
      // Delete response
      const confirmDeleteResponse = (response) => {
        responseToDelete.value = response
        showDeleteResponseModal.value = true
      }
      
      const cancelDeleteResponse = () => {
        showDeleteResponseModal.value = false
        responseToDelete.value = null
      }
      
      const deleteResponse = async () => {
        if (!responseToDelete.value) return
        
        try {
          isDeleting.value = true
          
          await QnaController.deleteResponse(responseToDelete.value.id)
          
          // Update responses list
          responses.value = responses.value.filter(r => r.id !== responseToDelete.value.id)
          
          showDeleteResponseModal.value = false
          responseToDelete.value = null
          
          alert('Xóa câu trả lời thành công!')
        } catch (err) {
          alert(`Lỗi: ${err.message}`)
        } finally {
          isDeleting.value = false
        }
      }
      
      onMounted(() => {
        loadQuestionAndResponses()
      })
  
      return {
        question,
        responses,
        sortedResponses,
        loading,
        error,
        newResponse,
        errors,
        submitError,
        isSubmitting,
        editingResponse,
        isUpdating,
        showDeleteQuestionModal,
        showDeleteResponseModal,
        responseToDelete,
        isDeleting,
        canEditQuestion,
        canEditResponse,
        formatDate,
        getRoleBadgeClass,
        getRoleTitle,
        createResponse,
        startEditResponse,
        cancelEditResponse,
        updateResponse,
        confirmDeleteQuestion,
        cancelDeleteQuestion,
        deleteQuestion,
        confirmDeleteResponse,
        cancelDeleteResponse,
        deleteResponse
      }
    }
  }
  </script>
  
  <style scoped>
  .admin-qna-detail {
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
    margin-bottom: 1.5rem;
  }
  
  .admin-card:hover {
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
  }
  
  /* Question Styles */
  .question-title {
    font-size: 1.5rem;
    font-weight: 600;
    color: #0B2942;
    margin-bottom: 0.5rem;
  }
  
  .question-content {
    color: #333;
    line-height: 1.6;
    margin-bottom: 1.5rem;
    white-space: pre-line;
  }
  
  .question-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.5rem;
    padding-top: 1rem;
    border-top: 1px solid #e9ecef;
  }
  
  .question-user {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.5rem;
  }
  
  .question-date {
    color: #6c757d;
    font-size: 0.9rem;
  }
  
  .date-label {
    font-weight: 500;
  }
  
  .user-name {
    font-weight: 600;
    color: #333;
  }
  
  .user-email {
    color: #6c757d;
    font-size: 0.9rem;
  }
  
  /* Response Styles */
  .responses-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: #0B2942;
    margin: 1.5rem 0 1rem;
  }
  
  .add-response-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #0B2942;
    margin-bottom: 1rem;
  }
  
  .response-form .form-control {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    font-size: 0.95rem;
    transition: all 0.3s;
  }
  
  .response-form .form-control:focus {
    outline: none;
    border-color: #4da0ff;
    box-shadow: 0 0 0 3px rgba(77, 160, 255, 0.25);
  }
  
  .response-form .form-control.is-invalid {
    border-color: #dc3545;
  }
  
  .invalid-feedback {
    color: #dc3545;
    font-size: 0.875em;
    margin-top: 0.25rem;
  }
  
  .btn-submit {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background-color: #0B2942;
    color: #fff;
    font-weight: 500;
    padding: 0.75rem 1.25rem;
    border-radius: 8px;
    transition: all 0.3s;
    border: none;
    cursor: pointer;
    margin-top: 1rem;
  }
  
  .btn-submit:hover:not(:disabled) {
    background-color: #4da0ff;
    transform: translateY(-2px);
  }
  
  .btn-submit:disabled {
    background-color: #e9ecef;
    color: #6c757d;
    cursor: not-allowed;
  }
  
  .response-card {
    padding: 1.25rem;
  }
  
  .response-user {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
  }
  
  .response-date {
    color: #6c757d;
    font-size: 0.85rem;
    margin-left: 0.5rem;
  }
  
  .response-content {
    color: #333;
    line-height: 1.5;
    white-space: pre-line;
  }
  
  .user-role-badge {
    display: inline-block;
    padding: 0.25rem 0.6rem;
    border-radius: 50px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
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
  
  /* Edit Response Form */
  .edit-response-form {
    margin-top: 0.5rem;
  }
  
  .edit-actions {
    display: flex;
    justify-content: flex-end;
    gap: 0.5rem;
    margin-top: 0.5rem;
  }
  
  .btn-save-edit {
    display: inline-flex;
    align-items: center;
    background-color: #0B2942;
    color: #fff;
    font-weight: 500;
    padding: 0.5rem 0.75rem;
    border-radius: 6px;
    transition: all 0.3s;
    border: none;
    cursor: pointer;
    font-size: 0.9rem;
  }
  
  .btn-save-edit:hover:not(:disabled) {
    background-color: #4da0ff;
  }
  
  .btn-save-edit:disabled {
    background-color: #e9ecef;
    color: #6c757d;
    cursor: not-allowed;
  }
  
  .btn-cancel-edit {
    display: inline-flex;
    align-items: center;
    background-color: #f8f9fa;
    color: #6c757d;
    font-weight: 500;
    padding: 0.5rem 0.75rem;
    border-radius: 6px;
    transition: all 0.3s;
    border: 1px solid #e0e0e0;
    cursor: pointer;
    font-size: 0.9rem;
  }
  
  .btn-cancel-edit:hover {
    background-color: #e9ecef;
    color: #0B2942;
  }
  
  /* Actions */
  .question-actions, .response-actions {
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
  
  /* Empty Responses */
  .empty-responses {
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
  
  .empty-responses h4 {
    font-size: 1.25rem;
    color: #0B2942;
    margin-bottom: 0.5rem;
  }
  
  .empty-responses p {
    color: #6c757d;
  }
  
  /* Alert */
  .alert {
    padding: 1rem;
    margin-top: 1rem;
    border-radius: 8px;
  }
  
  .alert-danger {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c2c7;
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
  
  .response-preview {
    background-color: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #6c757d;
    margin-top: 0.5rem;
    max-height: 150px;
    overflow-y: auto;
    white-space: pre-line;
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
  
  .required {
    color: #dc3545;
  }
  
  /* Responsive adjustments */
  @media (max-width: 768px) {
    .question-meta {
      flex-direction: column;
      align-items: flex-start;
    }
    
    .response-user {
      flex-direction: column;
      align-items: flex-start;
    }
    
    .response-date {
      margin-left: 0;
    }
  }
  </style>