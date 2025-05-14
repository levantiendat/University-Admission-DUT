<template>
  <div class="profile-container">
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-md-10 col-lg-8">
          <!-- Profile Card -->
          <div class="card profile-card shadow-sm mb-4">
            <!-- Profile Header -->
            <div class="card-header profile-header" :class="{'profile-header-instructor': isInstructor, 'profile-header-user': isRegularUser}">
              <div class="d-flex align-items-center">
                <div class="profile-avatar">
                  <i class="bi bi-person-circle"></i>
                </div>
                <div class="ms-3">
                  <h1 class="profile-title mb-0">Thông tin cá nhân</h1>
                  <p class="profile-subtitle mb-0">
                    <span class="badge" :class="roleBadgeClass">{{ userRole }}</span>
                    <span class="ms-2 text-white">{{ formatDate(user.created_at) }}</span>
                  </p>
                </div>
              </div>
            </div>

            <!-- Profile Body -->
            <div class="card-body p-4">
              <!-- Loading State -->
              <div v-if="isLoading" class="text-center py-5">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-3">Đang tải thông tin...</p>
              </div>

              <!-- Error State -->
              <div v-else-if="error" class="alert alert-danger">
                <i class="bi bi-exclamation-triangle-fill me-2"></i>
                {{ error }}
              </div>

              <!-- Profile Form -->
              <form v-else @submit.prevent="updateProfile" class="profile-form">
                <!-- Alert for success/error message -->
                <div v-if="alertMessage" class="alert" :class="alertClass" role="alert">
                  <i :class="alertIcon" class="me-2"></i>
                  {{ alertMessage }}
                </div>

                <!-- Name -->
                <div class="mb-4">
                  <label for="name" class="form-label">Họ và tên</label>
                  <div class="input-group">
                    <span class="input-group-text"><i class="bi bi-person-fill"></i></span>
                    <input 
                      type="text" 
                      class="form-control" 
                      id="name" 
                      v-model="formData.name" 
                      placeholder="Nhập họ và tên"
                      required
                    >
                  </div>
                </div>

                <!-- Email (disabled) -->
                <div class="mb-4">
                  <label for="email" class="form-label">Email</label>
                  <div class="input-group">
                    <span class="input-group-text"><i class="bi bi-envelope-fill"></i></span>
                    <input 
                      type="email" 
                      class="form-control bg-light" 
                      id="email" 
                      v-model="formData.email" 
                      disabled
                    >
                  </div>
                  <small class="text-muted">Email không thể thay đổi</small>
                </div>

                <!-- Phone Number -->
                <div class="mb-4">
                  <label for="phone" class="form-label">Số điện thoại</label>
                  <div class="input-group">
                    <span class="input-group-text"><i class="bi bi-telephone-fill"></i></span>
                    <input 
                      type="tel" 
                      class="form-control" 
                      id="phone" 
                      v-model="formData.phone_number" 
                      placeholder="Nhập số điện thoại"
                    >
                  </div>
                </div>

                <!-- Account Info -->
                <div class="account-info mb-4 p-3 rounded">
                  <h5><i class="bi bi-info-circle-fill me-2"></i>Thông tin tài khoản</h5>
                  <div class="row mt-3">
                    <div class="col-md-6 mb-3 mb-md-0">
                      <p class="mb-1 fw-bold text-muted">ID người dùng:</p>
                      <p>{{ user.id }}</p>
                    </div>
                    <div class="col-md-6">
                      <p class="mb-1 fw-bold text-muted">Ngày tạo tài khoản:</p>
                      <p>{{ formatDate(user.created_at, true) }}</p>
                    </div>
                  </div>
                </div>

                <!-- Submit Button -->
                <div class="text-center">
                  <button 
                    type="submit" 
                    class="btn btn-primary profile-submit-btn px-5"
                    :disabled="isSubmitting"
                  >
                    <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2" role="status"></span>
                    <span v-if="isSubmitting">Đang cập nhật...</span>
                    <span v-else>Cập nhật thông tin</span>
                  </button>
                </div>
              </form>
            </div>
          </div>

          <!-- Password Change Card -->
          <div class="card profile-card shadow-sm">
            <div class="card-header password-header">
              <div class="d-flex align-items-center">
                <i class="bi bi-shield-lock-fill fs-4 me-2"></i>
                <h2 class="password-title mb-0">Đổi mật khẩu</h2>
              </div>
            </div>

            <div class="card-body p-4">
              <!-- Password Change Form -->
              <form @submit.prevent="changePassword" class="profile-form">
                <!-- Alert for password change message -->
                <div v-if="passwordAlertMessage" class="alert" :class="passwordAlertClass" role="alert">
                  <i :class="passwordAlertIcon" class="me-2"></i>
                  {{ passwordAlertMessage }}
                </div>

                <!-- Old Password -->
                <div class="mb-4">
                  <label for="oldPassword" class="form-label">Mật khẩu hiện tại</label>
                  <div class="input-group">
                    <span class="input-group-text"><i class="bi bi-key-fill"></i></span>
                    <input 
                      :type="showOldPassword ? 'text' : 'password'" 
                      class="form-control" 
                      id="oldPassword" 
                      v-model="passwordData.oldPassword" 
                      placeholder="Nhập mật khẩu hiện tại"
                      required
                    >
                    <button 
                      type="button" 
                      class="input-group-text password-toggle" 
                      @click="showOldPassword = !showOldPassword"
                    >
                      <i :class="showOldPassword ? 'bi bi-eye-slash-fill' : 'bi bi-eye-fill'"></i>
                    </button>
                  </div>
                </div>

                <!-- New Password -->
                <div class="mb-4">
                  <label for="newPassword" class="form-label">Mật khẩu mới</label>
                  <div class="input-group">
                    <span class="input-group-text"><i class="bi bi-lock-fill"></i></span>
                    <input 
                      :type="showNewPassword ? 'text' : 'password'" 
                      class="form-control" 
                      id="newPassword" 
                      v-model="passwordData.newPassword" 
                      placeholder="Nhập mật khẩu mới"
                      required
                      minlength="6"
                    >
                    <button 
                      type="button" 
                      class="input-group-text password-toggle" 
                      @click="showNewPassword = !showNewPassword"
                    >
                      <i :class="showNewPassword ? 'bi bi-eye-slash-fill' : 'bi bi-eye-fill'"></i>
                    </button>
                  </div>
                  <small class="text-muted">Mật khẩu phải có ít nhất 6 ký tự</small>
                </div>

                <!-- Confirm Password -->
                <div class="mb-4">
                  <label for="confirmPassword" class="form-label">Xác nhận mật khẩu mới</label>
                  <div class="input-group">
                    <span class="input-group-text"><i class="bi bi-lock-fill"></i></span>
                    <input 
                      :type="showConfirmPassword ? 'text' : 'password'" 
                      class="form-control" 
                      id="confirmPassword" 
                      v-model="passwordData.confirmPassword" 
                      placeholder="Nhập lại mật khẩu mới"
                      required
                    >
                    <button 
                      type="button" 
                      class="input-group-text password-toggle" 
                      @click="showConfirmPassword = !showConfirmPassword"
                    >
                      <i :class="showConfirmPassword ? 'bi bi-eye-slash-fill' : 'bi bi-eye-fill'"></i>
                    </button>
                  </div>
                  <small v-if="!passwordsMatch && passwordData.confirmPassword" class="text-danger">
                    Mật khẩu xác nhận không khớp
                  </small>
                </div>

                <!-- Password Change Button -->
                <div class="text-center">
                  <button 
                    type="submit" 
                    class="btn btn-warning password-submit-btn px-5"
                    :disabled="isChangingPassword || !passwordsMatch"
                  >
                    <span v-if="isChangingPassword" class="spinner-border spinner-border-sm me-2" role="status"></span>
                    <span v-if="isChangingPassword">Đang đổi mật khẩu...</span>
                    <span v-else>Đổi mật khẩu</span>
                  </button>
                </div>
              </form>

              <!-- Password Requirements -->
              <div class="password-requirements mt-4">
                <h6><i class="bi bi-info-circle me-2"></i>Lưu ý khi đổi mật khẩu:</h6>
                <ul>
                  <li>Mật khẩu phải có ít nhất 6 ký tự</li>
                  <li>Bạn sẽ được yêu cầu đăng nhập lại sau khi đổi mật khẩu thành công</li>
                  <li>Nên sử dụng mật khẩu kết hợp chữ, số và ký tự đặc biệt để tăng độ bảo mật</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Modal thông báo đổi mật khẩu thành công -->
    <div class="modal fade" id="passwordSuccessModal" tabindex="-1" aria-hidden="true" ref="passwordSuccessModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header bg-success text-white">
            <h5 class="modal-title">Đổi mật khẩu thành công</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <p>Mật khẩu của bạn đã được thay đổi thành công. Vui lòng đăng nhập lại với mật khẩu mới.</p>
            <p>Bạn sẽ được chuyển hướng đến trang đăng nhập sau <strong>{{ logoutCountdown }}</strong> giây.</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="logoutAndRedirect">Đăng nhập ngay</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import UserController from '@/controllers/UserControllers'
import { Modal } from 'bootstrap'

export default {
  name: 'UserProfileView',
  data() {
    return {
      user: {},
      formData: {
        name: '',
        email: '',
        phone_number: ''
      },
      passwordData: {
        oldPassword: '',
        newPassword: '',
        confirmPassword: ''
      },
      isLoading: true,
      isSubmitting: false,
      isChangingPassword: false,
      error: null,
      
      // Thông báo cho thông tin cá nhân
      alertMessage: '',
      alertClass: '',
      alertIcon: '',
      
      // Thông báo cho đổi mật khẩu
      passwordAlertMessage: '',
      passwordAlertClass: '',
      passwordAlertIcon: '',
      
      // Hiện/ẩn mật khẩu
      showOldPassword: false,
      showNewPassword: false,
      showConfirmPassword: false,
      
      // Modal đổi mật khẩu thành công
      passwordSuccessModal: null,
      logoutCountdown: 5
    }
  },
  computed: {
    // Kiểm tra xem người dùng có phải là instructor không
    isInstructor() {
      return UserController.isInstructor(this.user)
    },
    // Kiểm tra xem người dùng có phải là user thường không
    isRegularUser() {
      return UserController.isRegularUser(this.user)
    },
    // Hiển thị role dưới dạng text
    userRole() {
      if (this.isInstructor) return 'Giảng viên'
      if (this.isRegularUser) return 'Học sinh/Sinh viên'
      return this.user.role || 'Người dùng'
    },
    // CSS class cho role badge
    roleBadgeClass() {
      if (this.isInstructor) return 'badge-instructor'
      if (this.isRegularUser) return 'badge-user'
      return 'badge-default'
    },
    // Kiểm tra mật khẩu xác nhận có khớp không
    passwordsMatch() {
      if (!this.passwordData.confirmPassword) return true
      return this.passwordData.newPassword === this.passwordData.confirmPassword
    }
  },
  async mounted() {
    this.loadUserInfo()
  },
  methods: {
    // Lấy thông tin người dùng
    async loadUserInfo() {
      try {
        this.isLoading = true
        this.error = null
        this.user = await UserController.getUserInfo()
        
        // Cập nhật form data
        this.formData.name = this.user.name
        this.formData.email = this.user.email
        this.formData.phone_number = this.user.phone_number

        // Cập nhật title của trang
        document.title = `Thông tin cá nhân - ${this.user.name || 'Người dùng'}`
      } catch (error) {
        console.error('Error loading user info:', error)
        this.error = 'Không thể tải thông tin người dùng. Vui lòng thử lại sau.'
      } finally {
        this.isLoading = false
      }
    },

    // Cập nhật thông tin cá nhân
    async updateProfile() {
      try {
        this.isSubmitting = true
        this.alertMessage = ''
        
        // Chuẩn bị dữ liệu để cập nhật
        const updateData = {
          name: this.formData.name,
          phone_number: this.formData.phone_number
        }
        
        // Gọi API cập nhật
        await UserController.updateUserInfo(updateData)
        
        // Hiển thị thông báo thành công
        this.showAlert('Cập nhật thông tin thành công!', 'alert-success', 'bi bi-check-circle-fill')
        
        // Làm mới thông tin người dùng
        await this.loadUserInfo()
      } catch (error) {
        console.error('Error updating profile:', error)
        this.showAlert('Không thể cập nhật thông tin. Vui lòng thử lại sau.', 'alert-danger', 'bi bi-exclamation-triangle-fill')
      } finally {
        this.isSubmitting = false
      }
    },

    // Đổi mật khẩu
    async changePassword() {
      // Kiểm tra mật khẩu xác nhận
      if (!this.passwordsMatch) {
        this.showPasswordAlert('Mật khẩu xác nhận không khớp!', 'alert-danger', 'bi bi-exclamation-triangle-fill')
        return
      }
      
      try {
        this.isChangingPassword = true
        this.passwordAlertMessage = ''
        
        // Gọi API đổi mật khẩu
        await UserController.changePassword(this.passwordData.oldPassword, this.passwordData.newPassword)
        
        // Reset form
        this.passwordData = {
          oldPassword: '',
          newPassword: '',
          confirmPassword: ''
        }
        
        // Hiển thị modal thông báo thành công
        this.showPasswordSuccessModal()
      } catch (error) {
        console.error('Error changing password:', error)
        let errorMessage = 'Không thể đổi mật khẩu. Vui lòng thử lại sau.'
        
        // Kiểm tra các lỗi phổ biến
        if (error.response) {
          if (error.response.status === 401) {
            errorMessage = 'Mật khẩu hiện tại không chính xác!'
          } else if (error.response.data && error.response.data.detail) {
            errorMessage = error.response.data.detail
          }
        }
        
        this.showPasswordAlert(errorMessage, 'alert-danger', 'bi bi-exclamation-triangle-fill')
      } finally {
        this.isChangingPassword = false
      }
    },
    
    // Hiển thị modal thông báo đổi mật khẩu thành công
    showPasswordSuccessModal() {
      // Khởi tạo modal
      this.passwordSuccessModal = new Modal(document.getElementById('passwordSuccessModal'))
      this.passwordSuccessModal.show()
      
      // Bắt đầu đếm ngược để đăng xuất
      this.logoutCountdown = 5
      const countdownInterval = setInterval(() => {
        this.logoutCountdown--
        
        if (this.logoutCountdown <= 0) {
          clearInterval(countdownInterval)
          this.logoutAndRedirect()
        }
      }, 1000)
    },
    
    // Đăng xuất và chuyển hướng đến trang đăng nhập
    logoutAndRedirect() {
      // Đóng modal nếu đang mở
      if (this.passwordSuccessModal) {
        this.passwordSuccessModal.hide()
      }
      
      // Đăng xuất
      UserController.logout()
      
      // Chuyển hướng đến trang đăng nhập
      this.$router.push({ name: 'Login', query: { message: 'password_changed' } })
    },

    // Hiển thị thông báo cho thông tin cá nhân
    showAlert(message, alertClass, icon) {
      this.alertMessage = message
      this.alertClass = alertClass
      this.alertIcon = icon
      
      // Tự động ẩn thông báo sau 5 giây
      setTimeout(() => {
        this.alertMessage = ''
      }, 5000)
    },
    
    // Hiển thị thông báo cho đổi mật khẩu
    showPasswordAlert(message, alertClass, icon) {
      this.passwordAlertMessage = message
      this.passwordAlertClass = alertClass
      this.passwordAlertIcon = icon
      
      // Tự động ẩn thông báo sau 5 giây nếu là thông báo thành công
      if (alertClass === 'alert-success') {
        setTimeout(() => {
          this.passwordAlertMessage = ''
        }, 5000)
      }
    },

    // Format date để hiển thị
    formatDate(dateString, showTime = false) {
      if (!dateString) return ''
      
      const date = new Date(dateString)
      const options = { 
        year: 'numeric', 
        month: '2-digit', 
        day: '2-digit' 
      }
      
      if (showTime) {
        options.hour = '2-digit'
        options.minute = '2-digit'
      }
      
      return new Intl.DateTimeFormat('vi-VN', options).format(date)
    }
  }
}
</script>

<style scoped>
.profile-container {
  background-color: #f8f9fa;
  min-height: calc(100vh - 60px);
}

.profile-card {
  border: none;
  border-radius: 12px;
  overflow: hidden;
}

.profile-header {
  background-color: #0a4275;
  color: white;
  padding: 2rem;
}

.password-header {
  background-color: #0a4275;
  color: white;
  padding: 1.5rem 2rem;
}

.profile-header-user {
  background: linear-gradient(135deg, #0a4275 0%, #1565c0 100%);
}

.profile-header-instructor {
  background: linear-gradient(135deg, #0a4275 0%, #ffc107 100%);
}

.profile-avatar {
  font-size: 3rem;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
}

.profile-title {
  font-size: 1.75rem;
  font-weight: 600;
}

.password-title {
  font-size: 1.5rem;
  font-weight: 600;
}

.profile-subtitle {
  font-size: 0.9rem;
  opacity: 0.9;
}

.badge {
  padding: 0.5em 1em;
  font-weight: 500;
  border-radius: 30px;
}

.badge-user {
  background-color: rgba(255, 255, 255, 0.25);
  color: white;
}

.badge-instructor {
  background-color: rgba(255, 193, 7, 0.3);
  color: white;
}

.badge-default {
  background-color: rgba(255, 255, 255, 0.25);
  color: white;
}

.profile-form {
  max-width: 600px;
  margin: 0 auto;
}

.form-label {
  font-weight: 500;
  color: #495057;
}

.input-group-text {
  background-color: #0a4275;
  color: white;
  border: 1px solid #0a4275;
}

.password-toggle {
  cursor: pointer;
  transition: all 0.2s ease;
}

.password-toggle:hover {
  background-color: #083158;
}

.form-control:focus {
  border-color: #0a4275;
  box-shadow: 0 0 0 0.2rem rgba(10, 66, 117, 0.25);
}

.account-info {
  background-color: #f8f9fa;
  border-left: 4px solid #0a4275;
}

.account-info h5 {
  color: #0a4275;
  font-size: 1.1rem;
}

.profile-submit-btn {
  background-color: #0a4275;
  border-color: #0a4275;
  transition: all 0.3s ease;
  padding: 0.5rem 2rem;
  font-weight: 500;
}

.profile-submit-btn:hover {
  background-color: #083158;
  border-color: #083158;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.password-submit-btn {
  background-color: #e67e22;
  border-color: #e67e22;
  transition: all 0.3s ease;
  padding: 0.5rem 2rem;
  font-weight: 500;
  color: white;
}

.password-submit-btn:hover:not([disabled]) {
  background-color: #d35400;
  border-color: #d35400;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.password-requirements {
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 6px;
  font-size: 0.9rem;
  margin-top: 1.5rem;
  border-left: 4px solid #e67e22;
}

.password-requirements h6 {
  color: #e67e22;
  font-weight: 600;
}

.password-requirements ul {
  margin-left: 1.5rem;
  margin-bottom: 0;
}

.password-requirements li {
  margin-bottom: 0.5rem;
}

.password-requirements li:last-child {
  margin-bottom: 0;
}

/* Modal styles */
.modal-header {
  border-bottom: 0;
}

.modal-footer {
  border-top: 0;
}

/* Responsive adjustments */
@media (max-width: 767.98px) {
  .profile-header, .password-header {
    padding: 1.5rem;
  }
  
  .profile-title {
    font-size: 1.5rem;
  }
  
  .password-title {
    font-size: 1.3rem;
  }
  
  .profile-avatar {
    font-size: 2.5rem;
  }
}

@media (max-width: 575.98px) {
  .profile-card {
    border-radius: 0;
    margin-left: -12px;
    margin-right: -12px;
  }
  
  .profile-container {
    background-color: white;
  }
  
  .container {
    padding-left: 0;
    padding-right: 0;
  }
}
</style>