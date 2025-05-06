import CalculateScoreServices from '@/models/CalculateScoreServices'

const CalculateScoreController = {
  /**
   * Get all available subjects for score calculation
   */
  async getSubjects() {
    try {
      const subjects = await CalculateScoreServices.getAllSubjects()
      return subjects
    } catch (error) {
      console.error('Failed to retrieve subjects:', error)
      throw error
    }
  },
  
  /**
   * Calculate scores based on high school records
   * @param {Array} subjectsData - Array of subjects with scores
   * @param {String} scoreType - "semester" for 6 semester scores or "year" for 3 year scores
   */
  async calculateHBScores(subjectsData, scoreType) {
    try {
      // Filter out any subjects with incomplete data
      const validSubjects = subjectsData.filter(subject => 
        (subject.subject_id || subject.subject_name) && subject.scores.length > 0
      )
      
      if (validSubjects.length === 0) {
        throw new Error('No valid subject data provided')
      }
      
      const result = await CalculateScoreServices.calculateScoreHB(validSubjects, scoreType)
      return result
    } catch (error) {
      console.error('Failed to calculate high school record scores:', error)
      throw error
    }
  },
  
  /**
   * Calculate scores based on high school exam results
   * @param {Array} subjectsData - Array of subjects with scores
   */
  async calculateTHPTScores(subjectsData) {
    try {
      // Filter out any subjects with incomplete data
      const validSubjects = subjectsData.filter(subject => 
        (subject.subject_id || subject.subject_name) && 
        subject.scores && 
        subject.scores.length > 0 && 
        subject.scores[0] > 0
      )
      
      if (validSubjects.length === 0) {
        throw new Error('No valid subject data provided')
      }
      
      const result = await CalculateScoreServices.calculateScoreTHPT(validSubjects)
      return result
    } catch (error) {
      console.error('Failed to calculate high school exam scores:', error)
      throw error
    }
  },
  
  /**
   * Get available subject groups and their details
   */
  async getSubjectGroupsWithDetails() {
    try {
      const groups = await CalculateScoreServices.getSubjectGroups()
      const groupsWithDetails = await Promise.all(
        groups.map(async group => {
          try {
            const details = await CalculateScoreServices.getSubjectGroupDetails(group.id)
            return {
              ...group,
              details
            }
          } catch (error) {
            console.error(`Failed to get details for group ${group.id}:`, error)
            return {
              ...group,
              details: []
            }
          }
        })
      )
      return groupsWithDetails
    } catch (error) {
      console.error('Failed to retrieve subject groups with details:', error)
      throw error
    }
  }
}

export default CalculateScoreController