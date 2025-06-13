import tkinter as tk
from tkinter import ttk
import subprocess
from hide import hide_by_exe
import webbrowser
import os

class GamePauser:
    def __init__(self, root):
        self.root = root
        self.root.title("pause my game")
        self.root.geometry("440x230")
        
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
        
        # 游戏选择部分
        ttk.Label(self.main_frame, text="Game Pauser", foreground="#78DCDC", font=('Arial', 18, 'bold')).pack(pady=10)
        
        self.game_var = tk.StringVar()
        self.game_combo = ttk.Combobox(self.main_frame, textvariable=self.game_var, height=5 ,font=('Arial', 13))
        self.game_combo.pack(fill=tk.X, pady=5, padx=20)
        
        self.status_label = ttk.Label(self.main_frame, text="Game Status untouched", foreground="#787878", font=('Arial', 10))
        self.status_label.pack(pady=5)
        
        # 主要控制按钮框架
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(fill=tk.X, pady=15)
        
        # 使用更大的按钮
        ttk.Button(btn_frame, text="⏸ Pause", command=self.pause_game, width=15).pack(side=tk.LEFT, padx=10, expand=True)
        ttk.Button(btn_frame, text="▶ Resume", command=self.resume_game, width=15).pack(side=tk.LEFT, padx=10, expand=True)
        ttk.Button(btn_frame, text="⏹ Kill", command=self.kill_game, width=15).pack(side=tk.LEFT, padx=10, expand=True)
        
        ttk.Separator(self.main_frame, orient='horizontal').pack(fill=tk.X, pady=15)
        
        # 配置部分
        config_frame = ttk.Frame(self.main_frame)
        config_frame.pack(fill=tk.X, pady=5)
        
        
        ttk.Button(config_frame, text="✏️ Edit", command=self.edit_config, width=15).pack(side=tk.LEFT, padx=10, expand=True)
        ttk.Button(config_frame, text="🔄 Reload", command=self.load_config, width=15).pack(side=tk.LEFT, padx=10, expand=True)
        
        self.info_label = ttk.Label(config_frame, text="Game loaded:", foreground="#787878")
        self.info_label.pack(side=tk.LEFT, padx=10, expand=True)
        
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
            self.game_combo['values'] = game_names
            if game_names:
                self.game_var.set(game_names[0])
            self.info_label.config(text=f'Game loaded: {len(game_names)} ')
        except FileNotFoundError:
            self.info_label.config(text='No game_name.txt found')

    def edit_config(self):
        self.run_in_subprocess('notepad game_name.txt')

    def pause_game(self):
        self.status_label.config(text="Game Paused", foreground="#FF00FF")
        game_name = self.game_var.get()
        hide_by_exe(game_name)
        self.run_in_subprocess(f'PsSuspend "{game_name}"')

    def kill_game(self):
        self.status_label.config(text="Game Killed", foreground="#FF0000")
        game_name = self.game_var.get()
        self.run_in_subprocess(f'taskkill /IM "{game_name}" /F')

    def resume_game(self):
        self.status_label.config(text="Game Resumed", foreground="#00FF00")
        game_name = self.game_var.get()
        self.run_in_subprocess(f'PsSuspend -r "{game_name}"')

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

v2024.10.26"""
        
        ttk.Label(help_window, text=help_text, wraplength=350, foreground='#ffffff').pack(padx=20, pady=20)
        ttk.Button(help_window, text="OK", command=help_window.destroy).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = GamePauser(root)
    root.mainloop() 