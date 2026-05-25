// detail.js
const app = getApp();

Page({
  data: {
    newsId: '',
    newsDetail: null,
    loading: true
  },
  onLoad: function(options) {
    if (options.id) {
      this.setData({
        newsId: options.id
      });
      this.getNewsDetail();
    }
  },
  getNewsDetail: function() {
    // 从后端API获取资讯详情
    this.setData({ loading: true });
    
    // 构建正确的API请求URL
    const url = `${app.globalData.baseUrl}/refuse-news/api/detail/${this.data.newsId}`;
    
    // 调用后端API获取新闻详情
    wx.request({
      url: url,
      method: 'GET',
      success: (res) => {
        if (res.statusCode === 200) {
          const newsDetail = res.data;
          
          wx.setNavigationBarTitle({ title: newsDetail.title });
          
          // 处理资讯内容，将字符串按换行符分割成数组以便正确渲染
          if (newsDetail.content && typeof newsDetail.content === 'string') {
            // 去除前后空白字符
            const trimmedContent = newsDetail.content.trim();
            // 按换行符分割内容，过滤掉空行
            newsDetail.content = trimmedContent.split('\n').filter(line => line.trim().length > 0);
          } else {
            // 如果不是字符串或者为空，设置为空数组
            newsDetail.content = [];
          }
          
          this.setData({
            newsDetail: newsDetail,
            loading: false
          });
        } else {
          console.error('获取新闻详情失败', res);
          this.setData({ loading: false });
          wx.showToast({
            title: '获取资讯详情失败',
            icon: 'none'
          });
        }
      },
      fail: (err) => {
        console.error('请求失败', err);
        this.setData({ loading: false });
        wx.showToast({
          title: '网络异常，请检查网络连接',
          icon: 'none'
        });
      }
    });
  },
  likeNews: function() {
    if (this.data.newsDetail) {
      // 构建点赞API请求URL
      const url = `${app.globalData.baseUrl}/refuse-news/api/like/${this.data.newsId}`;
      
      wx.request({
        url: url,
        method: 'POST',
        success: (res) => {
          if (res.statusCode === 200 && res.data.success) {
            this.setData({
              'newsDetail.likes': res.data.likes
            });
            wx.showToast({
              title: '点赞成功',
              icon: 'success',
              duration: 1500
            });
          } else {
            wx.showToast({
              title: '点赞失败，请稍后重试',
              icon: 'none'
            });
          }
        },
        fail: () => {
          wx.showToast({
            title: '网络异常，请检查网络连接',
            icon: 'none'
          });
        }
      });
    }
  },
  shareNews: function() {
    wx.showShareMenu({
      withShareTicket: true,
      menus: ['shareAppMessage', 'shareTimeline']
    });
  },
  onShareAppMessage: function() {
    return {
      title: this.data.newsDetail ? this.data.newsDetail.title : '垃圾分类资讯',
      path: '/pages/news/detail?id=' + this.data.newsId,
      imageUrl: this.data.newsDetail ? this.data.newsDetail.coverImage : ''
    };
  }
});