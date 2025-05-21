import tkinter as tk
from tkinter import messagebox, simpledialog
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Головний клас додатку
class GraphApp:
    def __init__(self, master):
        self.master = master
        master.title("Генератор графів")

        # Створюємо порожній граф (за замовчуванням неорієнтований)
        self.G = nx.Graph()

        # Елементи інтерфейсу
        self.label = tk.Label(master, text="Введіть кількість вершин і ребер:")
        self.label.pack()

        self.vertices_entry = tk.Entry(master)
        self.vertices_entry.pack()
        self.vertices_entry.insert(0, "5")  # Значення за замовчуванням

        self.edges_entry = tk.Entry(master)
        self.edges_entry.pack()
        self.edges_entry.insert(0, "4")

        self.gen_button = tk.Button(master, text="Згенерувати граф", command=self.generate_graph)
        self.gen_button.pack()

        self.shortest_path_button = tk.Button(master, text="Пошук найкоротшого шляху", command=self.find_shortest_path)
        self.shortest_path_button.pack()

        self.connectivity_button = tk.Button(master, text="Перевірити зв’язність", command=self.check_connectivity)
        self.connectivity_button.pack()

        # Віджет для matplotlib
        self.fig, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master)
        self.canvas.get_tk_widget().pack()

    # Функція генерації графа
    def generate_graph(self):
        try:
            n = int(self.vertices_entry.get())
            m = int(self.edges_entry.get())
            if m > n * (n - 1) // 2:
                messagebox.showerror("Помилка", "Занадто багато ребер!")
                return

            self.G = nx.gnm_random_graph(n, m)  # Випадковий граф
            self.draw_graph()
        except Exception as e:
            messagebox.showerror("Помилка", str(e))

    # Відобразити граф
    def draw_graph(self):
        self.ax.clear()
        pos = nx.spring_layout(self.G)
        nx.draw(self.G, pos, ax=self.ax, with_labels=True, node_color='skyblue', node_size=700, font_weight='bold')
        self.canvas.draw()

    # Знайти найкоротший шлях між двома вершинами
    def find_shortest_path(self):
        try:
            src = simpledialog.askinteger("Вибір початкової вершини", "З якої вершини?")
            dst = simpledialog.askinteger("Вибір кінцевої вершини", "До якої вершини?")
            if src is None or dst is None:
                return
            path = nx.shortest_path(self.G, source=src, target=dst)
            messagebox.showinfo("Шлях", f"Найкоротший шлях: {path}")
        except Exception as e:
            messagebox.showerror("Помилка", f"Неможливо знайти шлях: {str(e)}")

    # Перевірити зв’язність графа
    def check_connectivity(self):
        if nx.is_connected(self.G):
            messagebox.showinfo("Зв’язність", "Граф є зв’язним!")
        else:
            messagebox.showinfo("Зв’язність", "Граф НЕ є зв’язним.")

# Запуск програми
if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()