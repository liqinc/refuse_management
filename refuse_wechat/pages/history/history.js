// history.js
Page({
  data: {
    historyList: [],
    statusBarHeight: wx.getSystemInfoSync().statusBarHeight
  },

  onLoad: function() {
    this.loadHistoryData();
  },

  // 加载历史数据
  loadHistoryData: function() {
    const historyList = wx.getStorageSync('historyList') || [];
    this.setData({
      historyList: historyList
    });
  },

  // 删除单条记录
  deleteRecord: function(e) {
    const id = e.currentTarget.dataset.id;
    
    wx.showModal({
      title: '确认删除',
      content: '确定要删除这条记录吗？',
      success: res => {
        if (res.confirm) {
          let historyList = this.data.historyList;
          historyList = historyList.filter(item => item.id !== id);
          
          this.setData({
            historyList: historyList
          });
          
          // 更新本地存储
          wx.setStorageSync('historyList', historyList);
          
          wx.showToast({
            title: '删除成功',
            icon: 'success',
            duration: 1500
          });
        }
      }
    });
  },

  // 清空历史记录
  clearHistory: function() {
    wx.showModal({
      title: '确认清空',
      content: '确定要清空所有历史记录吗？',
      success: res => {
        if (res.confirm) {
          this.setData({
            historyList: []
          });
          
          // 更新本地存储
          wx.setStorageSync('historyList', []);
          
          wx.showToast({
            title: '已清空历史记录',
            icon: 'success',
            duration: 1500
          });
        }
      }
    });
  },

  // 返回上一页
  goBack: function() {
    wx.navigateBack({
      delta: 1
    });
  },

  // 返回首页
  goHome: function() {
    wx.switchTab({
      url: '/pages/index/index'
    });
  }
})