import customtkinter as ctk
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

class SteinerTreeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Задача Штейнера на графах")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.frame = ctk.CTkFrame(master=self.root)
        self.frame.pack(pady=20, padx=20)

        self.label = ctk.CTkLabel(master=self.frame, text="Введите количество вершин:")
        self.label.pack()

        self.vertex_entry = ctk.CTkEntry(master=self.frame)
        self.vertex_entry.pack()

        self.u_entry = ctk.CTkEntry(master=self.frame, placeholder_text="Вершина u")
        self.u_entry.pack()

        self.v_entry = ctk.CTkEntry(master=self.frame, placeholder_text="Вершина v")
        self.v_entry.pack()

        self.weight_entry = ctk.CTkEntry(master=self.frame, placeholder_text="Вес")
        self.weight_entry.pack()

        self.add_edge_button = ctk.CTkButton(master=self.frame, text="Добавить ребро", command=self.add_edge)
        self.add_edge_button.pack()

        self.calculate_button = ctk.CTkButton(master=self.frame, text="Решить", command=self.calculate_steiner_tree)
        self.calculate_button.pack(pady=10)

        self.result_label = ctk.CTkLabel(master=self.frame, text="")
        self.result_label.pack(pady=10)

        self.edges = []
        self.adjacency_matrix = []

        self.adjacency_label = ctk.CTkLabel(master=self.frame, text="Таблица смежности:")
        self.adjacency_label.pack(pady=10)

        self.adjacency_textbox = ctk.CTkTextbox(master=self.frame, width=300, height=150)
        self.adjacency_textbox.pack()

    def add_edge(self):
        u = self.u_entry.get()
        v = self.v_entry.get()
        weight = self.weight_entry.get()
        if u and v and weight:
            self.edges.append((int(u), int(v), float(weight)))
            self.update_adjacency_matrix()
            self.u_entry.delete(0, ctk.END)
            self.v_entry.delete(0, ctk.END)
            self.weight_entry.delete(0, ctk.END)

    def update_adjacency_matrix(self):
        num_vertices = int(self.vertex_entry.get()) if self.vertex_entry.get() else 0
        self.adjacency_matrix = np.zeros((num_vertices, num_vertices))

        for u, v, w in self.edges:
            self.adjacency_matrix[u][v] = w
            self.adjacency_matrix[v][u] = w  
        adjacency_str = "  " + "  ".join(str(i) for i in range(num_vertices)) + "\n"
        for i in range(num_vertices):
            adjacency_str += str(i) + " " + "  ".join(f"{int(self.adjacency_matrix[i][j])}" for j in range(num_vertices)) + "\n"

        self.adjacency_textbox.delete("1.0", ctk.END)
        self.adjacency_textbox.insert("1.0", adjacency_str)

    def calculate_steiner_tree(self):
        try:
            num_vertices = int(self.vertex_entry.get())
            graph = nx.Graph()
            for u, v, w in self.edges:
                graph.add_edge(u, v, weight=w)

            steiner_tree = nx.algorithms.approximation.steiner_tree(graph, range(num_vertices), weight='weight')

            total_weight = sum(data['weight'] for u, v, data in steiner_tree.edges(data=True))
            self.result_label.configure(text=f"Минимальный вес пути: {total_weight}")

            self.plot_graph(graph, steiner_tree)
        except Exception as e:
            self.show_error(e)

    def plot_graph(self, graph, steiner_tree):
        pos = nx.spring_layout(graph)
        plt.figure(figsize=(10, 5))
        nx.draw(graph, pos, with_labels=True, node_color='lightblue', edge_color='gray', width=2)
        nx.draw(steiner_tree, pos, with_labels=True, node_color='orange', edge_color='red', width=2)
        plt.title("Исходный граф и Штейнерово дерево")
        plt.show()

    def show_error(self, message):
        error_window = ctk.CTkToplevel(self.root)
        error_window.title("Ошибка")
        error_label = ctk.CTkLabel(master=error_window, text=str(message))
        error_label.pack(pady=10, padx=10)

if __name__ == "__main__":
    root = ctk.CTk()
    app = SteinerTreeApp(root)
    root.mainloop()