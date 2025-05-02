from ui.main_window import MainWindow

def run_app():
    window = MainWindow()
    window.window.mainloop()  # Directly calling Tkinter's main loop

if __name__ == "__main__":
    run_app()
