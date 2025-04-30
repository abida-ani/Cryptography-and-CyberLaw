from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


class IMG_Stegno:
    def __init__(self):
        self.image_path = None

    def main(self, root):
        self.root = root
        root.title('Image Steganography')
        root.geometry('500x600')
        root.resizable(False, False)
        root.config(bg='#e3f4f1')

        frame = Frame(root, bg='#e3f4f1')
        frame.pack(expand=True)

        Label(frame, text='Image Steganography', font=('Times New Roman', 25, 'bold'), bg='#e3f4f1').pack(pady=20)
        Button(frame, text="Encode", font=('Helvetica', 14), bg='#e8c1c7', command=self.encode_page).pack(pady=10)
        Button(frame, text="Decode", font=('Helvetica', 14), bg='#e8c1c7', command=self.decode_page).pack(pady=10)

    def encode_page(self):
        self.clear_frame()
        frame = Frame(self.root, bg='#e3f4f1')
        frame.pack(expand=True)

        Label(frame, text='Select Image to Hide Text', font=('Times New Roman', 18, 'bold'), bg='#e3f4f1').pack(pady=10)
        Button(frame, text='Browse', font=('Helvetica', 14), bg='#e8c1c7', command=lambda: self.select_image(frame)).pack()
        Button(frame, text='Back', font=('Helvetica', 14), bg='#e8c1c7', command=self.reset).pack(pady=10)

    def select_image(self, frame):
        file_path = filedialog.askopenfilename(filetypes=[('Image Files', '*.png *.jpg *.jpeg')])
        if not file_path:
            messagebox.showerror("Error", "No file selected.")
            return

        self.image_path = file_path
        img = Image.open(file_path)
        img = img.resize((300, 200))
        tk_img = ImageTk.PhotoImage(img)

        Label(frame, text='Selected Image', font=('Helvetica', 14, 'bold'), bg='#e3f4f1').pack(pady=10)
        Label(frame, image=tk_img, bg='#e3f4f1').pack()
        frame.image = tk_img  # keep reference

        Label(frame, text='Enter message to hide:', font=('Helvetica', 14), bg='#e3f4f1').pack(pady=10)
        self.text_input = Text(frame, width=50, height=5)
        self.text_input.pack()

        Button(frame, text='Encode & Save Image', font=('Helvetica', 14), bg='#e8c1c7', command=self.encode).pack(pady=10)

    def encode(self):
        message = self.text_input.get("1.0", END).strip()
        if not message:
            messagebox.showerror("Error", "No message entered.")
            return

        img = Image.open(self.image_path)
        encoded_img = img.copy()
        self.hide_data(encoded_img, message + "###")  # End marker
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
        if save_path:
            encoded_img.save(save_path)
            messagebox.showinfo("Success", "Image saved with hidden message.")
            self.reset()

    def hide_data(self, img, data):
        binary_data = ''.join([format(ord(c), '08b') for c in data])
        data_index = 0
        pixels = img.getdata()
        new_pixels = []

        for pixel in pixels:
            r, g, b = pixel
            if data_index < len(binary_data):
                r = r & ~1 | int(binary_data[data_index])
                data_index += 1
            if data_index < len(binary_data):
                g = g & ~1 | int(binary_data[data_index])
                data_index += 1
            if data_index < len(binary_data):
                b = b & ~1 | int(binary_data[data_index])
                data_index += 1
            new_pixels.append((r, g, b))

        img.putdata(new_pixels)

    def decode_page(self):
        self.clear_frame()
        frame = Frame(self.root, bg='#e3f4f1')
        frame.pack(expand=True)

        Label(frame, text='Select Image to Decode', font=('Times New Roman', 18, 'bold'), bg='#e3f4f1').pack(pady=10)
        Button(frame, text='Browse', font=('Helvetica', 14), bg='#e8c1c7', command=lambda: self.select_decode_image(frame)).pack()
        Button(frame, text='Back', font=('Helvetica', 14), bg='#e8c1c7', command=self.reset).pack(pady=10)

    def select_decode_image(self, frame):
        file_path = filedialog.askopenfilename(filetypes=[('Image Files', '*.png *.jpg *.jpeg')])
        if not file_path:
            messagebox.showerror("Error", "No file selected.")
            return

        img = Image.open(file_path)
        img = img.resize((300, 200))
        tk_img = ImageTk.PhotoImage(img)

        Label(frame, text='Selected Image', font=('Helvetica', 14, 'bold'), bg='#e3f4f1').pack(pady=10)
        Label(frame, image=tk_img, bg='#e3f4f1').pack()
        frame.image = tk_img

        hidden_msg = self.reveal_data(Image.open(file_path))

        Label(frame, text='Hidden Message:', font=('Helvetica', 14, 'bold'), bg='#e3f4f1').pack(pady=10)
        output = Text(frame, width=50, height=5)
        output.insert(END, hidden_msg)
        output.config(state='disabled')
        output.pack()

    def reveal_data(self, img):
        binary_data = ""
        for pixel in img.getdata():
            for color in pixel[:3]:
                binary_data += str(color & 1)

        chars = [chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8)]
        message = ''.join(chars)
        return message.split("###")[0]  # split by end marker

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def reset(self):
        self.clear_frame()
        self.main(self.root)


# Start GUI
if __name__ == "__main__":
    root = Tk()
    app = IMG_Stegno()
    app.main(root)
    root.mainloop()