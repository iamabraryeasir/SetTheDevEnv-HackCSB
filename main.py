import os
import threading
import pyperclip
import customtkinter as ctk
import requests
from tkinter import ttk, messagebox
import subprocess

# ***************************** <defining all global variables> *****************************
language = ''
system_name = ''
vscode_windows_url = 'https://vscode.download.prss.microsoft.com/dbazure/download/stable/ea1445cc7016315d0f5728f8e8b12a45dc0a7286/VSCodeUserSetup-x64-1.91.0.exe'
msys2_windows_url = 'https://github.com/msys2/msys2-installer/releases/download/2024-01-13/msys2-x86_64-20240113.exe'
path_to_add_to_environment_variable = r"C:\msys64\ucrt64\bin"
extension_list = ["ms-vscode.cpptools", "formulahendry.code-runner", "sumitsaha.learn-with-sumit-theme"]
downloaded_file_path = ''

# ***************************** <ctk settings> *****************************

# Setting the theme and color options
ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

# defining the app object for customtkinter
app = ctk.CTk()  # create CTk window like you do with the Tk window
app.geometry("700x550")
app.resizable(False, False)  # to make the window size fixed
app.title("SetTheDevEnv - Abrar Yeasir")
app.iconbitmap('')


# Function to create frames
def create_frames(app):
    frames = {}
    frame_names = [
        'welcome_frame', 'language_select_frame', 'os_asker_frame', 'c_windows_frame', 'coming_soon_frame',
        'download_vscode_for_windows_frame',
        'download_msys2_for_windows_frame', 'install_mingw64_frame', 'add_to_path_and_install_extensions_frame',
        'coming_soon_os_frame'
    ]
    for name in frame_names:
        frames[name] = ctk.CTkFrame(master=app)
    return frames


# Creating Frames.
frames = create_frames(app)
install_mingw64_frame = ctk.CTkFrame(master=frames['install_mingw64_frame'], fg_color='transparent')


# ***************************** <defining all methods> *****************************
def decision_maker(language, system_name):  # method to take decision
    # Hide the OS asker frame
    frames['os_asker_frame'].pack_forget()

    # Show the appropriate frame based on the selected language and OS
    frame_key = f'{language}_{system_name}_frame'
    if frame_key in frames:
        frames[frame_key].pack(fill="both", expand=True)


def download_file(url, filename='', progress_callback=None):  # Downloader function
    try:  # parameters file_url and filename (optional)
        if not filename:
            filename = url[url.rfind('/') + 1:]

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
            install_button.configure(text='Next', command=show_download_msys2_page)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to install VSCode: {e}")


# Function to show the MSYS2 download page
def show_download_msys2_page():
    frames['download_vscode_for_windows_frame'].pack_forget()
    frames['download_msys2_for_windows_frame'].pack(fill="both", expand=True)


def install_msys2():
    def show_install_mingw64_frame():
        frames['install_mingw64_frame'].pack(fill="both", expand=True)
        frames['download_msys2_for_windows_frame'].pack_forget()

    if downloaded_file_path:
        subprocess.run([downloaded_file_path])
        msys2_install_button.configure(text='Goto Next Step', command=show_install_mingw64_frame)


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

    def show_coming_soon_frame():
        for frame in frames:
            frames[frame].pack_forget()
        frames['coming_soon_frame'].pack(fill="both", expand=True)

    window_title = ctk.CTkLabel(master=frames['language_select_frame'], text="Select Your Programming Language.",
                                font=('Poppins Semibold', 25))
    window_title.grid(row=0, column=0, columnspan=4, pady=50)

    c_and_cpp_btn = ctk.CTkButton(master=frames['language_select_frame'], text='C/C++', width=140, height=45,
                                  corner_radius=7,
                                  font=('Poppins', 17), command=c_and_cpp_btn_click)
    java_btn = ctk.CTkButton(master=frames['language_select_frame'], text='Java', width=140, height=45, corner_radius=7,
                             font=('Poppins', 17), command=show_coming_soon_frame)
    python_btn = ctk.CTkButton(master=frames['language_select_frame'], text='Python', width=140, height=45,
                               corner_radius=7,
                               font=('Poppins', 17), command=show_coming_soon_frame)
    others_btn = ctk.CTkButton(master=frames['language_select_frame'], text='Others', width=140, height=45,
                               corner_radius=7,
                               font=('Poppins', 17), command=show_coming_soon_frame)

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

    # def macos_button_click():
    #     global system_name
    #     system_name = 'macos'
    #     decision_maker(language, system_name)
    #
    # def linux_button_click():
    #     global system_name
    #     system_name = 'linux'
    #     decision_maker(language, system_name)
    def show_coming_soon_os_frame():
        for frame in frames:
            frames[frame].pack_forget()
        frames['coming_soon_os_frame'].pack(fill="both", expand=True)

    basic_label = ctk.CTkLabel(master=frames['os_asker_frame'], text="What is Your Operating System?",
                               font=('Poppins Semibold', 25))  # Top title text
    basic_label.grid(row=0, column=0, columnspan=3, pady=95)  # Span across 3 columns

    windows_button = ctk.CTkButton(master=frames['os_asker_frame'], text='Windows', width=140, height=45,
                                   corner_radius=7,
                                   font=('Poppins', 17), command=windows_button_click)
    macos_button = ctk.CTkButton(master=frames['os_asker_frame'], text='macOS', width=140, height=45, corner_radius=7,
                                 font=('Poppins', 17), command=show_coming_soon_os_frame)
    linux_button = ctk.CTkButton(master=frames['os_asker_frame'], text='Linux', width=140, height=45, corner_radius=7,
                                 font=('Poppins', 17), command=show_coming_soon_os_frame)

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
        download_button.configure(state="disabled")
        download_file(vscode_windows_url,
                      progress_callback=lambda cur, tot: update_progress_bar(progress_bar, percentage_label, cur, tot))
        download_button.configure(state="normal")
        download_button.pack_forget()  # Hide download button
        install_button.pack(pady=20)  # Show install button

    global install_button
    install_button = ctk.CTkButton(master=frames['download_vscode_for_windows_frame'], text='Install VSCode', width=200,
                                   height=50, corner_radius=7, font=('Poppins', 18), command=install_vscode)
    install_button.pack_forget()

    download_button = ctk.CTkButton(master=frames['download_vscode_for_windows_frame'], text='Download VSCode',
                                    width=200,
                                    height=50, corner_radius=7, font=('Poppins', 18), command=start_download_vscode)
    download_button.pack(pady=20)

    # ***************************** <download msys2 for windows frame> *****************************
    download_label = ctk.CTkLabel(master=frames['download_msys2_for_windows_frame'],
                                  text="Download MSYS2 for Windows",
                                  font=('Poppins Semibold', 25))
    download_label.pack(pady=20)

    # Function to download MSYS2
    def download_msys2():
        msys2_download_button.configure(state="disabled")
        download_file(msys2_windows_url,
                      progress_callback=lambda cur, tot: update_progress_bar(msys2_progress_bar, msys2_percentage_label,
                                                                             cur, tot))
        msys2_download_button.configure(state="normal")
        msys2_download_button.pack_forget()
        msys2_install_button.pack(pady=20)

    global msys2_progress_bar, msys2_percentage_label, msys2_download_button, msys2_install_button

    msys2_progress_bar = ttk.Progressbar(frames['download_msys2_for_windows_frame'], length=300, mode='determinate')
    msys2_progress_bar.pack(pady=20)

    msys2_percentage_label = ctk.CTkLabel(master=frames['download_msys2_for_windows_frame'], text="0%",
                                          font=('Poppins', 14))
    msys2_percentage_label.pack()

    msys2_download_button = ctk.CTkButton(master=frames['download_msys2_for_windows_frame'], text='Download MSYS2',
                                          width=200,
                                          height=50, corner_radius=7, font=('Poppins', 18), command=download_msys2)
    msys2_download_button.pack(pady=20)

    msys2_install_button = ctk.CTkButton(master=frames['download_msys2_for_windows_frame'], text='Install MSYS2',
                                         width=200,
                                         height=50, corner_radius=7, font=('Poppins', 18), command=install_msys2)
    msys2_install_button.pack_forget()

    # ***************************** <install mingw64 frame> *****************************
    def copy_command():
        command = "pacman -S --needed base-devel mingw-w64-ucrt-x86_64-toolchain"
        pyperclip.copy(command)

    def activate_button():
        run_msys2_terminal.configure(text="Goto Next Step", state="normal")

    # Function to switch to add_to_path_and_install_extensions_frame
    def run_terminal():
        def switch_frame():
            for frame in frames.values():
                frame.pack_forget()
            frames['add_to_path_and_install_extensions_frame'].pack(fill="both", expand=True)

        if run_msys2_terminal.cget("text") == "Run Terminal":
            subprocess.run(['C:\\msys64\\ucrt64.exe'])
            run_msys2_terminal.configure(state="disabled")
            threading.Timer(10, activate_button).start()
        elif run_msys2_terminal.cget("text") == "Goto Next Step":
            switch_frame()

    install_mingw64_label = ctk.CTkLabel(master=install_mingw64_frame,
                                         text="Run the Following Command on Run The Terminal",
                                         font=('Poppins Semibold', 20))
    install_mingw64_label.pack(pady=25)

    copy_command_label = ctk.CTkLabel(master=install_mingw64_frame,
                                      text="1. Copy the command by clicking on the copy command button.",
                                      font=('Poppins', 15))
    copy_command_label.pack()

    command_copy_button = ctk.CTkButton(master=install_mingw64_frame, text="Copy Command", width=200,
                                        height=50, corner_radius=7, font=('Poppins', 18), command=copy_command)
    command_copy_button.pack(pady=20)

    run_terminal_label = ctk.CTkLabel(master=install_mingw64_frame,
                                      text="2. Hit the run terminal button and paste the command \nand hit enter 2 times when asked",
                                      font=('Poppins', 15))
    run_terminal_label.pack()

    run_msys2_terminal = ctk.CTkButton(master=install_mingw64_frame, text="Run Terminal", width=200,
                                       height=50, corner_radius=7, font=('Poppins', 18), command=run_terminal)
    run_msys2_terminal.pack(pady=20)

    install_mingw64_frame.pack(pady=20)

    # ***************************** <add to path and install extensions frame> *****************************
    def add_to_user_path(new_path, add_to_path_btn):
        # Retrieve the current PATH
        current_path = os.environ.get('PATH')

        # Check if the new_path is already in the PATH
        if new_path in current_path:
            add_to_path_btn.configure(text="Path is There", state="normal")
            return

        # Add the new_path to the PATH
        updated_path = current_path + os.pathsep + new_path

        # Set the updated PATH for the current process
        os.environ['PATH'] = updated_path

        # Update the user PATH environment variable permanently
        subprocess.run(
            ['setx', 'PATH', updated_path],
            shell=True,
            check=True
        )
        add_to_path_btn.configure(text="Path Added", state="normal")

    def extension_update_progress(current, total):
        progress = (current / total) * 100
        extension_progress_bar['value'] = progress
        extension_percentage_label.configure(text=f'{progress:.2f}%')
        app.update_idletasks()

    # Extension Installation Process
    def install_extension(ext, label):
        try:
            user_profile = os.environ.get("USERPROFILE")
            code_path = os.path.join(user_profile, "AppData", "Local", "Programs", "Microsoft VS Code", "bin",
                                     "code.cmd")
            result = subprocess.run([code_path, "--install-extension", ext], check=True, capture_output=True, text=True)
            if result.returncode == 0:
                label.configure(text=ext + " ✅")
            else:
                label.configure(text=ext + " ❌")
        except subprocess.CalledProcessError as e:
            label.configure(text=ext + " ❌")
        except FileNotFoundError:
            label.configure(text=ext + " ❌ (code.cmd not found)")

    def install_extensions():
        total = len(extension_list)
        for i, ext in enumerate(extension_list):
            install_extension(ext, extension_labels[i])
            extension_update_progress(i + 1, total)
        install_button.configure(state="normal")

    def start_installation():
        install_button.configure(state="disabled")
        threading.Thread(target=install_extensions).start()

    page_label = ctk.CTkLabel(master=frames['add_to_path_and_install_extensions_frame'],
                              text="Let's do the next things",
                              font=('Poppins', 25))
    page_label.pack(pady=20)
    page_label_2 = ctk.CTkLabel(master=frames['add_to_path_and_install_extensions_frame'],
                                text="1. Click the following button to the path.",
                                font=('Poppins', 15))
    page_label_2.pack(pady=15)

    global add_to_path_btn
    add_to_path_btn = ctk.CTkButton(master=frames['add_to_path_and_install_extensions_frame'], text="Add To Path",
                                    width=200, height=50,
                                    corner_radius=7, font=('Poppins', 18),
                                    command=lambda: add_to_user_path(path_to_add_to_environment_variable,
                                                                     add_to_path_btn))
    add_to_path_btn.pack(pady=15)

    # Create a label for each extension
    extension_labels = []
    for ext in extension_list:
        label = ctk.CTkLabel(master=frames['add_to_path_and_install_extensions_frame'], text=ext, font=('Poppins', 14))
        label.pack(pady=5)
        extension_labels.append(label)

    # Extension installation progress bar and percentage label
    extension_progress_bar = ttk.Progressbar(frames['add_to_path_and_install_extensions_frame'], length=400,
                                             mode='determinate')
    extension_progress_bar.pack(pady=20)

    extension_percentage_label = ctk.CTkLabel(master=frames['add_to_path_and_install_extensions_frame'], text="0%",
                                              font=('Poppins', 14))
    extension_percentage_label.pack()

    vsocde_extension_install_button = ctk.CTkButton(master=frames['add_to_path_and_install_extensions_frame'],
                                                    text="Install Extensions", width=200, height=50,
                                                    corner_radius=7, font=('Poppins', 18), command=start_installation)
    vsocde_extension_install_button.pack(pady=20)

    # Return Back Frame
    def return_back():
        for frame in frames.values():
            frame.pack_forget()
        frames['language_select_frame'].pack(fill="both", expand=True)

    coming_soon_label = ctk.CTkLabel(master=frames['coming_soon_frame'], text="Coming Soon",
                                     font=('Poppins Semibold', 25))
    coming_soon_label.pack(pady=50)

    return_button = ctk.CTkButton(master=frames['coming_soon_frame'], text='Return Back', width=180, height=45,
                                  corner_radius=7,
                                  font=('Poppins', 17), command=return_back)
    return_button.pack(pady=20)

    # Return Back Frame Language
    def return_back_os():
        for frame in frames.values():
            frame.pack_forget()
        frames['os_asker_frame'].pack(fill="both", expand=True)

    coming_soon_label = ctk.CTkLabel(master=frames['coming_soon_os_frame'], text="Coming Soon",
                                     font=('Poppins Semibold', 25))
    coming_soon_label.pack(pady=50)

    return_button = ctk.CTkButton(master=frames['coming_soon_os_frame'], text='Return Back', width=180, height=45,
                                  corner_radius=7,
                                  font=('Poppins', 17), command=return_back_os)
    return_button.pack(pady=20)


if __name__ == "__main__":
    main()

app.mainloop()
