import axios from 'axios'
import config from '@/config/apiConfig'  // assuming you have this configuration file

const BASE_API_URL = config?.BASE_API_URL || 'https://university-admission-dut-hzdahmckevehhpdf.southeastasia-01.azurewebsites.net/api'

const CalculateScoreServices = {
  /**
   * Get all subjects available for score calculation
   * @returns {Promise<Array>} - List of subjects
   */
  getAllSubjects() {
    return axios.get(`${BASE_API_URL}/university-admissions/subjects`)
      .then(response => response.data)
      .catch(error => {
        console.error('Error fetching subjects:', error)
        throw error
      })
  },
  
  /**
   * Calculate admission scores based on high school records (học bạ)
   * @param {Object} data - Score data object containing subjects and their scores
   * @param {String} scoreType - Either "semester" for 6 semesters or "year" for 3 years
   * @returns {Promise<Object>} - Calculation results with combination scores
   */
  calculateScoreHB(data, scoreType) {
    const payload = {
      scores_type: scoreType,
      subjects: data
    }
    
    return axios.post(`${BASE_API_URL}/university-admissions/calculate-admission-scores`, payload)
      .then(response => response.data)
      .catch(error => {
        console.error('Error calculating high school record scores:', error)
        throw error
      })
  },
  
  /**
   * Calculate admission scores based on high school exam results (điểm thi THPT)
   * @param {Object} data - Score data object containing subjects and their scores
   * @returns {Promise<Object>} - Calculation results with combination scores
   */
  calculateScoreTHPT(data) {
    const payload = {
      scores_type: 'exam',
      subjects: data
    }
    
    return axios.post(`${BASE_API_URL}/university-admissions/calculate-admission-scores`, payload)
      .then(response => response.data)
      .catch(error => {
        console.error('Error calculating high school exam scores:', error)
        throw error
      })
  },
  
  /**
   * Get subject groups for admission
   * @returns {Promise<Array>} - List of subject groups
   */
  getSubjectGroups() {
    return axios.get(`${BASE_API_URL}/university-admissions/subject-score-method-groups`)
      .then(response => response.data)
      .catch(error => {
        console.error('Error fetching subject groups:', error)
        throw error
      })
  },
  
  /**
   * Get details of a specific subject group
   * @param {Number} groupId - ID of the subject group
   * @returns {Promise<Object>} - Subject group details
   */
  getSubjectGroupDetails(groupId) {
    return axios.get(`${BASE_API_URL}/university-admissions/subject-group-details/group/${groupId}`)
      .then(response => response.data)
      .catch(error => {
        console.error(`Error fetching details for group ${groupId}:`, error)
        throw error
      })
  }
}

export default CalculateScoreServices