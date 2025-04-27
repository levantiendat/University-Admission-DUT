import SubjectGroupDetailServices from '../../models/admins/SubjectGroupDetailServices';

export default {
  /**
   * Lấy danh sách tất cả chi tiết môn học trong tổ hợp
   */
  async getAllSubjectGroupDetails() {
    try {
      return await SubjectGroupDetailServices.getAllSubjectGroupDetails();
    } catch (error) {
      throw new Error(`Không thể lấy danh sách chi tiết môn học trong tổ hợp: ${error.message}`);
    }
  },

  /**
   * Lấy chi tiết của một môn trong tổ hợp
   * @param {number} detailId - ID của chi tiết môn trong tổ hợp
   */
  async getSubjectGroupDetailById(detailId) {
    try {
      return await SubjectGroupDetailServices.getSubjectGroupDetail(detailId);
    } catch (error) {
      throw new Error(`Không thể lấy thông tin chi tiết môn học trong tổ hợp: ${error.message}`);
    }
  },

  /**
   * Lấy tất cả chi tiết môn học trong một tổ hợp
   * @param {number} groupId - ID của tổ hợp
   */
  async getSubjectGroupDetailsByGroup(groupId) {
    try {
      return await SubjectGroupDetailServices.getSubjectGroupDetailsByGroup(groupId);
    } catch (error) {
      throw new Error(`Không thể lấy danh sách chi tiết môn học cho tổ hợp: ${error.message}`);
    }
  },

  /**
   * Tạo mới chi tiết môn học trong tổ hợp
   * @param {Object} detailData - Dữ liệu chi tiết môn học trong tổ hợp
   */
  async createSubjectGroupDetail(detailData) {
    try {
      // Validate input
      if (!detailData.group_id || !detailData.subject_id) {
        throw new Error('Vui lòng chọn tổ hợp và môn học');
      }

      // Ensure coefficient is a number
      if (detailData.coefficient !== undefined) {
        detailData.coefficient = parseFloat(detailData.coefficient);
        if (isNaN(detailData.coefficient) || detailData.coefficient <= 0) {
          throw new Error('Hệ số phải là số dương');
        }
      } else {
        detailData.coefficient = 1; // Default coefficient
      }

      return await SubjectGroupDetailServices.createSubjectGroupDetail(detailData);
    } catch (error) {
      throw new Error(`Không thể tạo chi tiết môn học trong tổ hợp: ${error.message}`);
    }
  },

  /**
   * Cập nhật chi tiết môn học trong tổ hợp
   * @param {number} detailId - ID của chi tiết môn học trong tổ hợp
   * @param {Object} detailData - Dữ liệu cập nhật
   */
  async updateSubjectGroupDetail(detailId, detailData) {
    try {
      // Validate coefficient if provided
      if (detailData.coefficient !== undefined) {
        detailData.coefficient = parseFloat(detailData.coefficient);
        if (isNaN(detailData.coefficient) || detailData.coefficient <= 0) {
          throw new Error('Hệ số phải là số dương');
        }
      }

      return await SubjectGroupDetailServices.updateSubjectGroupDetail(detailId, detailData);
    } catch (error) {
      throw new Error(`Không thể cập nhật chi tiết môn học trong tổ hợp: ${error.message}`);
    }
  },

  /**
   * Xóa chi tiết môn học trong tổ hợp
   * @param {number} detailId - ID của chi tiết môn học trong tổ hợp
   */
  async deleteSubjectGroupDetail(detailId) {
    try {
      return await SubjectGroupDetailServices.deleteSubjectGroupDetail(detailId);
    } catch (error) {
      throw new Error(`Không thể xóa chi tiết môn học trong tổ hợp: ${error.message}`);
    }
  }
};