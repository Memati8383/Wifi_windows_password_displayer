import tkinter as tk
from tkinter import Menu, messagebox, filedialog
import subprocess
import webbrowser

def get_wifi_passwords():
    try:
        result = subprocess.check_output(["netsh", "wlan", "show", "profiles"]).decode("utf-8", errors="ignore")
        wifi_profiles = [line.split(":")[1].strip() for line in result.split("\n") if "All User Profile" in line]
        passwords = []

        for profile in wifi_profiles:
            try:
                password = subprocess.check_output(["netsh", "wlan", "show", "profile", profile, "key=clear"]).decode("utf-8", errors="ignore")
                password = [line.split(":")[1].strip() for line in password.split("\n") if "Key Content" in line][0]
                passwords.append((profile, password))
            except subprocess.CalledProcessError:
                passwords.append((profile, "Şifre yok"))

        return passwords
    except Exception as e:
        return str(e)

def show_passwords():
    passwords = get_wifi_passwords()
    text.delete("1.0", tk.END)
    for profile, password in passwords:
        text.insert(tk.END, f"SSID: {profile}\nŞifre: {password}\n\n")

def save_password():
    passwords = get_wifi_passwords()
    if not passwords:
        messagebox.showerror("Hata", "Hiç Wi-Fi şifresi bulunamadı.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])

    if file_path:
        try:
            with open(file_path, "w") as file:
                for ssid, password in passwords:
                    file.write(f"SSID: {ssid}\nŞifre: {password}\n\n")
            messagebox.showinfo("Başarılı", "Wi-Fi şifreleri başarıyla kaydedildi.")
        except Exception as e:
            messagebox.showerror("Hata", f"Kaydetme işlemi sırasında bir hata oluştu:\n{str(e)}")

def set_light_theme():
    text.config(bg="white", fg="black")
    button_show.config(bg="blue", fg="white")
    button_save.config(bg="green", fg="white")
    title_label.config(fg="black", bg="white")
    root.config(bg="white")

def set_dark_theme():
    text.config(bg="black", fg="white")
    button_show.config(bg="gray", fg="black")
    button_save.config(bg="darkgreen", fg="white")
    title_label.config(fg="white", bg="black")
    root.config(bg="black")

def set_red_theme():
    text.config(bg="red", fg="white")
    button_show.config(bg="darkred", fg="white")
    button_save.config(bg="darkred", fg="white")
    title_label.config(fg="white", bg="red")
    root.config(bg="red")

def set_green_theme():
    text.config(bg="green", fg="white")
    button_show.config(bg="darkgreen", fg="white")
    button_save.config(bg="darkgreen", fg="white")
    title_label.config(fg="white", bg="green")
    root.config(bg="green")

def set_gold_theme():
    text.config(bg="gold", fg="black")
    button_show.config(bg="goldenrod", fg="black")
    button_save.config(bg="goldenrod", fg="black")
    title_label.config(fg="black", bg="gold")
    root.config(bg="gold")

def update_theme():
    current_theme = theme_var.get()
    if current_theme == "Açık Tema":
        set_light_theme()
    elif current_theme == "Koyu Tema":
        set_dark_theme()
    elif current_theme == "Kırmızı Tema":
        set_red_theme()
    elif current_theme == "Yeşil Tema":
        set_green_theme()
    elif current_theme == "Altın Tema":
        set_gold_theme()

def about():
    about_window = tk.Toplevel(root)
    about_window.title("Hakkında")

    about_title = tk.Label(about_window, text="Wi-Fi Şifre Görüntüleyici", font=("Helvetica", 18, "bold"))
    about_title.pack(pady=(20, 10))

    about_text = tk.Label(about_window, text="Bu program, kayıtlı Wi-Fi ağlarının şifrelerini görüntülemenizi sağlar. \n"
                                            "Açık Tema, Koyu Tema, Kırmızı Tema, Yeşil Tema ve Altın Tema seçenekleriyle arayüzü özelleştirebilirsiniz", 
                                            padx=20, pady=10, wraplength=400, font=("Helvetica", 12))
    about_text.pack()

    info_frame = tk.Frame(about_window)
    info_frame.pack(pady=(10, 20))

    developer_info = tk.Label(info_frame, text="Geliştirici: Ferit Akdemir", font=("Helvetica", 15))
    developer_info.grid(row=0, column=0, padx=10, pady=(5, 0))

    version_info = tk.Label(info_frame, text="Sürüm: 1.0", font=("Helvetica", 14))
    version_info.grid(row=0, column=1, padx=10, pady=(5, 0))

    website_info = tk.Label(info_frame, text="Web Sitesi: akdemirferit.rf.gd", font=("Helvetica", 14))
    website_info.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

    about_window.geometry("600x300")

def ferit_instagram():
    webbrowser.open("https://instagram.com/ferit22901") 

def luced_instagram():
    webbrowser.open("https://instagram.com/iamluced") 

root = tk.Tk()
root.title("Wi-Fi Şifre Görüntüleyici")

title_label = tk.Label(root, text="Wi-Fi Şifre Görüntüleyici", font=("Helvetica", 16))
title_label.pack(pady=10)

frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

text = tk.Text(frame, width=40, height=10, font=("Courier New", 12))
text.pack()

frame_button = tk.Frame(root)
frame_button.pack(side="bottom", pady=20)

button_show = tk.Button(frame_button, text="Wi-Fi Şifrelerini Göster", command=show_passwords, font=("Helvetica", 12), bg="blue", fg="white")
button_show.pack(side="left", padx=10)

button_save = tk.Button(frame_button, text="Wi-Fi Şifrelerini Kaydet", command=save_password, font=("Helvetica", 12), bg="green", fg="white")
button_save.pack(side="left", padx=10)

menubar = Menu(root)
root.config(menu=menubar)

theme_menu = Menu(menubar, tearoff=0)
theme_var = tk.StringVar()
theme_var.set("Açık Tema")

theme_menu.add_radiobutton(label="Açık Tema", variable=theme_var, command=update_theme)
theme_menu.add_radiobutton(label="Koyu Tema", variable=theme_var, command=update_theme)
theme_menu.add_radiobutton(label="Kırmızı Tema", variable=theme_var, command=update_theme)
theme_menu.add_radiobutton(label="Yeşil Tema", variable=theme_var, command=update_theme)
theme_menu.add_radiobutton(label="Altın Tema", variable=theme_var, command=update_theme)

menubar.add_cascade(label="Tema", menu=theme_menu)

about_menu = Menu(menubar, tearoff=0)
about_menu.add_command(label="Hakkında", command=about)

menubar.add_cascade(label="Hakkında", menu=about_menu)

instagram_menu = Menu(menubar, tearoff=0)
instagram_menu.add_command(label="ferit22901", command=ferit_instagram)
instagram_menu.add_command(label="iamluced", command=luced_instagram)

menubar.add_cascade(label="Instagram", menu=instagram_menu)

menubar.add_command(label="Çıkış", command=root.quit)

root.mainloop()
