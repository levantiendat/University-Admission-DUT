import qnaService from '@/models/qnaService'

export default {
  async createQuestion(questionData) {
    try {
      return await qnaService.createQuestion(questionData)
    } catch (error) {
      console.error('Error in createQuestion controller:', error)
      throw error
    }
  },

  async updateQuestion(questionId, questionData) {
    try {
      return await qnaService.updateQuestion(questionId, questionData)
    } catch (error) {
      console.error('Error in updateQuestion controller:', error)
      throw error
    }
  },

  async getQuestionForUpdate(questionId) {
    try {
      return await qnaService.getQuestionById(questionId)
    } catch (error) {
      console.error('Error in getQuestionForUpdate controller:', error)
      throw error
    }
  }
}