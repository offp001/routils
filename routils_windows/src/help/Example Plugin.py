import tkinter as tk
from tkinter import ttk, filedialog, messagebox


                                                     
PLUGIN_NAME = "Example"

                                                  
PLUGIN_DESCRIPTION = "example plugin showing common routils ui components."


def run(app):

                                                      
    tab = ttk.Frame(app.nb, padding=16)
    app.nb.add(tab, text=PLUGIN_NAME)

                                  
    ttk.Label(
        tab,
        text="Example Plugin",
        font=("Segoe UI Semibold", 18)
    ).pack(anchor="w", pady=(0, 5))

                                                          
    ttk.Label(
        tab,
        text="RoUtils Plugin Components",
        font=("Segoe UI Semibold", 12)
    ).pack(anchor="w", pady=(0, 4))

                                                                  
    ttk.Label(
        tab,
        text=(
            "This is an example RoUtils Python plugin. "
            "It demonstrates text boxes, checkboxes, buttons, "
            "sliders, radio buttons, custom windows, notifications "
            "and file selection."
        ),
        wraplength=700,
        justify="left"
    ).pack(anchor="w", pady=(0, 15))


                                                                         
    text_box = ttk.LabelFrame(
        tab,
        text="Text Box",
        padding=10
    )
    text_box.pack(fill="x", pady=6)

    ttk.Label(
        text_box,
        text="Example Text"
    ).pack(anchor="w")

                                                   
    text_value = tk.StringVar(value="Example")

                                 
    ttk.Entry(
        text_box,
        textvariable=text_value
    ).pack(
        fill="x",
        pady=(6, 0)
    )


                                                     
    checkbox_box = ttk.LabelFrame(
        tab,
        text="Checkbox",
        padding=10
    )
    checkbox_box.pack(fill="x", pady=6)

                                                      
    checkbox_value = tk.BooleanVar(value=False)

                                            
    ttk.Checkbutton(
        checkbox_box,
        text="Enable Example",
        variable=checkbox_value
    ).pack(anchor="w")


                                               
    button_box = ttk.LabelFrame(
        tab,
        text="Button",
        padding=10
    )
    button_box.pack(fill="x", pady=6)

                                                          
    button_status = ttk.Label(
        button_box,
        text="Ready"
    )
    button_status.pack(anchor="w", pady=(0, 7))

                                                   
    def button_clicked():

                                                           
        button_status.configure(
            text="Button clicked!"
        )

                                                 
        try:
            app._console_log(
                "[Example] Button clicked."
            )
        except Exception:
            pass

                        
    ttk.Button(
        button_box,
        text="Click Me",
        command=button_clicked
    ).pack(anchor="w")


                                     
    slider_box = ttk.LabelFrame(
        tab,
        text="Slider",
        padding=10
    )
    slider_box.pack(fill="x", pady=6)

                                            
    slider_value = tk.DoubleVar(value=50)

                                             
    slider_value_label = ttk.Label(
        slider_box,
        text="Value: 50"
    )
    slider_value_label.pack(anchor="w")

                                                   
    def slider_changed(value):

        try:
            value_int = int(float(value))
        except Exception:
            value_int = 0

        slider_value_label.configure(
            text=f"Value: {value_int}"
        )

                                          
    ttk.Scale(
        slider_box,
        from_=0,
        to=100,
        variable=slider_value,
        command=slider_changed
    ).pack(
        fill="x",
        pady=(6, 0)
    )


                                          
    radio_box = ttk.LabelFrame(
        tab,
        text="Radio Buttons",
        padding=10
    )
    radio_box.pack(fill="x", pady=6)

                                                     
    radio_value = tk.StringVar(
        value="Option 1"
    )

                                                                   
    ttk.Radiobutton(
        radio_box,
        text="Option 1",
        value="Option 1",
        variable=radio_value
    ).pack(anchor="w")

    ttk.Radiobutton(
        radio_box,
        text="Option 2",
        value="Option 2",
        variable=radio_value
    ).pack(anchor="w")

    ttk.Radiobutton(
        radio_box,
        text="Option 3",
        value="Option 3",
        variable=radio_value
    ).pack(anchor="w")


                                                             
    choose_box = ttk.LabelFrame(
        tab,
        text="File Chooser",
        padding=10
    )
    choose_box.pack(fill="x", pady=6)

                                                  
    selected_file = tk.StringVar(
        value="No file selected."
    )

    ttk.Label(
        choose_box,
        textvariable=selected_file,
        wraplength=650
    ).pack(
        anchor="w",
        pady=(0, 7)
    )

                                          
    def choose_file():

        path = filedialog.askopenfilename(
            title="Choose a file",
            filetypes=[
                ("All Files", "*.*"),
                ("Python Files", "*.py"),
                ("Text Files", "*.txt"),
                ("JSON Files", "*.json")
            ]
        )

                                                              
        if path:

            selected_file.set(path)

                                                                  
            try:
                app._console_log(
                    f"[Example] Selected file: {path}"
                )
            except Exception:
                pass

                                       
    ttk.Button(
        choose_box,
        text="Choose",
        command=choose_file
    ).pack(anchor="w")


                                                  
    notification_box = ttk.LabelFrame(
        tab,
        text="Notification",
        padding=10
    )
    notification_box.pack(fill="x", pady=6)

                                                       
                                                                
    def send_notification():

        title = "Example"
        text = "This notification was sent by the Example plugin."

        possible_functions = [
            "show_notification",
            "_show_notification",
            "notify",
            "_notify",
            "notification",
            "_notification",
        ]

                                                               
        for function_name in possible_functions:

            function = getattr(
                app,
                function_name,
                None
            )

            if callable(function):

                try:
                    function(
                        title,
                        text
                    )
                    return

                except TypeError:

                    try:
                        function(text)
                        return

                    except Exception:
                        pass

                except Exception:
                    pass

                                                                              
        try:
            messagebox.showinfo(
                title,
                text,
                parent=app
            )
        except Exception:
            messagebox.showinfo(
                title,
                text
            )

                                        
    ttk.Button(
        notification_box,
        text="Send Notification",
        command=send_notification
    ).pack(anchor="w")


                                                     
    window_box = ttk.LabelFrame(
        tab,
        text="Custom Window",
        padding=10
    )
    window_box.pack(fill="x", pady=6)

                                    
    def open_window():

        win = tk.Toplevel(app)

        win.title("Example Window")
        win.geometry("500x300")
        win.resizable(False, False)

                                                                  
        theme_function = globals().get(
            "theme_toplevel"
        )

        if callable(theme_function):

            try:
                theme_function(win)
            except Exception:
                pass

                                     
        ttk.Label(
            win,
            text="Example Window",
            font=("Segoe UI Semibold", 17)
        ).pack(
            pady=(50, 10)
        )

                                                   
        ttk.Label(
            win,
            text="This window was created by the Example plugin."
        ).pack()

                                        
        ttk.Button(
            win,
            text="Close",
            command=win.destroy
        ).pack(
            pady=25
        )

                                         
    ttk.Button(
        window_box,
        text="Open Window",
        command=open_window
    ).pack(anchor="w")


                                                                
    settings_box = ttk.LabelFrame(
        tab,
        text="Settings",
        padding=10
    )
    settings_box.pack(fill="x", pady=6)

                                                                      
    def save_settings():

        try:

            app.settings["example_text"] = text_value.get()

            app.settings["example_checkbox"] = (
                checkbox_value.get()
            )

            app.settings["example_radio"] = (
                radio_value.get()
            )

            app.settings["example_slider"] = (
                slider_value.get()
            )

                                        
            app._save_settings()

            try:
                app._console_log(
                    "[Example] Settings saved."
                )
            except Exception:
                pass

            button_status.configure(
                text="Settings saved!"
            )

        except Exception as e:

            button_status.configure(
                text=f"Settings error: {e}"
            )

                                                   
    def load_settings():

        try:

            text_value.set(
                app.settings.get(
                    "example_text",
                    "Example"
                )
            )

            checkbox_value.set(
                app.settings.get(
                    "example_checkbox",
                    False
                )
            )

            radio_value.set(
                app.settings.get(
                    "example_radio",
                    "Option 1"
                )
            )

            slider_value.set(
                app.settings.get(
                    "example_slider",
                    50
                )
            )

                                                                   
            slider_changed(
                slider_value.get()
            )

        except Exception:
            pass

                                       
    ttk.Button(
        settings_box,
        text="Save Settings",
        command=save_settings
    ).pack(
        side="left",
        padx=(0, 6)
    )

                                                
    ttk.Button(
        settings_box,
        text="Load Settings",
        command=load_settings
    ).pack(
        side="left"
    )

                                               
    load_settings()


                                                           
                                                                        
    def cleanup():

        try:

            if tab.winfo_exists():
                tab.destroy()

        except Exception:
            pass

                                        
    return {
        "cleanup": cleanup
    }
