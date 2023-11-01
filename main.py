import tkinter as tk
from tkinter import messagebox
import glob
import os
import subprocess
import xml.etree.ElementTree as ET

class WiFiPasswordApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wi-Fi Şifre Görüntüleyici")

        self.label_info = tk.Label(root, text="Kayıtlı Wi-Fi Ağları:")
        self.label_info.pack(pady=(10, 0))

        self.listbox_wifi = tk.Listbox(root)
        self.listbox_wifi.pack(pady=(0, 10), padx=10, fill=tk.BOTH, expand=True)

        self.button_show_password = tk.Button(root, text="Şifreyi Göster", command=self.show_password)
        self.button_show_password.pack()

        self.password_var = tk.StringVar()
        self.entry_password = tk.Entry(root, textvariable=self.password_var, state="readonly")
        self.entry_password.pack(pady=(0, 10), padx=10, fill=tk.BOTH, expand=True)

        self.button_copy = tk.Button(root, text="Kopyala", command=self.copy_password)
        self.button_copy.pack()

        self.export_xml(command="netsh wlan export profile interface=wi-fi key=clear folder=passwords")
        self.fill_listbox()

    def export_xml(self, command=None):
        with open("tmp.txt", "w") as tmp:
            export_command = command.split(' ')
            subprocess.run(export_command, stdout=tmp)
        os.remove("tmp.txt")

    def file_path(self) -> list[str]:
        file_paths = glob.glob("passwords/*.xml")
        return file_paths

    def get_ssid_pwd(self) -> dict:
        ssid_pwd = {}
        for i in self.file_path():
            tree = ET.parse(i)
            root = tree.getroot()
            ssid = root[1][0][1].text
            pwd = root[4][0][1][2].text
            ssid_pwd[ssid] = pwd
        return ssid_pwd

    def fill_listbox(self):
        info = self.get_ssid_pwd()
        for ssid in info:
            self.listbox_wifi.insert(tk.END, ssid)

    def show_password(self):
        selected_index = self.listbox_wifi.curselection()
        if not selected_index:
            messagebox.showwarning("Uyarı", "Lütfen bir Wi-Fi ağı seçin.")
            return

        index = selected_index[0]
        selected_wifi = self.listbox_wifi.get(index)
        info = self.get_ssid_pwd()

        if selected_wifi in info:
            password = info[selected_wifi]
            self.password_var.set(password)
        else:
            self.password_var.set("")
            messagebox.showerror("Hata", "Seçilen Wi-Fi ağının şifresi bulunamadı.")

    def copy_password(self):
        password = self.password_var.get()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            self.root.update()
            messagebox.showinfo("Kopyalama", "Şifre kopyalandı.")
        else:
            messagebox.showwarning("Uyarı", "Kopyalanacak bir şifre bulunmuyor.")

if __name__ == '__main__':
    root = tk.Tk()
    app = WiFiPasswordApp(root)
    root.geometry("400x300")
    root.mainloop()
