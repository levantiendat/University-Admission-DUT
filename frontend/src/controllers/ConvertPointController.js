import ConvertPointServices from '@/models/ConvertPointServices'

const ConvertPointController = {
  /**
   * Get all admission methods with conversion tables
   * @returns {Promise<Array>} - Filtered list of admission methods with conversion tables
   */
  async getAdmissionMethodsWithConversion() {
    try {
      const [methods, allConversions] = await Promise.all([
        ConvertPointServices.getAdmissionMethods(),
        ConvertPointServices.getAllConversionTables()
      ])

      // Get unique admission method IDs that have conversion tables
      const methodIdsWithConversion = [...new Set(allConversions.map(c => c.admission_methods_id))]
      
      // Filter admission methods that have conversion tables
      return methods.filter(method => methodIdsWithConversion.includes(method.id))
    } catch (error) {
      console.error('Failed to retrieve admission methods with conversion tables:', error)
      throw error
    }
  },
  
  /**
   * Get conversion table for a specific admission method
   * @param {Number} methodId - ID of the admission method
   */
  async getConversionTable(methodId) {
    try {
      if (!methodId) {
        return []
      }
      
      const conversionTable = await ConvertPointServices.getConversionTableByMethod(methodId)
      
      // Sort by origin_min in ascending order
      return conversionTable.sort((a, b) => a.origin_min - b.origin_min)
    } catch (error) {
      console.error(`Failed to retrieve conversion table for method ${methodId}:`, error)
      throw error
    }
  },
  
  /**
   * Convert a score based on selected admission method
   * @param {Number} methodId - ID of the admission method
   * @param {Number} score - Score to convert
   */
  async convertScore(methodId, score) {
    try {
      if (!methodId || isNaN(score)) {
        throw new Error('Invalid method ID or score value')
      }
      
      // Convert score to number and ensure it's valid
      const numericScore = parseFloat(score)
      if (isNaN(numericScore)) {
        throw new Error('Invalid score value')
      }
      
      const result = await ConvertPointServices.convertScore(methodId, numericScore)
      return result
    } catch (error) {
      console.error('Failed to convert score:', error)
      throw error
    }
  },
  
  /**
   * Get admission method name by ID
   * @param {Number} methodId - ID of the admission method
   */
  async getAdmissionMethodName(methodId) {
    try {
      const methods = await ConvertPointServices.getAdmissionMethods()
      const method = methods.find(m => m.id === methodId)
      return method ? method.name : 'Unknown Method'
    } catch (error) {
      console.error('Failed to get admission method name:', error)
      throw error
    }
  }
}

export default ConvertPointController