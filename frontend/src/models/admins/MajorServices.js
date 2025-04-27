import axios from 'axios';
import config from '@/config/apiConfig';

const BASE_API_URL = config?.BASE_API_URL || 'https://university-admission-dut-hzdahmckevehhpdf.southeastasia-01.azurewebsites.net/api';

export default {
  /**
   * Lấy danh sách tất cả ngành học
   */
  async getAllMajors() {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-admissions/majors`);
      return response.data;
    } catch (error) {
      console.error('Error fetching majors:', error);
      throw error;
    }
  },

  /**
   * Lấy thông tin chi tiết của một ngành học
   * @param {number} majorId - ID của ngành học
   */
  async getMajor(majorId) {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-admissions/majors/${majorId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching major ${majorId}:`, error);
      throw error;
    }
  },

  /**
   * Lấy danh sách ngành học theo khoa
   * @param {number} facultyId - ID của khoa
   */
  async getMajorsByFaculty(facultyId) {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-admissions/majors/faculty/${facultyId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching majors for faculty ${facultyId}:`, error);
      throw error;
    }
  },

  /**
   * Tạo ngành học mới
   * @param {Object} majorData - Dữ liệu ngành học mới
   */
  async createMajor(majorData) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.post(`${BASE_API_URL}/university-admissions/majors`, majorData, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error creating major:', error);
      throw error;
    }
  },

  /**
   * Cập nhật thông tin ngành học
   * @param {number} majorId - ID của ngành học
   * @param {Object} majorData - Dữ liệu cập nhật
   */
  async updateMajor(majorId, majorData) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.put(`${BASE_API_URL}/university-admissions/majors/${majorId}`, majorData, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error updating major ${majorId}:`, error);
      throw error;
    }
  },

  /**
   * Xóa ngành học
   * @param {number} majorId - ID của ngành học
   */
  async deleteMajor(majorId) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.delete(`${BASE_API_URL}/university-admissions/majors/${majorId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error deleting major ${majorId}:`, error);
      throw error;
    }
  }
};