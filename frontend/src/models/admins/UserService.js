import axios from 'axios';
import config from '@/config/apiConfig';

const BASE_API_URL = config?.BASE_API_URL || 'https://university-admission-dut-hzdahmckevehhpdf.southeastasia-01.azurewebsites.net/api';

export default {
  /**
   * Lấy danh sách tất cả người dùng
   */
  async getUsers() {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.get(`${BASE_API_URL}/users/admin/get-users`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching users:', error);
      throw error;
    }
  },

  /**
   * Lấy thông tin chi tiết của một người dùng
   * @param {number} userId - ID của người dùng
   */
  async getUser(userId) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.get(`${BASE_API_URL}/users/admin/get-user/${userId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error fetching user ${userId}:`, error);
      throw error;
    }
  },

  /**
   * Cập nhật thông tin người dùng
   * @param {number} userId - ID của người dùng
   * @param {Object} userData - Dữ liệu cập nhật (name, phone_number)
   */
  async updateUser(userId, userData) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.put(`${BASE_API_URL}/users/admin/update-user/${userId}`, userData, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error updating user ${userId}:`, error);
      throw error;
    }
  },

  /**
   * Cập nhật role của người dùng
   * @param {number} userId - ID của người dùng
   * @param {string} role - Role mới (user/instructor)
   */
  async updateUserRole(userId, role) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.put(`${BASE_API_URL}/users/admin/update-user-role/${userId}`, {}, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'role': role
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error updating role for user ${userId}:`, error);
      throw error;
    }
  },

  /**
   * Tạo người dùng mới
   * @param {Object} userData - Dữ liệu người dùng mới
   * @param {string} role - Role của người dùng (user/instructor)
   */
  async createUser(userData, role) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.post(`${BASE_API_URL}/users/admin/create-user`, userData, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'role': role
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error creating user:', error);
      throw error;
    }
  }
};