import preAdmissionService from '@/models/preAdmissionService'

export default {
  async getAllData() {
    try {
      // Lấy dữ liệu từ các API
      const faculties = await preAdmissionService.getFaculties()
      const majors = await preAdmissionService.getMajors()
      const admissionMethods = await preAdmissionService.getAdmissionMethods()
      const previousAdmissions = await preAdmissionService.getPreviousAdmissions()
      
      // Ghép dữ liệu thành một mảng duy nhất
      const combinedData = majors.map(major => {
        // Tìm khoa tương ứng
        const faculty = faculties.find(f => f.id === major.faculty_id) || {
          name: 'Chưa xác định',
          faculty_code: 'N/A'
        }
        
        // Lấy các điểm chuẩn của ngành này
        const majorAdmissions = previousAdmissions.filter(admission => 
          admission.major_id === major.id
        )
        
        // Tổ chức điểm chuẩn theo phương thức và năm
        const admissionScores = []
        
        // Xử lý từng phương thức xét tuyển (chỉ lấy phương thức 2-6)
        admissionMethods.forEach(method => {
          if (method.id >= 2 && method.id <= 6) {
            // Tìm điểm theo từng năm
            const scores = {
              methodId: method.id,
              methodName: method.name,
              years: {}
            }
            
            majorAdmissions.forEach(admission => {
              if (admission.admission_methods_id === method.id) {
                scores.years[admission.year] = admission.score
              }
            })
            
            admissionScores.push(scores)
          }
        })
        
        // Tạo đối tượng kết quả
        return {
          id: major.id,
          name: major.name,
          major_code: major.major_code,
          seats: major.seats,
          faculty: {
            id: faculty.id,
            name: faculty.name,
            code: faculty.faculty_code
          },
          admissionScores: admissionScores
        }
      })
      
      // Trả về cả dữ liệu và phương thức xét tuyển
      return {
        combinedData: combinedData,
        admissionMethods: admissionMethods.filter(method => method.id >= 2 && method.id <= 6)
      }
    } catch (error) {
      console.error('Error in getAllData:', error)
      throw error
    }
  },
  
  // Tính toán dữ liệu cho biểu đồ
  prepareChartData(combinedData, viewType) {
    if (viewType === 'major') {
      // Dữ liệu biểu đồ theo ngành
      return this.prepareMajorChartData(combinedData)
    } else if (viewType === 'faculty') {
      // Dữ liệu biểu đồ theo khoa
      return this.prepareFacultyChartData(combinedData)
    } else if (viewType === 'university') {
      // Dữ liệu biểu đồ theo trường
      return this.prepareUniversityChartData(combinedData)
    }
    
    return null
  },
  
  prepareMajorChartData(combinedData) {
    // Hiển thị điểm chuẩn của một ngành qua các năm và phương thức
    const chartData = combinedData.map(major => {
      const datasets = []
      
      // Lấy danh sách tất cả các năm từ dữ liệu
      const allYears = new Set()
      major.admissionScores.forEach(method => {
        Object.keys(method.years).forEach(year => allYears.add(parseInt(year)))
      })
      const years = Array.from(allYears).sort()
      
      // Tạo datasets cho biểu đồ
      major.admissionScores.forEach(method => {
        // Tính toán điểm theo thang điểm tương đối
        const maxScore = this.getMaxScoreForMethod(method.methodId)
        
        const data = years.map(year => {
          const score = method.years[year] || null
          // Nếu score có giá trị, chuẩn hóa về thang 100
          return score !== null ? (score / maxScore) * 100 : null
        })
        
        datasets.push({
          label: method.methodName,
          data: data,
          backgroundColor: this.getColorForMethod(method.methodId)
        })
      })
      
      return {
        majorName: major.name,
        labels: years.map(year => year.toString()),
        datasets: datasets
      }
    })
    
    return chartData
  },
  
  prepareFacultyChartData(combinedData) {
    // Tổ chức dữ liệu theo khoa
    const facultyMap = {}
    
    combinedData.forEach(major => {
      const facultyId = major.faculty.id
      if (!facultyMap[facultyId]) {
        facultyMap[facultyId] = {
          id: facultyId,
          name: major.faculty.name,
          code: major.faculty.code,
          majors: []
        }
      }
      facultyMap[facultyId].majors.push(major)
    })
    
    // Chuyển thành mảng các khoa
    const faculties = Object.values(facultyMap)
    
    // Tạo dữ liệu biểu đồ cho từng khoa
    return faculties.map(faculty => {
      const latestYear = this.getLatestYearFromData(combinedData)
      
      // Lấy điểm của các ngành trong khoa ở năm mới nhất
      const datasets = []
      
      // Xử lý từng phương thức xét tuyển (2-6)
      for (let methodId = 2; methodId <= 6; methodId++) {
        const data = faculty.majors.map(major => {
          const methodData = major.admissionScores.find(m => m.methodId === methodId)
          if (!methodData || !methodData.years[latestYear]) return null
          
          // Chuẩn hóa điểm về thang 100
          const maxScore = this.getMaxScoreForMethod(methodId)
          return (methodData.years[latestYear] / maxScore) * 100
        })
        
        datasets.push({
          label: `Phương thức ${methodId}`,
          data: data,
          backgroundColor: this.getColorForMethod(methodId)
        })
      }
      
      return {
        facultyName: faculty.name,
        labels: faculty.majors.map(major => major.name),
        datasets: datasets
      }
    })
  },
  
  prepareUniversityChartData(combinedData) {
    // Biểu đồ tổng thể của trường, so sánh điểm trung bình các ngành
    const latestYear = this.getLatestYearFromData(combinedData)
    
    const datasets = []
    
    // Xử lý từng phương thức xét tuyển (2-6)
    for (let methodId = 2; methodId <= 6; methodId++) {
      const data = combinedData.map(major => {
        const methodData = major.admissionScores.find(m => m.methodId === methodId)
        if (!methodData || !methodData.years[latestYear]) return null
        
        // Chuẩn hóa điểm về thang 100
        const maxScore = this.getMaxScoreForMethod(methodId)
        return (methodData.years[latestYear] / maxScore) * 100
      })
      
      datasets.push({
        label: `Phương thức ${methodId}`,
        data: data,
        backgroundColor: this.getColorForMethod(methodId)
      })
    }
    
    return {
      universityName: "Trường Đại học",
      labels: combinedData.map(major => major.name),
      datasets: datasets
    }
  },
  
  getLatestYearFromData(combinedData) {
    const allYears = new Set()
    
    combinedData.forEach(major => {
      major.admissionScores.forEach(method => {
        Object.keys(method.years).forEach(year => allYears.add(parseInt(year)))
      })
    })
    
    return Math.max(...Array.from(allYears))
  },
  
  getMaxScoreForMethod(methodId) {
    // Thang điểm tối đa của từng phương thức
    const maxScores = {
      2: 300,
      3: 30,
      4: 1200,
      5: 100,
      6: 30
    }
    
    return maxScores[methodId] || 100  // Mặc định nếu không tìm thấy
  },
  
  getColorForMethod(methodId) {
    // Màu sắc cho từng phương thức
    const colors = {
      2: 'rgba(54, 162, 235, 0.7)',  // Xanh dương
      3: 'rgba(255, 206, 86, 0.7)',  // Vàng
      4: 'rgba(75, 192, 192, 0.7)',  // Xanh lá
      5: 'rgba(153, 102, 255, 0.7)', // Tím
      6: 'rgba(255, 159, 64, 0.7)'   // Cam
    }
    
    return colors[methodId] || 'rgba(201, 203, 207, 0.7)'  // Màu xám mặc định
  }
}