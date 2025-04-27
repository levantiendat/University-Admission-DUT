import axios from 'axios';
import config from '@/config/apiConfig';

const BASE_API_URL = config?.BASE_API_URL || 'https://university-admission-dut-hzdahmckevehhpdf.southeastasia-01.azurewebsites.net/api';

export default {
  /**
   * Lấy danh sách tất cả các môn thi
   */
  async getAllSubjects() {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-admissions/subjects`);
      return response.data;
    } catch (error) {
      console.error('Error fetching subjects:', error);
      throw error;
    }
  },

  /**
   * Lấy thông tin chi tiết của một môn thi
   * @param {number} subjectId - ID của môn thi
   */
  async getSubject(subjectId) {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-admissions/subjects/${subjectId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching subject ${subjectId}:`, error);
      throw error;
    }
  },

  /**
   * Tạo môn thi mới
   * @param {Object} subjectData - Dữ liệu môn thi mới
   */
  async createSubject(subjectData) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.post(`${BASE_API_URL}/university-admissions/subjects`, subjectData, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error creating subject:', error);
      throw error;
    }
  },

  /**
   * Cập nhật thông tin môn thi
   * @param {number} subjectId - ID của môn thi
   * @param {Object} subjectData - Dữ liệu cập nhật
   */
  async updateSubject(subjectId, subjectData) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.put(`${BASE_API_URL}/university-admissions/subjects/${subjectId}`, subjectData, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error updating subject ${subjectId}:`, error);
      throw error;
    }
  },

  /**
   * Xóa môn thi
   * @param {number} subjectId - ID của môn thi
   */
  async deleteSubject(subjectId) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.delete(`${BASE_API_URL}/university-admissions/subjects/${subjectId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error deleting subject ${subjectId}:`, error);
      throw error;
    }
  }
};