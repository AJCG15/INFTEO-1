import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QComboBox, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem,
    QGraphicsTextItem, QInputDialog, QMessageBox, QLabel)

from PyQt5.QtGui import QBrush, QPen, QPainter
from PyQt5.QtCore import Qt, QTimer
from tree_metodos import root


# ---------------- pocisiones del Árbol ----------------
class DisposicionArbol:
    def __init__(self, root):
        self.root = root
        self.posiciones_inorden = {}
        self._contador = 0
        self._asignar_posiciones(root, 0)

    def _asignar_posiciones(self, nodo, profundidad):
        if nodo is None:
            return
        if getattr(nodo, 'left', None):
            self._asignar_posiciones(nodo.left, profundidad + 1)
        self.posiciones_inorden[nodo] = (self._contador, profundidad)
        self._contador += 1
        if getattr(nodo, 'right', None):
            self._asignar_posiciones(nodo.right, profundidad + 1)

    def obtener_posiciones(self, espacio_x=80, espacio_y=80):
        pos = {}
        for nodo, (i, d) in self.posiciones_inorden.items():
            x = i * espacio_x
            y = d * espacio_y
            pos[nodo] = (x, y)
        return pos

# ---------------- Nodo del Árbol ----------------
class NodoItem(QGraphicsEllipseItem):
    RADIO = 20

    def __init__(self, nodo, x, y):
        super().__init__(-NodoItem.RADIO, -NodoItem.RADIO,
                         NodoItem.RADIO*2, NodoItem.RADIO*2)
        self.nodo = nodo
        self.setPos(x, y)
        self.brush_defecto = QBrush(Qt.white)
        self.brush_resaltado = QBrush(Qt.red)
        self.setBrush(self.brush_defecto)
        self.setPen(QPen(Qt.black))
        self.setFlag(QGraphicsEllipseItem.ItemIsSelectable, True)

        self.texto = QGraphicsTextItem(str(nodo.value), parent=self)
        self.texto.setDefaultTextColor(Qt.black)
        self.texto.setPos(-NodoItem.RADIO/2, -NodoItem.RADIO/2)

    def set_valor(self, valor):
        self.nodo.value = valor
        self.texto.setPlainText(str(valor))

    def resaltar(self):
        self.setBrush(self.brush_resaltado)

    def quitar_resaltado(self):
        self.setBrush(self.brush_defecto)

# ---------------- Escena del Árbol ----------------
class EscenaArbol(QGraphicsScene):
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.nodo_items = {}
        self.lineas_items = []
        if root:
            self._construir_escena()

    def _construir_escena(self):
        layout = DisposicionArbol(self.root)
        posiciones = layout.obtener_posiciones(espacio_x=80, espacio_y=80)
        xs = [x for (x, y) in posiciones.values()]
        centro = (min(xs) + max(xs)) / 2 if xs else 0

        for nodo, (x, y) in posiciones.items():
            xi = x - centro
            yi = y
            item = NodoItem(nodo, xi, yi)
            self.addItem(item)
            self.nodo_items[nodo] = item

        for nodo, item in list(self.nodo_items.items()):
            if getattr(nodo, 'left', None):
                hijo_item = self.nodo_items[nodo.left]
                self.addLine(item.x(), item.y(), hijo_item.x(), hijo_item.y(), QPen(Qt.black))
            if getattr(nodo, 'right', None):
                hijo_item = self.nodo_items[nodo.right]
                self.addLine(item.x(), item.y(), hijo_item.x(), hijo_item.y(), QPen(Qt.black))

# ---------------- Ventana Principal ----------------
class VentanaPrincipal(QMainWindow):
    def __init__(self, root):
        super().__init__()
        self.setWindowTitle('Visualizador de Árbol Binario')
        self.root = root
        self.escena = EscenaArbol(root)
        self.vista = QGraphicsView(self.escena)
        self.vista.setRenderHint(QPainter.Antialiasing)

        # Combo y botones
        self.combo_recorrido = QComboBox()
        self.combo_recorrido.addItems(['Inorden', 'Preorden', 'Postorden', 'BFS'])
        self.boton_iniciar = QPushButton('Iniciar recorrido')
        self.boton_editar = QPushButton('Editar nodo seleccionado')

        self.boton_iniciar.clicked.connect(self.iniciar_recorrido)
        self.boton_editar.clicked.connect(self.editar_nodo_seleccionado)

        controles = QHBoxLayout()
        controles.addWidget(self.combo_recorrido)
        controles.addWidget(self.boton_iniciar)
        controles.addWidget(self.boton_editar)

        # Label para mostrar recorrido
        self.label_recorrido = QLabel("Recorrido: ")
 
        # orden de los elementos (principal)
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.addWidget(self.vista)
        layout.addLayout(controles)
        layout.addWidget(self.label_recorrido)
        self.setCentralWidget(central)

        # Timer para resaltar nodos
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self._avanzar_resaltado)
        self.lista_recorrido = []
        self._indice_actual = -1
        self._item_anterior = None

    # ---------------- Métodos ----------------
    def editar_nodo_seleccionado(self):
        seleccionados = [it for it in self.escena.selectedItems() if isinstance(it, NodoItem)]
        if not seleccionados:
            QMessageBox.information(self, 'Editar', 'Selecciona primero un nodo haciendo clic en él.')
            return
        nodo_item = seleccionados[0]
        valor, ok = QInputDialog.getText(self, 'Editar nodo', 'Nuevo valor:', text=str(nodo_item.nodo.value))
        if ok:
            try:
                nuevo_valor = int(valor)
            except:
                nuevo_valor = valor
            nodo_item.set_valor(nuevo_valor)

    def iniciar_recorrido(self):

        tipo = self.combo_recorrido.currentText()
        if tipo == 'Inorden':
            self.lista_recorrido = list(self._inorden(self.root))
        elif tipo == 'Preorden':
            self.lista_recorrido = list(self._preorden(self.root))
        elif tipo == 'Postorden':
            self.lista_recorrido = list(self._postorden(self.root))
        else:
            self.lista_recorrido = list(self._bfs(self.root))


        # Mostrar todos los valores inicialmente
        valores = [str(n.value) for n in self.lista_recorrido]
        self.label_recorrido.setText(f"Recorrido {tipo}: {', '.join(valores)}")

        if self._item_anterior:
            self._item_anterior.quitar_resaltado()
            self._item_anterior = None
        self._indice_actual = -1
        self.timer.start()

    def _avanzar_resaltado(self):
        if self._item_anterior:
            self._item_anterior.quitar_resaltado()
        self._indice_actual += 1
        if self._indice_actual >= len(self.lista_recorrido):
            self.timer.stop()
            return
        nodo = self.lista_recorrido[self._indice_actual]
        item = self.escena.nodo_items.get(nodo)
        if item:
            item.resaltar()
            self._item_anterior = item


    # ---------------- Recorridos ----------------
    def _inorden(self, nodo):
        if nodo is None:
            return
        if getattr(nodo, 'left', None):
            for n in self._inorden(nodo.left):
                yield n
        yield nodo
        if getattr(nodo, 'right', None):
            for n in self._inorden(nodo.right):
                yield n

    def _preorden(self, nodo):
        if nodo is None:
            return
        yield nodo
        if getattr(nodo, 'left', None):
            for n in self._preorden(nodo.left):
                yield n
        if getattr(nodo, 'right', None):
            for n in self._preorden(nodo.right):
                yield n

    def _postorden(self, nodo):
        if nodo is None:
            return
        if getattr(nodo, 'left', None):
            for n in self._postorden(nodo.left):
                yield n
        if getattr(nodo, 'right', None):
            for n in self._postorden(nodo.right):
                yield n
        yield nodo

    def _bfs(self, nodo):
        cola = [nodo]
        while cola:
            actual = cola.pop(0)
            yield actual
            if getattr(actual, 'left', None):
                cola.append(actual.left)
            if getattr(actual, 'right', None):
                cola.append(actual.right)

# ---------------- Main ----------------
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal(root)
    ventana.resize(1000, 700)
    ventana.show()
    sys.exit(app.exec_())