import axios from 'axios';
import config from '@/config/apiConfig';

const BASE_API_URL = config?.BASE_API_URL || 'https://university-admission-dut-hzdahmckevehhpdf.southeastasia-01.azurewebsites.net/api';

export default {
  /**
   * Lấy tất cả chi tiết khung chương trình đào tạo
   */
  async getAllMajorCourseDetails() {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-educations/major_course_details`);
      return response.data;
    } catch (error) {
      console.error('Error fetching all major course details:', error);
      throw error;
    }
  },

  /**
   * Lấy chi tiết khung chương trình đào tạo theo ID khung chương trình
   * @param {number} majorCourseId - ID của khung chương trình đào tạo
   */
  async getMajorCourseDetailsByMajorCourseId(majorCourseId) {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-educations/major_course_details_by_major_course_id`, {
        params: { major_course_id: majorCourseId }
      });
      return response.data;
    } catch (error) {
      console.error(`Error fetching major course details for major course ${majorCourseId}:`, error);
      throw error;
    }
  },

  /**
   * Lấy chi tiết một học phần trong khung chương trình đào tạo
   * @param {number} id - ID của chi tiết học phần
   */
  async getMajorCourseDetail(id) {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-educations/major_course_details/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching major course detail ${id}:`, error);
      throw error;
    }
  },

  /**
   * Tạo chi tiết học phần mới trong khung chương trình đào tạo
   * @param {Object} data - Dữ liệu chi tiết học phần
   */
  async createMajorCourseDetail(data) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.post(`${BASE_API_URL}/university-educations/major_course_details`, data, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error creating major course detail:', error);
      throw error;
    }
  },

  /**
   * Cập nhật chi tiết học phần trong khung chương trình đào tạo
   * @param {number} id - ID của chi tiết học phần
   * @param {Object} data - Dữ liệu cập nhật
   */
  async updateMajorCourseDetail(id, data) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.put(`${BASE_API_URL}/university-educations/major_course_details/${id}`, data, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error updating major course detail ${id}:`, error);
      throw error;
    }
  },

  /**
   * Xóa chi tiết học phần trong khung chương trình đào tạo
   * @param {number} id - ID của chi tiết học phần
   */
  async deleteMajorCourseDetail(id) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.delete(`${BASE_API_URL}/university-educations/major_course_details/${id}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error deleting major course detail ${id}:`, error);
      throw error;
    }
  },

  /**
   * Lấy danh sách mối quan hệ học trước
   */
  async getAllCoursePriorCourses() {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-educations/course_prior_courses`);
      return response.data;
    } catch (error) {
      console.error('Error fetching course prior courses:', error);
      throw error;
    }
  },

  /**
   * Tạo mới mối quan hệ học trước
   * @param {Object} data - Dữ liệu mối quan hệ học trước
   */
  async createCoursePriorCourse(data) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.post(`${BASE_API_URL}/university-educations/course_prior_courses`, data, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error creating course prior course:', error);
      throw error;
    }
  },

  /**
   * Xóa mối quan hệ học trước
   * @param {number} id - ID của mối quan hệ học trước
   */
  async deleteCoursePriorCourse(id) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.delete(`${BASE_API_URL}/university-educations/course_prior_courses/${id}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error deleting course prior course ${id}:`, error);
      throw error;
    }
  },

  /**
   * Lấy danh sách mối quan hệ học tiên quyết
   */
  async getAllCoursePrerequisites() {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-educations/course_prerequisites`);
      return response.data;
    } catch (error) {
      console.error('Error fetching course prerequisites:', error);
      throw error;
    }
  },

  /**
   * Tạo mới mối quan hệ học tiên quyết
   * @param {Object} data - Dữ liệu mối quan hệ học tiên quyết
   */
  async createCoursePrerequisite(data) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.post(`${BASE_API_URL}/university-educations/course_prerequisites`, data, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error creating course prerequisite:', error);
      throw error;
    }
  },

  /**
   * Xóa mối quan hệ học tiên quyết
   * @param {number} id - ID của mối quan hệ học tiên quyết
   */
  async deleteCoursePrerequisite(id) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.delete(`${BASE_API_URL}/university-educations/course_prerequisites/${id}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error deleting course prerequisite ${id}:`, error);
      throw error;
    }
  },

  /**
   * Lấy danh sách mối quan hệ học song hành
   */
  async getAllCourseCorequisites() {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-educations/course_corequisites`);
      return response.data;
    } catch (error) {
      console.error('Error fetching course corequisites:', error);
      throw error;
    }
  },

  /**
   * Tạo mới mối quan hệ học song hành
   * @param {Object} data - Dữ liệu mối quan hệ học song hành
   */
  async createCourseCorequisite(data) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.post(`${BASE_API_URL}/university-educations/course_corequisites`, data, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error creating course corequisite:', error);
      throw error;
    }
  },

  /**
   * Xóa mối quan hệ học song hành
   * @param {number} id - ID của mối quan hệ học song hành
   */
  async deleteCourseCorequisite(id) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.delete(`${BASE_API_URL}/university-educations/course_corequisites/${id}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error deleting course corequisite ${id}:`, error);
      throw error;
    }
  }
};