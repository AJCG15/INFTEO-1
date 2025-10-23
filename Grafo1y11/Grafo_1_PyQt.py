from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QGraphicsView, QGraphicsScene,
    QVBoxLayout, QLabel, QInputDialog, QPushButton, QHBoxLayout, QLineEdit, QMessageBox
)
from PyQt5.QtGui import QBrush, QPen, QPainterPath, QPolygonF, QFont, QPainter
from PyQt5.QtCore import Qt, QPointF, QTimer
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsPathItem
import sys, math
from collections import deque

class NodoItem(QGraphicsEllipseItem):
    def __init__(self, id_text, x, y, radius=30):
        self.id_text = id_text 
        self.edges = [] 
        super().__init__(-radius, -radius, 2*radius, 2*radius)
        self.setFlags(QGraphicsEllipseItem.ItemIsMovable |
                      QGraphicsEllipseItem.ItemSendsGeometryChanges |
                      QGraphicsEllipseItem.ItemIsSelectable)
        
        self.default_brush = QBrush(Qt.white) 
        self.highlight_brush = QBrush(Qt.red)
        self.path_brush = QBrush(Qt.yellow) 
        self.setBrush(self.default_brush)
        self.setPen(QPen(Qt.black, 2))
        self.radius = radius

        self.text = QGraphicsTextItem(id_text, self)
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.text.setFont(font)
        rect = self.text.boundingRect()
        self.text.setPos(-rect.width()/2, -rect.height()/2)

        self.setPos(x, y)

    def add_edge(self, edge):
        self.edges.append(edge)

    def remove_edge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)

    def itemChange(self, change, value):
        if change == QGraphicsEllipseItem.ItemPositionChange:
            for e in getattr(self, 'edges', []):  
                e.update_position()
        return super().itemChange(change, value)

    def mouseDoubleClickEvent(self, event):
        text, ok = QInputDialog.getText(None, "Editar nodo", "Etiqueta:", text=self.text.toPlainText())
        if ok and text.strip() != "":
            self.id_text = text.strip() 
            self.text.setPlainText(self.id_text)
            rect = self.text.boundingRect()
            self.text.setPos(-rect.width()/2, -rect.height()/2)
        super().mouseDoubleClickEvent(event)

    def highlight(self, color='red'):
        if color == 'red':
            self.setBrush(self.highlight_brush)
        elif color == 'path':
            self.setBrush(self.path_brush)

    def unhighlight(self):
        self.setBrush(self.default_brush)

class AristaItem(QGraphicsPathItem):
   
    def __init__(self, nodo_from, nodo_to, directed=False):
        super().__init__()
        self.nodo_from = nodo_from
        self.nodo_to = nodo_to
        self.directed = directed
        self.pen_default = QPen(Qt.black, 3)
        self.pen_highlight = QPen(Qt.darkRed, 4)
        self.setPen(self.pen_default)
        self.setZValue(-1)
        self.nodo_from.add_edge(self)
        self.nodo_to.add_edge(self)
        self.update_position()

    def update_position(self):
        p1 = self.nodo_from.scenePos()
        p2 = self.nodo_to.scenePos()
        path = QPainterPath()
        
        if self.nodo_from is self.nodo_to:
            r = self.nodo_from.radius
            cx = p1.x()
            cy = p1.y()
            path.addEllipse(cx - r - 12, cy - r - 30, r + 20, r + 20)
        else:
            path.moveTo(p1)
            path.lineTo(p2)
        self.setPath(path)
        self.update()

    def highlight(self):
        self.setPen(self.pen_highlight)
        self.setZValue(0) 
    
    def unhighlight(self):
        self.setPen(self.pen_default)
        self.setZValue(-1)


class Grafo1Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(" Grafo 1 Interactivo ")
        self.resize(900, 700)
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        central.setLayout(layout)

       
        control_layout_top = QHBoxLayout()
        control_layout_path = QHBoxLayout()
        
        
        self.btn_recorrido_ascendente = QPushButton(" Recorrido Numérico Ascendente ")
        self.btn_recorrido_ascendente.clicked.connect(self._iniciar_recorrido_numerico_ascendente)
        control_layout_top.addWidget(self.btn_recorrido_ascendente)
        
        
        control_layout_path.addWidget(QLabel("Origen:"))
        self.line_origen = QLineEdit()
        self.line_origen.setPlaceholderText("Ej: 1")
        control_layout_path.addWidget(self.line_origen)

        control_layout_path.addWidget(QLabel("Destino:"))
        self.line_destino = QLineEdit()
        self.line_destino.setPlaceholderText("Ej: 7")
        control_layout_path.addWidget(self.line_destino)

        self.btn_buscar_ruta = QPushButton(" Buscar Ruta Más Corta ")
        self.btn_buscar_ruta.clicked.connect(self._iniciar_recorrido_ruta)
        control_layout_path.addWidget(self.btn_buscar_ruta)

        layout.addLayout(control_layout_top)
        layout.addLayout(control_layout_path)

        # --- Área de Visualización del Grafo ---
        self.view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        self.view.setRenderHints(self.view.renderHints() | QPainter.Antialiasing)
        layout.addWidget(self.view)

        # --- Variables de Estado ---
        self.nodos = {}
        self.aristas = []
        self.recorrido_timer = QTimer(self) 
        self.recorrido_timer.timeout.connect(self._paso_recorrido)
        self.recorrido_secuencia = [] # Almacena objetos NodoItem
        self.recorrido_indice = 0
        self.recorrido_modo = 'none' # 'numeric' o 'path'

        # --- Inicialización ---
        self._cargar_grafo_1()
        self.scene.setSceneRect(-400, -300, 1000, 800)
        self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

    # --- Funciones de Utilidad (add_node, add_edge, _cargar_grafo_1 son iguales) ---

    def add_node(self, id_text, x, y):
        n = NodoItem(id_text, x, y)
        self.scene.addItem(n)
        self.nodos[id_text] = n
        return n

    def add_edge(self, a, b, directed=False):
        e = AristaItem(self.nodos[a], self.nodos[b], directed)
        self.scene.addItem(e)
        self.aristas.append(e)
        return e

    def _cargar_grafo_1(self):
        # El grafo de ejemplo (basado en el código original)
        pos = {'1': (0, 120), '2': (-120, 60), '3': (0, 0), '4': (-40, -80), '5': (120, 20), '6': (120, 120), '7': (200, -40)}
        for k, v in pos.items():
            self.add_node(k, v[0], v[1])
        edges = [("1", "2"), ("1", "3"), ("2", "3"), ("2", "4"), ("3", "4"), ("3", "5"), ("5", "6"), ("5", "7")]
        for a, b in edges:
            self.add_edge(a, b, directed = False)

    def _reset_resaltado(self):
        """Quita el resaltado de todos los nodos y aristas."""
        self.recorrido_timer.stop()
        for nodo in self.nodos.values():
            nodo.unhighlight()
        for arista in self.aristas:
            arista.unhighlight()
        self.btn_recorrido_ascendente.setEnabled(True)
        self.btn_buscar_ruta.setEnabled(True)

    # --- Lógica de Búsqueda de Camino Más Corto (BFS Simulado) ---

    def _find_shortest_path(self, start_id, end_id):
        """
        Encuentra el camino más corto (en aristas) entre dos nodos usando BFS.
        Devuelve una lista de objetos NodoItem si se encuentra el camino, o una lista vacía.
        """
        # Validar IDs de nodos
        if start_id not in self.nodos or end_id not in self.nodos:
            QMessageBox.warning(self, "Error", "El nodo de inicio o fin no existe.")
            return []
        
        start_node = self.nodos[start_id]
        end_node = self.nodos[end_id]

        if start_node is end_node:
             return [start_node]

        # Estructuras para BFS
        queue = deque([start_node])
        visited = {start_node: None} # Almacena {nodo: nodo_padre}

        while queue:
            current = queue.popleft()

            # Encontrar vecinos a través de las aristas
            neighbors = []
            for edge in current.edges:
                neighbor = edge.nodo_to if edge.nodo_from is current else edge.nodo_from
                if neighbor not in visited:
                    visited[neighbor] = current
                    queue.append(neighbor)
                    if neighbor is end_node:
                        # Reconstruir el camino
                        path = []
                        n = end_node
                        while n is not None:
                            path.append(n)
                            n = visited.get(n)
                        return path[::-1] # Invertir para obtener [inicio, ..., fin]
        
        return [] # Camino no encontrado

    # --- Funciones de Recorrido ---

    def _iniciar_recorrido_ruta(self):
        """Inicia el recorrido de ruta más corta."""
        self._reset_resaltado()
        
        start_id = self.line_origen.text().strip()
        end_id = self.line_destino.text().strip()
        
        self.recorrido_secuencia = self._find_shortest_path(start_id, end_id)

        if not self.recorrido_secuencia:
            QMessageBox.information(self, "Ruta No Encontrada", 
                                    f"No se encontró ruta entre {start_id} y {end_id}.")
            return
            
        self.recorrido_modo = 'path'
        self.recorrido_indice = 0
        self.btn_buscar_ruta.setEnabled(False)
        self.btn_recorrido_ascendente.setEnabled(False)
        self.recorrido_timer.start(500)

    def _preparar_recorrido_numerico(self, reverse=False):
        # ... (Igual que en el código original, solo renombrado para claridad)
        self._reset_resaltado()
        
        nodos_y_valores = []
        for nodo in self.nodos.values():
            etiqueta_actual = nodo.text.toPlainText()
            try:
                valor_numerico = int(etiqueta_actual)
                nodos_y_valores.append((valor_numerico, nodo))
            except ValueError:
                pass 

        nodos_y_valores_ordenados = sorted(nodos_y_valores, key=lambda x: x[0], reverse=reverse)
        
        self.recorrido_secuencia = [nodo_obj for valor, nodo_obj in nodos_y_valores_ordenados]
        self.recorrido_indice = 0
        self.recorrido_modo = 'numeric'


    def _iniciar_recorrido_numerico_ascendente(self):
        """Inicia el recorrido numérico ascendente."""
        self._preparar_recorrido_numerico(reverse=False) 
        if not self.recorrido_secuencia:
            QMessageBox.information(self, "Advertencia", "No hay nodos con etiquetas numéricas para recorrer.")
            return

        self.btn_recorrido_ascendente.setEnabled(False) 
        self.btn_buscar_ruta.setEnabled(False)
        self.recorrido_timer.start(500) 

    def _paso_recorrido(self):
        """Avanza un paso en la animación (común para ambos modos)."""
        if self.recorrido_indice < len(self.recorrido_secuencia):
            
            current_node = self.recorrido_secuencia[self.recorrido_indice]

            # 1. Des-resaltar el nodo anterior
            if self.recorrido_indice > 0:
                prev_node = self.recorrido_secuencia[self.recorrido_indice - 1]
                
                if self.recorrido_modo == 'path':
                    prev_node.highlight(color='path') # Dejar los nodos de la ruta en amarillo
                    
                    # Resaltar la arista entre el nodo anterior y el actual
                    self._highlight_edge(prev_node, current_node)
                else:
                    prev_node.unhighlight()

            # 2. Resaltar el nodo actual de rojo
            current_node.highlight(color='red')
            
            self.recorrido_indice += 1
        else:
            # Fin del recorrido
            self.recorrido_timer.stop()
            
            # Limpiar/Finalizar el resaltado
            if len(self.recorrido_secuencia) > 0:
                last_node = self.recorrido_secuencia[-1]
                if self.recorrido_modo == 'path':
                    last_node.highlight(color='path')
                else:
                    last_node.unhighlight()

            self.btn_recorrido_ascendente.setEnabled(True)
            self.btn_buscar_ruta.setEnabled(True)

    def _highlight_edge(self, node1, node2):
        """Encuentra y resalta la arista entre dos nodos."""
        for arista in node1.edges:
            if (arista.nodo_from is node2) or (arista.nodo_to is node2):
                arista.highlight()
                break


def main():
    app = QApplication(sys.argv)
    win = Grafo1Window()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    # La aplicación requiere las bibliotecas de PyQt5.
    main()