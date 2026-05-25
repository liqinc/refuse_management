// news.js
const app = getApp();

Page({
  data: {
    newsList: [],
    allNewsList: [], // 存储所有新闻，用于搜索过滤
    categories: [
      { name: '全部', id: 'all', selected: true },
      { name: '政策法规', id: '政策法规', selected: false },
      { name: '科普知识', id: '科普知识', selected: false },
      { name: '行业动态', id: '行业动态', selected: false }
    ],
    page: 1,
    hasMore: true,
    loading: false,
    searchKeyword: ''
  },
  onLoad: function() {
    wx.setNavigationBarTitle({ title: '垃圾资讯' });
    this.getNewsList();
  },
  getNewsList: function() {
    if (this.data.loading || !this.data.hasMore) return;
    
    this.setData({ loading: true });
    
    // 获取当前选中的分类
    const selectedCategory = this.data.categories.find(cat => cat.selected).id;
    
    // 构建API请求URL
    const url = `${app.globalData.baseUrl}/refuse-news/api/list?category=${selectedCategory}&page=${this.data.page}&per_page=10`;
    
    // 发送API请求
    wx.request({
      url: url,
      method: 'GET',
      success: (res) => {
        if (res.statusCode === 200) {
          const data = res.data;
          
          // 映射API返回的数据格式到前端需要的格式
          const formattedNews = data.news_list.map(news => ({
            id: news.id.toString(),
            title: news.title,
            subtitle: news.subtitle,
            date: news.date,
            views: news.views,
            likes: news.likes,
            category: news.category,
            image: news.image
          }));
          
          this.setData({
            allNewsList: this.data.page === 1 ? formattedNews : [...this.data.allNewsList, ...formattedNews],
            newsList: this.data.searchKeyword ? 
              (this.data.page === 1 ? formattedNews : [...this.data.newsList, ...formattedNews])
                .filter(news => 
                  news.title.includes(this.data.searchKeyword) || 
                  news.subtitle.includes(this.data.searchKeyword)
                )
              : (this.data.page === 1 ? formattedNews : [...this.data.newsList, ...formattedNews]),
            page: this.data.page + 1,
            hasMore: data.has_more,
            loading: false
          });
        } else {
          wx.showToast({
            title: '获取资讯失败',
            icon: 'none',
            duration: 2000
          });
          this.setData({ loading: false });
        }
      },
      fail: () => {
        wx.showToast({
          title: '网络请求失败',
          icon: 'none',
          duration: 2000
        });
        this.setData({ loading: false });
      }
    });
  },
  changeCategory: function(e) {
    const categoryId = e.currentTarget.dataset.id;
    const newCategories = this.data.categories.map(cat => ({
      ...cat,
      selected: cat.id === categoryId
    }));
    
    this.setData({
      categories: newCategories,
      page: 1,
      newsList: [],
      hasMore: true
    });
    
    // 首先滚动到顶部
    wx.pageScrollTo({
      scrollTop: 0,
      duration: 0,
      success: () => {
        // 页面滚动完成后再加载数据
        setTimeout(() => {
          this.getNewsList();
        }, 50);
      }
    });
  },
  goToDetail: function(e) {
    const newsId = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: '/pages/news/detail?id=' + newsId
    });
  },
  onReachBottom: function() {
    this.getNewsList();
  },
  onPullDownRefresh: function() {
    this.setData({
      page: 1,
      newsList: [],
      allNewsList: [],
      hasMore: true
    });
    this.getNewsList();
    wx.stopPullDownRefresh();
  },
  
  // 搜索输入事件处理
  onSearchInput: function(e) {
    const keyword = e.detail.value.trim();
    this.setData({ searchKeyword: keyword });
    
    // 过滤新闻列表
    if (keyword) {
      const filteredNews = this.data.allNewsList.filter(news => 
        news.title.includes(keyword) || news.subtitle.includes(keyword)
      );
      this.setData({ newsList: filteredNews });
    } else {
      // 如果搜索关键词为空，显示所有新闻
      this.setData({ newsList: this.data.allNewsList });
    }
  },
  
  // 搜索确认事件处理
  onSearchConfirm: function() {
    // 这里可以添加搜索确认时的额外逻辑，比如显示加载提示等
    if (this.data.searchKeyword) {
      const filteredNews = this.data.allNewsList.filter(news => 
        news.title.includes(this.data.searchKeyword) || news.subtitle.includes(this.data.searchKeyword)
      );
      this.setData({ newsList: filteredNews });
      
      // 如果没有搜索结果，显示提示
      if (filteredNews.length === 0) {
        wx.showToast({
          title: '未找到相关资讯',
          icon: 'none',
          duration: 2000
        });
      }
    }
  }
});