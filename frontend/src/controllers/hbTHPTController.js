import hbTHPTService from '@/models/hbTHPTService'

const TNTHPTController = {
  /**
   * Lấy và xử lý dữ liệu tuyển sinh để hiển thị
   * @returns {Promise<Object>} - Dữ liệu đã được xử lý
   */
  async getHocBaData() {
    try {
      // Gọi trực tiếp các hàm async (không cần Promise.all nếu không phải mảng promises)
      const hocba = await hbTHPTService.getTestTHPTs();
      const majors = await hbTHPTService.getMajors();

      console.log('hocba', hocba);
      console.log('majors', majors);
      
      return {
        hocba,
        majors
      };
    } catch (error) {
      console.error('Lỗi khi xử lý dữ liệu tuyển sinh:', error);
      throw error;
    }
  }
};

export default TNTHPTController;
