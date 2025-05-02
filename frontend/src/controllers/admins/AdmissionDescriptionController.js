import AdmissionDescriptionServices from '../../models/admins/AdmissionDescriptionServices';

export default {
  /**
   * Lấy danh sách môn học / lĩnh vực xét tuyển của tất cả các ngành
   */
  async getAllAdmissionDescriptions() {
    try {
      return await AdmissionDescriptionServices.getAllAdmissionDescriptions();
    } catch (error) {
      throw new Error(`Không thể lấy danh sách môn học/lĩnh vực xét tuyển: ${error.message}`);
    }
  },

  /**
   * Lấy danh sách môn học / lĩnh vực xét tuyển của một ngành cụ thể
   * @param {number} majorId - ID của ngành
   */
  async getAdmissionDescriptionsByMajor(majorId) {
    try {
      return await AdmissionDescriptionServices.getAdmissionDescriptionsByMajor(majorId);
    } catch (error) {
      throw new Error(`Không thể lấy danh sách môn học/lĩnh vực của ngành: ${error.message}`);
    }
  },

  /**
   * Lấy thông tin chi tiết của một mô tả xét tuyển
   * @param {number} id - ID của mô tả xét tuyển
   */
  async getAdmissionDescriptionById(id) {
    try {
      return await AdmissionDescriptionServices.getAdmissionDescription(id);
    } catch (error) {
      throw new Error(`Không thể lấy thông tin môn học/lĩnh vực: ${error.message}`);
    }
  },

  /**
   * Tạo mô tả xét tuyển mới
   * @param {Object} data - Dữ liệu mô tả xét tuyển mới
   */
  async createAdmissionDescription(data) {
    try {
      // Validate input
      if (!data.major_id) {
        throw new Error('Vui lòng chọn ngành');
      }

      if (!data.field_or_subject_name || data.field_or_subject_name.trim() === '') {
        throw new Error('Vui lòng nhập tên lĩnh vực hoặc môn học');
      }

      // Format data
      const formattedData = {
        major_id: parseInt(data.major_id),
        field_or_subject_name: data.field_or_subject_name.trim()
      };

      return await AdmissionDescriptionServices.createAdmissionDescription(formattedData);
    } catch (error) {
      throw new Error(`Không thể tạo môn học/lĩnh vực mới: ${error.message}`);
    }
  },

  /**
   * Cập nhật thông tin mô tả xét tuyển
   * @param {number} id - ID của mô tả xét tuyển
   * @param {Object} data - Dữ liệu cập nhật
   */
  async updateAdmissionDescription(id, data) {
    try {
      // Validate
      if (data.field_or_subject_name && data.field_or_subject_name.trim() === '') {
        throw new Error('Tên lĩnh vực hoặc môn học không được để trống');
      }

      // Format data
      const formattedData = { ...data };
      if (formattedData.major_id) formattedData.major_id = parseInt(formattedData.major_id);
      if (formattedData.field_or_subject_name) formattedData.field_or_subject_name = formattedData.field_or_subject_name.trim();

      return await AdmissionDescriptionServices.updateAdmissionDescription(id, formattedData);
    } catch (error) {
      throw new Error(`Không thể cập nhật môn học/lĩnh vực: ${error.message}`);
    }
  },

  /**
   * Xóa mô tả xét tuyển
   * @param {number} id - ID của mô tả xét tuyển
   */
  async deleteAdmissionDescription(id) {
    try {
      return await AdmissionDescriptionServices.deleteAdmissionDescription(id);
    } catch (error) {
      throw new Error(`Không thể xóa môn học/lĩnh vực: ${error.message}`);
    }
  }
};