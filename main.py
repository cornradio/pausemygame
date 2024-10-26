import dearpygui.dearpygui as dpg
import subprocess
from hide import hide_by_exe
import webbrowser #导入webbrowser模块才能打开超链接

dpg.create_context()
dpg.create_viewport(title="pause my game", width=440, height=480)

# 公共函数
def runinsubprocess(thing):
    creation_flags = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP |subprocess.CREATE_BREAKAWAY_FROM_JOB
    subprocess.Popen(thing, shell=True, creationflags=creation_flags,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# 按钮函数
def loadconfig():
    with open('game_name.txt', 'r') as f:
        game_name = f.read().splitlines()
    dpg.configure_item('game_name_exe', items=game_name)
    dpg.set_value('infotext' , 'Game loaded: ' + str(len(game_name)) + ' games')
    # 自动选择 第一个
    if len(game_name) > 0:
        dpg.set_value('game_name_exe', game_name[0])

def editconfig():
    runinsubprocess('notepad game_name.txt')

def pausegame():
    dpg.configure_item('indicator', default_value='Game Paused' , color=(0,0,255))
    game_name = dpg.get_value('game_name_exe')
    hide_by_exe(game_name)
    runinsubprocess('PsSuspend ' + game_name)

def killgame():
    dpg.configure_item('indicator', default_value='Game Killed' , color=(255,0,0))
    game_name = dpg.get_value('game_name_exe')
    runinsubprocess("taskkill /IM "+ game_name + " /F")

def resumegame():
    dpg.configure_item('indicator', default_value='Game Resumed' , color=(0,255,0))
    game_name = dpg.get_value('game_name_exe')
    runinsubprocess('PsSuspend -r ' + game_name)

def opentaskmgr():
    runinsubprocess('taskmgr')

def openntop():
    runinsubprocess('ntop')



# 加载字体
with dpg.font_registry():
    with dpg.font("afont.ttf", 18) as font1:  # 增加中文编码范围，数字是字号,会比官方字体模糊
        # dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Simplified_Common)
        # dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Full)
    dpg.bind_font(font1)





# 窗体主函数 
with dpg.window(label='pauser',tag="pauser",  width=400, height=400,pos=(10, 10)):


    # dpg.add_input_text(default_value='PsSuspend DevilMayCry5.exe' , tag='pause_DevilMayCry5_cmd')
    # dpg.add_input_text(default_value='PsSuspend -r DevilMayCry5.exe ' , tag='remuse_DevilMayCry5_cmd')


    dpg.add_text(default_value='Game Pauser'  , color=(120,220,220)  )
    dpg.add_combo(default_value='' , items=['XXX.exe'], tag='game_name_exe')
    dpg.add_text(default_value='Game Status untouched' , color=(120,120,120) ,tag='indicator')
    dpg.add_button(label='Pause', callback=pausegame);dpg.add_same_line()
    dpg.add_button(label='Resume', callback=resumegame);dpg.add_same_line()
    dpg.add_button(label="kill",callback=killgame)
    dpg.add_spacing(count=3)

    dpg.add_separator()


    dpg.add_text(default_value='Config'  , color=(120,220,120) )
    with dpg.group(horizontal=True):
        dpg.add_button(label='Reload', callback=loadconfig)
        dpg.add_button(label='Edit', callback=editconfig)
        dpg.add_text(tag='infotext', default_value='Game loaded:', color=(120,120,120))
    dpg.add_separator()

    dpg.add_text(default_value='Tools'  , color=(120,220,120) )
    with dpg.group(horizontal=True):
        dpg.add_button(label='Taskmgr', callback=opentaskmgr)
        dpg.add_button(label='Ntop', callback=openntop)

    dpg.add_separator()
    dpg.add_spacing(count=3)
    with dpg.menu(label="Help"):
        dpg.add_menu_item(label="Github",callback=lambda:webbrowser.open("https://github.com/cornradio/pausemygame"))
        dpg.add_menu_item(label="Download Ntop",callback=lambda:webbrowser.open("https://github.com/gsass1/NTop/releases/"))
        dpg.add_menu_item(label="info", callback=lambda: dpg.configure_item("help_pop_up", show=True))
    dpg.add_separator()

# 提示窗口
with dpg.window(label="help_pop_up", modal=True, show=False, tag="help_pop_up", no_title_bar=True):
    dpg.add_text("""1. use Taskmgr ,get your game's name
2. Config - Edit 
3. add your ganme name as new line
4. Config - Reload
5. now you can select your game
6. Pause / Resume 

when you stop your game
the RAM is still being used
but CPU is free now

v2024.10.26
""")
    dpg.add_separator()
    dpg.add_button(label="OK", width=75, callback=lambda: dpg.configure_item("help_pop_up", show=False))

    # dpg.show_documentation()
# onload 事件
loadconfig()

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("pauser", True) # 使用这个可以让整个窗体变成一个窗体
dpg.start_dearpygui()
dpg.destroy_context()