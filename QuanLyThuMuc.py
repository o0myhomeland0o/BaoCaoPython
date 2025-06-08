import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.font import Font


class DirectoryManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trình quản lý thư mục")
        self.root.geometry("800x600")
        
        # Tạo font đậm cho tiêu đề
        bold_font = Font(weight="bold")
        
        # Frame chính
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tiêu đề
        self.title_label = ttk.Label(
            self.main_frame, 
            text="QUẢN LÝ TẬP TIN TRONG THƯ MỤC", 
            font=bold_font
        )
        self.title_label.pack(pady=10)
        
        # Frame chứa nút chọn thư mục
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=5)
        
        # Nút chọn thư mục
        self.select_button = ttk.Button(
            self.button_frame, 
            text="Chọn thư mục", 
            command=self.select_directory
        )
        self.select_button.pack(side=tk.LEFT)
        
        # Nút mở file
        self.open_button = ttk.Button(
            self.button_frame, 
            text="Mở tập tin", 
            command=self.open_file,
            state=tk.DISABLED
        )
        self.open_button.pack(side=tk.LEFT, padx=5)
        
        # Thanh cuộn
        self.scrollbar = ttk.Scrollbar(self.main_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview để hiển thị file
        self.tree = ttk.Treeview(
            self.main_frame, 
            columns=("Type", "Size"), 
            yscrollcommand=self.scrollbar.set,
            selectmode="browse"
        )
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Cấu hình thanh cuộn
        self.scrollbar.config(command=self.tree.yview)
        
        # Đặt tên cho các cột
        self.tree.heading("#0", text="Tên tập tin")
        self.tree.heading("Type", text="Loại")
        self.tree.heading("Size", text="Kích thước (KB)")
        
        # Đặt chiều rộng cột
        self.tree.column("#0", width=400)
        self.tree.column("Type", width=150)
        self.tree.column("Size", width=150)
        
        # Gắn sự kiện double click
        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        
        # Biến lưu thư mục hiện tại
        self.current_directory = ""
        
    def select_directory(self):
        """Mở hộp thoại chọn thư mục và hiển thị các file"""
        directory = filedialog.askdirectory(title="Chọn thư mục")
        if directory:
            try:
                self.current_directory = directory
                self.show_files(directory)
                self.root.title(f"Trình quản lý thư mục - {directory}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể đọc thư mục: {e}")
    
    def show_files(self, directory):
        """Hiển thị các file trong thư mục lên Treeview"""
        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            # Lấy danh sách file và thư mục con
            items = os.listdir(directory)
            
            # Phân loại và thêm vào Treeview
            for item in items:
                full_path = os.path.join(directory, item)
                
                if os.path.isdir(full_path):
                    # Nếu là thư mục
                    self.tree.insert("", tk.END, text=item, values=("Thư mục", ""))
                else:
                    # Nếu là file
                    file_ext = os.path.splitext(item)[1].lower()
                    file_size = os.path.getsize(full_path) / 1024  # KB
                    
                    # Xác định loại file
                    if file_ext == ".txt":
                        file_type = "Text File"
                    elif file_ext == ".py":
                        file_type = "Python File"
                    elif file_ext in (".jpg", ".jpeg", ".png", ".gif"):
                        file_type = "Image File"
                    else:
                        file_type = f"{file_ext.upper()} File"
                    
                    self.tree.insert(
                        "", tk.END, 
                        text=item, 
                        values=(file_type, f"{file_size:.2f}"),
                        tags=("file",)
                    )
            
        except PermissionError:
            messagebox.showerror("Lỗi", "Không có quyền truy cập thư mục này")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc thư mục: {e}")
    
    def on_double_click(self, event):
        """Xử lý sự kiện double click để mở file hoặc thư mục"""
        item = self.tree.selection()[0]
        item_text = self.tree.item(item, "text")
        item_values = self.tree.item(item, "values")
        
        full_path = os.path.join(self.current_directory, item_text)
        
        if os.path.isdir(full_path):
            # Nếu là thư mục, mở thư mục đó
            self.current_directory = full_path
            self.show_files(full_path)
            self.root.title(f"Trình quản lý thư mục - {full_path}")
        else:
            # Nếu là file, mở file
            self.open_selected_file()
    
    def on_tree_select(self, event):
        """Kích hoạt nút Mở khi có item được chọn"""
        selected_items = self.tree.selection()
        if selected_items:
            self.open_button.config(state=tk.NORMAL)
        else:
            self.open_button.config(state=tk.DISABLED)
    
    def open_selected_file(self):
        """Mở file được chọn bằng chương trình mặc định"""
        selected_item = self.tree.selection()[0]
        item_text = self.tree.item(selected_item, "text")
        full_path = os.path.join(self.current_directory, item_text)
        
        if os.path.isdir(full_path):
            messagebox.showinfo("Thông báo", "Đây là thư mục, vui lòng double click để mở")
            return
        
        try:
            os.startfile(full_path)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở file: {e}")
    
    def open_file(self):
        """Xử lý khi nhấn nút Mở"""
        self.open_selected_file()


if __name__ == "__main__":
    root = tk.Tk()
    app = DirectoryManagerApp(root)
    root.mainloop()