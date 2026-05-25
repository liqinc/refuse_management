// chat.js
Page({
  data: {
    messages: [
      { id: Date.now(), type: 'system', content: '请问有什么可以帮助你的' }
    ],
    inputValue: '',
    scrollTop: 0,
    deepSeekConfig: null,
    isConfigLoaded: false,
    userInfo: null,
    defaultAiAvatar: '/images/ai-avatar.png',
    defaultUserAvatar: '/images/default-avatar.png' // 使用文档中的默认头像路径
  },

  onLoad() {
    this.getDeepSeekConfig();
    this.checkLoginStatus();
  },
  getDeepSeekConfig() {
    wx.request({
      url: 'http://127.0.0.1:9003/getDeepSeekConfig',
      method: 'GET',
      success: (res) => {
        if (res.statusCode === 200) {
          this.setData({
            deepSeekConfig: res.data,
            isConfigLoaded: true
          });
        } else {
          console.error('获取配置失败:', res);
          wx.showToast({ title: '配置加载失败', icon: 'none' });
        }
      },
      fail: (err) => {
        console.error('获取配置出错:', err);
        wx.showToast({ title: '网络错误，请重试', icon: 'none' });
      }
    });
  },

  onInputChange(e) {
    this.setData({ inputValue: e.detail.value });
  },

  sendMessage() {
    const input = this.data.inputValue.trim();
    if (!input) {
      wx.showToast({ title: '请输入内容', icon: 'none' });
      return;
    }

    this.addMessage('user', input);
    this.setData({ inputValue: '' });

    if (this.data.isConfigLoaded) {
      this.callDeepSeekAPI(input);
    } else {
      wx.showToast({ title: '配置加载中', icon: 'none' });
      this.getDeepSeekConfig();
    }
  },

  addMessage(type, content) {
    const newMessages = [
      ...this.data.messages,
      { id: Date.now(), type, content }
    ];
    this.setData({ messages: newMessages }, () => {
      this.setData({ scrollTop: 99999 });
    });
  },

  callDeepSeekAPI(input) {
    wx.showLoading({ title: '思考中...', mask: true });
    
    wx.request({
      url: this.data.deepSeekConfig.apiUrl,
      method: 'POST',
      data: { input, history: this.getHistory() },
      success: (res) => {
        wx.hideLoading();
        if (res.statusCode === 200) {
          this.addMessage('ai', res.data.response);
        } else {
          console.error('请求失败:', res);
          this.showError(res.data.error || '服务异常');
        }
      },
      fail: (err) => {
        wx.hideLoading();
        console.error('请求出错:', err);
        this.showError('网络连接失败');
      }
    });
  },

  getHistory() {
    return this.data.messages
     .filter(m => ['user', 'ai'].includes(m.type))
     .map(m => ({
        role: m.type === 'user' ? 'user' : 'assistant',
        content: m.content
      }));
  },

  showError(msg) {
    wx.showToast({ title: msg, icon: 'none', duration: 2000 });
    this.addMessage('ai', '抱歉，当前无法提供回答，请稍后再试');
  }
});