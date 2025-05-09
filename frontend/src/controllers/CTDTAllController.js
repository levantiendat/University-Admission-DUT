import CTDTAllServices from '@/models/CTDTAllServices'

const CTDTAllController = {
  /**
   * Lấy danh sách tất cả các khoa
   * @returns {Promise<Array>} - Danh sách khoa
   */
  async getFaculties() {
    try {
      const faculties = await CTDTAllServices.getFaculties()
      return faculties
    } catch (error) {
      console.error('Lỗi controller khi lấy danh sách khoa:', error)
      throw error
    }
  }
}

export default CTDTAllController