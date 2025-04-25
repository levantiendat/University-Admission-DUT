import axios from 'axios'
import config from '@/config/apiConfig'  // nếu bạn đã tách riêng file cấu hình base API

const BASE_API_URL = config?.BASE_API_URL || 'https://university-admission-dut-hzdahmckevehhpdf.southeastasia-01.azurewebsites.net/api'

export default {
  /**
   * Lấy thông tin khoa theo ID
   * @param {number} facultyId - ID của khoa
   * @returns {Promise} - Promise trả về thông tin khoa
   */
  getFacultyById(facultyId) {
    return axios.get(`${BASE_API_URL}/university-admissions/faculties/${facultyId}`)
  },

  /**
   * Lấy danh sách ngành theo khoa
   * @param {number} facultyId - ID của khoa
   * @returns {Promise} - Promise trả về danh sách ngành
   */
  getMajorsByFaculty(facultyId) {
    return axios.get(`${BASE_API_URL}/university-admissions/majors/faculty/${facultyId}`)
  },

  /**
   * Lấy danh sách chương trình đào tạo theo ngành
   * @param {number} majorId - ID của ngành
   * @returns {Promise} - Promise trả về danh sách chương trình đào tạo
   */
  getMajorCoursesByMajorId(majorId) {
    return axios.get(`${BASE_API_URL}/university-educations/major_courses_by_major_id`, {
      params: {
        major_id: majorId
      }
    })
  },

  /**
   * Lấy chi tiết chương trình đào tạo theo ID chương trình
   * @param {number} majorCourseId - ID của chương trình đào tạo
   * @returns {Promise} - Promise trả về chi tiết chương trình đào tạo
   */
  getMajorCourseDetailsByMajorCourseId(majorCourseId) {
    return axios.get(`${BASE_API_URL}/university-educations/major_course_details_by_major_course_id`, {
      params: {
        major_course_id: majorCourseId
      }
    })
  }
}