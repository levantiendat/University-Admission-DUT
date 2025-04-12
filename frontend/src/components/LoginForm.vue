<!-- src/components/LoginForm.vue -->
<template>
  <form @submit.prevent="submitForm">
    <!-- Ô nhập email -->
    <div class="input-field mb-3">
      <i class="bi bi-envelope icon"></i>
      <input 
        type="email" 
        id="email" 
        v-model="email" 
        placeholder="Nhập email"
      />
    </div>
    <!-- Ô nhập mật khẩu -->
    <div class="input-field mb-3">
      <i class="bi bi-lock icon"></i>
      <input 
        type="password" 
        id="password" 
        v-model="password" 
        placeholder="Nhập mật khẩu"
      />
    </div>
    <!-- Nút đăng nhập -->
    <button 
      type="submit" 
      class="btn-modern w-100 mt-3"
    >
      Đăng nhập
    </button>
  </form>
</template>

<script>
export default {
  name: 'LoginForm',
  data() {
    return {
      email: '',
      password: ''
    }
  },
  methods: {
    submitForm() {
      // Emit sự kiện 'login' kèm dữ liệu lên View cha (LoginView.vue)
      this.$emit('login', {
        email: this.email,
        password: this.password
      })
    }
  }
}
</script>

<style scoped>
/* Reset margin của input-field nếu cần */
.input-field {
  position: relative;
  width: 100%;
}

/* Style cho ô input */
.input-field input {
  width: 100%;
  padding: 12px 16px 12px 44px; /* Chừa không gian cho icon ở bên trái */
  border: none;
  border-radius: 25px;
  outline: none;
  background-color: #fff;
  font-size: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.2s;
}

/* Thay đổi shadow khi input được focus */
.input-field input:focus {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

/* Icon bên trái hiển thị bên trong input */
.icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.2rem;
  color: #888;
}

/* Thiết kế nút đăng nhập hiện đại */
.btn-modern {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  font-size: 1.1rem;
  font-weight: 500;
  color: #fff;
  background-image: linear-gradient(135deg, #3b8dff, #004aad);
  border: none;
  border-radius: 25px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
}

.btn-modern:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
}

.btn-modern:active {
  transform: translateY(0);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
