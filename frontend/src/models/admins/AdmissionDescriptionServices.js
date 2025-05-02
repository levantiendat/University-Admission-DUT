import axios from 'axios';
import config from '@/config/apiConfig';

const BASE_API_URL = config?.BASE_API_URL || 'https://university-admission-dut-hzdahmckevehhpdf.southeastasia-01.azurewebsites.net/api';

export default {
  /**
   * Lấy danh sách môn học / lĩnh vực xét tuyển của tất cả các ngành
   */
  async getAllAdmissionDescriptions() {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-admissions/admission-descriptions`);
      return response.data;
    } catch (error) {
      console.error('Error fetching admission descriptions:', error);
      throw error;
    }
  },

  /**
   * Lấy danh sách môn học / lĩnh vực xét tuyển của một ngành cụ thể
   * @param {number} majorId - ID của ngành
   */
  async getAdmissionDescriptionsByMajor(majorId) {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-admissions/admission-descriptions`);
      // Lọc kết quả theo major_id
      const filteredData = response.data.filter(item => item.major_id === parseInt(majorId));
      return filteredData;
    } catch (error) {
      console.error(`Error fetching admission descriptions for major ${majorId}:`, error);
      throw error;
    }
  },

  /**
   * Lấy thông tin chi tiết của một mô tả xét tuyển
   * @param {number} id - ID của mô tả xét tuyển
   */
  async getAdmissionDescription(id) {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-admissions/admission-descriptions/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching admission description ${id}:`, error);
      throw error;
    }
  },

  /**
   * Tạo mô tả xét tuyển mới
   * @param {Object} data - Dữ liệu mô tả xét tuyển mới
   */
  async createAdmissionDescription(data) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.post(`${BASE_API_URL}/university-admissions/admission-descriptions`, data, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error creating admission description:', error);
      throw error;
    }
  },

  /**
   * Cập nhật thông tin mô tả xét tuyển
   * @param {number} id - ID của mô tả xét tuyển
   * @param {Object} data - Dữ liệu cập nhật
   */
  async updateAdmissionDescription(id, data) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.put(`${BASE_API_URL}/university-admissions/admission-descriptions/${id}`, data, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error updating admission description ${id}:`, error);
      throw error;
    }
  },

  /**
   * Xóa mô tả xét tuyển
   * @param {number} id - ID của mô tả xét tuyển
   */
  async deleteAdmissionDescription(id) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.delete(`${BASE_API_URL}/university-admissions/admission-descriptions/${id}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error deleting admission description ${id}:`, error);
      throw error;
    }
  }
};