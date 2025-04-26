import qnaService from '@/models/qnaService'

export default {
  async getQuestionDetail(questionId) {
    try {
      return await qnaService.getQuestionById(questionId)
    } catch (error) {
      console.error('Error in getQuestionDetail controller:', error)
      throw error
    }
  },

  async getResponses(questionId) {
    try {
      return await qnaService.getResponsesByQuestionId(questionId)
    } catch (error) {
      console.error('Error in getResponses controller:', error)
      throw error
    }
  },

  async createResponse(responseData) {
    try {
      return await qnaService.createResponse(responseData)
    } catch (error) {
      console.error('Error in createResponse controller:', error)
      throw error
    }
  },

  async updateResponse(responseId, responseData) {
    try {
      return await qnaService.updateResponse(responseId, responseData)
    } catch (error) {
      console.error('Error in updateResponse controller:', error)
      throw error
    }
  },

  async deleteResponse(responseId) {
    try {
      return await qnaService.deleteResponse(responseId)
    } catch (error) {
      console.error('Error in deleteResponse controller:', error)
      throw error
    }
  },

  async deleteQuestion(questionId) {
    try {
      return await qnaService.deleteQuestion(questionId)
    } catch (error) {
      console.error('Error in deleteQuestion controller:', error)
      throw error
    }
  }
}