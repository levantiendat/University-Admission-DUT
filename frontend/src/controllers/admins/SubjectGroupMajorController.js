import SubjectGroupMajorServices from '../../models/admins/SubjectGroupMajorServices';

export default {
  /**
   * Lấy danh sách tất cả các mối quan hệ giữa tổ hợp môn và ngành tuyển sinh
   */
  async getAllSubjectGroupMajors() {
    try {
      return await SubjectGroupMajorServices.getAllSubjectGroupMajors();
    } catch (error) {
      throw new Error(`Không thể lấy danh sách mối quan hệ: ${error.message}`);
    }
  },

  /**
   * Lấy thông tin chi tiết của một mối quan hệ
   * @param {number} relationId - ID của mối quan hệ
   */
  async getSubjectGroupMajorById(relationId) {
    try {
      return await SubjectGroupMajorServices.getSubjectGroupMajor(relationId);
    } catch (error) {
      throw new Error(`Không thể lấy thông tin mối quan hệ: ${error.message}`);
    }
  },

  /**
   * Tạo mối quan hệ mới giữa tổ hợp môn và ngành tuyển sinh
   * @param {Object} data - Dữ liệu mối quan hệ mới
   */
  async createSubjectGroupMajor(data) {
    try {
      // Validate input
      if (!data.group_id || !data.admission_method_major_id) {
        throw new Error('Vui lòng chọn tổ hợp môn và phương thức tuyển sinh của ngành');
      }

      return await SubjectGroupMajorServices.createSubjectGroupMajor(data);
    } catch (error) {
      throw new Error(`Không thể tạo mối quan hệ mới: ${error.message}`);
    }
  },

  /**
   * Cập nhật thông tin mối quan hệ
   * @param {number} relationId - ID của mối quan hệ
   * @param {Object} data - Dữ liệu cập nhật
   */
  async updateSubjectGroupMajor(relationId, data) {
    try {
      // Validate input
      if ((!data.group_id && data.group_id !== 0) || (!data.admission_method_major_id && data.admission_method_major_id !== 0)) {
        throw new Error('Vui lòng chọn tổ hợp môn và phương thức tuyển sinh của ngành');
      }

      return await SubjectGroupMajorServices.updateSubjectGroupMajor(relationId, data);
    } catch (error) {
      throw new Error(`Không thể cập nhật mối quan hệ: ${error.message}`);
    }
  },

  /**
   * Xóa mối quan hệ
   * @param {number} relationId - ID của mối quan hệ
   */
  async deleteSubjectGroupMajor(relationId) {
    try {
      return await SubjectGroupMajorServices.deleteSubjectGroupMajor(relationId);
    } catch (error) {
      throw new Error(`Không thể xóa mối quan hệ: ${error.message}`);
    }
  }
};