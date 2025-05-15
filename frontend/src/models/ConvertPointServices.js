import axios from 'axios'
import config from '@/config/apiConfig'

const BASE_API_URL = config?.BASE_API_URL || 'https://university-admission-dut-hzdahmckevehhpdf.southeastasia-01.azurewebsites.net/api'

const ConvertPointServices = {
  /**
   * Get all admission methods available in the system
   * @returns {Promise<Array>} - List of admission methods
   */
  getAdmissionMethods() {
    return axios.get(`${BASE_API_URL}/university-admissions/admission-methods`)
      .then(response => response.data)
      .catch(error => {
        console.error('Error fetching admission methods:', error)
        throw error
      })
  },

  /**
   * Get all score conversion tables
   * @returns {Promise<Array>} - List of all conversion tables
   */
  getAllConversionTables() {
    return axios.get(`${BASE_API_URL}/university-admissions/convert-points`)
      .then(response => response.data)
      .catch(error => {
        console.error('Error fetching conversion tables:', error)
        throw error
      })
  },

  /**
   * Get conversion table for a specific admission method
   * @param {Number} admissionMethodId - ID of the admission method
   * @returns {Promise<Array>} - List of conversion ranges for the admission method
   */
  getConversionTableByMethod(admissionMethodId) {
    return axios.get(`${BASE_API_URL}/university-admissions/convert-points/admission-method/${admissionMethodId}`)
      .then(response => response.data)
      .catch(error => {
        console.error(`Error fetching conversion table for method ${admissionMethodId}:`, error)
        throw error
      })
  },

  /**
   * Convert a score based on admission method
   * @param {Number} admissionMethodId - ID of the admission method
   * @param {Number} originScore - Original score to convert
   * @returns {Promise<Object>} - Conversion result with details
   */
  convertScore(admissionMethodId, originScore) {
    const payload = {
      admission_method_id: admissionMethodId,
      origin_score: originScore
    }

    return axios.post(`${BASE_API_URL}/university-admissions/convert-points/convert`, payload)
      .then(response => response.data)
      .catch(error => {
        console.error('Error converting score:', error)
        throw error
      })
  }
}

export default ConvertPointServices