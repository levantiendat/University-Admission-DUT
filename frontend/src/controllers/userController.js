import qnaService from '@/models/qnaService'

export default {
  async getCurrentUser() {
    try {
      const user = await qnaService.getCurrentUser()
      // Lưu thông tin người dùng vào sessionStorage để sử dụng xuyên suốt ứng dụng
      sessionStorage.setItem('user', JSON.stringify(user))
      return user
    } catch (error) {
      console.error('Error in getCurrentUser controller:', error)
      throw error
    }
  }
}