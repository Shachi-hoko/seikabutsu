import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime

Todolist_json = "Todolist.json"
complete_list = []
undo_list = []

#ウィンドウ処理
root = tk.Tk()
root.title("ToDolist_proto")
root.geometry("350x410")
root.maxsize(1024,768)
root.minsize(300,300)
root.resizable(True,True)

#保存されたTodolist読み込み
def load_todolist():
    try:
        with open(Todolist_json,'r') as file:
            return json.load(file)
    except FileNotFoundError as FNFE:
        print(type(FNFE))
        print("Created json file.")
        return []

#todolistへの保存
def save_todolist(tasks):
    with open(Todolist_json,'w') as file:
        json.dump(tasks,file,indent=2)

#メッセージのみ表示の部分
def show_messagebox():
    result = messagebox.askokcancel("確認", "この操作を実行しますか？")
    if result:
        print("OK が選択されました")
    else:
        print("キャンセルが選択されました")

#タスク追加
def add_task():
    task = entry.get()
    if(task==""):
        messagebox.showwarning("警告", "タスクを入力してください")
        return
    tasks.append({"task": task, "created": str(datetime.now())})
    listbox_update()
    save_todolist(tasks)
    entry.delete(0,tk.END)

#完了タスク処理(未完成)
def complete_task():
    global complete_list
    try:
        selectindex = listbox.curselection()[0]
        remove_task = tasks.pop(selectindex)
        complete_list.append(remove_task)
        print(remove_task)
        #complete_listbox_update()
        save_todolist(tasks)
    except IndexError:
        messagebox.showwarning("警告", "完了するタスクを選択してください")

#タスク削除(消した内容はターミナルに描画)
def delete_task():
    global undo_list
    try:
        selectindex = listbox.curselection()[0]
        remove_task = tasks.pop(selectindex)
        undo_list.append(remove_task)
        print("削除したタスク：",remove_task["task"])
        listbox_update()
        save_todolist(tasks)
    except IndexError:
        messagebox.showwarning("警告", "削除したいタスクを選択してください")

#タスク削除取り消し
def undo_task():
    global undo_list
    try:
        undo_task = undo_list[0]
        tasks.append(undo_task)
        del undo_list[0]
        listbox_update()
        save_todolist(tasks)
    except IndexError:
        messagebox.showwarning("警告", "取り消すタスクがありません")

#タスクリスト内更新
def listbox_update():
    listbox.delete(0,tk.END)
    for t in tasks:
        listbox.insert(tk.END,t["task"])

#完了リスト内更新
#def complete_listbox_update():
#   complete_listbox.delete(0,tk.END)
#    for t in tasks:
#        complete_listbox.insert(tk.END,t["task"])

#ウィンドウ閉じ部分
def close_window():
    root.destroy()


#ウィジェットやイベントの配置

#スケールの横バー設定
#var = tk.IntVar()
#scale = tk.Scale(root,from_=1,to=51,orient=tk.HORIZONTAL,variable=var)
#scale.pack()

#タスク一時保管領域
tasks = load_todolist()

#文字情報
label = tk.Label(root,text="入力タスク")
label.pack()

#文字入力
entry = tk.Entry(root, width=40)
entry.pack(pady=2)

#ボタン配置
button = tk.Button(root, text="メッセージボックスを開く", command=show_messagebox)
button.pack(pady=2)
button_add = tk.Button(root, text="追加", command=add_task)
button_add.pack(pady=2)
#button_complete = tk.Button(root, text="完了", command=complete_task)
#button_complete.pack(pady=2)
button_delete = tk.Button(root, text="削除", command=delete_task)
button_delete.pack(pady=2)
button_undo = tk.Button(root, text="削除取り消し", command=undo_task)
button_undo.pack(pady=2)
button_close = tk.Button(root, text="閉じる", command=close_window)
button_close.place(relx=0.9,rely=0.9,anchor=tk.CENTER)

#格納リスト
label_task = tk.Label(root,text="現在タスク")
label_task.pack()
listbox = tk.Listbox(root, width=50, height=10)
listbox.pack(pady=5)

#label_complete_task = tk.Label(root,text="完了したタスク")
#label_complete_task.pack()
#complete_listbox = tk.Listbox(root, width=50, height=10)
#complete_listbox.pack(pady=5)

#ループ処理
#listbox_update()を書かない場合、一度タスクの追加をしないと、すでに記録されている内容が表示されない
listbox_update()
root.mainloop()