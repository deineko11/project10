import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json, pickle

# -------------------------
# Функції генерації розподілів
# -------------------------
def generate_distribution(dist_type, params, size=1000):
    if dist_type == 'Нормальний':
        mu, sigma = params
        return np.random.normal(mu, sigma, size)
    elif dist_type == 'Рівномірний':
        a, b = params
        return np.random.uniform(a, b, size)
    elif dist_type == 'Біноміальний':
        n, p = params
        return np.random.binomial(n, p, size)
    else:
        raise ValueError("Невідомий розподіл")

# -------------------------
# Оцінка рівномірності
# -------------------------
def uniformity_test(data, N=10):
    hist, _ = np.histogram(data, bins=N, range=(0, 1))
    return np.var(hist)

# -------------------------
# Некорельовані вектори
# -------------------------
def generate_uncorrelated_vectors(n, count=1000):
    data = np.random.randn(count, n)
    q, _ = np.linalg.qr(data)
    return q * np.sqrt(count)

def check_uncorrelated(data):
    corr = np.corrcoef(data.T)
    off_diag = corr - np.diag(np.diag(corr))
    return np.all(np.abs(off_diag) < 0.1)

# -------------------------
# Монте-Карло об’єм n-сфери
# -------------------------
def monte_carlo_sphere_volume(n, num_points=100000):
    points = np.random.uniform(-1, 1, (num_points, n))
    inside = np.sum(np.linalg.norm(points, axis=1) <= 1)
    volume = (2**n) * inside / num_points
    return volume

# -------------------------
# GUI додаток
# -------------------------
class RandomGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор випадкових чисел")

        self.dist_var = tk.StringVar(value='Нормальний')
        self.param_entries = []
        self.data = None

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        ttk.Label(frame, text="Розподіл:").grid(row=0, column=0)
        dist_menu = ttk.Combobox(frame, textvariable=self.dist_var, values=['Нормальний', 'Рівномірний', 'Біноміальний'])
        dist_menu.grid(row=0, column=1)
        dist_menu.bind("<<ComboboxSelected>>", self.update_param_fields)

        self.param_frame = ttk.Frame(frame)
        self.param_frame.grid(row=1, column=0, columnspan=2)

        self.update_param_fields()

        gen_button = ttk.Button(frame, text="Згенерувати", command=self.generate)
        gen_button.grid(row=2, column=0, columnspan=2, pady=5)

        test_button = ttk.Button(frame, text="Оцінити рівномірність", command=self.test_uniformity)
        test_button.grid(row=3, column=0, columnspan=2, pady=5)

        save_text = ttk.Button(frame, text="Зберегти (текст)", command=self.save_text)
        save_text.grid(row=4, column=0)
        save_bin = ttk.Button(frame, text="Зберегти (бінарно)", command=self.save_binary)
        save_bin.grid(row=4, column=1)

        fig = plt.Figure(figsize=(5, 3))
        self.ax = fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.get_tk_widget().pack()

    def update_param_fields(self, event=None):
        for widget in self.param_frame.winfo_children():
            widget.destroy()
        self.param_entries.clear()

        dist = self.dist_var.get()
        if dist == 'Нормальний':
            labels = ['Середнє (mu):', 'С. відхилення (sigma):']
        elif dist == 'Рівномірний':
            labels = ['Нижня межа (a):', 'Верхня межа (b):']
        elif dist == 'Біноміальний':
            labels = ['Кількість випробувань (n):', 'Ймовірність (p):']
        else:
            labels = []

        for i, text in enumerate(labels):
            ttk.Label(self.param_frame, text=text).grid(row=i, column=0)
            entry = ttk.Entry(self.param_frame)
            entry.grid(row=i, column=1)
            self.param_entries.append(entry)

    def generate(self):
        try:
            params = [float(e.get()) for e in self.param_entries]
            self.data = generate_distribution(self.dist_var.get(), params)
            self.ax.clear()
            self.ax.hist(self.data, bins=30, edgecolor='black')
            self.ax.set_title("Гістограма")
            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("Помилка", str(e))

    def test_uniformity(self):
        if self.data is None:
            messagebox.showwarning("Увага", "Спочатку згенеруйте дані")
            return
        normed = (self.data - np.min(self.data)) / (np.max(self.data) - np.min(self.data))
        var = uniformity_test(normed)
        messagebox.showinfo("Результат", f"Варіація: {var:.5f}")

    def save_text(self):
        if self.data is not None:
            path = filedialog.asksaveasfilename(defaultextension=".json")
            with open(path, 'w') as f:
                json.dump(self.data.tolist(), f)

    def save_binary(self):
        if self.data is not None:
            path = filedialog.asksaveasfilename(defaultextension=".bin")
            with open(path, 'wb') as f:
                pickle.dump(self.data, f)

if __name__ == '__main__':
    root = tk.Tk()
    app = RandomGeneratorApp(root)
    root.mainloop()

