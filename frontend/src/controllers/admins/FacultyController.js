import FacultyServices from '../../models/admins/FacultyServices';

export default {
  /**
   * Lấy danh sách tất cả khoa
   */
  async getAllFaculties() {
    try {
      return await FacultyServices.getAllFaculties();
    } catch (error) {
      throw new Error(`Không thể lấy danh sách khoa: ${error.message}`);
    }
  },

  /**
   * Lấy thông tin chi tiết của một khoa
   * @param {number} facultyId - ID của khoa
   */
  async getFacultyById(facultyId) {
    try {
      return await FacultyServices.getFaculty(facultyId);
    } catch (error) {
      throw new Error(`Không thể lấy thông tin khoa: ${error.message}`);
    }
  },

  /**
   * Tạo khoa mới
   * @param {Object} facultyData - Dữ liệu khoa mới
   */
  async createFaculty(facultyData) {
    try {
      // Validate input
      if (!facultyData.name || !facultyData.faculty_code) {
        throw new Error('Vui lòng điền đầy đủ thông tin khoa');
      }

      return await FacultyServices.createFaculty(facultyData);
    } catch (error) {
      throw new Error(`Không thể tạo khoa mới: ${error.message}`);
    }
  },

  /**
   * Cập nhật thông tin khoa
   * @param {number} facultyId - ID của khoa
   * @param {Object} facultyData - Dữ liệu cập nhật
   */
  async updateFaculty(facultyId, facultyData) {
    try {
      return await FacultyServices.updateFaculty(facultyId, facultyData);
    } catch (error) {
      throw new Error(`Không thể cập nhật khoa: ${error.message}`);
    }
  },

  /**
   * Xóa khoa
   * @param {number} facultyId - ID của khoa
   */
  async deleteFaculty(facultyId) {
    try {
      return await FacultyServices.deleteFaculty(facultyId);
    } catch (error) {
      throw new Error(`Không thể xóa khoa: ${error.message}`);
    }
  }
};