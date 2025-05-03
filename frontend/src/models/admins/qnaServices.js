import axios from 'axios';
import config from '@/config/apiConfig';

const BASE_API_URL = config?.BASE_API_URL || 'https://university-admission-dut-hzdahmckevehhpdf.southeastasia-01.azurewebsites.net/api';

export default {
  /**
   * Lấy danh sách câu hỏi
   */
  async getAllQuestions() {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.get(`${BASE_API_URL}/qna/questions`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching questions:', error);
      throw error;
    }
  },

  /**
   * Lấy chi tiết câu hỏi theo ID
   * @param {number} id - ID của câu hỏi
   */
  async getQuestion(id) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.get(`${BASE_API_URL}/qna/questions/${id}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error fetching question ${id}:`, error);
      throw error;
    }
  },

  /**
   * Tạo câu hỏi mới
   * @param {Object} data - Dữ liệu câu hỏi mới
   */
  async createQuestion(data) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.post(`${BASE_API_URL}/qna/questions`, data, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error creating question:', error);
      throw error;
    }
  },

  /**
   * Cập nhật thông tin câu hỏi
   * @param {number} id - ID của câu hỏi
   * @param {Object} data - Dữ liệu cập nhật
   */
  async updateQuestion(id, data) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.put(`${BASE_API_URL}/qna/questions/${id}`, data, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error updating question ${id}:`, error);
      throw error;
    }
  },

  /**
   * Xóa câu hỏi
   * @param {number} id - ID của câu hỏi
   */
  async deleteQuestion(id) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.delete(`${BASE_API_URL}/qna/questions/${id}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error deleting question ${id}:`, error);
      throw error;
    }
  },

  /**
   * Lấy danh sách câu trả lời cho câu hỏi
   * @param {number} questionId - ID của câu hỏi
   */
  async getResponsesByQuestionId(questionId) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.get(`${BASE_API_URL}/qna/questions/${questionId}/responses`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error fetching responses for question ${questionId}:`, error);
      throw error;
    }
  },

  /**
   * Lấy chi tiết câu trả lời theo ID
   * @param {number} id - ID của câu trả lời
   */
  async getResponse(id) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.get(`${BASE_API_URL}/qna/responses/${id}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error fetching response ${id}:`, error);
      throw error;
    }
  },

  /**
   * Tạo câu trả lời mới
   * @param {Object} data - Dữ liệu câu trả lời mới
   */
  async createResponse(data) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.post(`${BASE_API_URL}/qna/responses`, data, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error creating response:', error);
      throw error;
    }
  },

  /**
   * Cập nhật thông tin câu trả lời
   * @param {number} id - ID của câu trả lời
   * @param {Object} data - Dữ liệu cập nhật
   */
  async updateResponse(id, data) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.put(`${BASE_API_URL}/qna/responses/${id}`, data, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error updating response ${id}:`, error);
      throw error;
    }
  },

  /**
   * Xóa câu trả lời
   * @param {number} id - ID của câu trả lời
   */
  async deleteResponse(id) {
    try {
      const token = sessionStorage.getItem('token');
      const response = await axios.delete(`${BASE_API_URL}/qna/responses/${id}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      console.error(`Error deleting response ${id}:`, error);
      throw error;
    }
  }
};