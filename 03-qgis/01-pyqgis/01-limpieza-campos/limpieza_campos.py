CAPA_ENTRADA = "Paquete 33"

"""Detecta campos sin información y prepara su eliminación en una capa de QGIS.

El script no guarda los cambios: la sesión de edición queda abierta para revisión.
Ejecutar con runpy desde la consola Python de QGIS (ver README.md).
"""

from decimal import Decimal, InvalidOperation
from numbers import Number


def valor_es_invalido(valor, nulo_qgis=None):
    """Clasifica los valores indicados como vacíos sin depender de PyQGIS."""
    if valor is None or valor is nulo_qgis:
        return True

    es_nulo = getattr(valor, "isNull", None)
    if callable(es_nulo) and es_nulo():
        return True

    if isinstance(valor, str):
        texto = valor.strip()
        if not texto or texto == "#D":
            return True
        try:
            return Decimal(texto) == 0
        except InvalidOperation:
            return False

    # bool hereda de int, pero False puede ser un dato booleano válido.
    if isinstance(valor, bool):
        return False
    if isinstance(valor, (Number, Decimal)):
        return valor == 0
    return False


def clasificar_campos(registros, cantidad_campos, indices_evaluables, nulo_qgis=None):
    """Devuelve índices con todos los valores inválidos y registros analizados.

    Los índices no evaluables (por ejemplo, claves primarias) nunca son
    candidatos. Una capa sin registros se rechaza por seguridad.
    """
    indices = sorted(set(indices_evaluables))
    if cantidad_campos < 0 or any(i < 0 or i >= cantidad_campos for i in indices):
        raise ValueError("Los índices de campos no corresponden a la capa.")

    candidatos = set(indices)
    cantidad_registros = 0
    for atributos in registros:
        if len(atributos) != cantidad_campos:
            raise ValueError("Un registro tiene un número de atributos inesperado.")
        cantidad_registros += 1
        for indice in tuple(candidatos):
            if not valor_es_invalido(atributos[indice], nulo_qgis):
                candidatos.remove(indice)

    if cantidad_registros == 0:
        raise ValueError("La capa no tiene registros; no se eliminarán campos.")
    return sorted(candidatos), cantidad_registros


def indices_que_permite_eliminar(capa, proveedor):
    """Excluye claves, campos virtuales, de solo lectura o con restricciones."""
    campos_capa = capa.fields()
    campos_proveedor = proveedor.fields()
    claves_primarias = set(proveedor.pkAttributeIndexes())
    claves_de_capa = set(capa.primaryKeyAttributes())
    evaluables = []
    protegidos = []

    for indice, campo in enumerate(campos_capa):
        indice_proveedor = campos_capa.fieldOriginIndex(indice)
        pertenece_al_proveedor = (
            0 <= indice_proveedor < len(campos_proveedor)
            and campos_proveedor.at(indice_proveedor).name() == campo.name()
        )
        if (
            not pertenece_al_proveedor
            or indice in claves_de_capa
            or indice_proveedor in claves_primarias
            or campo.isReadOnly()
            or campo.constraints().constraints()
        ):
            protegidos.append(campo.name())
        else:
            evaluables.append(indice)
    return evaluables, protegidos


def ejecutar():
    """Analiza la capa y, tras confirmar, deja los borrados sin guardar."""
    from qgis.core import NULL, Qgis, QgsProject, QgsVectorDataProvider, QgsVectorLayer
    from qgis.PyQt.QtWidgets import QMessageBox

    capas = QgsProject.instance().mapLayersByName(CAPA_ENTRADA)
    if len(capas) != 1:
        raise RuntimeError(
            "Se necesita exactamente una capa cargada con el nombre {!r}; encontradas: {}."
            .format(CAPA_ENTRADA, len(capas))
        )
    capa = capas[0]
    if not isinstance(capa, QgsVectorLayer) or not capa.isValid():
        raise RuntimeError("La capa debe ser vectorial y válida.")
    if capa.isReadOnly() or capa.isEditable():
        raise RuntimeError(
            "La capa es de solo lectura o ya tiene una sesión de edición. "
            "Guarda o descarta primero las ediciones existentes."
        )

    proveedor = capa.dataProvider()
    if proveedor is None:
        raise RuntimeError("La capa no tiene proveedor de datos.")
    try:
        permiso_borrado = Qgis.VectorProviderCapability.DeleteAttributes
    except AttributeError:
        permiso_borrado = QgsVectorDataProvider.DeleteAttributes
    if not proveedor.capabilities() & permiso_borrado:
        raise RuntimeError("El proveedor no admite eliminar atributos.")

    nombres_originales = [campo.name() for campo in capa.fields()]
    evaluables, protegidos = indices_que_permite_eliminar(capa, proveedor)
    if not evaluables:
        print("No hay campos eliminables. Conservados: {}".format(", ".join(nombres_originales)))
        return

    indices_candidatos, analizados = clasificar_campos(
        (entidad.attributes() for entidad in capa.getFeatures()),
        len(nombres_originales),
        evaluables,
        NULL,
    )
    esperado = capa.featureCount()
    if esperado >= 0 and analizados != esperado:
        mensaje = (
            "El número de registros leído ({}) difiere del informado por la capa ({}). "
            "No se harán cambios."
        )
        raise RuntimeError(mensaje.format(analizados, esperado))

    nombres_candidatos = [nombres_originales[i] for i in indices_candidatos]
    nombres_conservados = [
        nombre for i, nombre in enumerate(nombres_originales) if i not in indices_candidatos
    ]
    print("Registros analizados: {}".format(analizados))
    print("Campos candidatos: {}".format(", ".join(nombres_candidatos) or "ninguno"))
    print("Campos protegidos o no editables: {}".format(", ".join(protegidos) or "ninguno"))
    print("Campos que se conservarán: {}".format(", ".join(nombres_conservados) or "ninguno"))
    if not indices_candidatos:
        print("No se inició ninguna edición.")
        return

    mensaje = (
        "Se preparará la eliminación de estos campos en {!r}:\n\n{}\n\n"
        "Los cambios quedarán sin guardar en QGIS para su revisión. ¿Continuar?"
    )
    respuesta = QMessageBox.question(
        None,
        "Confirmar limpieza de campos",
        mensaje.format(CAPA_ENTRADA, "\n".join(nombres_candidatos)),
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No,
    )
    if respuesta != QMessageBox.Yes:
        print("Operación cancelada. No se modificó la capa.")
        return

    if not capa.startEditing():
        raise RuntimeError("QGIS no pudo iniciar la edición; no se modificó la capa.")
    try:
        if not capa.deleteAttributes(indices_candidatos):
            raise RuntimeError("QGIS rechazó la eliminación de uno o más campos.")
        capa.updateFields()
        nombres_esperados = [
            nombre for i, nombre in enumerate(nombres_originales) if i not in indices_candidatos
        ]
        if [campo.name() for campo in capa.fields()] != nombres_esperados:
            raise RuntimeError("La eliminación preparada no coincide con la lista prevista.")
    except Exception as error:
        if not capa.rollBack():
            raise RuntimeError(
                "Falló la reversión de la edición. Revisa la capa manualmente; "
                "no se puede garantizar su estado."
            ) from error
        raise RuntimeError("Se revirtió la edición: {}".format(error)) from error

    print("Campos preparados para eliminar: {}".format(", ".join(nombres_candidatos)))
    print("Campos conservados: {}".format(", ".join(nombres_conservados) or "ninguno"))
    print("La edición sigue abierta. Revisa la capa y guarda o descarta los cambios en QGIS.")


if __name__ == "__main__":
    try:
        ejecutar()
    except (RuntimeError, ValueError) as error:
        print("Limpieza detenida: {}".format(error))
