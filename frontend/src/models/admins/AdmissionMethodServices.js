import axios from 'axios';
import config from '@/config/apiConfig';

const BASE_API_URL = config?.BASE_API_URL || 'https://university-admission-dut-hzdahmckevehhpdf.southeastasia-01.azurewebsites.net/api';

export default {
  /**
   * Lấy danh sách tất cả phương thức tuyển sinh
   */
  async getAllAdmissionMethods() {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-admissions/admission-methods`);
      return response.data;
    } catch (error) {
      console.error('Error fetching admission methods:', error);
      throw error;
    }
  },

  /**
   * Lấy thông tin chi tiết của một phương thức tuyển sinh
   * @param {number} admissionMethodId - ID của phương thức tuyển sinh
   */
  async getAdmissionMethod(admissionMethodId) {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-admissions/admission-methods/${admissionMethodId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching admission method ${admissionMethodId}:`, error);
      throw error;
    }
  },

  /**
   * Tạo phương thức tuyển sinh mới
   * @param {Object} admissionMethodData - Dữ liệu phương thức tuyển sinh mới
   */
  async createAdmissionMethod(admissionMethodData) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.post(`${BASE_API_URL}/university-admissions/admission-methods`, admissionMethodData, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error creating admission method:', error);
      throw error;
    }
  },

  /**
   * Cập nhật thông tin phương thức tuyển sinh
   * @param {number} admissionMethodId - ID của phương thức tuyển sinh
   * @param {Object} admissionMethodData - Dữ liệu cập nhật
   */
  async updateAdmissionMethod(admissionMethodId, admissionMethodData) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.put(`${BASE_API_URL}/university-admissions/admission-methods/${admissionMethodId}`, admissionMethodData, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error updating admission method ${admissionMethodId}:`, error);
      throw error;
    }
  },

  /**
   * Xóa phương thức tuyển sinh
   * @param {number} admissionMethodId - ID của phương thức tuyển sinh
   */
  async deleteAdmissionMethod(admissionMethodId) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.delete(`${BASE_API_URL}/university-admissions/admission-methods/${admissionMethodId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error deleting admission method ${admissionMethodId}:`, error);
      throw error;
    }
  }
};