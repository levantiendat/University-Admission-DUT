import axios from 'axios';
import config from '@/config/apiConfig';

const BASE_API_URL = config?.BASE_API_URL || 'https://university-admission-dut-hzdahmckevehhpdf.southeastasia-01.azurewebsites.net/api';

export default {
  /**
   * Lấy danh sách quy đổi điểm
   */
  async getAllConvertPoints() {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-admissions/convert-points`);
      return response.data;
    } catch (error) {
      console.error('Error fetching convert points:', error);
      throw error;
    }
  },

  /**
   * Lấy thông tin chi tiết của một quy đổi điểm
   * @param {number} id - ID của quy đổi điểm
   */
  async getConvertPoint(id) {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-admissions/convert-points/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching convert point ${id}:`, error);
      throw error;
    }
  },

  /**
   * Tạo quy đổi điểm mới
   * @param {Object} data - Dữ liệu quy đổi điểm mới
   */
  async createConvertPoint(data) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.post(`${BASE_API_URL}/university-admissions/convert-points`, data, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error creating convert point:', error);
      throw error;
    }
  },

  /**
   * Cập nhật thông tin quy đổi điểm
   * @param {number} id - ID của quy đổi điểm
   * @param {Object} data - Dữ liệu cập nhật
   */
  async updateConvertPoint(id, data) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.put(`${BASE_API_URL}/university-admissions/convert-points/${id}`, data, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error updating convert point ${id}:`, error);
      throw error;
    }
  },

  /**
   * Xóa quy đổi điểm
   * @param {number} id - ID của quy đổi điểm
   */
  async deleteConvertPoint(id) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.delete(`${BASE_API_URL}/university-admissions/convert-points/${id}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error deleting convert point ${id}:`, error);
      throw error;
    }
  }
};