import axios from 'axios';
import config from '@/config/apiConfig';

const BASE_API_URL = config?.BASE_API_URL || 'https://university-admission-dut-hzdahmckevehhpdf.southeastasia-01.azurewebsites.net/api';

export default {
  /**
   * Lấy danh sách tất cả chi tiết môn học trong tổ hợp
   */
  async getAllSubjectGroupDetails() {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-admissions/subject-group-details`);
      return response.data;
    } catch (error) {
      console.error('Error fetching subject group details:', error);
      throw error;
    }
  },

  /**
   * Lấy chi tiết của một môn trong tổ hợp
   * @param {number} detailId - ID của chi tiết môn trong tổ hợp
   */
  async getSubjectGroupDetail(detailId) {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-admissions/subject-group-details/${detailId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching subject group detail ${detailId}:`, error);
      throw error;
    }
  },

  /**
   * Lấy tất cả chi tiết môn học trong một tổ hợp
   * @param {number} groupId - ID của tổ hợp
   */
  async getSubjectGroupDetailsByGroup(groupId) {
    try {
      const response = await axios.get(`${BASE_API_URL}/university-admissions/subject-group-details/group/${groupId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching subject group details for group ${groupId}:`, error);
      throw error;
    }
  },

  /**
   * Tạo mới chi tiết môn học trong tổ hợp
   * @param {Object} detailData - Dữ liệu chi tiết môn học trong tổ hợp
   */
  async createSubjectGroupDetail(detailData) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.post(`${BASE_API_URL}/university-admissions/subject-group-details`, detailData, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error creating subject group detail:', error);
      throw error;
    }
  },

  /**
   * Cập nhật chi tiết môn học trong tổ hợp
   * @param {number} detailId - ID của chi tiết môn học trong tổ hợp
   * @param {Object} detailData - Dữ liệu cập nhật
   */
  async updateSubjectGroupDetail(detailId, detailData) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.put(`${BASE_API_URL}/university-admissions/subject-group-details/${detailId}`, detailData, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error updating subject group detail ${detailId}:`, error);
      throw error;
    }
  },

  /**
   * Xóa chi tiết môn học trong tổ hợp
   * @param {number} detailId - ID của chi tiết môn học trong tổ hợp
   */
  async deleteSubjectGroupDetail(detailId) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.delete(`${BASE_API_URL}/university-admissions/subject-group-details/${detailId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error deleting subject group detail ${detailId}:`, error);
      throw error;
    }
  }
};