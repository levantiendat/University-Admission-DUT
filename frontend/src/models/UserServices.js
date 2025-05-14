import axios from 'axios'
import config from '@/config/apiConfig'

const BASE_API_URL = config?.BASE_API_URL || 'https://university-admission-dut-hzdahmckevehhpdf.southeastasia-01.azurewebsites.net/api'

const userServices = {
  // Lấy token từ session storage
  getToken() {
    return sessionStorage.getItem('token')
  },

  // Cấu hình headers với token
  getHeaders() {
    return {
      headers: {
        'Authorization': `Bearer ${this.getToken()}`
      }
    }
  },

  // Lấy thông tin cá nhân của người dùng hiện tại
  async getUserInfo() {
    try {
      const response = await axios.get(`${BASE_API_URL}/users/me`, this.getHeaders())
      return response.data
    } catch (error) {
      console.error('Error fetching user info:', error)
      throw error
    }
  },

  // Cập nhật thông tin cá nhân của người dùng
  async updateUserInfo(userData) {
    try {
      const response = await axios.put(`${BASE_API_URL}/users/update`, userData, this.getHeaders())
      return response.data
    } catch (error) {
      console.error('Error updating user info:', error)
      throw error
    }
  },

  // Đổi mật khẩu người dùng
  async changePassword(passwordData) {
    try {
      const response = await axios.post(`${BASE_API_URL}/auth/reset-password`, passwordData, this.getHeaders())
      return response.data
    } catch (error) {
      console.error('Error changing password:', error)
      throw error
    }
  }
}

export default userServices