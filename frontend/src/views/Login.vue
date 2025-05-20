<!-- src/views/LoginView.vue -->
<template>
  <div class="login-overlay">
    <div class="login-container">
      <div class="login-card shadow">
        <!-- Logo added at the top - positioned half in/half out -->
        <div class="logo-container">
          <img src="@/assets/dut_logo.jpg" alt="DUT Logo" class="dut-logo" width="120" height="120"/>
        </div>
        <div class="card-body">
          <h1 class="card-title text-center mb-4">Đăng nhập</h1>
          <!-- Form đăng nhập -->
          <LoginForm @login="onSubmitLogin" />
          <hr>
          <div class="d-grid mb-3">
            <button class="btn btn-outline-light w-100" @click="onGoogleLogin">
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
  metaInfo: {
    title: 'Đăng nhập - Hệ thống tuyển sinh Đại học Bách Khoa Đà Nẵng',
    meta: [
      { name: 'description', content: 'Đăng nhập vào hệ thống tuyển sinh Trường Đại học Bách Khoa - Đại học Đà Nẵng để tra cứu thông tin tuyển sinh và sử dụng các công cụ hỗ trợ.' }
    ]
  },
  data() {
    return {
      alertMessage: '',
      alertClass: '',
      alertIcon: ''
    }
  },
  methods: {
    async onSubmitLogin(formData) {
      try {
        await loginController.handleLogin(formData, this.$router)
      } catch (err) {
        this.showAlert(err, 'alert-danger', 'bi bi-exclamation-circle-fill')
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
    
    // Thêm xử lý focus input đầu tiên khi load trang
    setTimeout(() => {
      const firstInput = document.querySelector('.input-field input')
      if (firstInput) firstInput.focus()
    }, 500)
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
  background: linear-gradient(to bottom, #0B2942 50%, #0d3b69 75%, #1261c3 90%, #3a8dff 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.login-container {
  width: 100%;
  max-width: 400px;
  padding: 1rem;
  margin: 0 auto;
  position: relative;
}

.login-card {
  background: linear-gradient(to top, rgba(255, 255, 255, 0.15), rgba(6, 35, 74, 0.8));
  backdrop-filter: blur(10px);
  border-radius: 16px;
  color: #fff;
  overflow: visible; /* Changed from hidden to allow logo to overflow */
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transform: translateY(0);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  margin-top: 60px; /* Added to make space for the logo */
  position: relative;
}

.login-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5);
}

.logo-container {
  position: absolute;
  top: -60px; /* Positions logo halfway outside the card */
  left: 50%;
  transform: translateX(-50%);
  z-index: 2;
}

.dut-logo {
  width: 120px;
  height: 120px;
  border-radius: 60px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
  border: 3px solid white;
  object-fit: cover;
}

.card-body {
  padding: 2rem;
  padding-top: 4rem; /* Extra padding at top to accommodate logo */
}

.card-title {
  color: white;
  font-weight: 600;
  font-size: 1.8rem;
  letter-spacing: 0.5px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

hr {
  border-color: rgba(255, 255, 255, 0.3);
  margin: 1.5rem 0;
}

.alert {
  margin: 0 2rem 1.5rem 2rem;
  border-radius: 8px;
}

/* Responsive adjustments */
@media (max-width: 767px) {
  .login-container {
    max-width: 90%;
  }
  
  .card-body {
    padding: 1.5rem;
    padding-top: 3.5rem;
  }
}

@media (max-width: 576px) {
  .login-container {
    max-width: 95%;
    padding: 0.5rem;
  }
  
  .card-body {
    padding: 1.25rem;
    padding-top: 3.5rem;
  }
  
  .dut-logo {
    width: 100px;
    height: 100px;
  }
  
  .logo-container {
    top: -50px;
  }
  
  .login-card {
    margin-top: 50px;
  }
  
  .card-title {
    font-size: 1.5rem;
  }
}

@media (max-height: 700px) {
  .card-body {
    padding: 1rem 1.5rem;
    padding-top: 3rem;
  }
  
  .dut-logo {
    width: 90px;
    height: 90px;
  }
  
  .logo-container {
    top: -45px;
  }
  
  .login-card {
    margin-top: 45px;
  }
}
</style>