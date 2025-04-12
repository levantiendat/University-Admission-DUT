<!-- src/components/RegisterForm.vue -->
<template>
  <form @submit.prevent="submitForm">
    <!-- Ô nhập tên -->
    <div class="input-field mb-3">
      <i class="bi bi-person-circle icon"></i>
      <input 
        type="text" 
        id="name" 
        v-model="name" 
        placeholder="Nhập Họ và tên người dùng" 
        required
      />
    </div>
    <!-- Ô nhập email -->
    <div class="input-field mb-3">
      <i class="bi bi-envelope icon"></i>
      <input 
        type="email" 
        id="email" 
        v-model="email" 
        placeholder="Nhập email" 
        required
      />
    </div>
    <!-- Ô nhập số điện thoại -->
    <div class="input-field mb-3">
      <i class="bi bi-telephone icon"></i>
      <input 
        type="text" 
        id="phone_number" 
        v-model="phone_number" 
        placeholder="Nhập số điện thoại" 
        required
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
        required
      />
    </div>
    <!-- Nút đăng ký -->
    <button type="submit" class="btn-modern w-100 mt-3">
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
}

.input-field input {
  width: 100%;
  padding: 12px 16px 12px 44px; /* Chừa chỗ cho icon bên trái */
  border: none;
  border-radius: 25px;
  outline: none;
  background-color: #fff;
  font-size: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.2s;
}

.input-field input:focus {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

/* Icon hiển thị bên trái ô input */
.icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.2rem;
  color: #888;
}

/* Thiết kế nút hiện đại dùng chung */
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
