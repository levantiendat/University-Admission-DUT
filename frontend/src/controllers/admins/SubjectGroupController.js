import SubjectGroupServices from '../../models/admins/SubjectGroupServices';

export default {
  /**
   * Lấy danh sách tất cả các tổ hợp môn thi
   */
  async getAllSubjectGroups() {
    try {
      return await SubjectGroupServices.getAllSubjectGroups();
    } catch (error) {
      throw new Error(`Không thể lấy danh sách tổ hợp môn thi: ${error.message}`);
    }
  },

  /**
   * Lấy thông tin chi tiết của một tổ hợp môn thi
   * @param {number} groupId - ID của tổ hợp môn thi
   */
  async getSubjectGroupById(groupId) {
    try {
      return await SubjectGroupServices.getSubjectGroup(groupId);
    } catch (error) {
      throw new Error(`Không thể lấy thông tin tổ hợp môn thi: ${error.message}`);
    }
  },

  /**
   * Tạo tổ hợp môn thi mới
   * @param {Object} groupData - Dữ liệu tổ hợp môn thi mới
   */
  async createSubjectGroup(groupData) {
    try {
      // Validate input
      if (!groupData.name || !groupData.name.trim()) {
        throw new Error('Tên tổ hợp môn thi không được để trống');
      }

      return await SubjectGroupServices.createSubjectGroup(groupData);
    } catch (error) {
      throw new Error(`Không thể tạo tổ hợp môn thi mới: ${error.message}`);
    }
  },

  /**
   * Cập nhật thông tin tổ hợp môn thi
   * @param {number} groupId - ID của tổ hợp môn thi
   * @param {Object} groupData - Dữ liệu cập nhật
   */
  async updateSubjectGroup(groupId, groupData) {
    try {
      // Validate input
      if (!groupData.name || !groupData.name.trim()) {
        throw new Error('Tên tổ hợp môn thi không được để trống');
      }

      return await SubjectGroupServices.updateSubjectGroup(groupId, groupData);
    } catch (error) {
      throw new Error(`Không thể cập nhật tổ hợp môn thi: ${error.message}`);
    }
  },

  /**
   * Xóa tổ hợp môn thi
   * @param {number} groupId - ID của tổ hợp môn thi
   */
  async deleteSubjectGroup(groupId) {
    try {
      return await SubjectGroupServices.deleteSubjectGroup(groupId);
    } catch (error) {
      throw new Error(`Không thể xóa tổ hợp môn thi: ${error.message}`);
    }
  }
};