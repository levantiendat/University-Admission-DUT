import axios from 'axios';
import config from '@/config/apiConfig';

const BASE_API_URL = config?.BASE_API_URL || 'https://university-admission-dut-hzdahmckevehhpdf.southeastasia-01.azurewebsites.net/api';

export default {
  /**
   * Lấy danh sách tỉnh/thành phố
   */
  async getAllCities() {
    try {
      const response = await axios.get(`${BASE_API_URL}/priorities/cities`);
      return response.data;
    } catch (error) {
      console.error('Error fetching cities:', error);
      throw error;
    }
  },

  /**
   * Lấy thông tin chi tiết của một tỉnh/thành phố
   * @param {number} id - ID của tỉnh/thành phố
   */
  async getCity(id) {
    try {
      const response = await axios.get(`${BASE_API_URL}/priorities/cities/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching city ${id}:`, error);
      throw error;
    }
  },

  /**
   * Tạo tỉnh/thành phố mới
   * @param {Object} data - Dữ liệu tỉnh/thành phố mới
   */
  async createCity(data) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.post(`${BASE_API_URL}/priorities/cities`, data, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error creating city:', error);
      throw error;
    }
  },

  /**
   * Cập nhật thông tin tỉnh/thành phố
   * @param {number} id - ID của tỉnh/thành phố
   * @param {Object} data - Dữ liệu cập nhật
   */
  async updateCity(id, data) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.put(`${BASE_API_URL}/priorities/cities/${id}`, data, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error updating city ${id}:`, error);
      throw error;
    }
  },

  /**
   * Xóa tỉnh/thành phố
   * @param {number} id - ID của tỉnh/thành phố
   */
  async deleteCity(id) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.delete(`${BASE_API_URL}/priorities/cities/${id}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error deleting city ${id}:`, error);
      throw error;
    }
  },

  /**
   * Lấy danh sách quận/huyện theo tỉnh/thành phố
   * @param {number} cityId - ID của tỉnh/thành phố
   */
  async getDistrictsByCity(cityId) {
    try {
      const response = await axios.get(`${BASE_API_URL}/priorities/cities/${cityId}/districts`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching districts for city ${cityId}:`, error);
      throw error;
    }
  },

  /**
   * Lấy thông tin chi tiết của một quận/huyện
   * @param {number} id - ID của quận/huyện
   */
  async getDistrict(id) {
    try {
      const response = await axios.get(`${BASE_API_URL}/priorities/districts/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching district ${id}:`, error);
      throw error;
    }
  },

  /**
   * Tạo quận/huyện mới
   * @param {Object} data - Dữ liệu quận/huyện mới
   */
  async createDistrict(data) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.post(`${BASE_API_URL}/priorities/districts`, data, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error creating district:', error);
      throw error;
    }
  },

  /**
   * Cập nhật thông tin quận/huyện
   * @param {number} id - ID của quận/huyện
   * @param {Object} data - Dữ liệu cập nhật
   */
  async updateDistrict(id, data) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.put(`${BASE_API_URL}/priorities/districts/${id}`, data, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error updating district ${id}:`, error);
      throw error;
    }
  },

  /**
   * Xóa quận/huyện
   * @param {number} id - ID của quận/huyện
   */
  async deleteDistrict(id) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.delete(`${BASE_API_URL}/priorities/districts/${id}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error deleting district ${id}:`, error);
      throw error;
    }
  },

  /**
   * Lấy danh sách trường theo quận/huyện
   * @param {number} districtId - ID của quận/huyện
   */
  async getSchoolsByDistrict(districtId) {
    try {
      const response = await axios.get(`${BASE_API_URL}/priorities/districts/${districtId}/schools`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching schools for district ${districtId}:`, error);
      throw error;
    }
  },

  /**
   * Lấy danh sách trường theo tỉnh/thành phố
   * @param {number} cityId - ID của tỉnh/thành phố
   */
  async getSchoolsByCity(cityId) {
    try {
      const response = await axios.get(`${BASE_API_URL}/priorities/cities/${cityId}/schools`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching schools for city ${cityId}:`, error);
      throw error;
    }
  },

  /**
   * Lấy thông tin chi tiết của một trường
   * @param {number} id - ID của trường
   */
  async getSchool(id) {
    try {
      const response = await axios.get(`${BASE_API_URL}/priorities/schools/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching school ${id}:`, error);
      throw error;
    }
  },

  /**
   * Tạo trường mới
   * @param {Object} data - Dữ liệu trường mới
   */
  async createSchool(data) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.post(`${BASE_API_URL}/priorities/schools`, data, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error creating school:', error);
      throw error;
    }
  },

  /**
   * Cập nhật thông tin trường
   * @param {number} id - ID của trường
   * @param {Object} data - Dữ liệu cập nhật
   */
  async updateSchool(id, data) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.put(`${BASE_API_URL}/priorities/schools/${id}`, data, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error updating school ${id}:`, error);
      throw error;
    }
  },

  /**
   * Xóa trường
   * @param {number} id - ID của trường
   */
  async deleteSchool(id) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.delete(`${BASE_API_URL}/priorities/schools/${id}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error deleting school ${id}:`, error);
      throw error;
    }
  }
};