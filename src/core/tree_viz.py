import networkx as nx
import matplotlib.pyplot as plt
import colorsys

class HuffmanTreeVisualizer:
    def __init__(self):
        self.G = nx.DiGraph()
        self.labels = {}
        self.node_colors = []
        self.levels = {}

    def _get_level_color(self, level, max_level):
        hue = 0.3 + (0.3 * level / max_level)
        saturation = 0.4  
        value = 0.95 
        rgb = colorsys.hsv_to_rgb(hue, saturation, value)
        return rgb

    def _calculate_tree_depth(self, node, level=0):
        if not node:
            return level - 1
        left_depth = self._calculate_tree_depth(node.left, level + 1)
        right_depth = self._calculate_tree_depth(node.right, level + 1)
        return max(left_depth, right_depth)

    def create_visualization(self, root_node, figsize=(20, 12), node_size=1500, font_size=9):
        if not root_node:
            print("No tree to visualize. Encode some data first.")
            return

        self.G.clear()
        self.labels.clear()
        self.node_colors = []
        self.levels.clear()

        max_depth = self._calculate_tree_depth(root_node)
        self._add_nodes(root_node, 0, max_depth)

        layout = nx.nx_agraph.graphviz_layout(
            self.G, 
            prog='dot',
            args='-Grankdir=TB -Gnodesep=0.8 -Granksep=2.0'
        )

        # Create figure with window title
        fig = plt.figure(figsize=figsize)
        fig.canvas.manager.set_window_title('Huffman Tree')  # Set window title

        # Adjust the plot area
        plt.axes([0.1, 0.1, 0.8, 0.8])

        nx.draw_networkx_edges(
            self.G,
            pos=layout,
            edge_color='#CCCCCC',
            width=1,
            style='solid',
            arrows=False
        )

        nx.draw_networkx_nodes(
            self.G,
            pos=layout,
            node_color=self.node_colors,
            node_size=node_size,
            linewidths=2,
            edgecolors='#666666'
        )

        nx.draw_networkx_labels(
            self.G,
            pos=layout,
            labels=self.labels,
            font_size=font_size,
            font_weight='bold',
            font_family='sans-serif',
            bbox=dict(facecolor='white', 
                     edgecolor='none',
                     alpha=0.7,
                     pad=0.5)
        )

        plt.axis('off')
        plt.show()

    def _add_nodes(self, node, level, max_depth):
        if node is None:
            return

        node_id = id(node)
        self.levels[node_id] = level

        # Format node label
        if node.value is not None:
            if isinstance(node.value, str):
                if node.value.isspace():
                    label = f"'\\s'\n{node.freq}"
                else:
                    label = f"'{node.value}'\n{node.freq}"
            else:
                label = f"{node.value}\n{node.freq}"
        else:
            label = f"{node.freq}"

        self.G.add_node(node_id)
        self.labels[node_id] = label
        self.node_colors.append(self._get_level_color(level, max_depth))

        if node.left:
            left_id = id(node.left)
            self.G.add_edge(node_id, left_id)
            self._add_nodes(node.left, level + 1, max_depth)

        if node.right:
            right_id = id(node.right)
            self.G.add_edge(node_id, right_id)
            self._add_nodes(node.right, level + 1, max_depth)

    def save_visualization(self, filename='huffman_tree.png', dpi=300):
        plt.savefig(filename, dpi=dpi, bbox_inches='tight')
        plt.close()