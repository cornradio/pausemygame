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

class GamePauser:
    def __init__(self, root):
        self.root = root
        self.root.title("pause my game")
        self.root.geometry("440x380")
        
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
        ttk.Label(self.main_frame, text="Game Pauser", foreground="#78DCDC", font=('Arial', 18, 'bold')).pack(pady=10)
        
        # 创建左右分栏框架
        content_frame = ttk.Frame(self.main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 左侧：程序列表区域
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_frame.configure(width=250)  # 固定宽度
        left_frame.pack_propagate(False)  # 防止子组件改变父组件大小
        
        # 程序列表标题
        ttk.Label(left_frame, text="games", foreground="#ffffff", font=('Arial', 12, 'bold')).pack(pady=(0, 5))
        
        # 创建Listbox
        self.program_listbox = tk.Listbox(left_frame, 
                                         bg='#3c3f41', 
                                         fg='#ffffff', 
                                         selectbackground='#4b6eaf',
                                         selectforeground='#ffffff',
                                         font=('Arial', 11),
                                         height=12)
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
        
        # 使用更大的按钮
        ttk.Button(btn_frame, text="⏸ Pause", command=self.pause_game, width=15).pack(pady=5)
        ttk.Button(btn_frame, text="▶ Resume", command=self.resume_game, width=15).pack(pady=5)
        ttk.Button(btn_frame, text="⏹ Kill", command=self.kill_game, width=15).pack(pady=5)
        
        ttk.Separator(right_frame, orient='horizontal').pack(fill=tk.X, pady=15)
        
        # 配置部分
        config_frame = ttk.Frame(right_frame)
        config_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(config_frame, text="✏️ Edit", command=self.edit_config, width=15).pack(pady=5)
        ttk.Button(config_frame, text="🔄 Reload", command=self.load_config, width=15).pack(pady=5)
        
        self.info_label = ttk.Label(config_frame, text="Game loaded:", foreground="#787878")
        self.info_label.pack(pady=5)
        
        # 初始加载配置
        self.load_config()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Reload Config", command=self.load_config)
        file_menu.add_command(label="Edit Config", command=self.edit_config)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
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
                    return
            
            # 3. 如果没有找到真实图标，使用占位符
            placeholder_img = self.create_placeholder_icon(exe_name)
            if placeholder_img:
                self.icon_photo = ImageTk.PhotoImage(placeholder_img)
                
                # 显示占位符图标
                icon_label = ttk.Label(self.icon_frame, image=self.icon_photo)
                icon_label.pack()
                
                # 添加程序名称标签
                name_label = ttk.Label(self.icon_frame, text=f"{exe_name} (not running)", foreground="#787878", font=('Arial', 10))
                name_label.pack(pady=2)
                
                # 更新状态显示
                self.status_label.config(text=f"○ {exe_name} (未运行)", foreground="#787878")
            else:
                # 4. 如果连占位符都创建失败，显示文本
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

    def open_taskmgr(self):
        self.run_in_subprocess('taskmgr')

    def open_ntop(self):
        self.run_in_subprocess('ntop')

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