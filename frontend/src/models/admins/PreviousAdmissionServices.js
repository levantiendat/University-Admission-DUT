import axios from 'axios';
import config from '@/config/apiConfig';

const BASE_API_URL = config?.BASE_API_URL || 'https://university-admission-dut-hzdahmckevehhpdf.southeastasia-01.azurewebsites.net/api';

export default {
  /**
   * Lấy danh sách điểm chuẩn các năm trước
   */
  async getAllPreviousAdmissions() {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-admissions/previous-admissions`);
      return response.data;
    } catch (error) {
      console.error('Error fetching previous admissions:', error);
      throw error;
    }
  },

  /**
   * Lấy thông tin chi tiết của một điểm chuẩn năm trước
   * @param {number} id - ID của điểm chuẩn
   */
  async getPreviousAdmission(id) {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-admissions/previous-admissions/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching previous admission ${id}:`, error);
      throw error;
    }
  },

  /**
   * Tạo điểm chuẩn năm trước mới
   * @param {Object} data - Dữ liệu điểm chuẩn mới
   */
  async createPreviousAdmission(data) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.post(`${BASE_API_URL}/university-admissions/previous-admissions`, data, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error creating previous admission:', error);
      throw error;
    }
  },

  /**
   * Cập nhật thông tin điểm chuẩn năm trước
   * @param {number} id - ID của điểm chuẩn
   * @param {Object} data - Dữ liệu cập nhật
   */
  async updatePreviousAdmission(id, data) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.put(`${BASE_API_URL}/university-admissions/previous-admissions/${id}`, data, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error updating previous admission ${id}:`, error);
      throw error;
    }
  },

  /**
   * Xóa điểm chuẩn năm trước
   * @param {number} id - ID của điểm chuẩn
   */
  async deletePreviousAdmission(id) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.delete(`${BASE_API_URL}/university-admissions/previous-admissions/${id}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error deleting previous admission ${id}:`, error);
      throw error;
    }
  }
};