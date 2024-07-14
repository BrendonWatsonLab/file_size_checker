import os
import smtplib
import time
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def read_folder_paths(filename):
    try:
        with open(filename, "r") as file:
            return file.read().split('\n')
    except FileNotFoundError:
        return []

def write_folder_paths(paths,filename):
    with open(filename, "w") as file:
        for path in paths:
            file.write(path + '\n')

def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.exists(filepath):
                total_size += os.path.getsize(filepath)
    return total_size

def send_email(receiver_email, subject, body, sender_email='57283dprinter@gmail.com'):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    msg = MIMEMultipart()
    msg['From'] = "File Checker"
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, "lnad yzgo xbip czub")
        server.sendmail(sender_email, receiver_email, msg.as_string())

def monitor_folders(folders, receiver_email, wait_time):
    sizes = {folder: get_folder_size(folder) for folder in folders}
    print("Started Monitoring")
    while True:
        time.sleep(wait_time)
        unchanged_folders = []
        for folder, initial_size in sizes.items():
            current_size = get_folder_size(folder)
            if current_size <= initial_size:
                unchanged_folders.append(folder)
            sizes[folder] = current_size

        if unchanged_folders:
            subject = 'Folder Size Unchanged'
            body = f"The following folder(s) have not changed in size:\n\n" \
                   f"{', '.join(unchanged_folders)}\n\n" \
                   "Please check on them.\n\n" \
                   "Yours Sincerely,\nKhan Bot"
            send_email(receiver_email, subject, body)

# GUI for input
filename = ""
def launch_gui():
    
    def on_start():
        global filename
        if not filename:
            messagebox.showerror("Empty", "Please select the addresses file.")
            return
        email = email_entry.get()
        if not email:
            messagebox.showerror("Empty", "Please enter the receiver's email.")
            return

        folder_paths = folders_text.get("1.0", tk.END).strip().split('\n')
        folders = [path.strip() for path in folder_paths if path.strip()]
        try:
            wait_time = float(wait_time_entry.get())*60
        except:
            messagebox.showerror("Error", "Enter valid wait time.")
            return


        if not folders:
            messagebox.showerror("Empty", "Please enter at least one folder path.")
            return

        write_folder_paths(folders,filename)  # Save the folder paths back to the file
        root.destroy()  # Close the GUI
        monitor_folders(folders, email, wait_time) 

    def browse_file():
        global filename
        filename = filedialog.askopenfilename(title="Select Address File", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if filename:
            folder_paths = read_folder_paths(filename)
            folders_text.delete('1.0', tk.END)  # Clear existing text
            folders_text.insert(tk.INSERT, '\n'.join(folder_paths))
            #messagebox.showinfo("File Selected", f"Address file selected: {filename}")
    root = tk.Tk()
    root.title("Folder Monitor")

    tk.Label(root, text="Receiver's Email:", padx=10, pady=5).pack()
    email_entry = tk.Entry(root, width=50)
    email_entry.pack(padx=10, pady=5)

    tk.Label(root, text="Wait Time (in minutes):", padx=10, pady=5).pack()
    wait_time_entry = tk.Entry(root, width=20)
    wait_time_entry.pack(padx=10, pady=5)
    wait_time_entry.insert(tk.INSERT,5)
    tk.Button(root, text="Browse Address File", command=browse_file, padx=10, pady=5).pack(padx=10, pady=5)
    tk.Label(root, text="Folders to Monitor :", padx=10, pady=5).pack()
    folders_text = scrolledtext.ScrolledText(root, height=10, width=50)
    folders_text.pack(padx=10, pady=5)
    #folders_text.insert(tk.INSERT, "C:/Users/mujta/Videos;C:/Users/mujta/OneDrive/Pictures")
    

    tk.Button(root, text="Start Monitoring", command=on_start, padx=10, pady=5).pack(padx=10, pady=10)

    root.mainloop()

launch_gui()
