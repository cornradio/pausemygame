import dearpygui.dearpygui as dpg
import subprocess

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
    dpg.configure_item('indicator', default_value='Game Paused' , color=(255,0,0))
    game_name = dpg.get_value('game_name_exe')
    runinsubprocess('PsSuspend ' + game_name)

def resumegame():
    dpg.configure_item('indicator', default_value='Game Resumed' , color=(0,255,0))
    game_name = dpg.get_value('game_name_exe')
    runinsubprocess('PsSuspend -r ' + game_name)

def opentaskmgr():
    runinsubprocess('taskmgr')

# 加载字体
with dpg.font_registry():
    with dpg.font("afont.ttf", 18) as font1:  # 增加中文编码范围，数字是字号,会比官方字体模糊
        # dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Simplified_Common)
        # dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Full)
    dpg.bind_font(font1)

# 窗体主函数
with dpg.window(label='pauser',  width=400, height=400,pos=(10, 10)):
    # dpg.add_input_text(default_value='PsSuspend DevilMayCry5.exe' , tag='pause_DevilMayCry5_cmd')
    # dpg.add_input_text(default_value='PsSuspend -r DevilMayCry5.exe ' , tag='remuse_DevilMayCry5_cmd')

    dpg.add_combo(default_value='' , items=['XXX.exe'], tag='game_name_exe')
    dpg.add_text(default_value='Game Status untouched' , color=(120,120,120) ,tag='indicator')
    dpg.add_spacing(count=3)

    dpg.add_button(label='Pause', callback=pausegame);dpg.add_same_line()
    dpg.add_button(label='Resume', callback=resumegame);dpg.add_same_line()
    dpg.add_button(label='Taskmgr', callback=opentaskmgr)
    dpg.add_spacing(count=3)
    dpg.add_separator()
    dpg.add_spacing(count=3)

    dpg.add_button(label='reload config', callback=loadconfig);dpg.add_same_line()
    dpg.add_button(label='edit config', callback=editconfig)
    dpg.add_text(tag='infotext', default_value='Game loaded:', color=(120,120,120))
    # dpg.show_documentation()
# onload 事件
loadconfig()

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()