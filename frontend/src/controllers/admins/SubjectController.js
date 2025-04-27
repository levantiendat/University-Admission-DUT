import SubjectServices from '../../models/admins/SubjectServices';

export default {
  /**
   * Lấy danh sách tất cả các môn thi
   */
  async getAllSubjects() {
    try {
      return await SubjectServices.getAllSubjects();
    } catch (error) {
      throw new Error(`Không thể lấy danh sách môn thi: ${error.message}`);
    }
  },

  /**
   * Lấy thông tin chi tiết của một môn thi
   * @param {number} subjectId - ID của môn thi
   */
  async getSubjectById(subjectId) {
    try {
      return await SubjectServices.getSubject(subjectId);
    } catch (error) {
      throw new Error(`Không thể lấy thông tin môn thi: ${error.message}`);
    }
  },

  /**
   * Tạo môn thi mới
   * @param {Object} subjectData - Dữ liệu môn thi mới
   */
  async createSubject(subjectData) {
    try {
      // Validate input
      if (!subjectData.name || !subjectData.name.trim()) {
        throw new Error('Tên môn thi không được để trống');
      }

      return await SubjectServices.createSubject(subjectData);
    } catch (error) {
      throw new Error(`Không thể tạo môn thi mới: ${error.message}`);
    }
  },

  /**
   * Cập nhật thông tin môn thi
   * @param {number} subjectId - ID của môn thi
   * @param {Object} subjectData - Dữ liệu cập nhật
   */
  async updateSubject(subjectId, subjectData) {
    try {
      // Validate input
      if (!subjectData.name || !subjectData.name.trim()) {
        throw new Error('Tên môn thi không được để trống');
      }

      return await SubjectServices.updateSubject(subjectId, subjectData);
    } catch (error) {
      throw new Error(`Không thể cập nhật môn thi: ${error.message}`);
    }
  },

  /**
   * Xóa môn thi
   * @param {number} subjectId - ID của môn thi
   */
  async deleteSubject(subjectId) {
    try {
      return await SubjectServices.deleteSubject(subjectId);
    } catch (error) {
      throw new Error(`Không thể xóa môn thi: ${error.message}`);
    }
  }
};