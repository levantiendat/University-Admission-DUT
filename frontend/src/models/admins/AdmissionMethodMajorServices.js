import axios from 'axios';
import config from '@/config/apiConfig';

const BASE_API_URL = config?.BASE_API_URL || 'https://university-admission-dut-hzdahmckevehhpdf.southeastasia-01.azurewebsites.net/api';

export default {
  /**
   * Lấy danh sách tất cả mối quan hệ giữa phương thức tuyển sinh và ngành
   */
  async getAllAdmissionMethodMajors() {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-admissions/admission-method-majors`);
      return response.data;
    } catch (error) {
      console.error('Error fetching admission method majors:', error);
      throw error;
    }
  },

  /**
   * Lấy thông tin chi tiết của một mối quan hệ
   * @param {number} admissionMethodMajorId - ID của mối quan hệ
   */
  async getAdmissionMethodMajor(admissionMethodMajorId) {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-admissions/admission-method-majors/${admissionMethodMajorId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching admission method major ${admissionMethodMajorId}:`, error);
      throw error;
    }
  },

  /**
   * Lấy danh sách phương thức tuyển sinh áp dụng cho một ngành
   * @param {number} majorId - ID của ngành
   */
  async getAdmissionMethodsByMajor(majorId) {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-admissions/admission-method-majors/major/${majorId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching admission methods for major ${majorId}:`, error);
      throw error;
    }
  },

  /**
   * Lấy danh sách ngành áp dụng một phương thức tuyển sinh
   * @param {number} admissionMethodId - ID của phương thức tuyển sinh
   */
  async getMajorsByAdmissionMethod(admissionMethodId) {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-admissions/admission-method-majors/admission-method/${admissionMethodId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching majors for admission method ${admissionMethodId}:`, error);
      throw error;
    }
  },

  /**
   * Tạo mối quan hệ mới giữa phương thức tuyển sinh và ngành
   * @param {Object} data - Dữ liệu mối quan hệ mới
   */
  async createAdmissionMethodMajor(data) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.post(`${BASE_API_URL}/university-admissions/admission-method-majors`, data, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error creating admission method major relationship:', error);
      throw error;
    }
  },

  /**
   * Cập nhật thông tin mối quan hệ
   * @param {number} admissionMethodMajorId - ID của mối quan hệ
   * @param {Object} data - Dữ liệu cập nhật
   */
  async updateAdmissionMethodMajor(admissionMethodMajorId, data) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.put(`${BASE_API_URL}/university-admissions/admission-method-majors/${admissionMethodMajorId}`, data, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error updating admission method major ${admissionMethodMajorId}:`, error);
      throw error;
    }
  },

  /**
   * Xóa mối quan hệ
   * @param {number} admissionMethodMajorId - ID của mối quan hệ
   */
  async deleteAdmissionMethodMajor(admissionMethodMajorId) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.delete(`${BASE_API_URL}/university-admissions/admission-method-majors/${admissionMethodMajorId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error deleting admission method major ${admissionMethodMajorId}:`, error);
      throw error;
    }
  }
};