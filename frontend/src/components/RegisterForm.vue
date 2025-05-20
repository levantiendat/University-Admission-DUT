<!-- src/components/RegisterForm.vue -->
<template>
  <form @submit.prevent="submitForm">
    <!-- Ô nhập tên -->
    <div class="input-field mb-3">
      <label for="name" class="visually-hidden">Họ và tên</label>
      <i class="bi bi-person-circle icon"></i>
      <input 
        type="text" 
        id="name" 
        v-model="name" 
        placeholder="Nhập Họ và tên người dùng" 
        required
        aria-required="true"
      />
    </div>
    <!-- Ô nhập email -->
    <div class="input-field mb-3">
      <label for="email" class="visually-hidden">Email</label>
      <i class="bi bi-envelope icon"></i>
      <input 
        type="email" 
        id="email" 
        v-model="email" 
        placeholder="Nhập email" 
        required
        aria-required="true"
      />
    </div>
    <!-- Ô nhập số điện thoại -->
    <div class="input-field mb-3">
      <label for="phone_number" class="visually-hidden">Số điện thoại</label>
      <i class="bi bi-telephone icon"></i>
      <input 
        type="text" 
        id="phone_number" 
        v-model="phone_number" 
        placeholder="Nhập số điện thoại" 
        required
        aria-required="true"
        pattern="^0\d{9}$"
        title="Số điện thoại phải gồm 10 số và bắt đầu bằng số 0"
      />
    </div>
    <!-- Ô nhập mật khẩu -->
    <div class="input-field mb-3">
      <label for="password" class="visually-hidden">Mật khẩu</label>
      <i class="bi bi-lock icon"></i>
      <input 
        type="password" 
        id="password" 
        v-model="password" 
        placeholder="Nhập mật khẩu" 
        required
        aria-required="true"
        minlength="6"
      />
    </div>
    <!-- Nút đăng ký -->
    <button 
      type="submit" 
      class="btn-modern w-100 mt-4"
      aria-label="Đăng ký"
    >
      Đăng ký
    </button>
  </form>
</template>

<script>
export default {
  name: 'RegisterForm',
  data() {
    return {
      name: '',
      email: '',
      phone_number: '',
      password: ''
    }
  },
  methods: {
    submitForm() {
      // Kiểm tra hợp lệ số điện thoại: cần đúng 10 số, bắt đầu bằng số 0
      const phoneRegex = /^0\d{9}$/
      if (!phoneRegex.test(this.phone_number)) {
        alert("Số điện thoại không hợp lệ. Phải gồm 10 số và bắt đầu bằng số 0.")
        return
      }
      // Emit dữ liệu form lên View cha (RegisterView.vue)
      this.$emit('register', {
        name: this.name,
        email: this.email,
        phone_number: this.phone_number,
        password: this.password
      })
    }
  }
}
</script>

<style scoped>
/* Container cho ô input có icon */
.input-field {
  position: relative;
  width: 100%;
  margin-bottom: 20px;
}

.input-field input {
  width: 100%;
  padding: 14px 16px 14px 50px; /* Chừa chỗ cho icon bên trái */
  border: none;
  border-radius: 25px;
  outline: none;
  background-color: rgba(255, 255, 255, 0.15);
  color: white;
  font-size: 1rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.input-field input::placeholder {
  color: rgba(255, 255, 255, 0.7);
}

.input-field input:focus {
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
  background-color: rgba(255, 255, 255, 0.25);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

/* Icon hiển thị bên trái ô input */
.icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.3rem;
  color: rgba(255, 255, 255, 0.8);
  z-index: 1;
}

/* Thiết kế nút hiện đại dùng chung */
.btn-modern {
  display: inline-block;
  padding: 14px 1.5rem;
  font-size: 1.1rem;
  font-weight: 600;
  color: #fff;
  background-image: linear-gradient(135deg, #0B2942, #1261c3);
  border: none;
  border-radius: 30px;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
  text-align: center;
  transition: all 0.3s ease;
  cursor: pointer;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.btn-modern:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25);
  background-image: linear-gradient(135deg, #0d3b69, #3a8dff);
}

.btn-modern:active {
  transform: translateY(0);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

/* Hide labels visually but keep them for screen readers */
.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* Invalid input styling */
.input-field input:invalid:not(:placeholder-shown) {
  border-color: #ff4d6d;
  box-shadow: 0 0 0 2px rgba(255, 77, 109, 0.25);
}

/* Responsive adjustments */
@media (max-width: 576px) {
  .input-field input {
    padding: 12px 16px 12px 45px;
    font-size: 0.95rem;
  }
  
  .btn-modern {
    padding: 12px 1.5rem;
    font-size: 1rem;
  }
}

@media (max-height: 700px) {
  .input-field {
    margin-bottom: 15px;
  }
  
  .input-field input {
    padding: 10px 16px 10px 45px;
  }
  
  .btn-modern {
    padding: 10px 1.5rem;
  }
}
</style>