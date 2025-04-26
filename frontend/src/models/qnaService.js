import axios from 'axios'
import config from '@/config/apiConfig'

const BASE_API_URL = config?.BASE_API_URL || 'https://university-admission-dut-hzdahmckevehhpdf.southeastasia-01.azurewebsites.net/api'
// const BASE_API_URL = 'http://127.0.0.1:8000/api'

const qnaService = {
  // Lấy token từ session storage
  getToken() {
    return sessionStorage.getItem('token')
  },

  // Cấu hình headers với token
  getHeaders() {
    return {
      headers: {
        'Authorization': `Bearer ${this.getToken()}`
      }
    }
  },

  // API lấy thông tin người dùng hiện tại dựa trên token
  async getCurrentUser() {
    try {
      const response = await axios.get(`${BASE_API_URL}/users/me`, this.getHeaders())
      return response.data
    } catch (error) {
      console.error('Error fetching current user:', error)
      throw error
    }
  },

  // API lấy danh sách câu hỏi
  async getQuestions() {
    try {
      const response = await axios.get(`${BASE_API_URL}/qna/questions`, this.getHeaders())
      return response.data
    } catch (error) {
      console.error('Error fetching questions:', error)
      throw error
    }
  },

  // API lấy chi tiết câu hỏi theo ID
  async getQuestionById(questionId) {
    try {
      const response = await axios.get(`${BASE_API_URL}/qna/questions/${questionId}`, this.getHeaders())
      return response.data
    } catch (error) {
      console.error(`Error fetching question with ID ${questionId}:`, error)
      throw error
    }
  },

  // API tạo câu hỏi mới
  async createQuestion(questionData) {
    try {
      const response = await axios.post(`${BASE_API_URL}/qna/questions`, questionData, this.getHeaders())
      return response.data
    } catch (error) {
      console.error('Error creating question:', error)
      throw error
    }
  },

  // API cập nhật câu hỏi
  async updateQuestion(questionId, questionData) {
    try {
      const response = await axios.put(`${BASE_API_URL}/qna/questions/${questionId}`, questionData, this.getHeaders())
      return response.data
    } catch (error) {
      console.error(`Error updating question with ID ${questionId}:`, error)
      throw error
    }
  },

  // API xóa câu hỏi
  async deleteQuestion(questionId) {
    try {
      const response = await axios.delete(`${BASE_API_URL}/qna/questions/${questionId}`, this.getHeaders())
      return response.data
    } catch (error) {
      console.error(`Error deleting question with ID ${questionId}:`, error)
      throw error
    }
  },

  // API lấy danh sách responses của một câu hỏi
  async getResponsesByQuestionId(questionId) {
    try {
      const response = await axios.get(`${BASE_API_URL}/qna/questions/${questionId}/responses`, this.getHeaders())
      return response.data
    } catch (error) {
      console.error(`Error fetching responses for question with ID ${questionId}:`, error)
      throw error
    }
  },

  // API tạo response cho câu hỏi
  async createResponse(responseData) {
    try {
      const response = await axios.post(`${BASE_API_URL}/qna/responses`, responseData, this.getHeaders())
      return response.data
    } catch (error) {
      console.error('Error creating response:', error)
      throw error
    }
  },

  // API cập nhật response
  async updateResponse(responseId, responseData) {
    try {
      const response = await axios.put(`${BASE_API_URL}/qna/responses/${responseId}`, responseData, this.getHeaders())
      return response.data
    } catch (error) {
      console.error(`Error updating response with ID ${responseId}:`, error)
      throw error
    }
  },

  // API xóa response
  async deleteResponse(responseId) {
    try {
      const response = await axios.delete(`${BASE_API_URL}/qna/responses/${responseId}`, this.getHeaders())
      return response.data
    } catch (error) {
      console.error(`Error deleting response with ID ${responseId}:`, error)
      throw error
    }
  }
}

export default qnaService