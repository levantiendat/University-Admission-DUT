import axios from 'axios';
import config from '@/config/apiConfig';
import { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, BorderStyle } from 'docx';
import { saveAs } from 'file-saver';

const RASA_ENDPOINT = 'http://localhost:5005/webhooks/rest/webhook';

export default {
  /**
   * Send a message to the Rasa chatbot
   * @param {string} message - User message text
   * @param {string} userId - User identifier
   * @returns {Promise} - Promise with the Rasa response
   */
  async sendMessage(message, userId) {
    try {
      const response = await axios.post(RASA_ENDPOINT, {
        sender: userId,
        message: message
      });
      
      return response.data;
    } catch (error) {
      console.error('Error sending message to Rasa:', error);
      throw error;
    }
  },

  /**
   * Get chat history for this session from localStorage
   * @param {string} userId - User identifier
   * @returns {Array} - Array of message objects
   */
  getChatHistory(userId) {
    const historyKey = `rasa_chat_history_${userId}`;
    const history = localStorage.getItem(historyKey);
    return history ? JSON.parse(history) : [];
  },

  /**
   * Save chat history to localStorage
   * @param {string} userId - User identifier
   * @param {Array} messages - Array of message objects
   */
  saveChatHistory(userId, messages) {
    const historyKey = `rasa_chat_history_${userId}`;
    localStorage.setItem(historyKey, JSON.stringify(messages));
  },

  /**
   * Process message text to separate visible text from document content
   * @param {string} text - Full message text
   * @returns {Object} - Object with visibleText and documentContent
   */
  processMessageContent(text) {
    if (!text || typeof text !== 'string') {
      return { visibleText: text || '', documentContent: null };
    }
    
    const openTagIndex = text.indexOf('<document>');
    const closeTagIndex = text.lastIndexOf('<document>');
    
    // Không có thẻ document hoặc chỉ có một thẻ
    if (openTagIndex === -1 || openTagIndex === closeTagIndex) {
      // Không có thẻ document
      if (openTagIndex === -1) {
        return { visibleText: text, documentContent: null };
      }
      // Chỉ có một thẻ document (coi như thẻ mở)
      const visibleText = text.substring(0, openTagIndex).trim();
      const documentContent = text.substring(openTagIndex + 10).trim();
      return { 
        visibleText, 
        documentContent,
        docFilename: `data_${Date.now()}.docx` 
      };
    }
    
    // Có cả thẻ mở và thẻ đóng
    const beforeTag = text.substring(0, openTagIndex).trim();
    const afterTag = text.substring(closeTagIndex + 10).trim();
    const documentContent = text.substring(openTagIndex + 10, closeTagIndex).trim();
    
    // Kết hợp nội dung trước và sau thẻ để hiển thị trong chat
    const visibleText = beforeTag + (afterTag ? '\n\n' + afterTag : '');
    
    return { 
      visibleText, 
      documentContent,
      docFilename: `data_${Date.now()}.docx` 
    };
  },

  /**
   * Create and download a Word document
   * @param {string} content - Document content
   * @param {string} filename - Filename for download
   */
  createAndDownloadDocument(content, filename) {
    // Tạo tài liệu Word với định dạng phù hợp
    const doc = new Document({
      sections: [{
        properties: {
          page: {
            margin: {
              top: 1440, // 1 inch = 1440 twips
              right: 1080, // 3/4 inch
              bottom: 1440,
              left: 1080
            }
          }
        },
        children: [
          new Paragraph({
            heading: HeadingLevel.HEADING_1,
            alignment: AlignmentType.CENTER,
            children: [
              new TextRun({
                text: "ĐẠI HỌC ĐÀ NẴNG",
                bold: true,
                font: "Times New Roman",
                size: 28 // 14pt
              })
            ]
          }),
          new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [
              new TextRun({
                text: "TRƯỜNG ĐẠI HỌC BÁCH KHOA",
                bold: true,
                font: "Times New Roman",
                size: 28, // 14pt
                allCaps: true
              })
            ],
            spacing: {
              after: 400, // Khoảng cách sau đoạn
            }
          }),
          // Đường kẻ ngăn cách
          new Paragraph({
            border: {
              bottom: {
                color: "#000000",
                space: 1,
                style: BorderStyle.SINGLE,
                size: 6,
              },
            },
            spacing: {
              after: 400, // Khoảng cách sau đoạn
            }
          }),
          // Nội dung chính
          ...content.split('\n').map(line => 
            new Paragraph({
              children: [
                new TextRun({
                  text: line || " ", // Đảm bảo dòng trống vẫn được hiển thị
                  font: "Times New Roman",
                  size: 24, // 12pt
                })
              ],
              spacing: {
                before: 120, // Khoảng cách trước đoạn (6pt)
                after: 120,  // Khoảng cách sau đoạn (6pt)
                line: 360, // 1.5 dòng
                lineRule: "auto"
              }
            })
          )
        ]
      }]
    });
    
    // Tạo và tải xuống file
    Packer.toBlob(doc).then(blob => {
      saveAs(blob, filename);
    });
  }
};