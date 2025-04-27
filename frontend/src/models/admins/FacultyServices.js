import axios from 'axios';
import config from '@/config/apiConfig';

const BASE_API_URL = config?.BASE_API_URL || 'https://university-admission-dut-hzdahmckevehhpdf.southeastasia-01.azurewebsites.net/api';

export default {
  /**
   * Lấy danh sách tất cả khoa
   */
  async getAllFaculties() {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-admissions/faculties`);
      return response.data;
    } catch (error) {
      console.error('Error fetching faculties:', error);
      throw error;
    }
  },

  /**
   * Lấy thông tin chi tiết của một khoa
   * @param {number} facultyId - ID của khoa
   */
  async getFaculty(facultyId) {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-admissions/faculties/${facultyId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching faculty ${facultyId}:`, error);
      throw error;
    }
  },

  /**
   * Tạo khoa mới
   * @param {Object} facultyData - Dữ liệu khoa mới
   */
  async createFaculty(facultyData) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.post(`${BASE_API_URL}/university-admissions/faculties`, facultyData, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error creating faculty:', error);
      throw error;
    }
  },

  /**
   * Cập nhật thông tin khoa
   * @param {number} facultyId - ID của khoa
   * @param {Object} facultyData - Dữ liệu cập nhật
   */
  async updateFaculty(facultyId, facultyData) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.put(`${BASE_API_URL}/university-admissions/faculties/${facultyId}`, facultyData, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error updating faculty ${facultyId}:`, error);
      throw error;
    }
  },

  /**
   * Xóa khoa
   * @param {number} facultyId - ID của khoa
   */
  async deleteFaculty(facultyId) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.delete(`${BASE_API_URL}/university-admissions/faculties/${facultyId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error deleting faculty ${facultyId}:`, error);
      throw error;
    }
  }
};