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
    def __init__(self, id_text, x, y, parent_window=None, radius=30):
        """
        parent_window: referencia a la ventana principal para actualizar claves al renombrar nodos.
        """
        self.id_text = id_text
        self.parent_window = parent_window
        self.edges = []
        super().__init__(-radius, -radius, 2*radius, 2*radius)
        self.setFlags(QGraphicsEllipseItem.ItemIsMovable |
                      QGraphicsEllipseItem.ItemSendsGeometryChanges |
                      QGraphicsEllipseItem.ItemIsSelectable)

        self.default_brush = QBrush(Qt.white)
        self.highlight_brush = QBrush(Qt.green)
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
        old_label = self.id_text
        text, ok = QInputDialog.getText(None, "Editar nodo", "Etiqueta:", text=self.text.toPlainText())
        if ok and text.strip() != "":
            new_label = text.strip()
            
            self.id_text = new_label
            self.text.setPlainText(self.id_text)
            rect = self.text.boundingRect()
            self.text.setPos(-rect.width()/2, -rect.height()/2)
            
            if self.parent_window:
                self.parent_window._on_node_label_changed(old_label, new_label, self)
        super().mouseDoubleClickEvent(event)

    def highlight(self, color='green'):
        if color == 'green':
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

    def paint(self, painter, option, widget):
        painter.setPen(self.pen())
        painter.drawPath(self.path())
        if self.directed:
            if self.nodo_from is self.nodo_to:
                self._draw_arrow_selfloop(painter)
            else:
                self._draw_arrow(painter)

    def _draw_arrow(self, painter):
        p1 = self.nodo_from.scenePos()
        p2 = self.nodo_to.scenePos()
        dx, dy = p2.x() - p1.x(), p2.y() - p1.y()
        angle = math.atan2(dy, dx)
        r = self.nodo_to.radius
        end_x = p2.x() - r * math.cos(angle)
        end_y = p2.y() - r * math.sin(angle)
        arrow_size = 10
        left_angle = angle + math.pi/6
        right_angle = angle - math.pi/6
        p_left = QPointF(end_x - arrow_size*math.cos(left_angle), end_y - arrow_size*math.sin(left_angle))
        p_right = QPointF(end_x - arrow_size*math.cos(right_angle), end_y - arrow_size*math.sin(right_angle))
        painter.setBrush(Qt.black)
        painter.drawPolygon(QPolygonF([QPointF(end_x, end_y), p_left, p_right]))

    def _draw_arrow_selfloop(self, painter):
        node_pos = self.nodo_from.scenePos()
        top_x = node_pos.x()
        top_y = node_pos.y() - self.nodo_from.radius - 20
        p1 = QPointF(top_x, top_y)
        p_left = QPointF(top_x - 7, top_y + 14)
        p_right = QPointF(top_x + 7, top_y + 14)
        painter.setBrush(Qt.black)
        painter.drawPolygon(QPolygonF([p1, p_left, p_right]))

    def mouseDoubleClickEvent(self, event):
        self.directed = not self.directed
        self.update()
        super().mouseDoubleClickEvent(event)

    def remove(self):
        self.nodo_from.remove_edge(self)
        self.nodo_to.remove_edge(self)
        scene = self.scene()
        if scene:
            scene.removeItem(self)

    def highlight(self):
        self.setPen(self.pen_highlight)
        self.setZValue(0)

    def unhighlight(self):
        self.setPen(self.pen_default)
        self.setZValue(-1)



class Grafo11Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grafo 11 - Interactivo")
        self.resize(950, 720)
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        central.setLayout(layout)

        
        control_layout = QHBoxLayout()
        lbl = QLabel("Mueve nodos con el mouse. Doble clic en nodo para renombrar.")
        control_layout.addWidget(lbl)

        
        self.btn_recorrido = QPushButton("Recorrido Alfabético")
        self.btn_recorrido.clicked.connect(self._iniciar_recorrido_alfabetico)
        control_layout.addWidget(self.btn_recorrido)

        
        control_layout.addWidget(QLabel("Origen:"))
        self.line_origen = QLineEdit()
        self.line_origen.setPlaceholderText("Ej: A")
        self.line_origen.setMaximumWidth(60)
        control_layout.addWidget(self.line_origen)

        control_layout.addWidget(QLabel("Destino:"))
        self.line_destino = QLineEdit()
        self.line_destino.setPlaceholderText("Ej: E")
        self.line_destino.setMaximumWidth(60)
        control_layout.addWidget(self.line_destino)

        self.btn_buscar_ruta = QPushButton("Buscar Ruta")
        self.btn_buscar_ruta.clicked.connect(self._iniciar_recorrido_ruta)
        control_layout.addWidget(self.btn_buscar_ruta)

        layout.addLayout(control_layout)

        
        self.view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        self.view.setRenderHints(self.view.renderHints() | QPainter.Antialiasing)
        layout.addWidget(self.view)

        
        self.nodos = {}   
        self.aristas = [] 
        self.recorrido_timer = QTimer(self)
        self.recorrido_timer.timeout.connect(self._paso_recorrido)
        self.recorrido_secuencia = [] 
        self.recorrido_indice = 0
        self.recorrido_modo = 'none'  # 'alpha' o 'path'

        # Cargar grafo original (posiciones y aristas)
        self._cargar_grafo_11()

        # Ajustes de escena
        self.scene.setSceneRect(-450, -350, 1100, 900)
        self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

  
    def add_node(self, id_text, x, y):
        n = NodoItem(id_text, x, y, parent_window=self)
        self.scene.addItem(n)
        self.nodos[id_text] = n
        return n

    def add_edge(self, a_label, b_label, directed=False):
        if a_label not in self.nodos or b_label not in self.nodos:
            return None
        e = AristaItem(self.nodos[a_label], self.nodos[b_label], directed)
        self.scene.addItem(e)
        self.aristas.append(e)
        return e

    def _cargar_grafo_11(self):
        # Mantener forma y posiciones originales
        pos = {'A': (-120, -20), 'B': (120, -20), 'C': (-120, 120), 'D': (120, 120), 'E': (0, 180)}
        for k, v in pos.items():
            self.add_node(k, v[0], v[1])
        edges = [('A', 'A', True), ('A', 'B', False), ('A', 'D', False), ('A', 'C', False), ('C', 'D', False), ('C', 'E', False)]
        for a, b, d in edges:
            self.add_edge(a, b, directed=d)

    # ------------------
    # Actualización si el usuario renombra un nodo
    # ------------------
    def _on_node_label_changed(self, old_label, new_label, node_obj):
        """
        Cuando un nodo es renombrado, actualizamos el diccionario self.nodos
        para que las operaciones futuras (buscar por etiqueta) sigan funcionando.
        Si la nueva etiqueta ya existe, mostramos un warning y revertimos.
        """
        old_label = str(old_label)
        new_label = str(new_label)
        if old_label == new_label:
            return

        if new_label in self.nodos:
            QMessageBox.warning(self, "Etiqueta duplicada", f"Ya existe un nodo con la etiqueta '{new_label}'. Cambio cancelado.")
            # revertir visualmente al viejo label
            node_obj.id_text = old_label
            node_obj.text.setPlainText(old_label)
            rect = node_obj.text.boundingRect()
            node_obj.text.setPos(-rect.width()/2, -rect.height()/2)
            return

        
        if old_label in self.nodos and self.nodos[old_label] is node_obj:
            del self.nodos[old_label]
            self.nodos[new_label] = node_obj

    
    def _reset_resaltado(self):
        self.recorrido_timer.stop()
        for nodo in self.nodos.values():
            nodo.unhighlight()
        for arista in self.aristas:
            arista.unhighlight()
        self.btn_recorrido.setEnabled(True)
        self.btn_buscar_ruta.setEnabled(True)

   
    def _find_shortest_path(self, start_id, end_id):
        start_id = str(start_id).strip()
        end_id = str(end_id).strip()
        if start_id == "" or end_id == "":
            QMessageBox.warning(self, "Error", "Debe ingresar origen y destino.")
            return []

        if start_id not in self.nodos or end_id not in self.nodos:
            QMessageBox.warning(self, "Error", "El nodo de inicio o fin no existe.")
            return []

        start_node = self.nodos[start_id]
        end_node = self.nodos[end_id]

        if start_node is end_node:
            return [start_node]

        queue = deque([start_node])
        visited = {start_node: None}

        while queue:
            current = queue.popleft()
            # recorrer aristas de current
            for edge in current.edges:
                neighbor = edge.nodo_to if edge.nodo_from is current else edge.nodo_from
                if neighbor not in visited:
                    visited[neighbor] = current
                    if neighbor is end_node:
                        
                        # reconstruir camino
                        path = []
                        n = end_node
                        while n is not None:
                            path.append(n)
                            n = visited.get(n)
                        return path[::-1]
                    queue.append(neighbor)
        return []

   
    def _iniciar_recorrido_ruta(self):
        self._reset_resaltado()
        start_id = self.line_origen.text().strip()
        end_id = self.line_destino.text().strip()
        self.recorrido_secuencia = self._find_shortest_path(start_id, end_id)
        if not self.recorrido_secuencia:
            QMessageBox.information(self, "Ruta No Encontrada", f"No se encontró ruta entre {start_id} y {end_id}.")
            return
        self.recorrido_modo = 'path'
        self.recorrido_indice = 0
        self.btn_buscar_ruta.setEnabled(False)
        self.btn_recorrido.setEnabled(False)
        self.recorrido_timer.start(600)

   
    def _iniciar_recorrido_alfabetico(self):
        self._reset_resaltado()
        nodos_y_etiquetas = []
        for nodo in self.nodos.values():
            etiqueta_actual = nodo.text.toPlainText()
            nodos_y_etiquetas.append((etiqueta_actual, nodo))
        nodos_y_etiquetas_ordenados = sorted(nodos_y_etiquetas, key=lambda x: x[0])
        self.recorrido_secuencia = [nodo_obj for etiqueta, nodo_obj in nodos_y_etiquetas_ordenados]
        if not self.recorrido_secuencia:
            QMessageBox.information(self, "Advertencia", "No hay nodos para recorrer.")
            return
        self.recorrido_modo = 'alpha'
        self.recorrido_indice = 0
        self.btn_recorrido.setEnabled(False)
        self.btn_buscar_ruta.setEnabled(False)
        self.recorrido_timer.start(600)

    
    def _paso_recorrido(self):
        if self.recorrido_indice < len(self.recorrido_secuencia):
            current_node = self.recorrido_secuencia[self.recorrido_indice]

            
            if self.recorrido_indice > 0:
                prev_node = self.recorrido_secuencia[self.recorrido_indice - 1]
                if self.recorrido_modo == 'path':
                    prev_node.highlight(color='path')
                   
                    self._highlight_edge(prev_node, current_node)
                else:
                    prev_node.unhighlight()


            if self.recorrido_modo == 'path':
                
                current_node.highlight(color='green')
            else:
                
                current_node.highlight(color='green')

            self.recorrido_indice += 1
        else:
            
            self.recorrido_timer.stop()
            if len(self.recorrido_secuencia) > 0:
                last_node = self.recorrido_secuencia[-1]
                if self.recorrido_modo == 'path':
                    last_node.highlight(color='path')
                else:
                    last_node.unhighlight()
            self.btn_recorrido.setEnabled(True)
            self.btn_buscar_ruta.setEnabled(True)
            self.recorrido_modo = 'none'

    def _highlight_edge(self, node1, node2):
        """Encuentra y resalta la arista entre dos nodos (por objeto)."""
        for arista in node1.edges:
            if (arista.nodo_from is node2) or (arista.nodo_to is node2):
                arista.highlight()
                break


def main():
    app = QApplication(sys.argv)
    win = Grafo11Window()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
