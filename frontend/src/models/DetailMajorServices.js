import axios from 'axios'
import config from '@/config/apiConfig'

const BASE_API_URL = config?.BASE_API_URL || 'https://university-admission-dut-hzdahmckevehhpdf.southeastasia-01.azurewebsites.net/api'

const DetailMajorService = {
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
  },
  
  /**
   * Lấy danh sách tất cả các ngành
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
   * Lấy thông tin chi tiết của một ngành theo ID
   * @param {number} majorId - ID của ngành cần lấy thông tin
   * @returns {Promise<Object>} - Thông tin chi tiết ngành
   */
  getMajorById(majorId) {
    return axios.get(`${BASE_API_URL}/university-admissions/majors/${majorId}`)
      .then(response => response.data)
      .catch(error => {
        console.error(`Lỗi khi lấy thông tin ngành ${majorId}:`, error)
        throw error
      })
  },
  
  /**
   * Lấy danh sách phương thức xét tuyển
   * @returns {Promise<Array>} - Danh sách phương thức xét tuyển
   */
  getAdmissionMethods() {
    return axios.get(`${BASE_API_URL}/university-admissions/admission-methods`)
      .then(response => response.data)
      .catch(error => {
        console.error('Lỗi khi lấy danh sách phương thức xét tuyển:', error)
        throw error
      })
  },
  
  /**
   * Lấy phương thức xét tuyển của một ngành
   * @param {number} majorId - ID của ngành
   * @returns {Promise<Array>} - Danh sách phương thức xét tuyển áp dụng cho ngành
   */
  getMajorAdmissionMethods(majorId) {
    return axios.get(`${BASE_API_URL}/university-admissions/admission-method-majors/major/${majorId}`)
      .then(response => response.data)
      .catch(error => {
        console.error(`Lỗi khi lấy phương thức xét tuyển cho ngành ${majorId}:`, error)
        throw error
      })
  },
  
  /**
   * Lấy danh sách tổ hợp thi
   * @returns {Promise<Array>} - Danh sách tổ hợp thi
   */
  getSubjectGroups() {
    return axios.get(`${BASE_API_URL}/university-admissions/subject-score-method-groups`)
      .then(response => response.data)
      .catch(error => {
        console.error('Lỗi khi lấy danh sách tổ hợp thi:', error)
        throw error
      })
  },
  
  /**
   * Lấy tổ hợp thi áp dụng cho một ngành theo phương thức xét tuyển
   * @param {number} majorId - ID của ngành
   * @param {number} admissionMethodId - ID của phương thức xét tuyển
   * @returns {Promise<Array>} - Danh sách tổ hợp thi áp dụng
   */
  getMajorSubjectGroups(majorId, admissionMethodId) {
    return axios.get(`${BASE_API_URL}/university-admissions/subject-score-method-majors/major/${majorId}/admission-method/${admissionMethodId}`)
      .then(response => response.data)
      .catch(error => {
        console.error(`Lỗi khi lấy tổ hợp thi cho ngành ${majorId} và phương thức ${admissionMethodId}:`, error)
        throw error
      })
  },
  
  /**
   * Lấy danh sách thành tích áp dụng cho một ngành
   * @param {number} majorId - ID của ngành
   * @returns {Promise<Array>} - Danh sách thành tích áp dụng
   */
  getMajorAdmissionDescriptions(majorId) {
    return axios.get(`${BASE_API_URL}/university-admissions/admission-descriptions/major/${majorId}`)
      .then(response => response.data)
      .catch(error => {
        console.error(`Lỗi khi lấy thành tích cho ngành ${majorId}:`, error)
        throw error
      })
  },
  
  /**
   * Lấy điểm chuẩn các năm trước của một ngành
   * @param {number} majorId - ID của ngành
   * @returns {Promise<Array>} - Danh sách điểm chuẩn các năm
   */
  getPreviousAdmissionScores(majorId) {
    return axios.get(`${BASE_API_URL}/university-admissions/previous-admissions/major/${majorId}`)
      .then(response => response.data)
      .catch(error => {
        console.error(`Lỗi khi lấy điểm chuẩn các năm trước cho ngành ${majorId}:`, error)
        throw error
      })
  }
}

export default DetailMajorService