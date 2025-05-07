import axios from 'axios'
import config from '@/config/apiConfig'

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
   * @param {Array} data - Score data array containing subjects and their scores
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
   * @param {Array} data - Score data array containing subjects and their scores
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
   * Calculate priority points based on original score and priority info
   * @param {Number} score - Original score (on 30-point scale)
   * @param {String} priorityArea - Priority area code (e.g., "KV1", "KV2")
   * @param {String} priorityObject - Priority object code (e.g., "ĐT01", "ĐT02")
   * @param {Number} schoolId - Optional school ID to get priority area
   * @returns {Promise<Object>} - Priority calculation results
   */
  calculatePriorityPoints(score, priorityArea, priorityObject, schoolId = null) {
    const payload = {
      score: score,
      priority_area: priorityArea,
      priority_object: priorityObject,
      school_id: schoolId
    }
    
    return axios.post(`${BASE_API_URL}/university-admissions/calculate-priority`, payload)
      .then(response => response.data)
      .catch(error => {
        console.error('Error calculating priority points:', error)
        throw error
      })
  },
  
  /**
   * Get all subject score method groups (tổ hợp xét tuyển)
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
  },
  
  /**
   * Get list of all cities/provinces
   * @returns {Promise<Array>} - List of cities/provinces
   */
  getCities() {
    return axios.get(`${BASE_API_URL}/priorities/cities`)
      .then(response => response.data)
      .catch(error => {
        console.error('Error fetching cities:', error)
        throw error
      })
  },
  
  /**
   * Get districts for a specific city
   * @param {Number} cityId - ID of the city/province
   * @returns {Promise<Array>} - List of districts
   */
  getDistricts(cityId) {
    return axios.get(`${BASE_API_URL}/priorities/cities/${cityId}/districts`)
      .then(response => response.data)
      .catch(error => {
        console.error(`Error fetching districts for city ${cityId}:`, error)
        throw error
      })
  },
  
  /**
   * Get schools for a specific district
   * @param {Number} districtId - ID of the district
   * @returns {Promise<Array>} - List of schools
   */
  getSchools(districtId) {
    return axios.get(`${BASE_API_URL}/priorities/districts/${districtId}/schools`)
      .then(response => response.data)
      .catch(error => {
        console.error(`Error fetching schools for district ${districtId}:`, error)
        throw error
      })
  }
}

export default CalculateScoreServices