<!-- src/views/LoginView.vue -->
<template>
  <div class="login-overlay">
    <div class="login-container">
      <div class="login-card shadow">
        <div class="card-body">
          <h2 class="card-title text-center mb-4 text-white">Đăng nhập</h2>
          <!-- Form đăng nhập -->
          <LoginForm @login="onSubmitLogin" />
          <hr>
          <div class="d-grid mb-3">
            <button class="btn btn-outline-light" @click="onGoogleLogin">
              <i class="bi bi-google"></i> Đăng nhập bằng Google
            </button>
          </div>
          <!-- Nút chuyển sang trang đăng ký -->
          <div class="text-center">
            <router-link to="/register" class="btn btn-link text-white">
              Chưa có tài khoản? Đăng ký ngay
            </router-link>
          </div>
        </div>
        <div v-if="alertMessage" class="alert" :class="alertClass" role="alert">
          <i :class="alertIcon" class="me-2"></i>
          {{ alertMessage }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import LoginForm from '@/components/LoginForm.vue'
import loginController from '@/controllers/loginController.js'

export default {
  name: 'LoginView',
  components: { LoginForm },
  methods: {
    async onSubmitLogin(formData) {
      try {
        await loginController.handleLogin(formData, this.$router)
      } catch (err) {
        alert(err)
      }
    },
    onGoogleLogin() {
      const googleUrl = loginController.handleGoogleLogin()
      window.location.href = googleUrl
    },
    showAlert(message, alertClass, icon) {
      this.alertMessage = message
      this.alertClass = alertClass
      this.alertIcon = icon
      
      // Tự động ẩn thông báo sau 5 giây
      setTimeout(() => {
        this.alertMessage = ''
      }, 5000)
    },
  },
  mounted() {
    // Kiểm tra nếu có thông báo redirect từ trang đổi mật khẩu
    const message = this.$route.query.message
    if (message === 'password_changed') {
      this.showAlert('Mật khẩu đã được thay đổi thành công. Vui lòng đăng nhập lại với mật khẩu mới.', 'alert-success', 'bi bi-check-circle-fill')
    }
  },
}
</script>

<style scoped>
.login-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background: #0B2942; /* nền xanh dương đậm */
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.login-container {
  width: 100%;
  max-width: 500px;
  padding: 1rem;
}

.login-card {
  background-color: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(8px);
  border-radius: 8px;
  color: #fff;
}

.card-body {
  padding: 2rem;
}
</style>
