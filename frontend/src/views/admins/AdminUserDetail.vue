<template>
    <div class="admin-user-detail">
      <div class="admin-page-header">
        <div class="d-flex align-items-center">
          <router-link to="/admins/users" class="btn-back">
            <i class="bi bi-arrow-left"></i>
          </router-link>
          <div>
            <h2 class="admin-page-title">Chi tiết người dùng</h2>
            <p class="admin-page-description">Xem và chỉnh sửa thông tin người dùng</p>
          </div>
        </div>
      </div>
  
      <!-- Loading State -->
      <div v-if="loading" class="loading-container">
        <div class="spinner">
          <div class="bounce1"></div>
          <div class="bounce2"></div>
          <div class="bounce3"></div>
        </div>
        <p class="loading-text">Đang tải thông tin người dùng...</p>
      </div>
  
      <!-- Error State -->
      <div v-else-if="error" class="error-message">
        <i class="bi bi-exclamation-triangle-fill error-icon"></i>
        <span>{{ error }}</span>
      </div>
  
      <div v-else class="row">
        <!-- User Info Card -->
        <div class="col-md-4 mb-4">
          <div class="admin-card user-info-card">
            <div class="user-avatar">
              <i class="bi bi-person-circle"></i>
            </div>
            <h3 class="user-name">{{ user.name }}</h3>
            <p class="user-email">{{ user.email }}</p>
            <div class="user-meta">
              <div class="user-meta-item">
                <i class="bi bi-telephone-fill"></i>
                <span>{{ user.phone_number || 'Chưa cập nhật' }}</span>
              </div>
              <div class="user-meta-item">
                <i class="bi bi-shield-check"></i>
                <span class="user-role" :class="user.role === 'user' ? 'user-role-user' : 'user-role-instructor'">
                  {{ user.role }}
                </span>
              </div>
              <div class="user-meta-item">
                <i class="bi bi-calendar-event"></i>
                <span>{{ formatDate(user.created_at) }}</span>
              </div>
            </div>
  
            <div class="user-actions">
              <button 
                class="btn-role-toggle" 
                @click="toggleRole"
                :disabled="user.role === 'admin'"
              >
                <i class="bi" :class="user.role === 'user' ? 'bi-person-check' : 'bi-person'"></i>
                {{ user.role === 'user' ? 'Chuyển sang Instructor' : 'Chuyển sang User' }}
              </button>
            </div>
          </div>
        </div>
  
        <!-- Edit Form -->
        <div class="col-md-8">
          <div class="admin-card">
            <h3 class="section-title">Chỉnh sửa thông tin</h3>
  
            <form @submit.prevent="updateUser" class="edit-form">
              <div class="form-group">
                <label for="name">Họ tên</label>
                <input 
                  type="text" 
                  id="name" 
                  v-model="formData.name" 
                  class="form-control" 
                  required
                >
              </div>
  
              <div class="form-group">
                <label for="email">Email</label>
                <input 
                  type="email" 
                  id="email" 
                  v-model="user.email" 
                  class="form-control" 
                  disabled
                >
                <small class="form-text text-muted">Email không thể thay đổi.</small>
              </div>
  
              <div class="form-group">
                <label for="phone">Số điện thoại</label>
                <input 
                  type="text" 
                  id="phone" 
                  v-model="formData.phone_number" 
                  class="form-control" 
                  required
                >
              </div>
  
              <div class="form-actions">
                <button type="submit" class="btn-save" :disabled="isSaving">
                  <i class="bi bi-check-circle me-1"></i>
                  {{ isSaving ? 'Đang lưu...' : 'Lưu thay đổi' }}
                </button>
                <button type="button" class="btn-cancel" @click="resetForm">
                  <i class="bi bi-x-circle me-1"></i>
                  Hủy thay đổi
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, reactive, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import UserController from '@/controllers/admins/UserController'
  
  export default {
    name: 'AdminUserDetail',
    props: {
      userId: {
        type: [String, Number],
        required: true
      }
    },
    setup(props) {
      const router = useRouter()
      const user = ref({})
      const formData = reactive({
        name: '',
        phone_number: ''
      })
      const loading = ref(true)
      const error = ref(null)
      const isSaving = ref(false)
  
      // Format date
      const formatDate = (dateString) => {
        const date = new Date(dateString)
        return new Intl.DateTimeFormat('vi-VN', { 
          day: '2-digit', 
          month: '2-digit', 
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        }).format(date)
      }
  
      // Fetch user details
      const fetchUserDetails = async () => {
        try {
          loading.value = true
          error.value = null
          
          const userData = await UserController.getUserById(props.userId)
          user.value = userData
          
          // Set form data
          formData.name = userData.name
          formData.phone_number = userData.phone_number
        } catch (err) {
          error.value = `Không thể tải thông tin người dùng: ${err.message}`
        } finally {
          loading.value = false
        }
      }
  
      // Toggle user role
      const toggleRole = async () => {
        if (user.value.role === 'admin') {
          alert('Không thể thay đổi quyền của tài khoản admin!')
          return
        }
  
        try {
          const newRole = user.value.role === 'user' ? 'instructor' : 'user'
          await UserController.updateUserRole(props.userId, newRole)
          user.value.role = newRole
          alert(`Đã cập nhật vai trò người dùng thành ${newRole}`)
        } catch (err) {
          alert(`Lỗi: ${err.message}`)
        }
      }
  
      // Update user
      const updateUser = async () => {
        try {
          isSaving.value = true
          
          const updateData = {
            name: formData.name,
            phone_number: formData.phone_number
          }
          
          await UserController.updateUser(props.userId, updateData)
          
          // Update local user object
          user.value.name = formData.name
          user.value.phone_number = formData.phone_number
          
          alert('Cập nhật thông tin người dùng thành công')
        } catch (err) {
          alert(`Lỗi: ${err.message}`)
        } finally {
          isSaving.value = false
        }
      }
  
      // Reset form
      const resetForm = () => {
        formData.name = user.value.name
        formData.phone_number = user.value.phone_number
      }
  
      onMounted(() => {
        fetchUserDetails()
      })
  
      return {
        user,
        formData,
        loading,
        error,
        isSaving,
        formatDate,
        toggleRole,
        updateUser,
        resetForm
      }
    }
  }
  </script>
  
  <style scoped>
  .admin-user-detail {
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
    margin-bottom: 1.5rem;
    transition: all 0.3s ease;
  }
  
  .admin-card:hover {
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
  }
  
  /* User Info Card */
  .user-info-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  
  .user-avatar {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    background-color: #e9ecef;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1.5rem;
    color: #0B2942;
    font-size: 3rem;
  }
  
  .user-name {
    font-size: 1.5rem;
    font-weight: 600;
    color: #0B2942;
    margin-bottom: 0.25rem;
  }
  
  .user-email {
    color: #4da0ff;
    font-size: 0.95rem;
    margin-bottom: 1.5rem;
  }
  
  .user-meta {
    width: 100%;
    margin-bottom: 1.5rem;
  }
  
  .user-meta-item {
    display: flex;
    align-items: center;
    padding: 0.75rem 0;
    border-bottom: 1px solid #edf2f7;
  }
  
  .user-meta-item:last-child {
    border-bottom: none;
  }
  
  .user-meta-item i {
    width: 24px;
    margin-right: 0.75rem;
    color: #6c757d;
  }
  
  .user-role {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 50px;
    font-size: 0.85rem;
    font-weight: 500;
    text-transform: capitalize;
  }
  
  .user-role-user {
    background-color: #e3f2fd;
    color: #0d6efd;
  }
  
  .user-role-instructor {
    background-color: #e3faeb;
    color: #198754;
  }
  
  .user-actions {
    width: 100%;
    margin-top: 1rem;
  }
  
  .btn-role-toggle {
    width: 100%;
    padding: 0.75rem;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #0B2942;
    border: none;
    border-radius: 8px;
    color: #fff;
    font-weight: 500;
    transition: all 0.3s;
  }
  
  .btn-role-toggle:hover:not(:disabled) {
    background-color: #4da0ff;
  }
  
  .btn-role-toggle i {
    margin-right: 0.5rem;
  }
  
  .btn-role-toggle:disabled {
    background-color: #e9ecef;
    color: #6c757d;
    cursor: not-allowed;
  }
  
  /* Form Styling */
  .section-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: #0B2942;
    margin-bottom: 1.5rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid #e9ecef;
  }
  
  .edit-form {
    width: 100%;
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
  
  .form-control:disabled {
    background-color: #f8f9fa;
    cursor: not-allowed;
  }
  
  .form-text {
    display: block;
    margin-top: 0.5rem;
    font-size: 0.875rem;
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
  }
  
  .btn-cancel:hover {
    background-color: #e9ecef;
    color: #0B2942;
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
  
  @media (max-width: 768px) {
    .form-actions {
      flex-direction: column;
    }
    
    .btn-save, .btn-cancel {
      width: 100%;
    }
  }
  </style>