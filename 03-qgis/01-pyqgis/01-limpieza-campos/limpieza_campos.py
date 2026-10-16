# ==========================================
# CONFIGURACIÓN
# ==========================================

# OPCIÓN 1: nombre exacto de una capa cargada en QGIS.
CAPA_ENTRADA = "Paquete 33"

# OPCIÓN 2: archivo vectorial externo. Si se indica, tiene prioridad.
RUTA_ENTRADA = None
# Ejemplo: r"C:\Proyectos\archivo.shp"

# True muestra los campos candidatos y termina sin iniciar una edición.
SOLO_PREVISUALIZAR = False

"""Detecta campos sin información y prepara su eliminación en una capa de QGIS.

El script no guarda los cambios: la sesión de edición queda abierta para revisión.
Ejecutar con runpy desde la consola Python de QGIS (ver README.md).
"""

from decimal import Decimal, InvalidOperation
from numbers import Number
import os


def resolver_capa_entrada(
    ruta_entrada,
    capa_entrada,
    proyecto,
    crear_capa_vectorial,
    es_capa_vectorial_valida,
    existe_archivo=os.path.isfile,
):
    """Resuelve una capa cargada o crea una capa desde un archivo vectorial.

    La ruta externa, si se especifica, tiene prioridad y nunca provoca una
    alternativa silenciosa a la capa cargada cuando es inválida.
    """
    if ruta_entrada is not None:
        ruta = os.fspath(ruta_entrada).strip()
        if not ruta:
            raise RuntimeError("RUTA_ENTRADA está vacía; indica un archivo vectorial válido.")
        if not existe_archivo(ruta):
            raise RuntimeError("No existe el archivo indicado en RUTA_ENTRADA: {!r}.".format(ruta))

        nombre_archivo = ruta.replace("\\", "/").rsplit("/", 1)[-1]
        nombre_capa = os.path.splitext(nombre_archivo)[0]
        capa = crear_capa_vectorial(ruta, nombre_capa, "ogr")
        if not es_capa_vectorial_valida(capa):
            raise RuntimeError(
                "El archivo no se pudo cargar como capa vectorial compatible con OGR: {!r}."
                .format(ruta)
            )
        return capa, True

    if not isinstance(capa_entrada, str) or not capa_entrada.strip():
        raise RuntimeError(
            "Configura RUTA_ENTRADA o indica en CAPA_ENTRADA el nombre de una capa cargada."
        )
    capas = proyecto.mapLayersByName(capa_entrada)
    if len(capas) != 1:
        raise RuntimeError(
            "Se necesita exactamente una capa cargada con el nombre {!r}; encontradas: {}."
            .format(capa_entrada, len(capas))
        )
    capa = capas[0]
    if not es_capa_vectorial_valida(capa):
        raise RuntimeError("La capa {!r} debe ser vectorial y válida.".format(capa_entrada))
    return capa, False


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

    proyecto = QgsProject.instance()
    capa, es_archivo_externo = resolver_capa_entrada(
        RUTA_ENTRADA,
        CAPA_ENTRADA,
        proyecto,
        QgsVectorLayer,
        lambda candidata: isinstance(candidata, QgsVectorLayer) and candidata.isValid(),
    )
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
    if SOLO_PREVISUALIZAR:
        print("Previsualización solicitada. No se modificó la capa.")
        return

    mensaje = (
        "Se preparará la eliminación de estos campos en {!r}:\n\n{}\n\n"
        "Los cambios quedarán sin guardar en QGIS para su revisión. ¿Continuar?"
    )
    respuesta = QMessageBox.question(
        None,
        "Confirmar limpieza de campos",
        mensaje.format(capa.name(), "\n".join(nombres_candidatos)),
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No,
    )
    if respuesta != QMessageBox.Yes:
        print("Operación cancelada. No se modificó la capa.")
        return

    capa_agregada_al_proyecto = False
    if es_archivo_externo:
        if proyecto.addMapLayer(capa) is None:
            raise RuntimeError("QGIS no pudo añadir la capa externa al proyecto para revisarla.")
        capa_agregada_al_proyecto = True

    try:
        edicion_iniciada = capa.startEditing()
    except Exception as error:
        if capa_agregada_al_proyecto:
            proyecto.removeMapLayer(capa.id())
        raise RuntimeError("QGIS no pudo iniciar la edición: {}".format(error)) from error
    if not edicion_iniciada:
        if capa_agregada_al_proyecto:
            proyecto.removeMapLayer(capa.id())
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
        if capa_agregada_al_proyecto:
            proyecto.removeMapLayer(capa.id())
        raise RuntimeError("Se revirtió la edición: {}".format(error)) from error

    print("Campos preparados para eliminar: {}".format(", ".join(nombres_candidatos)))
    print("Campos conservados: {}".format(", ".join(nombres_conservados) or "ninguno"))
    print("La edición sigue abierta. Revisa la capa y guarda o descarta los cambios en QGIS.")


if __name__ == "__main__":
    try:
        ejecutar()
    except (OSError, RuntimeError, TypeError, ValueError) as error:
        print("Limpieza detenida: {}".format(error))
