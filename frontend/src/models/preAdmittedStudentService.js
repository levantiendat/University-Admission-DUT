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

  async getCities() {
    try {
      const response = await axios.get(`${BASE_API_URL}/priorities/cities`)
      return response.data
    } catch (error) {
      console.error('Error fetching cities:', error)
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


  //Lấy danh sách thống kê sinh viên các năm trước:
  async getPreviousAdmissionStudentByGender() {
    try {
      const response = await axios.get(`${BASE_API_URL}/admitted_students/stats/gender`)
      return response.data
    } catch (error) {
      console.error('Error fetching:', error)
      throw error
    }
  },

  //Lấy danh sách thống kê sinh viên theo Thành phố sinh sống
  async getPreviousAdmissionStudentByCity() {
    try {
      const response = await axios.get(`${BASE_API_URL}/admitted_students/stats/city`)
      return response.data
    } catch (error) {
      console.error('Error fetching:', error)
      throw error
    }
  },

  //Lấy danh sách thống kê sinh viên theo Phương thức trúng tuyển:
    async getPreviousAdmissionStudentByAdmissionMethod() {
        try {
        const response = await axios.get(`${BASE_API_URL}/admitted_students/stats/admission_method`)
        return response.data
        } catch (error) {
        console.error('Error fetching:', error)
        throw error
        }
    },

    //Lấy danh sách thống kê sinh viên theo khoản điểm trúng tuyển mỗi ngành:
    async getPreviousAdmissionStudentByMajorRangePoint() {
        try {
        const response = await axios.get(`${BASE_API_URL}/admitted_students/stats/score_range`)
        return response.data
        } catch (error) {
        console.error('Error fetching:', error)
        throw error
        }
    },
}