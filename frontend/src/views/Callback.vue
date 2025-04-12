<!-- src/views/Callback.vue -->
<template>
    <div class="callback">
      <p>Đang xử lý đăng nhập...</p>
    </div>
  </template>
  
  <script>
  import store from '@/store'
  
  export default {
    mounted() {
      // Lấy token từ query param (ví dụ: /callback?token=...)
      const token = this.$route.query.token
      if (token) {
        store.setToken(token)
        // Sau khi lưu token, chuyển hướng đến trang Home
        this.$router.push({ name: 'Home' })
      } else {
        // Nếu không có token, chuyển hướng về trang đăng nhập
        this.$router.push({ name: 'Login' })
      }
    }
  }
  </script>
  
  <style scoped>
  .callback {
    text-align: center;
    margin-top: 50px;
    font-size: 1.2em;
  }
  </style>
  