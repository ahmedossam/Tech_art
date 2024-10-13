import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import subprocess
import trimesh

class FileRenamerImporter:
    def __init__(self, root):
        self.root = root
        self.root.title("File Renamer and Importer Tool")
        self.filepaths = []

        # Set up UI
        self.label = tk.Label(root, text="Choose files to import")
        self.label.pack(pady=10)

        self.import_button = tk.Button(root, text="Import Files", command=self.import_files)
        self.import_button.pack(pady=5)

        self.rename_button = tk.Button(root, text="Batch Rename Files", command=self.batch_rename)
        self.rename_button.pack(pady=5)

        self.delete_button = tk.Button(root, text="Delete Selected Files", command=self.delete_files)
        self.delete_button.pack(pady=5)

        self.software_button = tk.Button(root, text="Import to Software", command=self.import_to_software)
        self.software_button.pack(pady=5)

        self.save_dir_button = tk.Button(root, text="Choose Save Directory", command=self.choose_save_directory)
        self.save_dir_button.pack(pady=5)

        self.preview_label = tk.Label(root, text="")
        self.preview_label.pack(pady=10)

        self.save_directory = ""
        self.file_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
        self.file_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

    def import_files(self):
        self.filepaths = filedialog.askopenfilenames(
            filetypes=[("All Files", "*.*"), ("Images", "*.png;*.jpg"), ("3D Mesh", "*.obj;*.fbx")]
        )
        if self.filepaths:
            self.file_listbox.delete(0, tk.END)
            for path in self.filepaths:
                self.file_listbox.insert(tk.END, os.path.basename(path))
            self.label.config(text=f"{len(self.filepaths)} files imported")

            # Preview the first file
            first_file = self.filepaths[0]
            if first_file.endswith(('.png', '.jpg')):
                self.preview_image(first_file)
            elif first_file.endswith(('.obj', '.fbx')):
                self.load_3d_mesh(first_file)

    def preview_image(self, image_path):
        img = Image.open(image_path)
        img.thumbnail((200, 200))
        img = ImageTk.PhotoImage(img)
        self.preview_label.config(image=img)
        self.preview_label.image = img

    def load_3d_mesh(self, mesh_path):
        mesh = trimesh.load(mesh_path)
        self.preview_label.config(text=f"Mesh: {mesh_path}\nVertices: {len(mesh.vertices)}\nFaces: {len(mesh.faces)}")

    def batch_rename(self):
        selected_files = [self.filepaths[i] for i in self.file_listbox.curselection()]
        if selected_files:
            prefix = simpledialog.askstring("Prefix", "Enter prefix for file names")
            suffix = simpledialog.askstring("Suffix", "Enter suffix for file names (optional)")
            for idx, file_path in enumerate(selected_files):
                file_dir = os.path.dirname(file_path)
                file_ext = os.path.splitext(file_path)[1]
                new_name = f"{prefix}_{idx+1}{suffix or ''}{file_ext}"
                new_path = os.path.join(self.save_directory or file_dir, new_name)
                os.rename(file_path, new_path)
            messagebox.showinfo("Success", "Files renamed successfully")
            self.import_files()  # Refresh list

    def delete_files(self):
        selected_files = [self.filepaths[i] for i in self.file_listbox.curselection()]
        if selected_files:
            confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete {len(selected_files)} files?")
            if confirm:
                for file_path in selected_files:
                    os.remove(file_path)
                messagebox.showinfo("Success", "Files deleted")
                self.import_files()  # Refresh list

    def choose_save_directory(self):
        self.save_directory = filedialog.askdirectory()
        if self.save_directory:
            self.label.config(text=f"Save Directory: {self.save_directory}")

    def import_to_software(self):
        selected_files = [self.filepaths[i] for i in self.file_listbox.curselection()]
        if selected_files:
            software_choice = simpledialog.askstring("Import to", "Enter software (Unreal, Unity, Maya, Houdini, 3ds Max):")
            if software_choice.lower() == "unreal":
                self.import_to_unreal(selected_files)
            elif software_choice.lower() == "unity":
                self.import_to_unity(selected_files)
            elif software_choice.lower() == "maya":
                self.import_to_maya(selected_files)
            elif software_choice.lower() == "houdini":
                self.import_to_houdini(selected_files)
            elif software_choice.lower() == "3ds max":
                self.import_to_3ds_max(selected_files)
            else:
                messagebox.showerror("Error", "Unknown software selected")

    def import_to_unreal(self, files):
        # Example: Copy files to Unreal Engine project directory
        unreal_content_dir = filedialog.askdirectory(title="Select Unreal Engine Content Directory")
        if unreal_content_dir:
            for file in files:
                file_name = os.path.basename(file)
                destination = os.path.join(unreal_content_dir, file_name)
                os.system(f'copy "{file}" "{destination}"')
            messagebox.showinfo("Success", "Files imported to Unreal Engine")

    def import_to_unity(self, files):
        # Example: Copy files to Unity Assets folder
        unity_assets_dir = filedialog.askdirectory(title="Select Unity Assets Directory")
        if unity_assets_dir:
            for file in files:
                file_name = os.path.basename(file)
                destination = os.path.join(unity_assets_dir, file_name)
                os.system(f'copy "{file}" "{destination}"')
            messagebox.showinfo("Success", "Files imported to Unity")

    def import_to_maya(self, files):
        # Launch Maya and import the selected file using command line (if Maya's command line interface is installed)
        for file in files:
            maya_import_cmd = f'maya -file "{file}"'
            subprocess.Popen(maya_import_cmd, shell=True)
        messagebox.showinfo("Success", "Files imported to Maya")

    def import_to_houdini(self, files):
        # Launch Houdini and import the selected file using command line
        for file in files:
            houdini_import_cmd = f"houdini -file '{file}'"
            subprocess.Popen(houdini_import_cmd, shell=True)
        messagebox.showinfo("Success", "Files imported to Houdini")

    def import_to_3ds_max(self, files):
        # Launch 3ds Max and import the selected file
        for file in files:
            max_import_cmd = f'3dsmax "{file}"'
            subprocess.Popen(max_import_cmd, shell=True)
        messagebox.showinfo("Success", "Files imported to 3ds Max")


# Initialize Tkinter window
root = tk.Tk()
app = FileRenamerImporter(root)
root.mainloop()
