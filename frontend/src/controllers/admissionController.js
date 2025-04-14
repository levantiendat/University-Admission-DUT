import admissionService from '@/models/admissionService'

const AdmissionController = {
  /**
   * Lấy và xử lý dữ liệu tuyển sinh để hiển thị
   * @returns {Promise<Object>} - Dữ liệu đã được xử lý
   */
  async getAdmissionData() {
    try {
      // Lấy dữ liệu từ cả 3 API
      const [majors, admissionMethods, admissionMethodMajors] = await Promise.all([
        admissionService.getMajors(),
        admissionService.getAdmissionMethods(),
        admissionService.getAdmissionMethodMajors()
      ])

      // Xử lý dữ liệu để tạo bảng thông tin
      const processedData = majors.map(major => {
        // Tìm tất cả các phương thức tuyển sinh cho ngành này
        const methodsForMajor = admissionMethodMajors
          .filter(item => item.major_id === major.id)
          .map(item => item.admission_methods_id)

        // Tạo đối tượng chứa trạng thái của từng phương thức
        const methodStatus = {}
        admissionMethods.forEach(method => {
          methodStatus[`method_${method.id}`] = methodsForMajor.includes(method.id)
        })

        // Trả về thông tin ngành kèm trạng thái phương thức
        return {
          major_code: major.major_code,
          name: major.name,
          seats: major.seats,
          ...methodStatus
        }
      })

      return {
        majors: processedData,
        admissionMethods: admissionMethods
      }
    } catch (error) {
      console.error('Lỗi khi xử lý dữ liệu tuyển sinh:', error)
      throw error
    }
  }
}

export default AdmissionController