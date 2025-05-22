import admissionService from '@/models/admissionService'

const AdmissionController = {
  /**
   * Lấy và xử lý dữ liệu tuyển sinh để hiển thị
   * @returns {Promise<Object>} - Dữ liệu đã được xử lý
   */
  async getAdmissionData() {
    try {
      // Lấy dữ liệu từ cả 4 API
      const [majors, admissionMethods, admissionMethodMajors, faculties] = await Promise.all([
        admissionService.getMajors(),
        admissionService.getAdmissionMethods(),
        admissionService.getAdmissionMethodMajors(),
        admissionService.getFaculties()
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

        // Tìm thông tin khoa của ngành
        const faculty = faculties.find(faculty => faculty.id === major.faculty_id) || {
          name: 'Chưa xác định',
          id: 0,
          faculty_code: 'N/A'
        }

        // Trả về thông tin ngành kèm trạng thái phương thức và thông tin khoa
        return {
          id: major.id,
          major_code: major.major_code,
          name: major.name,
          seats: major.seats,
          faculty_id: major.faculty_id,
          faculty_name: faculty.name,
          faculty_code: faculty.faculty_code,
          description: major.description,
          ...methodStatus
        }
      })

      return {
        majors: processedData,
        admissionMethods: admissionMethods,
        faculties: faculties
      }
    } catch (error) {
      console.error('Lỗi khi xử lý dữ liệu tuyển sinh:', error)
      throw error
    }
  }
}

export default AdmissionController