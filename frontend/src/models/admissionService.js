import axios from 'axios'
import config from '@/config/apiConfig'  // nếu bạn đã tách riêng file cấu hình base API

const BASE_API_URL = config?.BASE_API_URL || 'https://university-admission-dut-hzdahmckevehhpdf.southeastasia-01.azurewebsites.net/api'

const admissionService = {
  /**
   * Lấy danh sách ngành tuyển sinh
   * @returns {Promise<Array>} - Danh sách ngành
   */
  getMajors() {
    return axios.get(`${BASE_API_URL}/university-admissions/majors`)
      .then(response => response.data)
      .catch(error => {
        console.error('Lỗi khi lấy danh sách ngành:', error)
        throw error
      })
  },

  /**
   * Lấy danh sách phương thức tuyển sinh
   * @returns {Promise<Array>} - Danh sách phương thức tuyển sinh
   */
  getAdmissionMethods() {
    return axios.get(`${BASE_API_URL}/university-admissions/admission-methods`)
      .then(response => response.data)
      .catch(error => {
        console.error('Lỗi khi lấy danh sách phương thức tuyển sinh:', error)
        throw error
      })
  },

  /**
   * Lấy thông tin về phương thức tuyển sinh của từng ngành
   * @returns {Promise<Array>} - Danh sách quan hệ ngành-phương thức
   */
  getAdmissionMethodMajors() {
    return axios.get(`${BASE_API_URL}/university-admissions/admission-method-majors`)
      .then(response => response.data)
      .catch(error => {
        console.error('Lỗi khi lấy thông tin phương thức tuyển sinh của ngành:', error)
        throw error
      })
  }
}

export default admissionService