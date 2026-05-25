// recycle.js
Page({
  data: {
    currentLocation: '定位中...',
    recycleStations: [],
    markers: [],
    currentLatitude: 0,
    currentLongitude: 0,
    selectedStation: null,
    showStationDetail: false
  },
  onLoad: function() {
    wx.setNavigationBarTitle({ title: '站点回收' });
    this.getUserLocation();
  },
  getUserLocation: function() {
    // 获取用户位置
    wx.getLocation({
      type: 'gcj02',
      success: (res) => {
        const latitude = res.latitude;
        const longitude = res.longitude;
        
        // 逆地理编码获取位置信息
        wx.request({
          url: 'https://apis.map.qq.com/ws/geocoder/v1/',
          data: {
            location: `${latitude},${longitude}`,
            key: 'YOUR_TENCENT_MAP_KEY' // 实际应用中需要使用自己的腾讯地图API密钥
          },
          success: (res) => {
            if (res.data.status === 0) {
              const address = res.data.result.address;
              this.setData({
                currentLocation: address,
                currentLatitude: latitude,
                currentLongitude: longitude
              });
              this.getNearbyStations();
            }
          },
          fail: () => {
            this.setData({
              currentLocation: '获取位置失败'
            });
          }
        });
      },
      fail: () => {
        wx.showToast({
          title: '需要位置权限才能使用此功能',
          icon: 'none'
        });
        this.setData({
          currentLocation: '未获取位置权限'
        });
      }
    });
  },
  getNearbyStations: function() {
    // 模拟附近的垃圾回收站点数据
    // 实际应用中应该调用地图API获取附近的回收站点
    const stations = [
      {
        id: '1',
        name: '绿色回收站(中心广场)',
        address: '市中心广场西北角',
        distance: '350米',
        openingHours: '08:00-20:00',
        phone: '13800138001',
        latitude: this.data.currentLatitude + 0.001,
        longitude: this.data.currentLongitude + 0.001,
        services: ['可回收物', '有害垃圾', '其他垃圾'],
        rating: 4.5,
        image: '/images/default.png'
      },
      {
        id: '2',
        name: '智能垃圾分类箱(东湖小区)',
        address: '东湖小区南门入口处',
        distance: '800米',
        openingHours: '24小时',
        phone: '13900139002',
        latitude: this.data.currentLatitude - 0.002,
        longitude: this.data.currentLongitude + 0.003,
        services: ['可回收物', '有害垃圾', '厨余垃圾', '其他垃圾'],
        rating: 4.8,
        image: '/images/default.png'
      },
      {
        id: '3',
        name: '环保回收点(科技园)',
        address: '科技园A区停车场旁',
        distance: '1.2公里',
        openingHours: '09:00-18:00',
        phone: '13700137003',
        latitude: this.data.currentLatitude + 0.003,
        longitude: this.data.currentLongitude - 0.002,
        services: ['可回收物', '其他垃圾'],
        rating: 4.2,
        image: '/images/default.png'
      }
    ];
    
    // 转换为地图标记
    const markers = stations.map((station, index) => ({
      id: station.id,
      latitude: station.latitude,
      longitude: station.longitude,
      iconPath: '/images/marker.png',
      width: 50,
      height: 50,
      callout: {
        content: station.name + '\n' + station.distance,
        color: '#333',
        fontSize: 14,
        borderRadius: 5,
        bgColor: 'rgba(255, 255, 255, 0.9)',
        padding: 10,
        display: 'BYCLICK'
      }
    }));
    
    this.setData({
      recycleStations: stations,
      markers: markers
    });
  },
  showStationDetail: function(e) {
    const stationId = e.currentTarget.dataset.id;
    const station = this.data.recycleStations.find(s => s.id === stationId);
    
    this.setData({
      selectedStation: station,
      showStationDetail: true
    });
  },
  closeStationDetail: function() {
    this.setData({
      showStationDetail: false
    });
  },
  callPhone: function() {
    if (this.data.selectedStation && this.data.selectedStation.phone) {
      wx.makePhoneCall({
        phoneNumber: this.data.selectedStation.phone
      });
    }
  },
  navigateToStation: function() {
    if (this.data.selectedStation) {
      const { latitude, longitude, name, address } = this.data.selectedStation;
      wx.openLocation({
        latitude: latitude,
        longitude: longitude,
        name: name,
        address: address,
        scale: 18
      });
    }
  },
  onShareAppMessage: function() {
    return {
      title: '附近的垃圾回收站点',
      path: '/pages/recycle/recycle'
    };
  }
});