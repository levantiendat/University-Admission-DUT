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
  }
};