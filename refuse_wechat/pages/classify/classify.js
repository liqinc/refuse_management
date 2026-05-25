// classify.js
Page({
  data: {
    categories: [], // 将从API获取数据
    searchQuery: '',
    searchResults: [], // 搜索结果
    isSearching: false, // 搜索状态
    showSearchResults: false, // 是否显示搜索结果
    isLoading: true, // 加载状态
    errorMsg: '' // 错误信息
  },
  
  onLoad: function() {
    wx.setNavigationBarTitle({ title: '垃圾分类' });
    this.getRefuseTypes(); // 加载数据
  },
  
  // 从API获取垃圾分类数据
  getRefuseTypes: function() {
    const that = this;
    
    this.setData({
      isLoading: true,
      errorMsg: ''
    });
    
    // 调用后端API接口获取数据
    wx.request({
      url: 'http://localhost:5001/refuse-type/api/list', // 后端API地址
      method: 'GET',
      success: function(res) {
        if (res.data && res.data.success) {
          // 处理返回的数据，将type_name映射到name字段以保持与原代码的兼容性
          const formattedCategories = res.data.data.map(item => ({
            name: item.type_name,
            icon: item.icon_url || '/images/default.png',
            color: item.color || '#1296db',
            description: item.description || ''
          }));
          
          that.setData({
            categories: formattedCategories,
            isLoading: false
          });
        } else {
          that.setData({
            errorMsg: '获取数据失败: ' + (res.data.message || '未知错误'),
            isLoading: false
          });
          console.error('API调用失败:', res);
        }
      },
      fail: function(err) {
        that.setData({
          errorMsg: '网络请求失败，请检查网络连接',
          isLoading: false
        });
        console.error('网络请求失败:', err);
      }
    });
  },
  
  // 搜索输入框变化时触发
  search: function(e) {
    this.setData({
      searchQuery: e.detail.value
    });
  },
  
  // 执行搜索
  executeSearch: function() {
    const keyword = this.data.searchQuery.trim();
    
    if (!keyword) {
      wx.showToast({
        title: '请输入搜索关键词',
        icon: 'none'
      });
      return;
    }
    
    const that = this;
    
    this.setData({
      isSearching: true,
      showSearchResults: true,
      searchResults: []
    });
    
    // 调用后端搜索API接口
    wx.request({
      url: 'http://localhost:5001/refuse-type/api/search',
      method: 'GET',
      data: {
        keyword: keyword
      },
      success: function(res) {
        if (res.data && res.data.success) {
          that.setData({
            searchResults: res.data.data || [],
            isSearching: false
          });
          
          if (res.data.data && res.data.data.length === 0) {
            wx.showToast({
              title: '未找到相关垃圾信息',
              icon: 'none'
            });
          }
        } else {
          that.setData({
            isSearching: false,
            errorMsg: '搜索失败: ' + (res.data.message || '未知错误')
          });
          wx.showToast({
            title: res.data.message || '搜索失败',
            icon: 'none'
          });
          console.error('搜索API调用失败:', res);
        }
      },
      fail: function(err) {
        that.setData({
          isSearching: false,
          errorMsg: '网络请求失败，请检查网络连接'
        });
        wx.showToast({
          title: '网络请求失败',
          icon: 'none'
        });
        console.error('网络请求失败:', err);
      }
    });
  },
  
  // 点击分类导航项
  navigateToDetail: function(e) {
    const category = e.currentTarget.dataset.category;
    wx.navigateTo({
      url: '/pages/classify/detail?category=' + category
    });
  },
  
  // 点击搜索结果项
  navigateToSearchDetail: function(e) {
    const item = e.currentTarget.dataset.item;
    // 可以根据需要传递更多参数
    wx.navigateTo({
      url: `/pages/classify/detail?category=${item.type_name}&item_id=${item.id}&item_name=${item.category_name}`
    });
  },
  
  // 清除搜索结果
  clearSearchResults: function() {
    this.setData({
      showSearchResults: false,
      searchResults: [],
      searchQuery: ''
    });
  },
  
  // 点击热门搜索标签
  tapHotSearch: function(e) {
    const query = e.currentTarget.dataset.query;
    this.setData({
      searchQuery: query
    });
    this.executeSearch();
  }
});