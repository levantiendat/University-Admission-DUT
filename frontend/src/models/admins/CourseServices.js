import axios from 'axios';
import config from '@/config/apiConfig';

const BASE_API_URL = config?.BASE_API_URL || 'https://university-admission-dut-hzdahmckevehhpdf.southeastasia-01.azurewebsites.net/api';

export default {
  /**
   * Lấy danh sách lớp học phần
   */
  async getAllCourses() {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-educations/courses`);
      return response.data;
    } catch (error) {
      console.error('Error fetching courses:', error);
      throw error;
    }
  },

  /**
   * Lấy thông tin chi tiết của một lớp học phần
   * @param {number} id - ID của lớp học phần
   */
  async getCourse(id) {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-educations/courses/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching course ${id}:`, error);
      throw error;
    }
  },

  /**
   * Tạo lớp học phần mới
   * @param {Object} data - Dữ liệu lớp học phần mới
   */
  async createCourse(data) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.post(`${BASE_API_URL}/university-educations/courses`, data, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error creating course:', error);
      throw error;
    }
  },

  /**
   * Cập nhật thông tin lớp học phần
   * @param {number} id - ID của lớp học phần
   * @param {Object} data - Dữ liệu cập nhật
   */
  async updateCourse(id, data) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.put(`${BASE_API_URL}/university-educations/courses/${id}`, data, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error updating course ${id}:`, error);
      throw error;
    }
  },

  /**
   * Xóa lớp học phần
   * @param {number} id - ID của lớp học phần
   */
  async deleteCourse(id) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.delete(`${BASE_API_URL}/university-educations/courses/${id}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error deleting course ${id}:`, error);
      throw error;
    }
  }
};