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
   * Calculate priority points for a given score
   * @param {Number} score - Original score
   * @param {String} priorityArea - Priority area code
   * @param {String} priorityObject - Priority object code
   * @param {Number} schoolId - Optional school ID
   */
  async calculatePriorityPoints(score, priorityArea, priorityObject, schoolId = null) {
    try {
      if (isNaN(score) || score < 0 || score > 30) {
        throw new Error('Invalid score value')
      }
      
      const result = await CalculateScoreServices.calculatePriorityPoints(
        score, 
        priorityArea, 
        priorityObject, 
        schoolId
      )
      return result
    } catch (error) {
      console.error('Failed to calculate priority points:', error)
      throw error
    }
  },
  
  /**
   * Calculate priority points for multiple combination scores
   * @param {Array} combinations - Array of combination results with scores
   * @param {String} priorityArea - Priority area code
   * @param {String} priorityObject - Priority object code
   * @param {Number} schoolId - Optional school ID
   */
  async calculateCombinationPriorityPoints(combinations, priorityArea, priorityObject, schoolId = null) {
    try {
      const combinationsWithPriority = await Promise.all(
        combinations.map(async (combination) => {
          try {
            const priorityResult = await this.calculatePriorityPoints(
              combination.score,
              priorityArea,
              priorityObject,
              schoolId
            )
            
            return {
              ...combination,
              priority_points: {
                origin_priority: priorityResult.origin_priority,
                convert_priority: priorityResult.convert_priority,
                total_point: priorityResult.total_point
              }
            }
          } catch (error) {
            console.error(`Error calculating priority for combination ${combination.group_id}:`, error)
            return {
              ...combination,
              priority_points: {
                origin_priority: 0,
                convert_priority: 0,
                total_point: combination.score
              }
            }
          }
        })
      )
      
      // Sort by total score in descending order
      return combinationsWithPriority.sort(
        (a, b) => b.priority_points.total_point - a.priority_points.total_point
      )
    } catch (error) {
      console.error('Failed to calculate priority points for combinations:', error)
      throw error
    }
  },
  
  /**
   * Get available subject groups and their details
   */
  async getSubjectGroups() {
    try {
      const groups = await CalculateScoreServices.getSubjectGroups()
      return groups
    } catch (error) {
      console.error('Failed to retrieve subject groups:', error)
      throw error
    }
  },
  
  /**
   * Get cities/provinces for the location selector
   */
  async getCities() {
    try {
      const cities = await CalculateScoreServices.getCities()
      return cities
    } catch (error) {
      console.error('Failed to retrieve cities:', error)
      throw error
    }
  },
  
  /**
   * Get districts for a selected city/province
   * @param {Number} cityId - ID of the selected city
   */
  async getDistricts(cityId) {
    try {
      if (!cityId) {
        return []
      }
      const districts = await CalculateScoreServices.getDistricts(cityId)
      return districts
    } catch (error) {
      console.error(`Failed to retrieve districts for city ${cityId}:`, error)
      throw error
    }
  },
  
  /**
   * Get schools for a selected district
   * @param {Number} districtId - ID of the selected district
   */
  async getSchools(districtId) {
    try {
      if (!districtId) {
        return []
      }
      const schools = await CalculateScoreServices.getSchools(districtId)
      return schools
    } catch (error) {
      console.error(`Failed to retrieve schools for district ${districtId}:`, error)
      throw error
    }
  }
}

export default CalculateScoreController