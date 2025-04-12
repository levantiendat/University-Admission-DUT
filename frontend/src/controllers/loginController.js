// src/controllers/loginController.js

import authService from '@/models/authService'

export default {
  async handleLogin(formData, router) {
    try {
      const response = await authService.login(formData.email, formData.password)
      const token = response.data.access_token

      // Thay vì lưu token trực tiếp, chuyển hướng đến trang callback với token trong query
      router.push({ name: 'Callback', query: { token } })
    } catch (error) {
      console.error(error)
      // Tuỳ backend, bạn có thể thay detail bằng field khác
      throw error.response?.data?.detail || "Đăng nhập thất bại"
    }
  },

  handleGoogleLogin() {
    // Trả về đường dẫn Google OAuth
    return authService.googleLoginUrl()
  }
}
