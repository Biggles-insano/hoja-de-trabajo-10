import unittest

class TestProgramaLogistica(unittest.TestCase):
    def setUp(self):
        self.grafo = GrafoLogistica()
        self.programa = ProgramaLogistica(self.grafo)
        texto_grafo = """
        Ciudad1,Ciudad2,tiempoNormal,tiempoLluvia,tiempoNieve,tiempoTormenta
        BuenosAires,SaoPaulo,10,15,20,50
        BuenosAires,Lima,15,20,30,70
        Lima,Quito,10,12,15,20
        """
        self.programa.cargar_grafo_desde_texto(texto_grafo)

    def test_calcular_ruta_mas_corta(self):
        ruta_mas_corta = self.programa.calcular_ruta_mas_corta("BuenosAires", "Quito")
        self.assertEqual(ruta_mas_corta, ["BuenosAires", "Lima", "Quito"])

    def test_calcular_ruta_mas_corta_no_existente(self):
        ruta_mas_corta = self.programa.calcular_ruta_mas_corta("Lima", "SaoPaulo")
        self.assertIsNone(ruta_mas_corta)

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
