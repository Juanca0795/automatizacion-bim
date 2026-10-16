"""Pruebas de clasificación ejecutables sin instalar QGIS."""

from decimal import Decimal
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from limpieza_campos import (
    clasificar_campos, indices_que_permite_eliminar, valor_es_invalido,
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


if __name__ == "__main__":
    unittest.main()
