import axios from 'axios'
import config from '@/config/apiConfig'  // nếu bạn đã tách riêng file cấu hình base API

const BASE_API_URL = config?.BASE_API_URL || 'https://university-admission-dut-hzdahmckevehhpdf.southeastasia-01.azurewebsites.net/api'
// const BASE_API_URL = 'http://127.0.0.1:8000/api'
const HBTHPTService = {
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
   * Lấy danh sách tổ hợp xét tuyển
   * @returns {Promise<Array>} - Danh sách ngành
   */
  getTestTHPTs() {
    return axios.get(`${BASE_API_URL}/university-admissions/admission-method-majors/admission-method/3`)
      .then(response => response.data)
      .catch(error => {
        console.error('Lỗi khi lấy danh sách tổ hợp xét tuyển:', error)
        throw error
      })
  },

}

export default HBTHPTService