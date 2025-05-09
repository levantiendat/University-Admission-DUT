import axios from 'axios'
import config from '@/config/apiConfig'

const BASE_API_URL = config?.BASE_API_URL || 'https://university-admission-dut-hzdahmckevehhpdf.southeastasia-01.azurewebsites.net/api'

const CTDTAllServices = {
  /**
   * Lấy danh sách tất cả các khoa
   * @returns {Promise<Array>} - Danh sách khoa
   */
  getFaculties() {
    return axios.get(`${BASE_API_URL}/university-admissions/faculties`)
      .then(response => response.data)
      .catch(error => {
        console.error('Lỗi khi lấy danh sách khoa:', error)
        throw error
      })
  }
}

export default CTDTAllServices