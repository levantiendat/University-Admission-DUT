import dgtdService from '@/models/DGTDService'

const DGTDController = {
  /**
   * Lấy và xử lý dữ liệu tuyển sinh để hiển thị
   * @returns {Promise<Object>} - Dữ liệu đã được xử lý
   */
  async getDGTDData() {
    try {
      // Gọi trực tiếp các hàm async (không cần Promise.all nếu không phải mảng promises)
      const dgtd = await dgtdService.getDGTDs();
      const majors = await dgtdService.getMajors();

      console.log('xtt', dgtd);
      console.log('majors', majors);
      
      return {
        dgtd,
        majors
      };
    } catch (error) {
      console.error('Lỗi khi xử lý dữ liệu tuyển sinh:', error);
      throw error;
    }
  }
};

export default DGTDController;
