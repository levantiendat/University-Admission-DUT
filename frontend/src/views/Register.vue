<!-- src/views/RegisterView.vue -->
<template>
  <div class="register-overlay">
    <div class="register-container">
      <div class="register-card shadow">
        <div class="card-body">
          <h2 class="card-title text-center mb-4 text-white">Đăng ký</h2>
          <!-- Form đăng ký -->
          <RegisterForm @register="onSubmitRegister" />
          <!-- Nút chuyển sang trang đăng nhập -->
          <div class="text-center mt-3">
            <router-link to="/login" class="btn btn-link text-white">
              Đã có tài khoản? Đăng nhập ngay
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import RegisterForm from '@/components/RegisterForm.vue'
import registerController from '@/controllers/registerController.js'

export default {
  name: 'RegisterView',
  components: { RegisterForm },
  methods: {
    async onSubmitRegister(formData) {
      try {
        await registerController.handleRegister(formData, this.$router)
      } catch (err) {
        alert(err)
      }
    }
  }
}
</script>

<style scoped>
.register-overlay {
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

.register-container {
  width: 100%;
  max-width: 500px;
  padding: 1rem;
}

.register-card {
  background-color: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(8px);
  border-radius: 8px;
  color: #fff;
}

.card-body {
  padding: 2rem;
}
</style>
