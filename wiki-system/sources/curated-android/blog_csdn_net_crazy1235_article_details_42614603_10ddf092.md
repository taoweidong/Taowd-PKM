---
source: "http://blog.csdn.net/crazy1235/article/details/42614603"
title: "Android百度地图开发（一）之初体验_<uses-permission android:name= 地图-CSDN博客"
fetched_at: "2026-10-05 15:26:52"
---

**转载请注明出处：<http://blog.csdn.net/crazy1235/article/details/42614603>**

做关于位置或者定位的app的时候免不了使用地图功能，本人最近由于项目的需求需要使用百度地图的一些功能，所以这几天研究了一下，现写一下blog记录一下，欢迎大家评论指正！

### 一、申请AK（API Key）

要想使用百度地图sdk，就必须申请一个百度地图的api key。申请流程挺简单的。

首先注册成为百度的开发者，然后打开<http://lbsyun.baidu.com/apiconsole/key>这个网址，添加应用：

![](https://img-blog.csdn.net/20150111201306141?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvY3JhenkxMjM1/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

创建应用最重要的一步是【安全码】。安全码是有【数字签名】和【;】和【包名】组成。包名就是你所创建的项目的包的结构，是指AndroidManifest.xml中的manifest标签下的package的值。

数字签名指android的签名证书的SHA1值。

获取数字签名有两种方法：

1\. 第一种方法：使用eclipse查看。

打开eclipse的preferences菜单，在Android下的【Build】中可以看到SHA1的值，如下图：

![](https://img-blog.csdn.net/20150111204054720?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvY3JhenkxMjM1/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

2\. 第二种方法：使用keytool工具（jdk自带）查看。

在控制台下，输入【cd .android】，然后输入【keytool -list -v -keystore debug.keystore】回车，然后提示你输入【秘钥库口令】，输入【android】回车然后就会显示SHA1的值。

![](https://img-blog.csdn.net/20150111204527281?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvY3JhenkxMjM1/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)



数字签名搞定了，然后创建应用就ok了。创建完成之后，应用列表中会显示相应的AK，也就是api key。

### 二、下载SDK开发包

打开<http://developer.baidu.com/map/index.php?title=androidsdk/sdkandev-download>网址下载sdk，可以全部下载，也可以自定义下载。从V2.3.0之后的版本，SDK的开发包以可定制的形式提供下载，用户可以根据自己的项目需要勾选相应的功能下载对应的SDK开发包。

### 三、在android项目中引用百度SDK

1\. 将开发包中的jar包和so文件添加到libs文件下。

![](https://img-blog.csdn.net/20150111210601745?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvY3JhenkxMjM1/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)



2\. 在AndroidManifest.xml中添加开发秘钥和所需权限。


    <application
            android:allowBackup="true"
            android:icon="@drawable/ic_launcher"
            android:label="@string/app_name"
            android:theme="@style/AppTheme" >
            <meta-data
                android:name="com.baidu.lbsapi.API_KEY"
                android:value="填写你申请的AK" />

权限：


    <!-- 百度API所需权限 -->
        <uses-permission android:name="android.permission.GET_ACCOUNTS" />
        <uses-permission android:name="android.permission.USE_CREDENTIALS" />
        <uses-permission android:name="android.permission.MANAGE_ACCOUNTS" />
        <uses-permission android:name="android.permission.AUTHENTICATE_ACCOUNTS" />
        <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
        <uses-permission android:name="android.permission.INTERNET" />
        <uses-permission android:name="com.android.launcher.permission.READ_SETTINGS" />
        <uses-permission android:name="android.permission.CHANGE_WIFI_STATE" />
        <uses-permission android:name="android.permission.ACCESS_WIFI_STATE" />
        <uses-permission android:name="android.permission.READ_PHONE_STATE" />
        <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
        <uses-permission android:name="android.permission.BROADCAST_STICKY" />
        <uses-permission android:name="android.permission.WRITE_SETTINGS" />
        <uses-permission android:name="android.permission.READ_PHONE_STATE" />

3\. 在布局文件中添加地图控件：


    <com.baidu.mapapi.map.MapView
            android:id="@+id/bmapview"
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            android:clickable="true" />

4\. 在应用程序创建时初始化SDK引用的Context全局变量。


    	@Override
    	protected void onCreate(Bundle savedInstanceState) {
    		super.onCreate(savedInstanceState);
    		requestWindowFeature(Window.FEATURE_NO_TITLE);
    		//
    		SDKInitializer.initialize(getApplicationContext());
    		setContentView(R.layout.activity_main);
    		init();
    	}

这里需要注意一下：initialize方法中必须传入的是ApplicationContext，传入this，或者MAinActivity.this都不行，不然会报运行时异常，所以百度建议把该方法放到Application的初始化方法中。

![](https://img-blog.csdn.net/20150111211830578?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvY3JhenkxMjM1/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

然后重写activity的生命周期的几个方法来管理地图的生命周期。在activity的onResume、onPause、onDestory方法中分别执行mapview的onReusme、onPause、onDestory方法。


    package com.bdmap.view;
    import com.baidu.mapapi.SDKInitializer;
    import com.baidu.mapapi.map.BaiduMap;
    import com.baidu.mapapi.map.MapView;
    import android.app.Activity;
    import android.os.Bundle;
    import android.view.View;
    import android.view.Window;
    public class MainActivity extends Activity {
    	// 百度地图控件
    	private MapView mMapView = null;
    	// 百度地图对象
    	private BaiduMap bdMap;
    	@Override
    	protected void onCreate(Bundle savedInstanceState) {
    		super.onCreate(savedInstanceState);
    		requestWindowFeature(Window.FEATURE_NO_TITLE);
    		//
    		SDKInitializer.initialize(getApplicationContext());
    		setContentView(R.layout.activity_main);
    		init();
    	}

    	/**
    	 * 初始化方法
    	 */
    	private void init() {
    		mMapView = (MapView) findViewById(R.id.bmapview);
    	}
    	@Override
    	protected void onResume() {
    		super.onResume();
    		mMapView.onResume();
    	}
    	@Override
    	protected void onPause() {
    		super.onPause();
    		mMapView.onPause();
    	}
    	@Override
    	protected void onDestroy() {
    		mMapView.onDestroy();
    		mMapView = null;
    		super.onDestroy();
    	}
    }



完成以上步骤，此时就可以完成一个简单的”Hello Map“程序了。

### 三、普通地图和卫星地图切换

百度地图将地图的类型分为两种：普通矢量地图和卫星图。


    mMapView = (MapView) findViewById(R.id.bmapView);
    mBaiduMap = mMapView.getMap();
    //普通地图
    mBaiduMap.setMapType(BaiduMap.MAP_TYPE_NORMAL);
    //卫星地图
    mBaiduMap.setMapType(BaiduMap.MAP_TYPE_SATELLITE);


### 四、显示实时交通图（路况图）


    //开启交通图
    mBaiduMap.setTrafficEnabled(true);


### 五、显示热力图

热力图就是以特殊高亮的形式显示访客热衷的页面区域和访客所在的地理区域的图示。通俗来说就是显示地图上某一块区域的人的密集程度。类似于下图所示：

![](https://img-blog.csdn.net/20150111213200406?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvY3JhenkxMjM1/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)


    //开启热力图
    mBaiduMap.setBaiduHeatMapEnabled(true);
