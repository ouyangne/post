import tkinter as tk
from tkinter import ttk, messagebox
import winreg
import os
import subprocess

# 垃圾软件关键词列表
JUNK_SOFTWARE_KEYWORDS = [
    '360', '金山毒霸', '百度卫士', '腾讯电脑管家', '鲁大师',
    '驱动精灵', '驱动人生', '2345', '好压', '快压',
    '搜狗输入法', '百度输入法', 'QQ输入法', '迅雷', '快车',
    '电驴', '风行', '暴风影音', 'pptv', 'pps',
    '酷我音乐', '酷狗音乐', '千千静听', '爱奇艺', '优酷',
    '土豆', '搜狐视频', '腾讯视频', '新浪视频', '网易视频',
    '屏保', '插件', '工具栏', '搜索框', '助手',
    '优化', '加速', '清理', '修复', '安全',
    'screensaver', 'toolbar', 'plugin', 'search', 'assistant',
    'optimizer', 'booster', 'cleaner', 'fixer', 'security',
    '任务栏', '检索框', '搜索栏', 'searchbar', 'taskbar',
    'toolbar', 'desktop', 'widget', 'gadget', 'sidebar'
]

def get_installed_software():
    """从Windows注册表读取已安装软件"""
    software_list = []
    
    # 注册表路径
    paths = [
        r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall',
        r'SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall'
    ]
    
    for path in paths:
        try:
            # 打开注册表项
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_READ)
            
            # 遍历所有子项
            for i in range(winreg.QueryInfoKey(key)[0]):
                try:
                    subkey_name = winreg.EnumKey(key, i)
                    subkey = winreg.OpenKey(key, subkey_name)
                    
                    # 获取软件名称
                    try:
                        name = winreg.QueryValueEx(subkey, 'DisplayName')[0]
                    except:
                        name = None
                    
                    # 获取卸载命令
                    try:
                        uninstall_string = winreg.QueryValueEx(subkey, 'UninstallString')[0]
                    except:
                        uninstall_string = None
                    
                    # 获取安装位置
                    try:
                        install_location = winreg.QueryValueEx(subkey, 'InstallLocation')[0]
                    except:
                        install_location = None
                    
                    if name:
                        software_list.append({
                            'name': name,
                            'uninstall_string': uninstall_string,
                            'install_location': install_location
                        })
                    
                    subkey.Close()
                except:
                    pass
            
            key.Close()
        except:
            pass
    
    return software_list

def is_junk_software(name):
    """判断是否为垃圾软件"""
    name_lower = name.lower()
    for keyword in JUNK_SOFTWARE_KEYWORDS:
        if keyword.lower() in name_lower:
            return True
    return False

def get_junk_software():
    """获取垃圾软件列表"""
    all_software = get_installed_software()
    # 去重
    seen = set()
    unique_software = []
    for sw in all_software:
        key = sw['name'] + (sw['install_location'] or '')
        if key not in seen:
            seen.add(key)
            unique_software.append(sw)
    # 过滤垃圾软件
    junk_software = [sw for sw in unique_software if is_junk_software(sw['name'])]
    return junk_software

class JunkCleanerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("垃圾软件清理工具")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 创建GUI组件
        self.create_widgets()
        
        # 初始化加载垃圾软件列表
        self.load_junk_software()
    
    def create_widgets(self):
        """创建GUI组件"""
        # 标题
        title_label = ttk.Label(self.root, text="垃圾软件清理工具", font=("微软雅黑", 16, "bold"))
        title_label.pack(pady=10)
        
        # 软件列表框架
        list_frame = ttk.Frame(self.root)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 软件列表
        self.software_tree = ttk.Treeview(list_frame, columns=('name', 'uninstall', 'location'), show='headings', yscrollcommand=scrollbar.set)
        self.software_tree.heading('name', text='软件名称')
        self.software_tree.heading('uninstall', text='卸载程序')
        self.software_tree.heading('location', text='安装位置')
        
        self.software_tree.column('name', width=300)
        self.software_tree.column('uninstall', width=250)
        self.software_tree.column('location', width=200)
        
        self.software_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.software_tree.yview)
        
        # 按钮框架
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 刷新按钮
        refresh_button = ttk.Button(button_frame, text="刷新列表", command=self.load_junk_software)
        refresh_button.pack(side=tk.LEFT, padx=5)
        
        # 卸载按钮
        uninstall_button = ttk.Button(button_frame, text="卸载选中软件", command=self.uninstall_selected)
        uninstall_button.pack(side=tk.LEFT, padx=5)
        
        # 打开目录按钮
        open_dir_button = ttk.Button(button_frame, text="打开安装目录", command=self.open_install_dir)
        open_dir_button.pack(side=tk.LEFT, padx=5)
    
    def load_junk_software(self):
        """加载垃圾软件列表"""
        # 清空现有列表
        for item in self.software_tree.get_children():
            self.software_tree.delete(item)
        
        # 获取垃圾软件列表
        junk_software = get_junk_software()
        
        # 添加到列表
        for software in junk_software:
            uninstall_text = "有" if software['uninstall_string'] else "无"
            location_text = software['install_location'] if software['install_location'] else "未知"
            self.software_tree.insert('', tk.END, values=(software['name'], uninstall_text, location_text), tags=(software['uninstall_string'], software['install_location']))
        
        # 显示统计信息
        messagebox.showinfo("提示", f"共检测到 {len(junk_software)} 个垃圾软件")
    
    def uninstall_selected(self):
        """卸载选中的软件"""
        selected_item = self.software_tree.selection()
        if not selected_item:
            messagebox.showwarning("警告", "请先选择要卸载的软件")
            return
        
        item = selected_item[0]
        software_name = self.software_tree.item(item, 'values')[0]
        uninstall_string = self.software_tree.item(item, 'tags')[0]
        
        if not uninstall_string:
            messagebox.showinfo("提示", f"{software_name} 没有找到卸载程序")
            return
        
        # 确认卸载
        if messagebox.askyesno("确认", f"确定要卸载 {software_name} 吗？"):
            try:
                # 执行卸载程序
                subprocess.run(uninstall_string, shell=True)
                messagebox.showinfo("提示", f"{software_name} 卸载程序已启动")
                # 刷新列表
                self.load_junk_software()
            except Exception as e:
                messagebox.showerror("错误", f"卸载失败: {str(e)}")
    
    def open_install_dir(self):
        """打开选中软件的安装目录"""
        selected_item = self.software_tree.selection()
        if not selected_item:
            messagebox.showwarning("警告", "请先选择要打开目录的软件")
            return
        
        item = selected_item[0]
        software_name = self.software_tree.item(item, 'values')[0]
        install_location = self.software_tree.item(item, 'tags')[1]
        
        if not install_location:
            messagebox.showinfo("提示", f"{software_name} 没有找到安装位置")
            return
        
        # 检查目录是否存在
        if os.path.exists(install_location):
            try:
                # 打开目录
                subprocess.run(['explorer', install_location])
            except Exception as e:
                messagebox.showerror("错误", f"打开目录失败: {str(e)}")
        else:
            messagebox.showinfo("提示", f"{software_name} 的安装目录不存在")

if __name__ == "__main__":
    root = tk.Tk()
    app = JunkCleanerApp(root)
    root.mainloop()