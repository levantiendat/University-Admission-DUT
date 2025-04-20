import axios from 'axios'
import config from '@/config/apiConfig'  // nếu bạn đã tách riêng file cấu hình base API

const BASE_API_URL = config?.BASE_API_URL || 'https://university-admission-dut-hzdahmckevehhpdf.southeastasia-01.azurewebsites.net/api'

export default {
  // Lấy danh sách khoa
  async getFaculties() {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-admissions/faculties`)
      return response.data
    } catch (error) {
      console.error('Error fetching faculties:', error)
      throw error
    }
  },

  // Lấy danh sách ngành
  async getMajors() {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-admissions/majors`)
      return response.data
    } catch (error) {
      console.error('Error fetching majors:', error)
      throw error
    }
  },

  // Lấy danh sách phương thức xét tuyển
  async getAdmissionMethods() {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-admissions/admission-methods`)
      return response.data
    } catch (error) {
      console.error('Error fetching admission methods:', error)
      throw error
    }
  },

  // Lấy danh sách điểm chuẩn các năm trước
  async getPreviousAdmissions() {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-admissions/previous-admissions`)
      return response.data
    } catch (error) {
      console.error('Error fetching previous admissions:', error)
      throw error
    }
  }
}