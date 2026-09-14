import tkinter as tk
from tkinter import ttk, filedialog, messagebox


# the name that will appear for the plugin in routils
PLUGIN_NAME = "Example"

# a short description shown in the plugins section
PLUGIN_DESCRIPTION = "example plugin showing common routils ui components."


def run(app):

    # creates a new tab inside the main routils window
    tab = ttk.Frame(app.nb, padding=16)
    app.nb.add(tab, text=PLUGIN_NAME)

    # the main title of the plugin
    ttk.Label(
        tab,
        text="Example Plugin",
        font=("Segoe UI Semibold", 18)
    ).pack(anchor="w", pady=(0, 5))

    # a smaller title that can be used for another section
    ttk.Label(
        tab,
        text="RoUtils Plugin Components",
        font=("Segoe UI Semibold", 12)
    ).pack(anchor="w", pady=(0, 4))

    # a short description explaining what this example plugin does
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


    # creates a section with a text box where the user can type something
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

    # keeps track of whatever text the user entered
    text_value = tk.StringVar(value="Example")

    # this is the actual text box
    ttk.Entry(
        text_box,
        textvariable=text_value
    ).pack(
        fill="x",
        pady=(6, 0)
    )


    # creates a section with a normal on/off checkbox
    checkbox_box = ttk.LabelFrame(
        tab,
        text="Checkbox",
        padding=10
    )
    checkbox_box.pack(fill="x", pady=6)

    # stores whether the checkbox is currently enabled
    checkbox_value = tk.BooleanVar(value=False)

    # creates the checkbox the user can tick
    ttk.Checkbutton(
        checkbox_box,
        text="Enable Example",
        variable=checkbox_value
    ).pack(anchor="w")


    # creates a section with a clickable button
    button_box = ttk.LabelFrame(
        tab,
        text="Button",
        padding=10
    )
    button_box.pack(fill="x", pady=6)

    # shows a small status message when the button is used
    button_status = ttk.Label(
        button_box,
        text="Ready"
    )
    button_status.pack(anchor="w", pady=(0, 7))

    # this function runs when the button is clicked
    def button_clicked():

        # changes the status text after clicking the button
        button_status.configure(
            text="Button clicked!"
        )

        # writes a message to the routils console
        try:
            app._console_log(
                "[Example] Button clicked."
            )
        except Exception:
            pass

    # creates the button
    ttk.Button(
        button_box,
        text="Click Me",
        command=button_clicked
    ).pack(anchor="w")


    # creates a section with a slider
    slider_box = ttk.LabelFrame(
        tab,
        text="Slider",
        padding=10
    )
    slider_box.pack(fill="x", pady=6)

    # stores the current value of the slider
    slider_value = tk.DoubleVar(value=50)

    # shows the current slider value above it
    slider_value_label = ttk.Label(
        slider_box,
        text="Value: 50"
    )
    slider_value_label.pack(anchor="w")

    # updates the text whenever the slider is moved
    def slider_changed(value):

        try:
            value_int = int(float(value))
        except Exception:
            value_int = 0

        slider_value_label.configure(
            text=f"Value: {value_int}"
        )

    # creates a slider going from 0 to 100
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


    # creates a section with radio buttons
    radio_box = ttk.LabelFrame(
        tab,
        text="Radio Buttons",
        padding=10
    )
    radio_box.pack(fill="x", pady=6)

    # stores which radio button is currently selected
    radio_value = tk.StringVar(
        value="Option 1"
    )

    # only one radio button using the same variable can be selected
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


    # creates a section for choosing a file from the computer
    choose_box = ttk.LabelFrame(
        tab,
        text="File Chooser",
        padding=10
    )
    choose_box.pack(fill="x", pady=6)

    # shows the path of the file that was selected
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

    # opens the normal windows file picker
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

        # only do something if the user actually picked a file
        if path:

            selected_file.set(path)

            # prints the selected file path in the routils console
            try:
                app._console_log(
                    f"[Example] Selected file: {path}"
                )
            except Exception:
                pass

    # button that opens the file picker
    ttk.Button(
        choose_box,
        text="Choose",
        command=choose_file
    ).pack(anchor="w")


    # creates a section for showing a notification
    notification_box = ttk.LabelFrame(
        tab,
        text="Notification",
        padding=10
    )
    notification_box.pack(fill="x", pady=6)

    # tries to use a notification function from routils
    # if none is available, it uses a normal message box instead
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

        # checks the possible notification functions one by one
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

        # fallback if the current routils version has no notification function
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

    # button that sends the notification
    ttk.Button(
        notification_box,
        text="Send Notification",
        command=send_notification
    ).pack(anchor="w")


    # creates a section for opening a separate window
    window_box = ttk.LabelFrame(
        tab,
        text="Custom Window",
        padding=10
    )
    window_box.pack(fill="x", pady=6)

    # opens a new window when called
    def open_window():

        win = tk.Toplevel(app)

        win.title("Example Window")
        win.geometry("500x300")
        win.resizable(False, False)

        # tries to use the routils window theme if it is available
        theme_function = globals().get(
            "theme_toplevel"
        )

        if callable(theme_function):

            try:
                theme_function(win)
            except Exception:
                pass

        # title inside the new window
        ttk.Label(
            win,
            text="Example Window",
            font=("Segoe UI Semibold", 17)
        ).pack(
            pady=(50, 10)
        )

        # a short description inside the new window
        ttk.Label(
            win,
            text="This window was created by the Example plugin."
        ).pack()

        # closes the window when clicked
        ttk.Button(
            win,
            text="Close",
            command=win.destroy
        ).pack(
            pady=25
        )

    # button that opens the custom window
    ttk.Button(
        window_box,
        text="Open Window",
        command=open_window
    ).pack(anchor="w")


    # creates a section showing how plugin settings can be saved
    settings_box = ttk.LabelFrame(
        tab,
        text="Settings",
        padding=10
    )
    settings_box.pack(fill="x", pady=6)

    # saves the values from the example controls into routils settings
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

            # saves the settings to disk
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

    # loads the settings that were saved previously
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

            # updates the slider text after loading the saved value
            slider_changed(
                slider_value.get()
            )

        except Exception:
            pass

    # saves the current plugin settings
    ttk.Button(
        settings_box,
        text="Save Settings",
        command=save_settings
    ).pack(
        side="left",
        padx=(0, 6)
    )

    # loads the previously saved plugin settings
    ttk.Button(
        settings_box,
        text="Load Settings",
        command=load_settings
    ).pack(
        side="left"
    )

    # loads saved values when the plugin starts
    load_settings()


    # this function is called when the plugin gets unloaded
    # use it to stop timers, threads or anything else the plugin created
    def cleanup():

        try:

            if tab.winfo_exists():
                tab.destroy()

        except Exception:
            pass

    # gives routils the cleanup function
    return {
        "cleanup": cleanup
    }