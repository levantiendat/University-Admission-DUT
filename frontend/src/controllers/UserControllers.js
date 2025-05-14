import userServices from '@/models/UserServices'

class UserController {
  // Lấy thông tin người dùng hiện tại
  static async getUserInfo() {
    try {
      const userInfo = await userServices.getUserInfo()
      return userInfo
    } catch (error) {
      console.error('Error in getUserInfo controller:', error)
      throw error
    }
  }

  // Cập nhật thông tin cá nhân
  static async updateUserInfo(userData) {
    try {
      const updatedUser = await userServices.updateUserInfo(userData)
      return updatedUser
    } catch (error) {
      console.error('Error in updateUserInfo controller:', error)
      throw error
    }
  }

  // Đổi mật khẩu người dùng
  static async changePassword(oldPassword, newPassword) {
    try {
      const passwordData = {
        old_password: oldPassword,
        new_password: newPassword
      }
      const response = await userServices.changePassword(passwordData)
      return response
    } catch (error) {
      console.error('Error in changePassword controller:', error)
      throw error
    }
  }

  // Đăng xuất người dùng
  static logout() {
    // Xóa token từ session storage
    sessionStorage.removeItem('token')
  }

  // Kiểm tra xem người dùng có phải là instructor không
  static isInstructor(user) {
    return user && user.role === 'instructor'
  }

  // Kiểm tra xem người dùng có phải là user thường không
  static isRegularUser(user) {
    return user && user.role === 'user'
  }
}

export default UserController