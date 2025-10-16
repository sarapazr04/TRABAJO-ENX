import customtkinter





import customtkinter
class ScrollableCheckboxFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, title, values):
        super().__init__(master, label_text=title)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.checkboxes = []

        for i, value in enumerate(self.values):
            checkbox = customtkinter.CTkCheckBox(self, text=value)
            checkbox.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="w")
            self.checkboxes.append(checkbox)

    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("my app")
        self.geometry("400x220")
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.checkbox_frame = ScrollableCheckboxFrame(self, "Values", values=["value 1", "value 2", "value 3"])
        self.checkbox_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")
        self.radiobutton_frame = customtkinter.CTkOptionMenu(self, values=["option 1", "option 2"],command=self.optionmenu_callback)
        self.radiobutton_frame.grid(row=0, column=1, padx=(0, 10), pady=(10, 0), sticky="nsew")

        self.button = customtkinter.CTkButton(self, text="my button", command=self.button_callback)
        self.button.grid(row=3, column=0, padx=10, pady=10, sticky="ew", columnspan=2)
    def optionmenu_callback(choice):
        print("optionmenu dropdown clicked:", choice)

    def button_callback(self):
        print("checkbox_frame:", self.checkbox_frame.get())
        print("radiobutton_frame:", self.radiobutton_frame.get())
app = App()
app.mainloop()