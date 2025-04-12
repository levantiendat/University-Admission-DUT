// src/controllers/registerController.js

import authService from '@/models/authService'

export default {
  async handleRegister(formData, router) {
    // Kiểm tra hợp lệ số điện thoại
    const phoneRegex = /^0\d{9}$/
    if (!phoneRegex.test(formData.phone_number)) {
      throw "Số điện thoại không hợp lệ. Phải gồm 10 số và bắt đầu bằng số 0."
    }
    try {
      const response = await authService.register(formData)
      const token = response.data.access_token
      // Lưu token (nếu cần, ví dụ qua Vuex/LocalStorage) và chuyển hướng
      router.push({ name: 'Callback', query: { token } })
    } catch (error) {
      console.error(error)
      // Đưa ra thông báo lỗi thích hợp
      throw error.response?.data?.detail || "Đăng ký thất bại"
    }
  }
}
