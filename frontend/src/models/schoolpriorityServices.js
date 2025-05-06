import axios from 'axios'
import config from '@/config/apiConfig'

const BASE_API_URL = config?.BASE_API_URL || 'https://university-admission-dut-hzdahmckevehhpdf.southeastasia-01.azurewebsites.net/api'

const SchoolPriorityServices = {
  /**
   * Get list of all cities/provinces
   * @returns {Promise<Array>} List of cities/provinces
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
   * Get districts for a specific city/province
   * @param {Number} cityId - ID of the city/province
   * @returns {Promise<Array>} List of districts
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
   * @returns {Promise<Array>} List of schools
   */
  getSchools(districtId) {
    return axios.get(`${BASE_API_URL}/priorities/districts/${districtId}/schools`)
      .then(response => response.data)
      .catch(error => {
        console.error(`Error fetching schools for district ${districtId}:`, error)
        throw error
      })
  },

  /**
   * Global search across cities, districts, and schools
   * @param {String} query - Search term
   * @returns {Promise<Object>} Search results for cities, districts, and schools
   */
  globalSearch(query) {
    return axios.get(`${BASE_API_URL}/priorities/search?q=${encodeURIComponent(query)}`)
      .then(response => response.data)
      .catch(error => {
        console.error(`Error performing global search for "${query}":`, error)
        throw error
      })
  }
}

export default SchoolPriorityServices