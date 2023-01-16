# bilibili@轻松学Python > Python爬虫实战项目教程 > 案例一、VIP视频解析软件
# 打开腾讯视频，点击某个会员影片，拷贝url，填写在工具的'play address:'栏，上面的port点选port2.
# https://www.wannengjiexi.com/
# 20230111

import tkinter as tk
import requests
import re
import webbrowser

def show():
    # choose the port and txt
    num = num_int_var.get()
    txt = input_var.get()
    print ('num = ', num)
    print ('text = ', txt)
    link = 'https://www.wannengjiexi.com/jiexi' + str(num) + '/?url=' + txt
    print ('link = ', link)
    html_data = requests.get(url=link).text
    video_url = re.findall('<iframe id="baiyug" scrolling="no" src="(.*?)"', html_data)[0]
    webbrowser.open(video_url)

# Create a window
root = tk.Tk()

root.geometry('800x300+200+200')       # not 800*300
root.title('Online movie')

# img = tk.PhotoImage(file='')
# tk.Label(root, image = img).pack()

# choose field
choose_frame = tk.LabelFrame(root)
choose_frame.pack(pady=10, fill='both')

tk.Label(choose_frame, text='port:', font=('calibri', 20)).pack(side=tk.LEFT)

num_int_var = tk.IntVar()
num_int_var.set(2)

tk.Radiobutton(choose_frame, text='port1', variable=num_int_var, value=1).pack(side=tk.LEFT, padx=5)
tk.Radiobutton(choose_frame, text='port2', variable=num_int_var, value=2).pack(side=tk.LEFT, padx=5)
tk.Radiobutton(choose_frame, text='port3', variable=num_int_var, value=3).pack(side=tk.LEFT)

# input field
input_frame = tk.LabelFrame(root)
input_frame.pack(pady=10, fill='both')

input_var = tk.StringVar()

tk.Label(input_frame, text='play address:', font=('calibri', 20)).pack(side=tk.LEFT)
tk.Entry(input_frame, width=100, relief='flat', textvariable=input_var).pack(side=tk.LEFT, fill='both')

# button
tk.Button(root, text='play', font=('calibri', 20), relief='flat', bg='#440000', command=show).pack(fill='both')

# Keep the window maintain
root.mainloop()

