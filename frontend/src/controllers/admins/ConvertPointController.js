import ConvertPointServices from '../../models/admins/ConvertPointServices';

export default {
  /**
   * Lấy danh sách quy đổi điểm
   */
  async getAllConvertPoints() {
    try {
      return await ConvertPointServices.getAllConvertPoints();
    } catch (error) {
      throw new Error(`Không thể lấy danh sách quy đổi điểm: ${error.message}`);
    }
  },

  /**
   * Lấy thông tin chi tiết của một quy đổi điểm
   * @param {number} id - ID của quy đổi điểm
   */
  async getConvertPointById(id) {
    try {
      return await ConvertPointServices.getConvertPoint(id);
    } catch (error) {
      throw new Error(`Không thể lấy thông tin quy đổi điểm: ${error.message}`);
    }
  },

  /**
   * Tạo quy đổi điểm mới
   * @param {Object} data - Dữ liệu quy đổi điểm mới
   */
  async createConvertPoint(data) {
    try {
      // Validate input
      this.validateConvertPointData(data);

      // Format data
      const formattedData = {
        admission_methods_id: parseInt(data.admission_methods_id),
        origin_min: parseFloat(parseFloat(data.origin_min).toFixed(2)),
        origin_max: parseFloat(parseFloat(data.origin_max).toFixed(2)),
        convert_score_min: parseFloat(parseFloat(data.convert_score_min).toFixed(2)),
        convert_score_max: parseFloat(parseFloat(data.convert_score_max).toFixed(2))
      };

      return await ConvertPointServices.createConvertPoint(formattedData);
    } catch (error) {
      throw new Error(`Không thể tạo quy đổi điểm mới: ${error.message}`);
    }
  },

  /**
   * Cập nhật thông tin quy đổi điểm
   * @param {number} id - ID của quy đổi điểm
   * @param {Object} data - Dữ liệu cập nhật
   */
  async updateConvertPoint(id, data) {
    try {
      // Validate data
      this.validateConvertPointData(data);

      // Format data
      const formattedData = { ...data };
      if (formattedData.admission_methods_id) formattedData.admission_methods_id = parseInt(formattedData.admission_methods_id);
      if (formattedData.origin_min !== undefined) formattedData.origin_min = parseFloat(parseFloat(formattedData.origin_min).toFixed(2));
      if (formattedData.origin_max !== undefined) formattedData.origin_max = parseFloat(parseFloat(formattedData.origin_max).toFixed(2));
      if (formattedData.convert_score_min !== undefined) formattedData.convert_score_min = parseFloat(parseFloat(formattedData.convert_score_min).toFixed(2));
      if (formattedData.convert_score_max !== undefined) formattedData.convert_score_max = parseFloat(parseFloat(formattedData.convert_score_max).toFixed(2));

      return await ConvertPointServices.updateConvertPoint(id, formattedData);
    } catch (error) {
      throw new Error(`Không thể cập nhật quy đổi điểm: ${error.message}`);
    }
  },

  /**
   * Xóa quy đổi điểm
   * @param {number} id - ID của quy đổi điểm
   */
  async deleteConvertPoint(id) {
    try {
      return await ConvertPointServices.deleteConvertPoint(id);
    } catch (error) {
      throw new Error(`Không thể xóa quy đổi điểm: ${error.message}`);
    }
  },

  /**
   * Kiểm tra dữ liệu quy đổi điểm
   * @param {Object} data - Dữ liệu quy đổi điểm
   */
  validateConvertPointData(data) {
    if (!data.admission_methods_id) {
      throw new Error('Vui lòng chọn phương thức xét tuyển');
    }

    if (data.origin_min === undefined || data.origin_min === null || isNaN(parseFloat(data.origin_min))) {
      throw new Error('Điểm gốc tối thiểu phải là một số hợp lệ');
    }

    if (data.origin_max === undefined || data.origin_max === null || isNaN(parseFloat(data.origin_max))) {
      throw new Error('Điểm gốc tối đa phải là một số hợp lệ');
    }

    if (parseFloat(data.origin_min) >= parseFloat(data.origin_max)) {
      throw new Error('Điểm gốc tối thiểu phải nhỏ hơn điểm gốc tối đa');
    }

    if (data.convert_score_min === undefined || data.convert_score_min === null || isNaN(parseFloat(data.convert_score_min))) {
      throw new Error('Điểm quy đổi tối thiểu phải là một số hợp lệ');
    }

    if (data.convert_score_max === undefined || data.convert_score_max === null || isNaN(parseFloat(data.convert_score_max))) {
      throw new Error('Điểm quy đổi tối đa phải là một số hợp lệ');
    }

    if (parseFloat(data.convert_score_min) >= parseFloat(data.convert_score_max)) {
      throw new Error('Điểm quy đổi tối thiểu phải nhỏ hơn điểm quy đổi tối đa');
    }

    if (parseFloat(data.convert_score_min) < 0 || parseFloat(data.convert_score_min) > 30) {
      throw new Error('Điểm quy đổi tối thiểu phải nằm trong khoảng từ 0 đến 30');
    }

    if (parseFloat(data.convert_score_max) < 0 || parseFloat(data.convert_score_max) > 30) {
      throw new Error('Điểm quy đổi tối đa phải nằm trong khoảng từ 0 đến 30');
    }
  }
};