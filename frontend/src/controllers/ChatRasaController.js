import ChatRasaServices from '@/models/ChatRasaServices';
import store from '@/store';

export default {
  /**
   * Send a message to the Rasa chatbot and process the response
   * @param {string} message - User message text
   * @returns {Promise} - Promise with the processed messages
   */
  async sendMessage(message) {
    try {
      // Get user ID from store
      const userId = store.state.user?.email || 'anonymous';
      
      // Get current chat history
      const chatHistory = ChatRasaServices.getChatHistory(userId);
      
      // Add user message to history
      const userMessage = {
        id: Date.now(),
        text: message,
        sender: 'user',
        timestamp: new Date().toISOString(),
        visibleText: message
      };
      chatHistory.push(userMessage);
      
      // Send message to Rasa
      const response = await ChatRasaServices.sendMessage(message, userId);
      
      // Process bot responses - consolidate multiple messages into one if needed
      if (response && response.length > 0) {
        if (response.length === 1) {
          // Single message response - handle normally
          const processedContent = ChatRasaServices.processMessageContent(response[0].text || '');
          
          const botMessage = {
            id: Date.now() + Math.random(),
            text: response[0].text || '',
            sender: 'bot',
            timestamp: new Date().toISOString(),
            buttons: response[0].buttons || [],
            image: response[0].image || null,
            custom: response[0].custom || null,
            visibleText: processedContent.visibleText,
            documentContent: processedContent.documentContent,
            docFilename: processedContent.docFilename
          };
          chatHistory.push(botMessage);
        } else {
          // Multiple messages in one response - consolidate them
          let consolidatedText = '';
          let buttons = [];
          let image = null;
          let custom = null;
          
          // First pass: Analyze messages to detect document pattern
          let hasDocument = false;
          let documentBegins = -1;
          let documentEnds = -1;
          let visibleTextBeforeDoc = [];
          let documentContent = [];
          let visibleTextAfterDoc = [];
          let currentState = 'before'; // 'before', 'document', 'after'
          
          for (let i = 0; i < response.length; i++) {
            const msg = response[i];
            if (!msg.text) continue;
            
            // Check for document tag marker
            if (msg.text === '<document>') {
              hasDocument = true;
              if (currentState === 'before') {
                currentState = 'document';
                documentBegins = i;
              } else if (currentState === 'document') {
                currentState = 'after';
                documentEnds = i;
              }
              continue;
            }
            
            // Add content to appropriate section based on current state
            if (currentState === 'before') {
              visibleTextBeforeDoc.push(msg.text);
            } else if (currentState === 'document') {
              documentContent.push(msg.text);
            } else {
              visibleTextAfterDoc.push(msg.text);
            }
            
            // Collect any UI elements
            if (msg.buttons && msg.buttons.length) {
              buttons = [...buttons, ...msg.buttons];
            }
            
            if (!image && msg.image) {
              image = msg.image;
            }
            
            if (msg.custom) {
              custom = {...custom, ...msg.custom};
            }
          }
          
          if (hasDocument) {
            // Consolidate document content and visible text
            const combinedVisibleText = [...visibleTextBeforeDoc, ...visibleTextAfterDoc].join('\n\n');
            const combinedDocContent = documentContent.join('\n\n');
            
            // Create message with document content
            const botMessage = {
              id: Date.now() + Math.random(),
              text: `${combinedVisibleText}\n<document>${combinedDocContent}`,
              sender: 'bot',
              timestamp: new Date().toISOString(),
              buttons: buttons.length > 0 ? buttons : null,
              image: image,
              custom: custom,
              visibleText: combinedVisibleText,
              documentContent: combinedDocContent,
              docFilename: `data_${Date.now()}.docx`
            };
            chatHistory.push(botMessage);
          } else {
            // No document pattern detected, combine messages as before
            response.forEach((msg) => {
              if (msg.text) {
                if (consolidatedText !== '') {
                  consolidatedText += '\n\n';
                }
                consolidatedText += msg.text;
              }
              
              if (msg.buttons && msg.buttons.length) {
                buttons = [...buttons, ...msg.buttons];
              }
              
              if (!image && msg.image) {
                image = msg.image;
              }
              
              if (msg.custom) {
                custom = {...custom, ...msg.custom};
              }
            });
            
            const botMessage = {
              id: Date.now() + Math.random(),
              text: consolidatedText,
              sender: 'bot',
              timestamp: new Date().toISOString(),
              buttons: buttons.length > 0 ? buttons : null,
              image: image,
              custom: custom,
              visibleText: consolidatedText
            };
            chatHistory.push(botMessage);
          }
        }
      } else {
        // Fallback if no response
        chatHistory.push({
          id: Date.now() + Math.random(),
          text: "Sorry, I'm having trouble connecting. Please try again later.",
          sender: 'bot',
          timestamp: new Date().toISOString(),
          visibleText: "Sorry, I'm having trouble connecting. Please try again later."
        });
      }
      
      // Save updated history
      ChatRasaServices.saveChatHistory(userId, chatHistory);
      
      // Return the updated message list
      return chatHistory;
    } catch (error) {
      console.error('Error in sendMessage:', error);
      // Return error as a bot message
      const chatHistory = ChatRasaServices.getChatHistory(store.state.user?.email || 'anonymous');
      chatHistory.push({
        id: Date.now(),
        text: "I'm sorry, something went wrong. Please try again later.",
        sender: 'bot',
        timestamp: new Date().toISOString(),
        isError: true,
        visibleText: "I'm sorry, something went wrong. Please try again later."
      });
      ChatRasaServices.saveChatHistory(store.state.user?.email || 'anonymous', chatHistory);
      return chatHistory;
    }
  },

  /**
   * Get major suggestions based on test scores and subjects
   * @param {Array} subjects - Array of subject names
   * @param {Number} score - Total score after priority points
   * @returns {Promise<Array>} - Promise with structured suggestion data
   */
  async getMajorSuggestions(subjects, score, method_key = true) {
    try {
      // Generate a unique user ID for this suggestion request to avoid chat history contamination
      const suggestionId = `suggestion_${Date.now()}`;
      // Construct query message for the chatbot
      const subjectsList = Array.isArray(subjects) ? subjects.join(', ') : subjects;
      const query = method_key ? 
      `em thi khối thi có các môn ${subjectsList} đạt được ${score} ở phương thức điểm thi tốt nghiệp thì có thể nộp đơn vào ngành nào` : 
      `em xét học bạ các môn ${subjectsList} với điểm xét tuyển là ${score} thì có thể nộp đơn vào ngành nào`;
      
      console.log('Sending suggestion query:', query);
      
      // Send direct request to Rasa without affecting chat history
      const response = await ChatRasaServices.sendMessage(query, suggestionId);
      
      if (!response || !response.length) {
        console.error('No response received from chatbot for suggestions');
        return [];
      }
      
      // Process the suggestion responses
      return this.processSuggestionResponses(response);
      
    } catch (error) {
      console.error('Error getting major suggestions:', error);
      throw new Error('Không thể lấy gợi ý ngành học. Vui lòng thử lại sau.');
    }
  },
  
  /**
   * Process chatbot responses into structured suggestion data
   * @param {Array} responses - Array of response messages from the chatbot
   * @returns {Array} - Structured suggestion data
   */
  processSuggestionResponses(responses) {
    console.log('Processing suggestion responses:', responses);
    
    const result = [];
    let currentCategory = null;
    
    // Process each response message
    for (const response of responses) {
      const text = response.text;
      
      if (!text) continue;
      
      // Check if this is a header
      if (text.includes('**Các ngành phù hợp với điểm')) {
        // Create first category for introduction
        currentCategory = {
          title: text,
          majors: []
        };
        result.push(currentCategory);
      }
      
      // Check if this is a category header (high/medium chance)
      else if (text.includes('**Tỷ lệ đỗ cao**') || text.includes('**Tỷ lệ đỗ trung bình**')) {
        // Start a new category
        currentCategory = {
          title: text,
          majors: []
        };
        result.push(currentCategory);
      }
      
      // Check if this is a list of majors
      else if (text.match(/\d+\.\s.*/) && currentCategory) {
        // Process list of majors
        const majorLines = text.split('\n');
        
        for (const line of majorLines) {
          // Extract major name and link using regex
          const match = line.match(/(\d+)\.\s(.*?)\.\sXem chi tiết ngành\s(\/major\/\d+)/);
          
          if (match) {
            const [_, num, name, link] = match;
            currentCategory.majors.push({
              name: name.trim(),
              link: link.trim()
            });
          }
        }
      }
      
      // Check if this is an explanatory note
      else if (text.includes('*Kết quả dựa trên điểm chuẩn')) {
        result.push({ 
          note: text,
          isNote: true 
        });
      }
    }
    
    console.log('Processed suggestions:', result);
    return result;
  },

  /**
   * Get the current chat history
   * @returns {Array} - Array of message objects
   */
  getChatHistory() {
    const userId = store.state.user?.email || 'anonymous';
    const chatHistory = ChatRasaServices.getChatHistory(userId);
    
    // Process any existing messages to ensure they have visibleText property
    return chatHistory.map(message => {
      if (message.sender === 'bot' && message.text && !message.visibleText) {
        const processedContent = ChatRasaServices.processMessageContent(message.text);
        return {
          ...message,
          visibleText: processedContent.visibleText,
          documentContent: processedContent.documentContent,
          docFilename: processedContent.docFilename
        };
      }
      return message.visibleText ? message : { ...message, visibleText: message.text };
    });
  },

  /**
   * Reset the chat history
   */
  resetChat() {
    const userId = store.state.user?.email || 'anonymous';
    ChatRasaServices.saveChatHistory(userId, []);
    return [];
  },
  
  /**
   * Initialize the chat with a welcome message if history is empty
   * @returns {Array} - Updated chat history
   */
  initializeChat() {
    const userId = store.state.user?.email || 'anonymous';
    let chatHistory = ChatRasaServices.getChatHistory(userId);
    
    if (chatHistory.length === 0) {
      // Add welcome message
      chatHistory = [{
        id: Date.now(),
        text: "Xin chào! Tôi là trợ lý ảo của Trường Đại học Bách Khoa - Đại Học Đà Nẵng. Tôi có thể giúp gì cho bạn về thông tin tuyển sinh?",
        sender: 'bot',
        timestamp: new Date().toISOString(),
        visibleText: "Xin chào! Tôi là trợ lý ảo của Trường Đại học Bách Khoa - Đại Học Đà Nẵng. Tôi có thể giúp gì cho bạn về thông tin tuyển sinh?"
      }];
      ChatRasaServices.saveChatHistory(userId, chatHistory);
    }
    
    return this.getChatHistory();
  }
};