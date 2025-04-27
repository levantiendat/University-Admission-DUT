import axios from 'axios';
import config from '@/config/apiConfig';

const BASE_API_URL = config?.BASE_API_URL || 'https://university-admission-dut-hzdahmckevehhpdf.southeastasia-01.azurewebsites.net/api';

export default {
  /**
   * Lấy danh sách tất cả các tổ hợp môn thi
   */
  async getAllSubjectGroups() {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-admissions/subject-score-method-groups`);
      return response.data;
    } catch (error) {
      console.error('Error fetching subject groups:', error);
      throw error;
    }
  },

  /**
   * Lấy thông tin chi tiết của một tổ hợp môn thi
   * @param {number} groupId - ID của tổ hợp môn thi
   */
  async getSubjectGroup(groupId) {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-admissions/subject-score-method-groups/${groupId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching subject group ${groupId}:`, error);
      throw error;
    }
  },

  /**
   * Tạo tổ hợp môn thi mới
   * @param {Object} groupData - Dữ liệu tổ hợp môn thi mới
   */
  async createSubjectGroup(groupData) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.post(`${BASE_API_URL}/university-admissions/subject-score-method-groups`, groupData, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error creating subject group:', error);
      throw error;
    }
  },

  /**
   * Cập nhật thông tin tổ hợp môn thi
   * @param {number} groupId - ID của tổ hợp môn thi
   * @param {Object} groupData - Dữ liệu cập nhật
   */
  async updateSubjectGroup(groupId, groupData) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.put(`${BASE_API_URL}/university-admissions/subject-score-method-groups/${groupId}`, groupData, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error updating subject group ${groupId}:`, error);
      throw error;
    }
  },

  /**
   * Xóa tổ hợp môn thi
   * @param {number} groupId - ID của tổ hợp môn thi
   */
  async deleteSubjectGroup(groupId) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.delete(`${BASE_API_URL}/university-admissions/subject-score-method-groups/${groupId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error deleting subject group ${groupId}:`, error);
      throw error;
    }
  }
};