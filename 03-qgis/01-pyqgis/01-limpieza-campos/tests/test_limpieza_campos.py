"""Pruebas de clasificación ejecutables sin instalar QGIS."""

from decimal import Decimal
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from limpieza_campos import (
    clasificar_campos, indices_que_permite_eliminar, resolver_capa_entrada,
    valor_es_invalido,
)


class ValorInvalidoTests(unittest.TestCase):
    def test_nulos_blancos_marcador_y_ceros(self):
        valores = [
            None, "", "   \t", "#D", "  #D  ", 0, 0.0, -0.0, Decimal("0"),
            "0", "00", "0000", "0.0", "0000.000", " -000.00 ", "+0", "0e5",
        ]
        for valor in valores:
            with self.subTest(valor=valor):
                self.assertTrue(valor_es_invalido(valor))

    def test_un_dato_distinto_de_cero_o_texto_informativo_se_conserva(self):
        valores = [
            0.8, 0.01, -0.5, 100, Decimal("0.0001"),
            "0000.8", "0.01", "-0.5", "100", "información", "0,0", "#d", False,
        ]
        for valor in valores:
            with self.subTest(valor=valor):
                self.assertFalse(valor_es_invalido(valor))

    def test_nulo_de_qgis_y_objeto_con_is_null(self):
        marcador_qgis = object()

        class VarianteNula:
            def isNull(self):
                return True

        self.assertTrue(valor_es_invalido(marcador_qgis, marcador_qgis))
        self.assertTrue(valor_es_invalido(VarianteNula()))


class ClasificacionCamposTests(unittest.TestCase):
    def test_combinacion_invalida_y_valor_valido_en_registros_distintos(self):
        registros = [
            [None, "0", "", "0"],
            ["#D", "0000.8", "dato", "0"],
            ["  ", "", "0.0", "0"],
        ]
        candidatos, analizados = clasificar_campos(registros, 4, [0, 1, 2])
        self.assertEqual(candidatos, [0])
        self.assertEqual(analizados, 3)

    def test_indice_protegido_nunca_es_candidato(self):
        candidatos, _ = clasificar_campos([[0, 0], ["00", "0.0"]], 2, [1])
        self.assertEqual(candidatos, [1])

    def test_capa_vacia_se_rechaza(self):
        with self.assertRaisesRegex(ValueError, "no tiene registros"):
            clasificar_campos([], 1, [0])

    def test_registro_incompleto_se_rechaza(self):
        with self.assertRaisesRegex(ValueError, "número de atributos"):
            clasificar_campos([[0]], 2, [0, 1])

    def test_clave_lectura_y_restricciones_se_excluyen(self):
        class Restricciones:
            def __init__(self, valor):
                self.valor = valor

            def constraints(self):
                return self.valor

        class Campo:
            def __init__(self, nombre, solo_lectura=False, restringido=False):
                self.nombre = nombre
                self.solo_lectura = solo_lectura
                self.restringido = restringido

            def name(self):
                return self.nombre

            def isReadOnly(self):
                return self.solo_lectura

            def constraints(self):
                return Restricciones(self.restringido)

        class Campos(list):
            def fieldOriginIndex(self, indice):
                return indice if indice < 4 else -1

            def at(self, indice):
                return self[indice]

        class Proveedor:
            def fields(self):
                return Campos(campos[:4])

            def pkAttributeIndexes(self):
                return [1]

        class Capa:
            def fields(self):
                return Campos(campos)

            def primaryKeyAttributes(self):
                return [1]

        campos = [
            Campo("editable"), Campo("fid"), Campo("calculado", True),
            Campo("obligatorio", restringido=True), Campo("unido"),
        ]
        evaluables, protegidos = indices_que_permite_eliminar(Capa(), Proveedor())
        self.assertEqual(evaluables, [0])
        self.assertEqual(protegidos, ["fid", "calculado", "obligatorio", "unido"])


class ResolucionEntradaTests(unittest.TestCase):
    class Proyecto:
        def __init__(self, capas):
            self.capas = capas
            self.consultas = []

        def mapLayersByName(self, nombre):
            self.consultas.append(nombre)
            return self.capas

    class Capa:
        def __init__(self, valida=True):
            self.valida = valida

        def isValid(self):
            return self.valida

    def resolver(self, ruta, nombre, proyecto, constructor=None, existe=None):
        return resolver_capa_entrada(
            ruta,
            nombre,
            proyecto,
            constructor or (lambda *args: self.Capa()),
            lambda capa: isinstance(capa, self.Capa) and capa.isValid(),
            existe or (lambda _ruta: True),
        )

    def test_usa_capa_cargada_sin_consultar_rutas(self):
        capa = self.Capa()
        proyecto = self.Proyecto([capa])

        resultado, es_externa = self.resolver(None, "Paquete 33", proyecto)

        self.assertIs(resultado, capa)
        self.assertFalse(es_externa)
        self.assertEqual(proyecto.consultas, ["Paquete 33"])

    def test_ruta_externa_tiene_prioridad_sobre_capa_cargada(self):
        cargada = self.Capa()
        externa = self.Capa()
        proyecto = self.Proyecto([cargada])
        llamadas_constructor = []

        def constructor(*args):
            llamadas_constructor.append(args)
            return externa

        resultado, es_externa = self.resolver(
            r"C:\Proyectos\archivo.shp", "Paquete 33", proyecto, constructor
        )

        self.assertIs(resultado, externa)
        self.assertTrue(es_externa)
        self.assertEqual(
            llamadas_constructor,
            [(r"C:\Proyectos\archivo.shp", "archivo", "ogr")],
        )
        self.assertEqual(proyecto.consultas, [])

    def test_ruta_inexistente_se_rechaza_sin_fallback(self):
        proyecto = self.Proyecto([self.Capa()])

        with self.assertRaisesRegex(RuntimeError, "No existe el archivo"):
            self.resolver("inexistente.shp", "Paquete 33", proyecto, existe=lambda _: False)
        self.assertEqual(proyecto.consultas, [])

    def test_archivo_no_vectorial_o_invalido_se_rechaza(self):
        proyecto = self.Proyecto([])

        with self.assertRaisesRegex(RuntimeError, "no se pudo cargar como capa vectorial"):
            self.resolver(
                "tabla.csv", "Paquete 33", proyecto,
                constructor=lambda *_: self.Capa(valida=False),
            )

    def test_capa_cargada_ausente_o_duplicada_se_rechaza(self):
        for capas in ([], [self.Capa(), self.Capa()]):
            with self.subTest(cantidad=len(capas)):
                proyecto = self.Proyecto(capas)
                with self.assertRaisesRegex(RuntimeError, "exactamente una capa"):
                    self.resolver(None, "Paquete 33", proyecto)

    def test_capa_cargada_no_vectorial_o_invalida_se_rechaza(self):
        for capa in (object(), self.Capa(valida=False)):
            with self.subTest(capa=capa):
                proyecto = self.Proyecto([capa])
                with self.assertRaisesRegex(RuntimeError, "debe ser vectorial y válida"):
                    self.resolver(None, "Paquete 33", proyecto)

    def test_ninguna_opcion_configurada_se_rechaza(self):
        with self.assertRaisesRegex(RuntimeError, "Configura RUTA_ENTRADA"):
            self.resolver(None, " ", self.Proyecto([]))


if __name__ == "__main__":
    unittest.main()
