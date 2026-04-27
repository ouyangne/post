# 单位换算工具APP

一款功能强大的单位换算工具，支持多种单位之间的换算，可以安装到手机上使用。

## 功能特性

- ✅ 快捷施工换算（首页核心）
  - ft ↔ m
  - in ↔ cm
  - sq ft ↔ sq m
  - gallon (US) ↔ liter
  - lb ↔ kg
  - ft³ ↔ m³

- ✅ 高级换算页（下拉选择）
  - 长度：ft, in, m, cm
  - 面积：sq ft, sq m
  - 体积：gallon (US), liter, ft³, m³
  - 重量：lb, kg

- ✅ 最近10条历史记录
  - 点击记录可自动填充输入框

- ✅ 离线可用
  - 所有换算逻辑本地实现
  - 历史记录本地存储

- ✅ 设置页面
  - Remove Ads 按钮
  - Restore Purchase 按钮
  - App Version 显示

## 技术栈

- HTML5 + CSS3 + JavaScript
- Cordova/PhoneGap
- 本地存储 (localStorage)

## 构建原生APP

### 准备工作

1. **安装 Node.js**
   - 访问 https://nodejs.org/ 下载并安装最新版本的 Node.js

2. **安装 Cordova/PhoneGap**
   ```bash
   npm install -g cordova phonegap
   ```

3. **安装平台依赖**
   - Android: 需要安装 Android Studio 和 JDK
   - iOS: 需要安装 Xcode (仅 macOS)

### 构建步骤

1. **进入项目目录**
   ```bash
   cd e:\TAER-测试\App
   ```

2. **安装依赖**
   ```bash
   npm install
   ```

3. **添加平台**
   ```bash
   cordova platform add android
   # 或
   cordova platform add ios
   ```

4. **构建APP**
   ```bash
   # 构建Android APP
   npm run build-android
   
   # 或构建iOS APP
   npm run build-ios
   ```

5. **安装到设备**
   ```bash
   # 运行到Android设备
   npm run run-android
   
   # 或运行到iOS设备
   npm run run-ios
   ```

## 构建产物

- Android: `platforms/android/app/build/outputs/apk/debug/app-debug.apk`
- iOS: `platforms/ios/build/device/` 目录下的 .ipa 文件

## 插件说明

已配置的Cordova插件：

- `cordova-plugin-whitelist` - 处理网络访问权限
- `cordova-plugin-statusbar` - 控制状态栏
- `cordova-plugin-splashscreen` - 显示启动屏幕
- `cordova-plugin-device` - 获取设备信息
- `cordova-plugin-storage` - 本地存储

## 离线功能

应用支持完全离线使用，所有换算逻辑和历史记录都存储在本地，无需网络连接。

## 注意事项

- 构建iOS APP需要 macOS 系统
- 构建Android APP需要配置好 Android 开发环境
- 首次构建可能需要下载较多依赖，请耐心等待
- 应用使用localStorage存储历史记录，数据会保存在设备本地