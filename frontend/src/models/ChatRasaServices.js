import axios from 'axios';
import config from '@/config/apiConfig';

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
  }
};