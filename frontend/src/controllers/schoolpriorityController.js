import SchoolPriorityServices from '@/models/schoolpriorityServices'

const SchoolPriorityController = {
  /**
   * Load all cities/provinces
   * @returns {Promise<Array>} List of cities/provinces
   */
  async loadCities() {
    try {
      return await SchoolPriorityServices.getCities()
    } catch (error) {
      console.error('Controller error loading cities:', error)
      throw error
    }
  },

  /**
   * Load districts for a specific city/province
   * @param {Number} cityId - ID of the city/province
   * @returns {Promise<Array>} List of districts
   */
  async loadDistricts(cityId) {
    try {
      if (!cityId) {
        return []
      }
      return await SchoolPriorityServices.getDistricts(cityId)
    } catch (error) {
      console.error(`Controller error loading districts for city ${cityId}:`, error)
      throw error
    }
  },

  /**
   * Load schools for a specific district
   * @param {Number} districtId - ID of the district
   * @returns {Promise<Array>} List of schools
   */
  async loadSchools(districtId) {
    try {
      if (!districtId) {
        return []
      }
      return await SchoolPriorityServices.getSchools(districtId)
    } catch (error) {
      console.error(`Controller error loading schools for district ${districtId}:`, error)
      throw error
    }
  },

  /**
   * Perform a global search and format results
   * @param {String} query - Search term
   * @returns {Promise<Array>} Formatted search results
   */
  async performGlobalSearch(query) {
    try {
      if (!query || query.length < 2) {
        return []
      }
      
      const searchResults = await SchoolPriorityServices.globalSearch(query)
      
      // Format results into a unified array with type indicators
      const citySuggestions = searchResults.cities.map(item => ({
        id: item.id,
        name: item.name,
        type: 'cities'
      }))
      
      const districtSuggestions = searchResults.districts.map(item => ({
        id: item.id,
        name: item.name,
        type: 'districts'
      }))
      
      const schoolSuggestions = searchResults.schools.map(item => ({
        id: item.id,
        name: item.name,
        type: 'schools'
      }))
      
      return [...citySuggestions, ...districtSuggestions, ...schoolSuggestions]
    } catch (error) {
      console.error(`Controller error performing global search for "${query}":`, error)
      return []
    }
  }
}

export default SchoolPriorityController