# makeAutomatic

Sitio web creado en Django como carta de presentación técnica para la empresa **makeAutomatic**. Incluye contenido básico y un formulario de contacto funcional.

---

## Requisitos

- Python 3.8+
- pip
- Entorno virtual recomendado (`venv`)

---

## Instalación y ejecución local

1. **Clona o descomprime este repositorio**

```bash
unzip makeAutomatic_django_con_estilos.zip
cd makeAutomatic
```

2. **Crea un entorno virtual y actívalo**

```bash
python -m venv env
source env/bin/activate      # En Linux/Mac
env\Scripts\activate.bat   # En Windows
```

3. **Instala Django**

```bash
pip install django
```

4. **Ejecuta las migraciones**

```bash
python manage.py migrate
```

5. **Inicia el servidor**

```bash
python manage.py runserver
```

6. Abre tu navegador y visita: `http://127.0.0.1:8000/`

---

## Configuración del correo

Por defecto, los mensajes del formulario se imprimen en consola (modo desarrollo). Para habilitar envío real, edita `makeautomatic/settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tucorreo@gmail.com'
EMAIL_HOST_PASSWORD = 'tucontraseña'
```

---

## Estructura

- `home`, `servicios`, `portafolio`, `contacto`: páginas básicas
- `formulario de contacto`: funcional y validado
- `templates`: sistema de herencia con `base.html`
- `static/css/style.css`: estilos personalizados

---

## Autor

Desarrollado por **Paulo Toro** usando Django.
