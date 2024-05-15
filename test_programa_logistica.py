import unittest

from ht10 import GrafoLogistica, ProgramaLogistica


class TestGrafoLogistica(unittest.TestCase):
    def setUp(self):
        self.grafo = GrafoLogistica()

    def test_agregar_conexion(self):
        self.grafo.agregar_conexion('BuenosAires', 'Lima', (10, 20, 30, 40))
        self.assertIn(('BuenosAires', 'Lima'), self.grafo.matriz_adyacencia)
        self.assertEqual(self.grafo.matriz_adyacencia[('BuenosAires', 'Lima')], (10, 20, 30, 40))

    def test_quitar_conexion(self):
        self.grafo.agregar_conexion('BuenosAires', 'Lima', (10, 20, 30, 40))
        self.grafo.quitar_conexion('BuenosAires', 'Lima')
        self.assertNotIn(('BuenosAires', 'Lima'), self.grafo.matriz_adyacencia)

    def test_cambiar_clima(self):
        self.grafo.agregar_conexion('BuenosAires', 'Lima', (10, 20, 30, 40))
        self.grafo.cambiar_clima('BuenosAires', 'Lima', 2)
        self.assertEqual(self.grafo.matriz_adyacencia[('BuenosAires', 'Lima')], (10, 20, 2, 40))


class TestProgramaLogistica(unittest.TestCase):
    def setUp(self):
        self.grafo = GrafoLogistica()
        self.programa = ProgramaLogistica(self.grafo)
        texto_grafo = """
        BuenosAires,SaoPaulo,10,15,20,50
        BuenosAires,Lima,15,20,30,70
        Lima,Quito,10,12,15,20
        """
        self.programa.cargar_grafo_desde_texto(texto_grafo)

    def test_calcular_ruta_mas_corta(self):
        ruta_mas_corta = self.programa.calcular_ruta_mas_corta("BuenosAires", "Quito")
        rutas_validas = [["BuenosAires", "Lima", "Quito"], ["BuenosAires", "Quito"]]
        self.assertIn(ruta_mas_corta, rutas_validas)

    def test_calcular_ruta_mas_corta_no_existente(self):
        ruta_mas_corta = self.programa.calcular_ruta_mas_corta("Quito", "SaoPaulo")
        rutas_validas = [["Quito", "SaoPaulo"], ["Quito", "BuenosAires", "SaoPaulo"],
                         ["Quito", "Lima", "BuenosAires", "SaoPaulo"], ["Quito", "Lima", "SaoPaulo"]]
        self.assertIn(ruta_mas_corta, rutas_validas)

    def test_calcular_ruta_mas_corta_misma_ciudad(self):
        ruta_mas_corta = self.programa.calcular_ruta_mas_corta("BuenosAires", "BuenosAires")
        self.assertEqual(ruta_mas_corta, ["BuenosAires"])

    def test_calcular_centro_del_grafo(self):
        centro = self.grafo.calcular_centro_del_grafo()
        self.assertEqual(centro, "BuenosAires")

    def test_mostrar_matriz_adyacencia(self):
        # Prueba visual, no se verifica la salida específica
        self.programa.mostrar_matriz_adyacencia()


if __name__ == "__main__":
    unittest.main()
