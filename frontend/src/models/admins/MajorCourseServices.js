import axios from 'axios';
import config from '@/config/apiConfig';

const BASE_API_URL = config?.BASE_API_URL || 'https://university-admission-dut-hzdahmckevehhpdf.southeastasia-01.azurewebsites.net/api';

export default {
  /**
   * Lấy danh sách khung chương trình đào tạo
   */
  async getAllMajorCourses() {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-educations/major_courses`);
      return response.data;
    } catch (error) {
      console.error('Error fetching major courses:', error);
      throw error;
    }
  },

  /**
   * Lấy thông tin chi tiết của một khung chương trình đào tạo
   * @param {number} id - ID của khung chương trình
   */
  async getMajorCourse(id) {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-educations/major_courses/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching major course ${id}:`, error);
      throw error;
    }
  },

  /**
   * Tạo khung chương trình đào tạo mới
   * @param {Object} data - Dữ liệu khung chương trình mới
   */
  async createMajorCourse(data) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.post(`${BASE_API_URL}/university-educations/major_courses`, data, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error creating major course:', error);
      throw error;
    }
  },

  /**
   * Cập nhật thông tin khung chương trình đào tạo
   * @param {number} id - ID của khung chương trình
   * @param {Object} data - Dữ liệu cập nhật
   */
  async updateMajorCourse(id, data) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.put(`${BASE_API_URL}/university-educations/major_courses/${id}`, data, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error updating major course ${id}:`, error);
      throw error;
    }
  },

  /**
   * Xóa khung chương trình đào tạo
   * @param {number} id - ID của khung chương trình
   */
  async deleteMajorCourse(id) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.delete(`${BASE_API_URL}/university-educations/major_courses/${id}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error deleting major course ${id}:`, error);
      throw error;
    }
  },
  /**
   * Lấy danh sách chi tiết khung chương trình theo major_course_id
   * @param {number} majorCourseId - ID của khung chương trình
   */
  async getMajorCourseDetailsById(majorCourseId) {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-educations/major_course_details_by_major_course_id?major_course_id=${majorCourseId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching major course details for ID ${majorCourseId}:`, error);
      throw error;
    }
  },

  /**
   * Lấy chi tiết một major_course_detail cụ thể
   * @param {number} id - ID của major course detail
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
   * Thêm học phần vào khung chương trình (tạo major_course_detail mới)
   * @param {Object} data - Dữ liệu thêm học phần
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
   * Cập nhật thông tin chi tiết học phần trong khung chương trình
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
   * Xóa học phần khỏi khung chương trình
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
  async getAllPriorCourses() {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-educations/course_prior_courses`);
      return response.data;
    } catch (error) {
      console.error('Error fetching prior courses:', error);
      throw error;
    }
  },

  /**
   * Thêm mối quan hệ học trước
   * @param {Object} data - Dữ liệu mối quan hệ học trước
   */
  async createPriorCourse(data) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.post(`${BASE_API_URL}/university-educations/course_prior_courses`, data, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error creating prior course relationship:', error);
      throw error;
    }
  },

  /**
   * Xóa mối quan hệ học trước
   * @param {number} id - ID của mối quan hệ học trước
   */
  async deletePriorCourse(id) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.delete(`${BASE_API_URL}/university-educations/course_prior_courses/${id}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error deleting prior course relationship ${id}:`, error);
      throw error;
    }
  },

  /**
   * Lấy danh sách mối quan hệ tiên quyết
   */
  async getAllPrerequisites() {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-educations/course_prerequisites`);
      return response.data;
    } catch (error) {
      console.error('Error fetching prerequisites:', error);
      throw error;
    }
  },

  /**
   * Thêm mối quan hệ tiên quyết
   * @param {Object} data - Dữ liệu mối quan hệ tiên quyết
   */
  async createPrerequisite(data) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.post(`${BASE_API_URL}/university-educations/course_prerequisites`, data, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error creating prerequisite relationship:', error);
      throw error;
    }
  },

  /**
   * Xóa mối quan hệ tiên quyết
   * @param {number} id - ID của mối quan hệ tiên quyết
   */
  async deletePrerequisite(id) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.delete(`${BASE_API_URL}/university-educations/course_prerequisites/${id}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error deleting prerequisite relationship ${id}:`, error);
      throw error;
    }
  },

  /**
   * Lấy danh sách mối quan hệ song hành
   */
  async getAllCorequisites() {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-educations/course_corequisites`);
      return response.data;
    } catch (error) {
      console.error('Error fetching corequisites:', error);
      throw error;
    }
  },

  /**
   * Thêm mối quan hệ song hành
   * @param {Object} data - Dữ liệu mối quan hệ song hành
   */
  async createCorequisite(data) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.post(`${BASE_API_URL}/university-educations/course_corequisites`, data, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error creating corequisite relationship:', error);
      throw error;
    }
  },

  /**
   * Xóa mối quan hệ song hành
   * @param {number} id - ID của mối quan hệ song hành
   */
  async deleteCorequisite(id) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.delete(`${BASE_API_URL}/university-educations/course_corequisites/${id}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error deleting corequisite relationship ${id}:`, error);
      throw error;
    }
  }
};