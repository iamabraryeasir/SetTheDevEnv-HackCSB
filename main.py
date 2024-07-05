import customtkinter as ctk
import requests
from tkinter import ttk, messagebox
import subprocess

# ***************************** <defining all global variables> *****************************
language = ''
system_name = ''
vscode_windows_url = 'https://vscode.download.prss.microsoft.com/dbazure/download/stable/ea1445cc7016315d0f5728f8e8b12a45dc0a7286/VSCodeUserSetup-x64-1.91.0.exe'
downloaded_file_path = ''

# ***************************** <ctk settings> *****************************

# Setting the theme and color options
ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

# defining the app object for customtkinter
app = ctk.CTk()  # create CTk window like you do with the Tk window
app.geometry("700x400")
app.resizable(False, False)  # to make the window size fixed
app.title("SetDevEnv - Abrar")
app.iconbitmap('')

# Function to create frames
def create_frames(app):
    frames = {}
    frame_names = [
        'welcome_frame', 'language_select_frame', 'os_asker_frame', 'c_windows_frame', 'c_macos_frame', 'c_linux_frame',
        'java_windows_frame', 'java_macos_frame', 'java_linux_frame', 'python_windows_frame', 'python_macos_frame',
        'python_linux_frame', 'others_windows_frame', 'others_macos_frame', 'others_linux_frame', 'download_vscode_for_windows_frame'
    ]
    for name in frame_names:
        frames[name] = ctk.CTkFrame(master=app)
    return frames

# Creating Frames.
frames = create_frames(app)

# ***************************** <defining all methods> *****************************
def decision_maker(language, system_name):  # method to take decision
    # Hide the OS asker frame
    frames['os_asker_frame'].pack_forget()

    # Show the appropriate frame based on the selected language and OS
    frame_key = f'{language}_{system_name}_frame'
    if frame_key in frames:
        frames[frame_key].pack(fill="both", expand=True)

def download_file(url, filename='', progress_callback=None):    # Downloader function
    try:                                # parameters file_url and filename (optional)
        if not filename:
            filename = url[url.rfind('/')+1:]

        global downloaded_file_path
        downloaded_file_path = filename

        # Get the response and the total file size
        with requests.get(url, stream=True) as req:
            total_size = int(req.headers.get('content-length', 0))
            downloaded_size = 0
            chunk_size = 8192
            with open(filename, 'wb') as f:
                for chunk in req.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        if progress_callback:
                            progress_callback(downloaded_size, total_size)
            return filename
    except Exception as e:
        print(e)
        return None

# Progress callback function
def update_progress_bar(progress_bar, percentage_label, current, total):
    progress = (current / total) * 100
    progress_bar['value'] = progress
    percentage_label.configure(text=f'{progress:.2f}%')
    app.update_idletasks()

# Function to run the downloaded file
def install_vscode():
    if downloaded_file_path:
        try:
            subprocess.run([downloaded_file_path], check=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to install VSCode: {e}")

# ***************************** <defining main method> *****************************

def main():

    # ***************************** <defining all frames> *****************************
    frames['welcome_frame'].pack(fill="both", expand=True)

    # ***************************** <welcome frame> *****************************
    def show_language_selector_page():
        frames['language_select_frame'].pack(fill="both", expand=True)
        frames['welcome_frame'].pack_forget()

    window_title = ctk.CTkLabel(master=frames['welcome_frame'], text='Welcome to SetDevEnv!',
                                font=('Poppins Semibold', 30))  # Adding Page Title
    window_title.pack(pady=80)

    my_button = ctk.CTkButton(master=frames['welcome_frame'], text='Get Started', width=200, height=50, corner_radius=7,
                              font=('Poppins', 18), command=show_language_selector_page)  # Adding a Page Button
    my_button.pack()

    # ***************************** <language selector frame> *****************************
    def show_os_selector_page():
        frames['os_asker_frame'].pack(fill="both", expand=True)
        frames['language_select_frame'].pack_forget()

    def c_and_cpp_btn_click():
        global language
        language = 'c'
        show_os_selector_page()

    def java_btn_click():
        global language
        language = 'java'
        show_os_selector_page()

    def python_btn_click():
        global language
        language = 'python'
        show_os_selector_page()

    def others_btn_click():
        global language
        language = 'others'
        show_os_selector_page()

    window_title = ctk.CTkLabel(master=frames['language_select_frame'], text="Select Your Programming Language.",
                                font=('Poppins Semibold', 25))
    window_title.grid(row=0, column=0, columnspan=4, pady=50)

    c_and_cpp_btn = ctk.CTkButton(master=frames['language_select_frame'], text='C/C++', width=140, height=45, corner_radius=7,
                                  font=('Poppins', 17), command=c_and_cpp_btn_click)
    java_btn = ctk.CTkButton(master=frames['language_select_frame'], text='Java', width=140, height=45, corner_radius=7,
                             font=('Poppins', 17), command=java_btn_click)
    python_btn = ctk.CTkButton(master=frames['language_select_frame'], text='Python', width=140, height=45, corner_radius=7,
                               font=('Poppins', 17), command=python_btn_click)
    others_btn = ctk.CTkButton(master=frames['language_select_frame'], text='Others', width=140, height=45, corner_radius=7,
                               font=('Poppins', 17), command=others_btn_click)

    c_and_cpp_btn.grid(row=1, column=1, pady=20)
    java_btn.grid(row=1, column=2, pady=20)
    python_btn.grid(row=2, column=1, pady=20)
    others_btn.grid(row=2, column=2, pady=20)

    frames['language_select_frame'].grid_columnconfigure(0, weight=1)
    frames['language_select_frame'].grid_columnconfigure(1, weight=1)
    frames['language_select_frame'].grid_columnconfigure(2, weight=1)
    frames['language_select_frame'].grid_columnconfigure(3, weight=1)

    # ***************************** <os asker frame> *****************************

    def windows_button_click():
        global system_name
        system_name = 'windows'
        decision_maker(language, system_name)

    def macos_button_click():
        global system_name
        system_name = 'macos'
        decision_maker(language, system_name)

    def linux_button_click():
        global system_name
        system_name = 'linux'
        decision_maker(language, system_name)

    basic_label = ctk.CTkLabel(master=frames['os_asker_frame'], text="What is Your Operating System?",
                               font=('Poppins Semibold', 25))  # Top title text
    basic_label.grid(row=0, column=0, columnspan=3, pady=95)  # Span across 3 columns

    windows_button = ctk.CTkButton(master=frames['os_asker_frame'], text='Windows', width=140, height=45, corner_radius=7,
                                   font=('Poppins', 17), command=windows_button_click)
    macos_button = ctk.CTkButton(master=frames['os_asker_frame'], text='macOS', width=140, height=45, corner_radius=7,
                                 font=('Poppins', 17), command=macos_button_click)
    linux_button = ctk.CTkButton(master=frames['os_asker_frame'], text='Linux', width=140, height=45, corner_radius=7,
                                 font=('Poppins', 17), command=linux_button_click)

    # Arrange buttons side by side using grid
    windows_button.grid(row=1, column=0, sticky="e")
    macos_button.grid(row=1, column=1)
    linux_button.grid(row=1, column=2, sticky="w")

    # Configure grid columns to expand equally
    frames['os_asker_frame'].grid_columnconfigure(0, weight=1)
    frames['os_asker_frame'].grid_columnconfigure(1, weight=1)
    frames['os_asker_frame'].grid_columnconfigure(2, weight=1)

    # ***************************** <c on windows frame> *****************************
    def c_windows_show_instruction_page_1():
        frames['c_windows_frame'].pack_forget()
        frames['download_vscode_for_windows_frame'].pack(fill="both", expand=True)

    c_windows_label = ctk.CTkLabel(master=frames['c_windows_frame'], text="C Language on Windows",
                                   font=('Poppins Semibold', 25))
    c_windows_label.pack(pady=30)
    c_windows_instruction = ctk.CTkLabel(master=frames['c_windows_frame'],
                                         text="Work Need To Be Done: \n1. Install Visual Studio \n2. Download GCC and G++ using MSYS2 \n3. Add GCC and G++ to path. \n4. Install necessary extensions for VSCode. ",
                                         font=('Poppins', 15))
    c_windows_instruction.pack()

    c_windows_btn = ctk.CTkButton(master=frames['c_windows_frame'], text='Next', width=200, height=50, corner_radius=7,
                                  font=('Poppins', 18), command=c_windows_show_instruction_page_1)
    c_windows_btn.pack(pady=40)

    # ***************************** <download vscode for windows frame> *****************************
    download_label = ctk.CTkLabel(master=frames['download_vscode_for_windows_frame'],
                                  text="Download VSCode for Windows",
                                  font=('Poppins Semibold', 25))
    download_label.pack(pady=20)

    progress_bar = ttk.Progressbar(frames['download_vscode_for_windows_frame'], length=300, mode='determinate')
    progress_bar.pack(pady=20)

    percentage_label = ctk.CTkLabel(master=frames['download_vscode_for_windows_frame'], text="0%", font=('Poppins', 14))
    percentage_label.pack()

    def start_download_vscode():
        download_file(vscode_windows_url, progress_callback=lambda cur, tot: update_progress_bar(progress_bar, percentage_label, cur, tot))
        download_button.pack_forget()  # Hide download button
        install_button.pack(pady=20)  # Show install button

    download_button = ctk.CTkButton(master=frames['download_vscode_for_windows_frame'], text='Download VSCode', width=200,
                                    height=50, corner_radius=7, font=('Poppins', 18), command=start_download_vscode)
    download_button.pack(pady=20)

    install_button = ctk.CTkButton(master=frames['download_vscode_for_windows_frame'], text='Install VSCode', width=200,
                                   height=50, corner_radius=7, font=('Poppins', 18), command=install_vscode)
    install_button.pack_forget()

if __name__ == "__main__":
    main()

app.mainloop()
