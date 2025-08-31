import tkinter as tk
from tkinter import ttk
import subprocess
from hide import hide_by_exe
import webbrowser
import os
import psutil
import win32api
import win32con
import win32gui
import win32ui
from PIL import Image
import PIL.ImageTk as ImageTk
import json
import base64
import io
import threading
import time

class GamePauser:
    def __init__(self, root):
        self.root = root
        self.root.title("pause my game")
        self.root.geometry("460x350")  # 增加窗口高度以容纳新按钮
        
        # 数据库文件路径
        self.db_file = 'game_database.json'
        self.game_db = {}
        self.load_database()
        
        # 快捷键设置
        self.hotkey_file = 'hotkeys.json'
        self.hotkeys = {'pause': 'Ctrl+Alt+P', 'resume': 'Ctrl+Alt+R'}
        self.load_hotkeys()
        
        # 启动快捷键监听线程
        self.hotkey_thread = threading.Thread(target=self.hotkey_listener, daemon=True)
        self.hotkey_thread.start()
        
        # 设置图标
        try:
            self.root.iconbitmap('icon.ico')
        except:
            print("Warning: icon.ico not found")
        
        # 设置暗色主题
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # 配置暗色主题颜色
        self.style.configure('.',
            background='#2b2b2b',
            foreground='#ffffff',
            fieldbackground='#3c3f41',
            troughcolor='#3c3f41',
            selectbackground='#4b6eaf',
            selectforeground='#ffffff'
        )
        
        self.style.configure('TButton',
            background='#3c3f41',
            foreground='#ffffff',
            padding=5
        )
        
        self.style.configure('TLabel',
            background='#2b2b2b',
            foreground='#ffffff'
        )
        
        self.style.configure('TFrame',
            background='#2b2b2b'
        )
        
        self.style.configure('TCombobox',
            fieldbackground='#3c3f41',
            background='#3c3f41',
            foreground='#ffffff',
            arrowcolor='#ffffff'
        )
        
        # 设置根窗口背景色
        self.root.configure(bg='#2b2b2b')
        
        # 创建菜单栏
        self.create_menu()
        
        # 创建主框架
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        # ttk.Label(self.main_frame, text="Game Pauser", foreground="#78DCDC", font=('Arial', 18, 'bold')).pack(pady=10)
        
        # 创建左右分栏框架
        content_frame = ttk.Frame(self.main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 左侧：程序列表区域
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_frame.configure(width=250)  # 固定宽度
        left_frame.pack_propagate(False)  # 防止子组件改变父组件大小
        
        # 程序列表标题
        # ttk.Label(left_frame, text="games", foreground="#ffffff", font=('Arial', 12, 'bold')).pack(pady=(0, 5))
        
        # 创建Listbox
        self.program_listbox = tk.Listbox(left_frame, 
                                         bg='#3c3f41', 
                                         fg='#ffffff', 
                                         selectbackground='#4b6eaf',
                                         selectforeground='#ffffff',
                                         font=('Arial', 11),
                                         height=12,
                                         relief='flat',
                                         bd=0,
                                         highlightthickness=1,
                                         highlightcolor='#4b6eaf',
                                         highlightbackground='#3c3f41')
        self.program_listbox.pack(fill=tk.BOTH, expand=True)
        
        # 绑定Listbox选择事件
        self.program_listbox.bind('<<ListboxSelect>>', self.on_listbox_selected)
        
        # 右侧：控制面板
        right_frame = ttk.Frame(content_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        # 图标显示区域
        self.icon_frame = ttk.Frame(right_frame)
        self.icon_frame.pack(pady=5)
        
        # 默认占位符
        self.icon_label = ttk.Label(self.icon_frame, text="选择程序显示图标", foreground="#787878", font=('Arial', 10))
        self.icon_label.pack()
        
        # 状态显示
        self.status_label = ttk.Label(right_frame, text="Game Status untouched", foreground="#787878", font=('Arial', 10))
        self.status_label.pack(pady=5)
        
        # 主要控制按钮框架
        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack(fill=tk.X, pady=15)
        
        # 使用带颜色的按钮
        pause_btn = tk.Button(btn_frame, text="Pause", command=self.pause_game, 
                             width=15, bg='#3c3f41', fg='#FF8E53', 
                             font=('Arial', 10, 'bold'), relief='flat',
                             activebackground='#4a4d4f', activeforeground='#FF8E53')
        pause_btn.pack(pady=5)
        
        resume_btn = tk.Button(btn_frame, text="Resume", command=self.resume_game, 
                              width=15, bg='#3c3f41', fg='#4ECDC4', 
                              font=('Arial', 10, 'bold'), relief='flat',
                              activebackground='#4a4d4f', activeforeground='#4ECDC4')
        resume_btn.pack(pady=5)
        
        kill_btn = tk.Button(btn_frame, text="Kill", command=self.kill_game, 
                            width=15, bg='#3c3f41', fg='#FF6B6B', 
                            font=('Arial', 10, 'bold'), relief='flat',
                            activebackground='#4a4d4f', activeforeground='#FF6B6B')
        kill_btn.pack(pady=5)
        
        launch_btn = tk.Button(btn_frame, text="Launch", command=self.launch_game, 
                              width=15, bg='#3c3f41', fg='#70AD07', 
                              font=('Arial', 10, 'bold'), relief='flat',
                              activebackground='#4a4d4f', activeforeground='#45B7D1')
        launch_btn.pack(pady=5)
        
        ttk.Separator(right_frame, orient='horizontal').pack(fill=tk.X, pady=15)
        
        # 配置部分
        config_frame = ttk.Frame(right_frame)
        config_frame.pack(fill=tk.X, pady=5)
        
        edit_btn = tk.Button(config_frame, text="Edit", command=self.edit_config, 
                            width=15, bg='#3c3f41', fg='#A8E6CF', 
                            font=('Arial', 10, 'bold'), relief='flat',
                            activebackground='#4a4d4f', activeforeground='#A8E6CF')
        edit_btn.pack(pady=5)
        
        reload_btn = tk.Button(config_frame, text="Reload", command=self.load_config, 
                              width=15, bg='#3c3f41', fg='#FFD93D', 
                              font=('Arial', 10, 'bold'), relief='flat',
                              activebackground='#4a4d4f', activeforeground='#FFD93D')
        reload_btn.pack(pady=5)
        
        self.info_label = ttk.Label(config_frame, text="Game loaded:", foreground="#787878")
        self.info_label.pack(pady=5)
        
        # 初始加载配置
        self.load_config()

    def load_database(self):
        """加载游戏数据库"""
        try:
            if os.path.exists(self.db_file):
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    self.game_db = json.load(f)
            else:
                self.game_db = {}
        except Exception as e:
            print(f"加载数据库失败: {e}")
            self.game_db = {}

    def save_database(self):
        """保存游戏数据库"""
        try:
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump(self.game_db, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存数据库失败: {e}")

    def image_to_base64(self, image):
        """将PIL图像转换为base64字符串"""
        try:
            buffer = io.BytesIO()
            image.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue()).decode()
            return img_str
        except Exception as e:
            print(f"图像转base64失败: {e}")
            return None

    def base64_to_image(self, base64_str):
        """将base64字符串转换为PIL图像"""
        try:
            img_data = base64.b64decode(base64_str)
            image = Image.open(io.BytesIO(img_data))
            return image
        except Exception as e:
            print(f"base64转图像失败: {e}")
            return None

    def update_database(self, game_name, exe_path=None, icon_image=None):
        """更新数据库中的游戏信息"""
        if game_name not in self.game_db:
            self.game_db[game_name] = {}
        
        if exe_path:
            self.game_db[game_name]['exe_path'] = exe_path
        
        if icon_image:
            icon_base64 = self.image_to_base64(icon_image)
            if icon_base64:
                self.game_db[game_name]['icon'] = icon_base64
        
        self.save_database()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Reload Config", command=self.load_config)
        file_menu.add_command(label="Edit Config", command=self.edit_config)
        file_menu.add_command(label="Show Database", command=self.show_database)
        file_menu.add_command(label="Show Path", command=self.show_path)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # 快捷键菜单
        hotkey_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Hotkey", menu=hotkey_menu)
        hotkey_menu.add_command(label=f"Set Pause Hotkey ({self.hotkeys.get('pause', 'Not set')})", command=self.set_pause_hotkey)
        hotkey_menu.add_command(label=f"Set Resume Hotkey ({self.hotkeys.get('resume', 'Not set')})", command=self.set_resume_hotkey)
        hotkey_menu.add_separator()
        hotkey_menu.add_command(label="Show Current Hotkeys", command=self.show_hotkeys)
        
        # 工具菜单
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Task Manager", command=self.open_taskmgr)
        tools_menu.add_command(label="Ntop", command=self.open_ntop)
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="View Help", command=self.show_help)
        help_menu.add_command(label="GitHub", command=lambda: webbrowser.open("https://github.com/cornradio/pausemygame"))

    def run_in_subprocess(self, command):
        creation_flags = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_BREAKAWAY_FROM_JOB
        subprocess.Popen(command, shell=True, creationflags=creation_flags, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def load_config(self):
        try:
            with open('game_name.txt', 'r') as f:
                game_names = f.read().splitlines()
            
            # 清空listbox
            self.program_listbox.delete(0, tk.END)
            
            # 添加程序到listbox
            for game_name in game_names:
                self.program_listbox.insert(tk.END, game_name)
            
            if game_names:
                # 选择第一个程序
                self.program_listbox.selection_set(0)
                self.program_listbox.see(0)
                # 显示第一个程序的图标
                self.update_icon(game_names[0])
            
            self.info_label.config(text=f'Game loaded: {len(game_names)} ')
        except FileNotFoundError:
            self.info_label.config(text='No game_name.txt found')

    def on_listbox_selected(self, event=None):
        """当listbox选择变化时调用"""
        selection = self.program_listbox.curselection()
        if selection:
            selected_game = self.program_listbox.get(selection[0])
            self.update_icon(selected_game)

    def find_exe_path(self, exe_name):
        """通过exe名称从当前运行的程序中提取到文件路径"""
        try:
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                if proc.info['name'] and proc.info['name'].lower() == exe_name.lower():
                    exe_path = proc.info['exe']
                    if exe_path and os.path.exists(exe_path):
                        return exe_path
            return None
        except Exception as e:
            print(f"查找进程时出错: {e}")
            return None

    def extract_icon_from_exe(self, exe_path):
        """从exe文件中提取图标"""
        try:
            # 提取 exe 中的第一个图标
            large, small = win32gui.ExtractIconEx(exe_path, 0)
            if large:
                hicon = large[0]
            elif small:
                hicon = small[0]
            else:
                return None

            # 创建临时文件
            temp_bmp = "temp_icon.bmp"
            
            # 保存到文件
            hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
            hbmp = win32ui.CreateBitmap()
            hbmp.CreateCompatibleBitmap(hdc, 32, 32)
            hdc_mem = hdc.CreateCompatibleDC()
            hdc_mem.SelectObject(hbmp)
            win32gui.DrawIconEx(hdc_mem.GetHandleOutput(), 0, 0, hicon, 32, 32, 0, None, win32con.DI_NORMAL)
            hbmp.SaveBitmapFile(hdc_mem, temp_bmp)

            # 转换为 PIL 图像
            img = Image.open(temp_bmp)
            
            # 清理临时文件
            try:
                os.remove(temp_bmp)
            except:
                pass
                
            return img
            
        except Exception as e:
            print(f"提取图标时出错: {e}")
            return None

    def create_placeholder_icon(self, exe_name):
        """创建占位符图标"""
        try:
            # 创建一个简单的占位符图标
            img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
            
            # 绘制一个简单的图标
            from PIL import ImageDraw
            draw = ImageDraw.Draw(img)
            
            # 根据程序名称选择不同的图标样式
            exe_name_lower = exe_name.lower()
            
            if 'chrome' in exe_name_lower:
                # Chrome浏览器 - 红色圆形
                draw.ellipse([2, 2, 30, 30], fill=(220, 20, 60, 255), outline=(255, 255, 255, 255), width=2)
                draw.ellipse([8, 8, 24, 24], fill=(255, 255, 255, 255))
                draw.ellipse([10, 10, 22, 22], fill=(220, 20, 60, 255))
            elif 'game' in exe_name_lower or 'devil' in exe_name_lower or 'sb-win' in exe_name_lower:
                # 游戏 - 绿色圆形
                draw.ellipse([2, 2, 30, 30], fill=(34, 139, 34, 255), outline=(255, 255, 255, 255), width=2)
                draw.rectangle([8, 8, 24, 24], fill=(255, 255, 255, 255))
                draw.rectangle([10, 10, 22, 22], fill=(34, 139, 34, 255))
            elif 'notepad' in exe_name_lower:
                # 记事本 - 白色方形
                draw.rectangle([2, 2, 30, 30], fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), width=2)
                draw.rectangle([8, 8, 24, 24], fill=(0, 0, 0, 255))
                draw.rectangle([10, 10, 22, 22], fill=(255, 255, 255, 255))
            elif 'calc' in exe_name_lower:
                # 计算器 - 橙色方形
                draw.rectangle([2, 2, 30, 30], fill=(255, 165, 0, 255), outline=(255, 255, 255, 255), width=2)
                draw.rectangle([8, 8, 24, 24], fill=(255, 255, 255, 255))
                draw.rectangle([10, 10, 22, 22], fill=(255, 165, 0, 255))
            else:
                # 默认程序图标 - 蓝色圆形
                draw.ellipse([2, 2, 30, 30], fill=(70, 130, 180, 255), outline=(255, 255, 255, 255), width=2)
                draw.rectangle([8, 8, 24, 24], fill=(255, 255, 255, 255))
                draw.rectangle([10, 10, 22, 22], fill=(70, 130, 180, 255))
            
            return img
            
        except Exception as e:
            print(f"创建占位符图标失败: {e}")
            return None

    def update_icon(self, exe_name):
        """更新显示的图标"""
        try:
            # 清除之前的图标
            for widget in self.icon_frame.winfo_children():
                widget.destroy()
            
            # 1. 查找exe路径
            exe_path = self.find_exe_path(exe_name)
            
            if exe_path:
                # 2. 提取真实图标
                icon_img = self.extract_icon_from_exe(exe_path)
                if icon_img:
                    # 调整图标大小
                    icon_img = icon_img.resize((32, 32), Image.Resampling.LANCZOS)
                    self.icon_photo = ImageTk.PhotoImage(icon_img)
                    
                    # 显示真实图标
                    icon_label = ttk.Label(self.icon_frame, image=self.icon_photo)
                    icon_label.pack()
                    
                    # 添加程序名称标签
                    name_label = ttk.Label(self.icon_frame, text=exe_name, foreground="#ffffff", font=('Arial', 10))
                    name_label.pack(pady=2)
                    
                    # 更新状态显示
                    self.status_label.config(text=f"✓ {exe_name} (运行中)", foreground="#00FF00")
                    
                    # 更新数据库
                    self.update_database(exe_name, exe_path=exe_path, icon_image=icon_img)
                    return
            
            # 3. 尝试从数据库加载图标
            if exe_name in self.game_db and 'icon' in self.game_db[exe_name]:
                db_icon = self.base64_to_image(self.game_db[exe_name]['icon'])
                if db_icon:
                    db_icon = db_icon.resize((32, 32), Image.Resampling.LANCZOS)
                    self.icon_photo = ImageTk.PhotoImage(db_icon)
                    
                    # 显示数据库中的图标
                    icon_label = ttk.Label(self.icon_frame, image=self.icon_photo)
                    icon_label.pack()
                    
                    # 添加程序名称标签
                    name_label = ttk.Label(self.icon_frame, text=f"{exe_name} (数据库)", foreground="#787878", font=('Arial', 10))
                    name_label.pack(pady=2)
                    
                    # 更新状态显示
                    self.status_label.config(text=f"○ {exe_name} (未运行)", foreground="#787878")
                    return
            
            # 4. 如果没有找到真实图标，使用占位符
            placeholder_img = self.create_placeholder_icon(exe_name)
            if placeholder_img:
                self.icon_photo = ImageTk.PhotoImage(placeholder_img)
                
                # 显示占位符图标
                icon_label = ttk.Label(self.icon_frame, image=self.icon_photo)
                icon_label.pack()
                
                # 添加程序名称标签
                name_label = ttk.Label(self.icon_frame, text=f"{exe_name} (占位符)", foreground="#787878", font=('Arial', 10))
                name_label.pack(pady=2)
                
                # 更新状态显示
                self.status_label.config(text=f"○ {exe_name} (未运行)", foreground="#787878")
            else:
                # 5. 如果连占位符都创建失败，显示文本
                default_label = ttk.Label(self.icon_frame, text=f"未找到 {exe_name} 的图标", foreground="#787878", font=('Arial', 10))
                default_label.pack()
                
                # 更新状态显示
                self.status_label.config(text=f"✗ {exe_name} (图标加载失败)", foreground="#FF0000")
                
        except Exception as e:
            print(f"更新图标时出错: {e}")
            # 显示错误信息
            for widget in self.icon_frame.winfo_children():
                widget.destroy()
            error_label = ttk.Label(self.icon_frame, text=f"图标加载失败", foreground="#FF0000", font=('Arial', 10))
            error_label.pack()
            
            # 更新状态显示
            self.status_label.config(text=f"✗ {exe_name} (错误)", foreground="#FF0000")

    def edit_config(self):
        self.run_in_subprocess('notepad game_name.txt')

    def get_selected_game(self):
        """获取当前选中的游戏名称"""
        selection = self.program_listbox.curselection()
        if selection:
            return self.program_listbox.get(selection[0])
        return None

    def pause_game(self):
        game_name = self.get_selected_game()
        if game_name:
            self.status_label.config(text=f"⏸ {game_name} Paused", foreground="#FF00FF")
            hide_by_exe(game_name)
            self.run_in_subprocess(f'PsSuspend "{game_name}"')
        else:
            self.status_label.config(text="请先选择一个程序", foreground="#FF0000")

    def kill_game(self):
        game_name = self.get_selected_game()
        if game_name:
            self.status_label.config(text=f"⏹ {game_name} Killed", foreground="#FF0000")
            self.run_in_subprocess(f'taskkill /IM "{game_name}" /F')
        else:
            self.status_label.config(text="请先选择一个程序", foreground="#FF0000")

    def resume_game(self):
        game_name = self.get_selected_game()
        if game_name:
            self.status_label.config(text=f"▶ {game_name} Resumed", foreground="#00FF00")
            self.run_in_subprocess(f'PsSuspend -r "{game_name}"')
        else:
            self.status_label.config(text="请先选择一个程序", foreground="#FF0000")

    def launch_game(self):
        game_name = self.get_selected_game()
        if game_name:
            exe_path = self.game_db.get(game_name, {}).get('exe_path')
            if exe_path and os.path.exists(exe_path):
                self.status_label.config(text=f"🚀 Launching {game_name}...", foreground="#007BFF")
                self.run_in_subprocess(f'"{exe_path}"')
            else:
                # 尝试直接运行程序名
                self.status_label.config(text=f"🚀 Launching {game_name}...", foreground="#007BFF")
                self.run_in_subprocess(f'"{game_name}"')
                # 更新图标以反映启动状态
                self.update_icon(game_name)
        else:
            self.status_label.config(text="请先选择一个程序", foreground="#FF0000")

    def open_taskmgr(self):
        self.run_in_subprocess('taskmgr')

    def open_ntop(self):
        self.run_in_subprocess('ntop')

    def show_database(self):
        """直接打开数据库文件"""
        try:
            if os.path.exists(self.db_file):
                self.run_in_subprocess(f'notepad "{self.db_file}"')
            else:
                # 如果文件不存在，创建一个空的数据库文件
                self.save_database()
                self.run_in_subprocess(f'notepad "{self.db_file}"')
        except Exception as e:
            print(f"打开数据库文件失败: {e}")

    def load_hotkeys(self):
        """加载快捷键设置"""
        try:
            if os.path.exists(self.hotkey_file):
                with open(self.hotkey_file, 'r', encoding='utf-8') as f:
                    self.hotkeys = json.load(f)
        except Exception as e:
            print(f"加载快捷键失败: {e}")

    def save_hotkeys(self):
        """保存快捷键设置"""
        try:
            with open(self.hotkey_file, 'w', encoding='utf-8') as f:
                json.dump(self.hotkeys, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存快捷键失败: {e}")

    def set_pause_hotkey(self):
        """设置暂停快捷键"""
        self.show_hotkey_dialog("pause", "Set Pause Hotkey")

    def set_resume_hotkey(self):
        """设置恢复快捷键"""
        self.show_hotkey_dialog("resume", "Set Resume Hotkey")

    def show_hotkey_dialog(self, action, title):
        """显示快捷键设置对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("400x300")
        dialog.configure(bg='#2b2b2b')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 说明文字
        ttk.Label(main_frame, text="Press the key combination you want to use:", 
                 foreground='#ffffff', font=('Arial', 12)).pack(pady=10)
        
        # 当前快捷键显示
        current_hotkey = self.hotkeys.get(action, 'Not set')
        current_label = ttk.Label(main_frame, text=f"Current: {current_hotkey}", 
                                 foreground='#78DCDC', font=('Arial', 10, 'bold'))
        current_label.pack(pady=5)
        
        # 新快捷键显示
        new_label = ttk.Label(main_frame, text="New: Press keys...", 
                             foreground='#FFD93D', font=('Arial', 10, 'bold'))
        new_label.pack(pady=5)
        
        # 按钮框架
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear", command=lambda: self.clear_hotkey(action, dialog)).pack(side=tk.LEFT, padx=5)
        
        # 绑定键盘事件
        def on_key(event):
            keys = []
            if event.state & 0x4:  # Ctrl
                keys.append('Ctrl')
            if event.state & 0x8:  # Alt
                keys.append('Alt')
            if event.state & 0x1:  # Shift
                keys.append('Shift')
            
            # 获取按键名称
            key_name = event.keysym
            if key_name not in ['Control_L', 'Control_R', 'Alt_L', 'Alt_R', 'Shift_L', 'Shift_R']:
                keys.append(key_name)
            
            if keys:
                new_hotkey = '+'.join(keys)
                new_label.config(text=f"New: {new_hotkey}")
                
                # 保存快捷键
                self.hotkeys[action] = new_hotkey
                self.save_hotkeys()
                
                # 更新当前显示
                current_label.config(text=f"Current: {new_hotkey}")
                
                # 更新快捷键注册
                self.update_hotkey_registration()
                
                # 更新菜单显示
                self.update_hotkey_menu()
        
        dialog.bind('<Key>', on_key)
        dialog.focus_set()

    def clear_hotkey(self, action, dialog):
        """清除快捷键"""
        self.hotkeys[action] = 'Not set'
        self.save_hotkeys()
        # 更新快捷键注册
        self.update_hotkey_registration()
        # 更新菜单显示
        self.update_hotkey_menu()
        dialog.destroy()

    def show_hotkeys(self):
        """显示当前快捷键设置"""
        hotkey_window = tk.Toplevel(self.root)
        hotkey_window.title("Current Hotkeys")
        hotkey_window.geometry("300x250")
        hotkey_window.configure(bg='#2b2b2b')
        
        main_frame = ttk.Frame(hotkey_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Current Hotkey Settings", 
                 foreground='#78DCDC', font=('Arial', 14, 'bold')).pack(pady=10)
        
        ttk.Label(main_frame, text=f"Pause: {self.hotkeys.get('pause', 'Not set')}", 
                 foreground='#FF8E53', font=('Arial', 12)).pack(pady=5)
        
        ttk.Label(main_frame, text=f"Resume: {self.hotkeys.get('resume', 'Not set')}", 
                 foreground='#4ECDC4', font=('Arial', 12)).pack(pady=5)
        
        ttk.Button(main_frame, text="OK", command=hotkey_window.destroy).pack(pady=20)

    def hotkey_listener(self):
        """全局快捷键监听线程"""
        try:
            import keyboard
            
            def on_pause_hotkey():
                """暂停快捷键回调"""
                try:
                    # 在主线程中执行UI更新
                    self.root.after(0, self.execute_pause_hotkey)
                except Exception as e:
                    print(f"执行暂停快捷键失败: {e}")
            
            def on_resume_hotkey():
                """恢复快捷键回调"""
                try:
                    # 在主线程中执行UI更新
                    self.root.after(0, self.execute_resume_hotkey)
                except Exception as e:
                    print(f"执行恢复快捷键失败: {e}")
            
            # 注册快捷键
            pause_hotkey = self.hotkeys.get('pause', 'Ctrl+Alt+P')
            resume_hotkey = self.hotkeys.get('resume', 'Ctrl+Alt+R')
            
            if pause_hotkey != 'Not set':
                keyboard.add_hotkey(pause_hotkey, on_pause_hotkey)
                print(f"注册暂停快捷键: {pause_hotkey}")
            
            if resume_hotkey != 'Not set':
                keyboard.add_hotkey(resume_hotkey, on_resume_hotkey)
                print(f"注册恢复快捷键: {resume_hotkey}")
            
            # 保持线程运行
            keyboard.wait()
            
        except ImportError:
            print("需要安装keyboard库: pip install keyboard")
        except Exception as e:
            print(f"快捷键监听失败: {e}")

    def execute_pause_hotkey(self):
        """执行暂停快捷键"""
        game_name = self.get_selected_game()
        if game_name:
            self.status_label.config(text=f"⏸ {game_name} Paused (Hotkey)", foreground="#FF00FF")
            hide_by_exe(game_name)
            self.run_in_subprocess(f'PsSuspend "{game_name}"')
        else:
            self.status_label.config(text="请先选择一个程序 (Hotkey)", foreground="#FF0000")

    def execute_resume_hotkey(self):
        """执行恢复快捷键"""
        game_name = self.get_selected_game()
        if game_name:
            self.status_label.config(text=f"▶ {game_name} Resumed (Hotkey)", foreground="#00FF00")
            self.run_in_subprocess(f'PsSuspend -r "{game_name}"')
        else:
            self.status_label.config(text="请先选择一个程序 (Hotkey)", foreground="#FF0000")

    def update_hotkey_registration(self):
        """更新快捷键注册"""
        try:
            import keyboard
            
            # 清除所有现有快捷键
            keyboard.unhook_all()
            
            # 重新注册快捷键
            pause_hotkey = self.hotkeys.get('pause', 'Ctrl+Alt+P')
            resume_hotkey = self.hotkeys.get('resume', 'Ctrl+Alt+R')
            
            def on_pause_hotkey():
                self.root.after(0, self.execute_pause_hotkey)
            
            def on_resume_hotkey():
                self.root.after(0, self.execute_resume_hotkey)
            
            if pause_hotkey != 'Not set':
                keyboard.add_hotkey(pause_hotkey, on_pause_hotkey)
                print(f"重新注册暂停快捷键: {pause_hotkey}")
            
            if resume_hotkey != 'Not set':
                keyboard.add_hotkey(resume_hotkey, on_resume_hotkey)
                print(f"重新注册恢复快捷键: {resume_hotkey}")
                
        except ImportError:
            print("需要安装keyboard库: pip install keyboard")
        except Exception as e:
            print(f"更新快捷键注册失败: {e}")

    def update_hotkey_menu(self):
        """更新快捷键菜单显示"""
        try:
            # 获取菜单栏
            menubar = self.root.config('menu')
            if menubar:
                # 找到Hotkey菜单
                for i in range(menubar.index('end') + 1):
                    try:
                        menu_label = menubar.entrycget(i, 'label')
                        if menu_label == 'Hotkey':
                            # 删除旧的Hotkey菜单
                            menubar.delete(i)
                            break
                    except:
                        continue
                
                # 重新创建Hotkey菜单
                hotkey_menu = tk.Menu(menubar, tearoff=0)
                menubar.insert_cascade(i, label="Hotkey", menu=hotkey_menu)
                hotkey_menu.add_command(label=f"Set Pause Hotkey ({self.hotkeys.get('pause', 'Not set')})", command=self.set_pause_hotkey)
                hotkey_menu.add_command(label=f"Set Resume Hotkey ({self.hotkeys.get('resume', 'Not set')})", command=self.set_resume_hotkey)
                hotkey_menu.add_separator()
                hotkey_menu.add_command(label="Show Current Hotkeys", command=self.show_hotkeys)
        except Exception as e:
            print(f"更新快捷键菜单失败: {e}")

    def show_path(self):
        """用资源管理器打开存储文件路径"""
        try:
            # 获取当前工作目录
            current_path = os.getcwd()
            # 使用资源管理器打开当前目录
            self.run_in_subprocess(f'explorer "{current_path}"')
        except Exception as e:
            print(f"打开路径失败: {e}")

    def show_help(self):
        help_window = tk.Toplevel(self.root)
        help_window.title("Help")
        help_window.geometry("400x300")
        help_window.configure(bg='#2b2b2b')
        
        help_text = """1. use Taskmgr ,get your game's name
2. Config - Edit 
3. add your ganme name as new line
4. Config - Reload
5. now you can select your game
6. Pause / Resume 

when you stop your game
the RAM is still being used
but CPU is free now

v2025.08.30"""
        
        ttk.Label(help_window, text=help_text, wraplength=350, foreground='#ffffff').pack(padx=20, pady=20)
        ttk.Button(help_window, text="OK", command=help_window.destroy).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = GamePauser(root)
    root.mainloop() 