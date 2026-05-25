// index.js
const app = getApp();

Page({
  data: {
    swiperImages: [
      '/images/default.png',
      '/images/banner.png',
      '/images/default.png'
    ],
    navItems: [
      { icon: '/images/garbage_classification.png', text: '垃圾分类' },
      { icon: '/images/photo_recognition.png', text: '拍照识别' },
      { icon: '/images/garbage_news.png', text: '垃圾资讯' },
      { icon: '/images/garbage_collection.png', text: '站点回收' }
    ],
    newsList: [],
    floatButtonLeft: 30,
    floatButtonBottom: 30,
  },
  
  onLoad: function() {
    // 获取最新两条垃圾资讯用于首页推荐
    this.getRecommendedNews();
  },
  
  // 获取推荐资讯
  getRecommendedNews: function() {
    const url = `${app.globalData.baseUrl}/refuse-news/api/list?category=all&page=1&per_page=2`;
    
    wx.request({
      url: url,
      method: 'GET',
      success: (res) => {
        if (res.statusCode === 200) {
          const data = res.data;
          
          // 映射API返回的数据格式
          const formattedNews = data.news_list.slice(0, 2).map(news => ({
            id: news.id.toString(), // 添加id字段，用于跳转到详情页
            image: news.image,
            title: news.title,
            subtitle: news.subtitle,
            date: news.date,
            views: news.views,
            likes: news.likes
          }));
          
          this.setData({
            newsList: formattedNews
          });
        }
      }
    });
  },
  
  // 导航到对应页面
  navigateToPage: function(e) {
    const index = e.currentTarget.dataset.index;
    switch(index) {
      case 0:
        wx.navigateTo({ url: '/pages/classify/classify' });
        break;
      case 1:
        wx.navigateTo({ url: '/pages/camera/camera' });
        break;
      case 2:
        wx.navigateTo({ url: '/pages/news/news' });
        break;
      case 3:
        wx.navigateTo({ url: '/pages/recycle/recycle' });
        break;
    }
  },
  
  // 点击新闻项跳转到详情页
  goToNewsDetail: function(e) {
    const newsId = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: '/pages/news/detail?id=' + newsId
    });
  },
// 点击悬浮窗按钮触发
openAI() {
  console.log('点击悬浮窗，准备跳转聊天界面');
  wx.navigateTo({
    url: '/pages/chat/chat',
    success: function () {
      console.log('跳转成功');
    },
    fail: function (err) {
      console.error('跳转失败:', err);
    }
  });
},

// 悬浮窗触摸开始事件
onFloatButtonTouchStart: function (e) {
  const touch = e.touches[0];
  this.setData({
    startX: touch.clientX,
    startY: touch.clientY,
    initialLeft: this.data.floatButtonLeft,
    initialBottom: this.data.floatButtonBottom
  });
},

// 悬浮窗触摸移动事件
onFloatButtonTouchMove: function (e) {
  const { startX, startY, initialLeft, initialBottom } = this.data;
  const touch = e.touches[0];

  // 计算移动距离
  const deltaX = touch.clientX - startX;
  const deltaY = touch.clientY - startY;

  // 转换为rpx单位
  const systemInfo = wx.getSystemInfoSync();
  const rpxRatio = 750 / systemInfo.windowWidth;
  const deltaXRpx = deltaX * rpxRatio;
  const deltaYRpx = deltaY * rpxRatio;

  // 计算新位置
  let newLeft = initialLeft + deltaXRpx;
  let newBottom = initialBottom - deltaYRpx;

  // 边界限制
  const buttonSize = 80;
  const maxLeft = 750 - buttonSize;
  const maxBottom = systemInfo.windowHeight * rpxRatio - buttonSize;
  newLeft = Math.max(0, Math.min(newLeft, maxLeft));
  newBottom = Math.max(0, Math.min(newBottom, maxBottom));

  this.setData({
    floatButtonLeft: newLeft,
    floatButtonBottom: newBottom
  });
},

// 悬浮窗触摸结束事件
onFloatButtonTouchEnd: function () {
  wx.setStorageSync('floatButtonPosition', {
    left: this.data.floatButtonLeft,
    bottom: this.data.floatButtonBottom
  });
},
  
});
