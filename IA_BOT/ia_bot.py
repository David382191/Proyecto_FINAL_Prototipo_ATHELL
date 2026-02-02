from flask import Flask, render_template, Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime
import os
from database.db import get_db
import openai
 
import psycopg2
from psycopg2.extras import RealDictCursor

#############################################################################
# Blueprint
bot_bp = Blueprint("bot_bp", __name__)
#############################################################################
# Leer la API Key desde variables de entorno
openai.api_key = os.environ.get("OPENAI_API_KEY")
#############################################################################
# Función para responder usando OpenAI
def responder_ia(texto):
    print("LLamando a OpenAI con:", texto)
    respuesta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user","content": texto}]
    )
    print("Respuesta de OpenAI:", respuesta.choices[0].message.content)
    return respuesta.choices[0].message.content
#############################################################################
# Endpoint de WhatsApp
@bot_bp.route("/bot", methods=["GET","POST"])
def whatsapp_bot():
    mensaje_usuario = request.form.get("Body", "").strip()

    # Obtener o crear conversación
    id_conv = obtener_conversacion()
    guardar_mensaje(id_conv, "usuario", mensaje_usuario)

    # Revisar palabra clave
    respuesta = buscar_palabra_clave(mensaje_usuario)

    # Si no hay palabra clave → IA
    if not respuesta:
        respuesta = responder_ia(mensaje_usuario)

    guardar_mensaje(id_conv, "bot", respuesta)

    # Responder a Twilio
    resp = MessagingResponse()
    resp.message(respuesta)

    return str(resp)
#############################################################################
def buscar_palabra_clave(texto_usuario):
    conn = get_db()
    cursor = conn.cursor()

    # Convertimos todo a minúsculas para insensibilidad
    query = """
        SELECT respuesta_designada
        FROM PALABRA_CLAVE
        WHERE LOWER(Palabra) LIKE '%' || LOWER(%s) || '%';
    """
    cursor.execute(query, (texto_usuario,))
    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    if resultado:
        return resultado[0]
    return None

#############################################################################
def guardar_mensaje(id_conversacion, remitente, contenido):
    conn = get_db()
    cursor = conn.cursor()

    query = """
        INSERT INTO mensaje (id_conversacion, remitente, contenido, fecha_hora)
        VALUES (%s, %s, %s, %s)
    """

    cursor.execute(query, (
        id_conversacion,
        remitente,
        contenido,
        datetime.now()
    ))

    conn.commit()
    cursor.close()
    conn.close()
#############################################################################
def obtener_conversacion():
    conn = get_db()
    cursor = conn.cursor()

    # Ver si hay alguna conversación en curso
    cursor.execute("SELECT ID_CONVERSACION FROM CONVERSACION ORDER BY ID_CONVERSACION DESC LIMIT 1")
    fila = cursor.fetchone()

    if fila:
        id_conv = fila[0]
    else:
        # Crear una nueva conversación y obtener el ID generado
        cursor.execute("""
            INSERT INTO CONVERSACION (usuario, fecha_hora)
            VALUES (%s, %s)
            RETURNING ID_CONVERSACION
        """, ("usuario_principal", datetime.now()))
        id_conv = cursor.fetchone()[0]  # Obtenemos el ID retornado
        conn.commit()

    cursor.close()
    conn.close()
    return id_conv
#############################################################################