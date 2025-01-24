import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing App with Real-Time Preview")
        
        # Maximize the window when the app starts
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")  # Resize window to screen size
 
        self.image_path = None
        self.original_image = None
        self.processed_image = None

        # UI Elements
        self.setup_ui()

    def setup_ui(self):
        # Frame to hold the entire UI elements and allow scrolling
        self.scrollable_frame = tk.Frame(self.root)
        self.scrollable_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas and scrollbar for scrolling
        self.canvas = tk.Canvas(self.scrollable_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar = tk.Scrollbar(self.scrollable_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Frame to hold actual content inside canvas
        self.content_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")

        # Create 3 columns
        self.left_frame = tk.Frame(self.content_frame)
        self.left_frame.grid(row=0, column=0, padx=20, pady=10, sticky="n")
        
        self.center_frame = tk.Frame(self.content_frame)
        self.center_frame.grid(row=0, column=1, padx=20, pady=10, sticky="n")
        
        self.right_frame = tk.Frame(self.content_frame)
        self.right_frame.grid(row=0, column=2, padx=20, pady=10, sticky="n")

        # 1st column -> Load button, original histogram and image
        load_button = tk.Button(self.left_frame, text="Load Image", command=self.load_image)
        load_button.pack(pady=10)
        self.create_tooltip(load_button, "Click to load an image from your computer.")

        self.histogram_frame = tk.Frame(self.left_frame)
        self.histogram_frame.pack(side=tk.TOP, pady=10, padx=10)

        self.image_canvas = tk.Canvas(self.left_frame, width=400, height=400, bg="gray")
        self.image_canvas.pack(pady=10)

        # 2nd column -> Options for image processing
        tk.Label(self.center_frame, text="Conversion Type:").pack()

        self.conversion_type = tk.StringVar(value="no_changes")
        
        no_changes_button = tk.Radiobutton(self.center_frame, text="No Changes", variable=self.conversion_type, value="no_changes", command=self.update_preview)
        no_changes_button.pack()
        self.create_tooltip(no_changes_button, "No processing will be applied to the image.")

        equalize_button = tk.Radiobutton(self.center_frame, text="Equalize Histogram", variable=self.conversion_type, value="equalize", command=self.update_preview)
        equalize_button.pack()
        self.create_tooltip(equalize_button, "Enhances image contrast by equalizing the histogram across the entire image.")

        clahe_button = tk.Radiobutton(self.center_frame, text="CLAHE", variable=self.conversion_type, value="clahe", command=self.update_preview)
        clahe_button.pack()
        self.create_tooltip(clahe_button, "Applies Contrast Limited Adaptive Histogram Equalization (CLAHE) to the image, enhancing contrast locally.")

        # Sliders for CLAHE parameters
        self.clip_limit = tk.DoubleVar(value=100.0)
        self.tile_grid_size = tk.IntVar(value=8)

        self.clahe_frame = tk.Frame(self.center_frame)
        self.clahe_frame.pack(pady=10)

        tk.Label(self.clahe_frame, text="CLAHE Parameters:").pack()

        clip_limit_label = tk.Label(self.clahe_frame, text="Clip Limit:")
        clip_limit_label.pack()
        clip_limit_slider = tk.Scale(self.clahe_frame, from_=1.0, to=200.0, resolution=1.0, orient=tk.HORIZONTAL, variable=self.clip_limit, command=lambda x: self.update_preview())
        clip_limit_slider.pack()
        self.create_tooltip(clip_limit_slider, "Controls the contrast enhancement limit. Higher values increase contrast. Too high may introduce noise.")

        tile_grid_size_label = tk.Label(self.clahe_frame, text="Tile Grid Size:")
        tile_grid_size_label.pack()
        tile_grid_size_slider = tk.Scale(self.clahe_frame, from_=1, to=16, resolution=1, orient=tk.HORIZONTAL, variable=self.tile_grid_size, command=lambda x: self.update_preview())
        tile_grid_size_slider.pack()
        self.create_tooltip(tile_grid_size_slider, "Defines the size of the local regions (tiles) for CLAHE. Smaller tiles lead to more localized contrast enhancement.")

        # 3rd column -> Save button, modified histogram and image
        save_button = tk.Button(self.right_frame, text="Save Image", command=self.save_image)
        save_button.pack(pady=10)
        self.create_tooltip(save_button, "Click to save the processed image to your computer.")

        self.modified_histogram_frame = tk.Frame(self.right_frame)
        self.modified_histogram_frame.pack(side=tk.TOP, pady=10, padx=10)

        self.modified_image_canvas = tk.Canvas(self.right_frame, width=400, height=400, bg="gray")
        self.modified_image_canvas.pack(pady=10)

        # Update scrollbar to accommodate content size
        self.content_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def create_tooltip(self, widget, text):
        tooltip = tk.Label(self.root, text=text, bg="yellow", relief="solid", borderwidth=1, font=("Arial", 10))
        tooltip.pack_forget()  # Initially hidden

        def on_enter(event):
            tooltip.place(x=widget.winfo_x() + widget.winfo_width(), y=widget.winfo_y())

        def on_leave(event):
            tooltip.place_forget()

        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def load_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if self.image_path:
            # Load the original image and store it separately
            self.original_image = cv.imread(self.image_path, cv.IMREAD_GRAYSCALE)
            self.processed_image = self.original_image.copy()  # Copy to processed image, it will be modified
            self.display_image(self.original_image, side="left")  # Display original image to the left
            self.display_histogram(self.original_image, side="left")  # Display histogram of the original image
            self.update_preview()  # Update the preview with the original image

    def update_preview(self):
        if self.original_image is None:
            return

        conversion_type = self.conversion_type.get()
        if conversion_type == "no_changes":
            self.processed_image = self.original_image.copy()  # Ensure processed image is not overwritten
        elif conversion_type == "equalize":
            self.processed_image = cv.equalizeHist(self.original_image)
        elif conversion_type == "clahe":
            clahe = cv.createCLAHE(clipLimit=self.clip_limit.get(), tileGridSize=(self.tile_grid_size.get(), self.tile_grid_size.get()))
            self.processed_image = clahe.apply(self.original_image)

        # Show processed image and its histogram on the right
        self.display_image(self.processed_image, side="right")  
        self.display_histogram(self.processed_image, side="right")

        # Show or hide CLAHE sliders based on selected conversion type
        if conversion_type == "clahe":
            self.clahe_frame.pack(pady=10)
        else:
            self.clahe_frame.pack_forget()

        # Update scrollbar after changing content
        self.content_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def save_image(self):
        if self.processed_image is None:
            messagebox.showerror("Error", "No processed image to save!")
            return

        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if output_path:
            cv.imwrite(output_path, self.processed_image)
            messagebox.showinfo("Success", f"Image saved to {output_path}")

    def display_image(self, image, side="left"):
        if image is not None:
            image_resized = Image.fromarray(image)
            image_resized = ImageTk.PhotoImage(image=image_resized.resize((400, 400)))

            if side == "left":
                # Clear the canvas before displaying the new image
                self.image_canvas.delete("all")
                self.image_canvas.create_image(200, 200, image=image_resized, anchor=tk.CENTER)
                self.original_image_ref = image_resized  # Store a reference to the original image (no overwrite)
            elif side == "right":
                # Display the processed image in the right column
                self.modified_image_canvas.delete("all")
                self.modified_image_canvas.create_image(200, 200, image=image_resized, anchor=tk.CENTER)
                self.processed_image_ref = image_resized  # Store a reference to the processed image (no overwrite)

            # Prevent garbage collection by holding references to both images
            self.root.original_image = getattr(self, 'original_image_ref', None)
            self.root.processed_image = getattr(self, 'processed_image_ref', None)

    def display_histogram(self, image, side="left"):
        if image is not None:
            if side == "left":
                # Display original histogram and make it static (will only update once after loading)
                for widget in self.histogram_frame.winfo_children():
                    widget.destroy()

                fig, ax = plt.subplots(figsize=(5, 3), dpi=100)
                ax.hist(image.ravel(), bins=256, range=(0, 256), color='gray')
                ax.set_title("Original Histogram")
                ax.set_xlim(0, 256)

                canvas = FigureCanvasTkAgg(fig, master=self.histogram_frame)
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.pack(side=tk.LEFT, padx=20)
                canvas.draw()

                # Close the figure to prevent memory issues
                plt.close(fig)

            else:
                # Display processed histogram
                for widget in self.modified_histogram_frame.winfo_children():
                    widget.destroy()

                fig, ax = plt.subplots(figsize=(5, 3), dpi=100)
                ax.hist(image.ravel(), bins=256, range=(0, 256), color='gray')
                ax.set_title("Processed Histogram")
                ax.set_xlim(0, 256)

                canvas = FigureCanvasTkAgg(fig, master=self.modified_histogram_frame)
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.pack(side=tk.LEFT, padx=20)
                canvas.draw()

                # Close the figure to prevent memory issues
                plt.close(fig)


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()
