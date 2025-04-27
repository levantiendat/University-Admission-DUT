import UserServices from '../../models/admins/UserService';

export default {
  /**
   * Lấy danh sách tất cả người dùng
   */
  async getAllUsers() {
    try {
      return await UserServices.getUsers();
    } catch (error) {
      throw new Error(`Không thể lấy danh sách người dùng: ${error.message}`);
    }
  },

  /**
   * Lấy thông tin chi tiết của một người dùng
   * @param {number} userId - ID của người dùng
   */
  async getUserById(userId) {
    try {
      return await UserServices.getUser(userId);
    } catch (error) {
      throw new Error(`Không thể lấy thông tin người dùng: ${error.message}`);
    }
  },

  /**
   * Cập nhật thông tin người dùng
   * @param {number} userId - ID của người dùng
   * @param {Object} userData - Dữ liệu cập nhật
   */
  async updateUser(userId, userData) {
    try {
      return await UserServices.updateUser(userId, userData);
    } catch (error) {
      throw new Error(`Không thể cập nhật người dùng: ${error.message}`);
    }
  },

  /**
   * Cập nhật role của người dùng
   * @param {number} userId - ID của người dùng
   * @param {string} role - Role mới (user/instructor)
   */
  async updateUserRole(userId, role) {
    try {
      if (!['user', 'instructor'].includes(role)) {
        throw new Error('Role không hợp lệ. Role phải là "user" hoặc "instructor"');
      }
      return await UserServices.updateUserRole(userId, role);
    } catch (error) {
      throw new Error(`Không thể cập nhật role người dùng: ${error.message}`);
    }
  },

  /**
   * Tạo người dùng mới
   * @param {Object} userData - Dữ liệu người dùng mới
   * @param {string} role - Role của người dùng (user/instructor)
   */
  async createUser(userData, role) {
    try {
      // Validate input
      if (!userData.name || !userData.email || !userData.phone_number || !userData.password) {
        throw new Error('Vui lòng điền đầy đủ thông tin người dùng');
      }
      
      if (!['user', 'instructor'].includes(role)) {
        throw new Error('Role không hợp lệ. Role phải là "user" hoặc "instructor"');
      }

      return await UserServices.createUser(userData, role);
    } catch (error) {
      throw new Error(`Không thể tạo người dùng mới: ${error.message}`);
    }
  }
};