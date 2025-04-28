import axios from 'axios';
import config from '@/config/apiConfig';

const BASE_API_URL = config?.BASE_API_URL || 'https://university-admission-dut-hzdahmckevehhpdf.southeastasia-01.azurewebsites.net/api';

export default {
  /**
   * Lấy danh sách tất cả các mối quan hệ giữa tổ hợp môn và ngành tuyển sinh
   */
  async getAllSubjectGroupMajors() {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-admissions/subject-score-method-majors`);
      return response.data;
    } catch (error) {
      console.error('Error fetching subject group majors:', error);
      throw error;
    }
  },

  /**
   * Lấy thông tin chi tiết của một mối quan hệ
   * @param {number} relationId - ID của mối quan hệ
   */
  async getSubjectGroupMajor(relationId) {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-admissions/subject-score-method-majors/${relationId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching subject group major ${relationId}:`, error);
      throw error;
    }
  },

  /**
    * Tạo mối quan hệ mới giữa tổ hợp môn và ngành tuyển sinh
    * @param {Object} data - Dữ liệu mối quan hệ mới
    */
  async createSubjectGroupMajor(data) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.post(`${BASE_API_URL}/university-admissions/subject-score-method-majors`, data, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error creating subject group major relationship:', error);
      throw error;
    }
  },

  /**
   * Cập nhật thông tin mối quan hệ
   * @param {number} relationId - ID của mối quan hệ
   * @param {Object} data - Dữ liệu cập nhật
   */
  async updateSubjectGroupMajor(relationId, data) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.put(`${BASE_API_URL}/university-admissions/subject-score-method-majors/${relationId}`, data, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error updating subject group major ${relationId}:`, error);
      throw error;
    }
  },

  /**
   * Xóa mối quan hệ
   * @param {number} relationId - ID của mối quan hệ
   */
  async deleteSubjectGroupMajor(relationId) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.delete(`${BASE_API_URL}/university-admissions/subject-score-method-majors/${relationId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error deleting subject group major ${relationId}:`, error);
      throw error;
    }
  },

  /**
 * Lấy danh sách ngành áp dụng cho một tổ hợp môn thi
 * @param {number} groupId - ID của tổ hợp môn thi
 */
  async getMajorsBySubjectGroup(groupId) {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-admissions/subject-score-method-majors/group/${groupId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching majors for subject group ${groupId}:`, error);
      throw error;
    }
  },

  /**
 * Tạo mối quan hệ mới giữa tổ hợp môn và một phương thức tuyển sinh của ngành
 * @param {Object} data - Dữ liệu mối quan hệ mới (group_id, admission_method_major_id)
 */
async createSubjectGroupForAdmissionMethodMajor(data) {
  try {
    const token = sessionStorage.getItem('token');
    const response = await axios.post(`${BASE_API_URL}/university-admissions/subject-score-method-majors`, data, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    return response.data;
  } catch (error) {
    console.error('Error creating subject group admission method major relationship:', error);
    throw error;
  }
}
};