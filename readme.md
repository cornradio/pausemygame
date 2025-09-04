The English version readme is at the bottom

## 这是什么
这是一个简单的 Windows 应用程序，通过进程名称来暂停和恢复进程。

这个工具可以非常轻松地暂停单机游戏，在需要的时候一键恢复，就像 xbox 和 ps 游戏机的快速恢复功能一样。

## 安装
从 GitHub [下载](https://github.com/cornradio/pausemygame/releases) 发布版本

或者使用 winget 安装：(版本比较旧，是v2）因为winget更新好麻烦还要审核以后也懒得更新了。
```
winget install cornradio.pausemygame
```

## 使用方法指南
[bilibili视频（大概三分钟）](https://www.bilibili.com/video/BV1HuhrzjEy2)
文字版：
1. 通过任务管理器获取游戏进程 exe 名称
2. file - edit config ，编辑配置文件，加入exe，然后  file - reload config 重载配置
3. 选择到你的游戏，然后可以使用 暂停/继续/kill 等指令

## 截图
v2  
![image](https://github.com/user-attachments/assets/f7f64024-f576-43ba-89f0-7aef7d5574e7)

v3  
<img width="1055" height="721" alt="image" src="https://github.com/user-attachments/assets/ade024b6-5834-4fae-9333-d981e23fc9c2" />


## 备注
- main.py 使用dpg作为ui组件, v1。
- main2.py 使用tk作为ui组件，v2。
- main3.py 更改了ui设计，增加了读取icon的功能 v3。
- 
为了兼容旧版使用习惯，我保留了这些源文件，但是最新版的编译将会使用 main3.py

## 相似工具推荐
https://github.com/Merrit/nyrna/  
https://gitee.com/damodms/hs-freezer-hidden-in-the-snow/



---

## What is This?
This is a simple Windows application designed to pause and resume processes by their name.

This tool makes it incredibly easy to pause single-player games and resume them with a single click whenever needed, much like the Quick Resume feature on Xbox and PlayStation consoles.

## Installation
Download the release from GitHub: [Download](https://github.com/cornradio/pausemygame/releases)

Alternatively, install using winget (note: this version might be older):
```
winget install cornradio.pausemygame
```

## Usage Guide
[Bilibili Video (approx. 3 minutes)](https://www.bilibili.com/video/BV1HuhrzjEy2)

Text version:
1.  Obtain the game process's `.exe` name from Task Manager.
2.  Go to `File > Edit Config` to edit the configuration file, add the `.exe` name, then `File > Reload Config` to apply changes.
3.  Select your game, and you can then use `Pause`, `Resume`, `Kill`, etc., commands.

## Screenshots
v2  
![image](https://github.com/user-attachments/assets/f7f64024-f576-43ba-89f0-7aef7d5574e7)

v3  
<img width="1046" height="737" alt="image" src="https://github.com/user-attachments/assets/5847fde1-aab6-4e33-8823-bcf90149e363" />

## Notes
-   `main.py` uses DPG (Dear PyGui) as the UI component, v1.
-   `main2.py` uses Tkinter as the UI component, v2.
-   `main3.py` features a redesigned UI and added the functionality to read icons, v3.
-   To maintain compatibility with older usage habits, I have kept these source files. However, the latest compilation will use `main3.py`.

## Similar Tools Recommended
*   https://github.com/Merrit/nyrna/
*   https://gitee.com/damodms/hs-freezer-hidden-in-the-snow/

---
