import xttService from '@/models/xtThangService'

const XTTController = {
  /**
   * Lấy và xử lý dữ liệu tuyển sinh để hiển thị
   * @returns {Promise<Object>} - Dữ liệu đã được xử lý
   */
  async getXTTData() {
    try {
      // Gọi trực tiếp các hàm async (không cần Promise.all nếu không phải mảng promises)
      const xtt = await xttService.getXTTs();
      const majors = await xttService.getMajors();

      console.log('xtt', xtt);
      console.log('majors', majors);
      
      return {
        xtt,
        majors
      };
    } catch (error) {
      console.error('Lỗi khi xử lý dữ liệu tuyển sinh:', error);
      throw error;
    }
  }
};

export default XTTController;
