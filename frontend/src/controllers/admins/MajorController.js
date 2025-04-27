import MajorServices from '../../models/admins/MajorServices';

export default {
  /**
   * Lấy danh sách tất cả ngành học
   */
  async getAllMajors() {
    try {
      return await MajorServices.getAllMajors();
    } catch (error) {
      throw new Error(`Không thể lấy danh sách ngành: ${error.message}`);
    }
  },

  /**
   * Lấy thông tin chi tiết của một ngành học
   * @param {number} majorId - ID của ngành học
   */
  async getMajorById(majorId) {
    try {
      return await MajorServices.getMajor(majorId);
    } catch (error) {
      throw new Error(`Không thể lấy thông tin ngành: ${error.message}`);
    }
  },

  /**
   * Lấy danh sách ngành học theo khoa
   * @param {number} facultyId - ID của khoa
   */
  async getMajorsByFaculty(facultyId) {
    try {
      return await MajorServices.getMajorsByFaculty(facultyId);
    } catch (error) {
      throw new Error(`Không thể lấy danh sách ngành theo khoa: ${error.message}`);
    }
  },

  /**
   * Tạo ngành học mới
   * @param {Object} majorData - Dữ liệu ngành học mới
   */
  async createMajor(majorData) {
    try {
      // Validate input
      if (!majorData.name || !majorData.major_code || !majorData.faculty_id) {
        throw new Error('Vui lòng điền đầy đủ thông tin ngành');
      }
      
      // Ensure seats is a number
      if (majorData.seats) {
        majorData.seats = parseInt(majorData.seats);
      }

      return await MajorServices.createMajor(majorData);
    } catch (error) {
      throw new Error(`Không thể tạo ngành mới: ${error.message}`);
    }
  },

  /**
   * Cập nhật thông tin ngành học
   * @param {number} majorId - ID của ngành học
   * @param {Object} majorData - Dữ liệu cập nhật
   */
  async updateMajor(majorId, majorData) {
    try {
      // Ensure seats is a number if provided
      if (majorData.seats) {
        majorData.seats = parseInt(majorData.seats);
      }
      
      return await MajorServices.updateMajor(majorId, majorData);
    } catch (error) {
      throw new Error(`Không thể cập nhật ngành: ${error.message}`);
    }
  },

  /**
   * Xóa ngành học
   * @param {number} majorId - ID của ngành học
   */
  async deleteMajor(majorId) {
    try {
      return await MajorServices.deleteMajor(majorId);
    } catch (error) {
      throw new Error(`Không thể xóa ngành: ${error.message}`);
    }
  }
};