import qnaService from '@/models/qnaService'

export default {
  async getQuestions() {
    try {
      return await qnaService.getQuestions()
    } catch (error) {
      console.error('Error in getQuestions controller:', error)
      throw error
    }
  }
}