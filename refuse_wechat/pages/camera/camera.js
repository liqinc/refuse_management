// camera.js
Page({
  data: {
    src: '',
    isTakingPhoto: false,
    result: '',
    motto:'识别结果：',
    isIdentifying: false
  },
  onLoad: function() {
    wx.setNavigationBarTitle({ title: '垃圾分类识别' });
  },
  
  // 拍照功能
  takePhoto: function() {
    // 在普通页面中调用系统相机
    this.setData({ isTakingPhoto: true });
    
    // 检查相机权限
    wx.getSetting({
      success: (res) => {
        if (!res.authSetting['scope.camera']) {
          // 请求相机权限
          wx.authorize({
            scope: 'scope.camera',
            success: () => {
              this.startTakingPhoto();
            },
            fail: () => {
              this.setData({ isTakingPhoto: false });
              wx.showToast({
                title: '需要相机权限才能拍照',
                icon: 'none'
              });
            }
          });
        } else {
          // 已授权，直接调用相机
          this.startTakingPhoto();
        }
      },
      fail: () => {
        this.setData({ isTakingPhoto: false });
        wx.showToast({
          title: '获取权限失败',
          icon: 'none'
        });
      }
    });
  },
  
  // 开始拍照
  startTakingPhoto: function() {
    wx.chooseMedia({
      count: 1,
      mediaType: ['image'],
      sourceType: ['camera'],
      camera: 'back',
      success: (res) => {
        this.setData({
          src: res.tempFiles[0].tempFilePath,
          isTakingPhoto: false,
          result: ''
        });
      },
      fail: (err) => {
        console.error('拍照失败', err);
        this.setData({ isTakingPhoto: false });
        wx.showToast({
          title: '拍照失败，请重试',
          icon: 'none'
        });
      }
    });
  },
  
  // 选择图片功能
  chooseImage: function() {
    wx.chooseMedia({
      count: 1,
      mediaType: ['image'],
      sourceType: ['album'],
      success: (res) => {
        this.setData({
          src: res.tempFiles[0].tempFilePath,
          result: ''
        });
      }
    });
  },
  
  // 重新开始功能
  retakePhoto: function() {
    this.setData({
      src: '',
      result: '',
      isIdentifying: false
    });
  },
  
  // 返回上一页
  onBackTap: function() {
    wx.navigateBack();
  },
  
  // 垃圾图片识别方法
  reidentifyGarbage: function() {
    if (!this.data.src) {
      wx.showToast({
        title: '请先拍摄或选择图片',
        icon: 'none'
      });
      return;
    }
    
    this.setData({ isIdentifying: true });
    
    // 调用垃圾图像识别接口
    wx.uploadFile({
      url: 'http://127.0.0.1:5000/wxuploader',
      filePath: this.data.src,
      name: 'content',
      header: {
        'content-type': 'multipart/form-data'
      },
      success: (res) => {
        console.log('识别成功', res);
        try {
          // 保存原始数据用于展示
          const rawData = JSON.parse(res.data)['value'];
          
          this.setData({
            // 直接存储原始的AI接口返回数据
            result: rawData
          });
        } catch (e) {
          console.error('解析识别结果失败', e);
          this.handleRecognitionError();
        }
      },
      fail: (err) => {
        console.error('识别请求失败', err);
        this.handleRecognitionError();
      },
      complete: () => {
        // 重置isIdentifying状态
        this.setData({ isIdentifying: false });
      }
    });
  },
  
  // 处理识别错误的方法
  handleRecognitionError: function() {
    // 识别失败时不使用模拟数据
    wx.showToast({
      title: '识别失败，请重试',
      icon: 'none'
    });
    
    this.setData({
      isIdentifying: false,
      result: ''
    });
  }
});