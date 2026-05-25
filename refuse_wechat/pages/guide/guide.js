// guide.js
Page({
  data: {
    currentTab: 0,
    searchText: '',
    searchResult: '',
    statusBarHeight: wx.getSystemInfoSync().statusBarHeight,
    // 垃圾分类数据库（简化版）
    wasteDatabase: [
      { name: '纸箱', category: '可回收物' },
      { name: '报纸', category: '可回收物' },
      { name: '纸巾', category: '其他垃圾' },
      { name: '塑料瓶', category: '可回收物' },
      { name: '易拉罐', category: '可回收物' },
      { name: '玻璃瓶', category: '可回收物' },
      { name: '旧衣服', category: '可回收物' },
      { name: '剩饭剩菜', category: '厨余垃圾' },
      { name: '果皮', category: '厨余垃圾' },
      { name: '骨头', category: '厨余垃圾' },
      { name: '茶叶渣', category: '厨余垃圾' },
      { name: '咖啡渣', category: '厨余垃圾' },
      { name: '电池', category: '有害垃圾' },
      { name: '灯管', category: '有害垃圾' },
      { name: '过期药品', category: '有害垃圾' },
      { name: '油漆桶', category: '有害垃圾' },
      { name: '杀虫剂', category: '有害垃圾' },
      { name: '卫生巾', category: '其他垃圾' },
      { name: '烟蒂', category: '其他垃圾' },
      { name: '牙刷', category: '其他垃圾' },
      { name: '一次性餐具', category: '其他垃圾' },
      { name: '猫砂', category: '其他垃圾' },
      { name: '尿不湿', category: '其他垃圾' },
      { name: '口香糖', category: '其他垃圾' },
      { name: '陶瓷', category: '其他垃圾' },
      { name: '菜叶', category: '厨余垃圾' },
      { name: '水果皮', category: '厨余垃圾' },
      { name: '鱼骨', category: '厨余垃圾' },
      { name: '鸡骨', category: '厨余垃圾' },
      { name: '废纸', category: '可回收物' },
      { name: '塑料袋', category: '可回收物' },
      { name: '金属', category: '可回收物' },
      { name: '旧书', category: '可回收物' },
      { name: '纽扣电池', category: '有害垃圾' },
      { name: '荧光灯', category: '有害垃圾' },
      { name: '温度计', category: '有害垃圾' },
      { name: '过期化妆品', category: '有害垃圾' },
      { name: '染发剂', category: '有害垃圾' },
      { name: '废弃口罩', category: '其他垃圾' },
      { name: '创可贴', category: '其他垃圾' }
    ]
  },

  // 切换分类标签
  switchTab: function(e) {
    const tab = parseInt(e.currentTarget.dataset.tab);
    this.setData({
      currentTab: tab
    });
  },

  // 搜索输入
  onSearchInput: function(e) {
    this.setData({
      searchText: e.detail.value
    });
  },

  // 搜索物品
  searchItem: function() {
    const searchText = this.data.searchText.trim();
    if (!searchText) {
      wx.showToast({
        title: '请输入物品名称',
        icon: 'none',
        duration: 2000
      });
      return;
    }

    // 在数据库中查找匹配项
    const result = this.data.wasteDatabase.find(item => 
      item.name.includes(searchText)
    );

    if (result) {
      this.setData({
        searchResult: `"${result.name}" 属于 ${result.category}`
      });
    } else {
      this.setData({
        searchResult: `未找到 "${searchText}" 的分类信息，请尝试其他关键词`
      });
    }
  },

  // 返回上一页
  goBack: function() {
    wx.navigateBack({
      delta: 1
    });
  }
})