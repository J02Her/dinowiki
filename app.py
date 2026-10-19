"""
DinoWiki - Mini Enciclopedia Web sobre Dinosaurios
Proyecto Final de Programacion - Flask
Estudiante: Josue Salazar - Seccion 10-8
Profesor: Gilberth Antonio Mora Guzman

Este archivo contiene toda la logica del servidor (rutas de Flask) y el
sistema CRUD (Crear, Leer, Actualizar, Eliminar) que trabaja sobre el
archivo data/dinosaurios.json, el cual funciona como "base de datos".
"""

import json
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Ruta absoluta al archivo JSON que guarda todos los dinosaurios
RUTA_JSON = os.path.join(os.path.dirname(__file__), "data", "dinosaurios.json")


# ---------------------------------------------------------------------
# FUNCIONES DE APOYO PARA LEER Y ESCRIBIR EL ARCHIVO JSON
# ---------------------------------------------------------------------

def leer_dinosaurios():
    """Lee el archivo JSON y devuelve la lista de dinosaurios (lista de dicts)."""
    if not os.path.exists(RUTA_JSON):
        return []
    with open(RUTA_JSON, "r", encoding="utf-8") as archivo:
        try:
            return json.load(archivo)
        except json.JSONDecodeError:
            return []


def guardar_dinosaurios(lista_dinosaurios):
    """Escribe la lista completa de dinosaurios de vuelta en el archivo JSON."""
    with open(RUTA_JSON, "w", encoding="utf-8") as archivo:
        json.dump(lista_dinosaurios, archivo, indent=2, ensure_ascii=False)


def obtener_siguiente_id(lista_dinosaurios):
    """Genera un id único nuevo (el mayor id existente + 1)."""
    if not lista_dinosaurios:
        return 1
    return max(d["id"] for d in lista_dinosaurios) + 1


def buscar_dinosaurio_por_id(lista_dinosaurios, id_buscado):
    """Devuelve el diccionario del dinosaurio con ese id, o None si no existe."""
    for dinosaurio in lista_dinosaurios:
        if dinosaurio["id"] == id_buscado:
            return dinosaurio
    return None


# ---------------------------------------------------------------------
# RUTAS DE LA APLICACIÓN
# ---------------------------------------------------------------------

@app.route("/")
def inicio():
    """Página de inicio: presentación general de DinoWiki."""
    dinosaurios = leer_dinosaurios()
    total = len(dinosaurios)
    return render_template("index.html", total=total)


@app.route("/catalogo")
def catalogo():
    """LEER (Read): muestra la tabla con todos los dinosaurios registrados."""
    dinosaurios = leer_dinosaurios()
    return render_template("catalogo.html", dinosaurios=dinosaurios)


@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    """CREAR (Create): muestra el formulario y guarda un nuevo dinosaurio."""
    if request.method == "POST":
        dinosaurios = leer_dinosaurios()

        nuevo_dinosaurio = {
            "id": obtener_siguiente_id(dinosaurios),
            "nombre": request.form.get("nombre", "").strip(),
            "periodo": request.form.get("periodo", "").strip(),
            "alimentacion": request.form.get("alimentacion", "").strip(),
            "tamano": request.form.get("tamano", "").strip(),
            "descripcion": request.form.get("descripcion", "").strip(),
        }

        dinosaurios.append(nuevo_dinosaurio)
        guardar_dinosaurios(dinosaurios)

        return redirect(url_for("catalogo"))

    # Si es GET, solo se muestra el formulario vacío
    return render_template("registrar.html")


@app.route("/editar/<int:id_dinosaurio>", methods=["GET", "POST"])
def editar(id_dinosaurio):
    """ACTUALIZAR (Update): muestra el formulario precargado y guarda los cambios."""
    dinosaurios = leer_dinosaurios()
    dinosaurio = buscar_dinosaurio_por_id(dinosaurios, id_dinosaurio)

    if dinosaurio is None:
        return redirect(url_for("catalogo"))

    if request.method == "POST":
        dinosaurio["nombre"] = request.form.get("nombre", "").strip()
        dinosaurio["periodo"] = request.form.get("periodo", "").strip()
        dinosaurio["alimentacion"] = request.form.get("alimentacion", "").strip()
        dinosaurio["tamano"] = request.form.get("tamano", "").strip()
        dinosaurio["descripcion"] = request.form.get("descripcion", "").strip()

        guardar_dinosaurios(dinosaurios)
        return redirect(url_for("catalogo"))

    # Si es GET, se muestra el formulario con los datos actuales cargados
    return render_template("editar.html", dinosaurio=dinosaurio)


@app.route("/eliminar/<int:id_dinosaurio>", methods=["POST"])
def eliminar(id_dinosaurio):
    """ELIMINAR (Delete): borra un dinosaurio del archivo JSON por su id."""
    dinosaurios = leer_dinosaurios()
    dinosaurios_filtrados = [d for d in dinosaurios if d["id"] != id_dinosaurio]
    guardar_dinosaurios(dinosaurios_filtrados)
    return redirect(url_for("catalogo"))


if __name__ == "__main__":
    app.run(debug=True)
