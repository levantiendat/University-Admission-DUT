import SchoolPriorityServices from '../../models/admins/SchoolPriorityServices';

export default {
  /**
   * Lấy danh sách tỉnh/thành phố
   */
  async getAllCities() {
    try {
      return await SchoolPriorityServices.getAllCities();
    } catch (error) {
      throw new Error(`Không thể lấy danh sách tỉnh/thành phố: ${error.message}`);
    }
  },

  /**
   * Lấy thông tin chi tiết của một tỉnh/thành phố
   * @param {number} id - ID của tỉnh/thành phố
   */
  async getCityById(id) {
    try {
      return await SchoolPriorityServices.getCity(id);
    } catch (error) {
      throw new Error(`Không thể lấy thông tin tỉnh/thành phố: ${error.message}`);
    }
  },

  /**
   * Tạo tỉnh/thành phố mới
   * @param {Object} data - Dữ liệu tỉnh/thành phố
   */
  async createCity(data) {
    try {
      // Validate input
      if (!data.city_code || data.city_code.trim() === '') {
        throw new Error('Vui lòng nhập mã tỉnh/thành phố');
      }

      if (!data.name || data.name.trim() === '') {
        throw new Error('Vui lòng nhập tên tỉnh/thành phố');
      }

      // Format data
      const formattedData = {
        city_code: data.city_code.trim(),
        name: data.name.trim()
      };

      return await SchoolPriorityServices.createCity(formattedData);
    } catch (error) {
      throw new Error(`Không thể tạo tỉnh/thành phố mới: ${error.message}`);
    }
  },

  /**
   * Cập nhật thông tin tỉnh/thành phố
   * @param {number} id - ID của tỉnh/thành phố
   * @param {Object} data - Dữ liệu cập nhật
   */
  async updateCity(id, data) {
    try {
      // Validate data
      if (data.city_code !== undefined && data.city_code.trim() === '') {
        throw new Error('Mã tỉnh/thành phố không được để trống');
      }

      if (data.name !== undefined && data.name.trim() === '') {
        throw new Error('Tên tỉnh/thành phố không được để trống');
      }

      // Format data
      const formattedData = { ...data };
      if (formattedData.city_code) formattedData.city_code = formattedData.city_code.trim();
      if (formattedData.name) formattedData.name = formattedData.name.trim();

      return await SchoolPriorityServices.updateCity(id, formattedData);
    } catch (error) {
      throw new Error(`Không thể cập nhật tỉnh/thành phố: ${error.message}`);
    }
  },

  /**
   * Xóa tỉnh/thành phố
   * @param {number} id - ID của tỉnh/thành phố
   */
  async deleteCity(id) {
    try {
      return await SchoolPriorityServices.deleteCity(id);
    } catch (error) {
      throw new Error(`Không thể xóa tỉnh/thành phố: ${error.message}`);
    }
  },

  /**
   * Lấy danh sách quận/huyện theo tỉnh/thành phố
   * @param {number} cityId - ID của tỉnh/thành phố
   */
  async getDistrictsByCity(cityId) {
    try {
      return await SchoolPriorityServices.getDistrictsByCity(cityId);
    } catch (error) {
      throw new Error(`Không thể lấy danh sách quận/huyện cho tỉnh/thành phố: ${error.message}`);
    }
  },

  /**
   * Lấy thông tin chi tiết của một quận/huyện
   * @param {number} id - ID của quận/huyện
   */
  async getDistrictById(id) {
    try {
      return await SchoolPriorityServices.getDistrict(id);
    } catch (error) {
      throw new Error(`Không thể lấy thông tin quận/huyện: ${error.message}`);
    }
  },

  /**
   * Tạo quận/huyện mới
   * @param {Object} data - Dữ liệu quận/huyện
   */
  async createDistrict(data) {
    try {
      // Validate input
      if (!data.district_code || data.district_code.trim() === '') {
        throw new Error('Vui lòng nhập mã quận/huyện');
      }

      if (!data.name || data.name.trim() === '') {
        throw new Error('Vui lòng nhập tên quận/huyện');
      }

      if (!data.city_id) {
        throw new Error('Vui lòng chọn tỉnh/thành phố');
      }

      // Format data
      const formattedData = {
        district_code: data.district_code.trim(),
        name: data.name.trim(),
        city_id: parseInt(data.city_id)
      };

      return await SchoolPriorityServices.createDistrict(formattedData);
    } catch (error) {
      throw new Error(`Không thể tạo quận/huyện mới: ${error.message}`);
    }
  },

  /**
   * Cập nhật thông tin quận/huyện
   * @param {number} id - ID của quận/huyện
   * @param {Object} data - Dữ liệu cập nhật
   */
  async updateDistrict(id, data) {
    try {
      // Validate data
      if (data.district_code !== undefined && data.district_code.trim() === '') {
        throw new Error('Mã quận/huyện không được để trống');
      }

      if (data.name !== undefined && data.name.trim() === '') {
        throw new Error('Tên quận/huyện không được để trống');
      }

      // Format data
      const formattedData = { ...data };
      if (formattedData.district_code) formattedData.district_code = formattedData.district_code.trim();
      if (formattedData.name) formattedData.name = formattedData.name.trim();
      if (formattedData.city_id) formattedData.city_id = parseInt(formattedData.city_id);

      return await SchoolPriorityServices.updateDistrict(id, formattedData);
    } catch (error) {
      throw new Error(`Không thể cập nhật quận/huyện: ${error.message}`);
    }
  },

  /**
   * Xóa quận/huyện
   * @param {number} id - ID của quận/huyện
   */
  async deleteDistrict(id) {
    try {
      return await SchoolPriorityServices.deleteDistrict(id);
    } catch (error) {
      throw new Error(`Không thể xóa quận/huyện: ${error.message}`);
    }
  },

  /**
   * Lấy danh sách trường theo quận/huyện
   * @param {number} districtId - ID của quận/huyện
   */
  async getSchoolsByDistrict(districtId) {
    try {
      return await SchoolPriorityServices.getSchoolsByDistrict(districtId);
    } catch (error) {
      throw new Error(`Không thể lấy danh sách trường cho quận/huyện: ${error.message}`);
    }
  },

  /**
   * Lấy danh sách trường theo tỉnh/thành phố
   * @param {number} cityId - ID của tỉnh/thành phố
   */
  async getSchoolsByCity(cityId) {
    try {
      return await SchoolPriorityServices.getSchoolsByCity(cityId);
    } catch (error) {
      throw new Error(`Không thể lấy danh sách trường cho tỉnh/thành phố: ${error.message}`);
    }
  },

  /**
   * Lấy thông tin chi tiết của một trường
   * @param {number} id - ID của trường
   */
  async getSchoolById(id) {
    try {
      return await SchoolPriorityServices.getSchool(id);
    } catch (error) {
      throw new Error(`Không thể lấy thông tin trường: ${error.message}`);
    }
  },

  /**
   * Tạo trường mới
   * @param {Object} data - Dữ liệu trường
   */
  async createSchool(data) {
    try {
      // Validate input
      if (!data.school_code || data.school_code.trim() === '') {
        throw new Error('Vui lòng nhập mã trường');
      }

      if (!data.name || data.name.trim() === '') {
        throw new Error('Vui lòng nhập tên trường');
      }

      if (!data.address || data.address.trim() === '') {
        throw new Error('Vui lòng nhập địa chỉ trường');
      }

      if (!data.district_id) {
        throw new Error('Vui lòng chọn quận/huyện');
      }

      if (!data.priority_area || !['KV1', 'KV2', 'KV2NT', 'KV3'].includes(data.priority_area)) {
        throw new Error('Vui lòng chọn khu vực ưu tiên hợp lệ');
      }

      // Format data
      const formattedData = {
        school_code: data.school_code.trim(),
        name: data.name.trim(),
        address: data.address.trim(),
        district_id: parseInt(data.district_id),
        priority_area: data.priority_area
      };

      return await SchoolPriorityServices.createSchool(formattedData);
    } catch (error) {
      throw new Error(`Không thể tạo trường mới: ${error.message}`);
    }
  },

  /**
   * Cập nhật thông tin trường
   * @param {number} id - ID của trường
   * @param {Object} data - Dữ liệu cập nhật
   */
  async updateSchool(id, data) {
    try {
      // Validate data
      if (data.school_code !== undefined && data.school_code.trim() === '') {
        throw new Error('Mã trường không được để trống');
      }

      if (data.name !== undefined && data.name.trim() === '') {
        throw new Error('Tên trường không được để trống');
      }

      if (data.address !== undefined && data.address.trim() === '') {
        throw new Error('Địa chỉ trường không được để trống');
      }

      if (data.priority_area !== undefined && !['KV1', 'KV2', 'KV2NT', 'KV3'].includes(data.priority_area)) {
        throw new Error('Khu vực ưu tiên không hợp lệ');
      }

      // Format data
      const formattedData = { ...data };
      if (formattedData.school_code) formattedData.school_code = formattedData.school_code.trim();
      if (formattedData.name) formattedData.name = formattedData.name.trim();
      if (formattedData.address) formattedData.address = formattedData.address.trim();
      if (formattedData.district_id) formattedData.district_id = parseInt(formattedData.district_id);

      return await SchoolPriorityServices.updateSchool(id, formattedData);
    } catch (error) {
      throw new Error(`Không thể cập nhật trường: ${error.message}`);
    }
  },

  /**
   * Xóa trường
   * @param {number} id - ID của trường
   */
  async deleteSchool(id) {
    try {
      return await SchoolPriorityServices.deleteSchool(id);
    } catch (error) {
      throw new Error(`Không thể xóa trường: ${error.message}`);
    }
  }
};