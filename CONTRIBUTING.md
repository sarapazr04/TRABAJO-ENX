# Guía de Contribución

Este documento describe las normas de colaboración, estilo de código y flujo de trabajo a seguir en este proyecto.  
El objetivo es mantener un desarrollo limpio, colaborativo y trazable mediante GitHub y la metodología **Scrum**.

---

## Normas básicas de uso del repositorio

**Flujo principal: GitHub Flow**

- Todo el código debe enviarse a través de GitHub (nunca por correo, WhatsApp, etc.).
- Los nombres de las ramas deben ser **cortos pero descriptivos**, usando guiones bajos `_` para separar palabras.
- Cada **nueva funcionalidad** se desarrollará en su **propia rama** con el prefijo:
  - `feature/nueva_funcion`
- Las **ramas de lanzamiento** se nombrarán como:
  - `release/nombre_rama`
- Las **correcciones de errores** usarán el prefijo:
  - `bugfix/nombre_funcion_mal`
- **No se permite hacer `push` directo a `main`**: todos los cambios se integrarán mediante **Pull Requests (PRs)**.
- **Ningún PR se mergea sin revisión previa**, que incluirá:
  - Revisión de código
  - Ejecución de pruebas
  - Revisión de documentación
- El revisor **no modifica el código**, solo deja comentarios o sugerencias.
- El **Scrum Master** autoriza el *merge* tras la revisión.
- Evitar subir código erróneo o que no pase las pruebas automatizadas.

---

## Estilo de los mensajes de *commit*

- **Idioma:** español.
- **Forma:** infinitivo o sustantivo, conciso y descriptivo.  
  Ejemplos:
  - `añadir función de carga de CSV`
  - `actualizar interfaz gráfica`
  - `corrección en cálculo de regresión`
- Es recomendable usar *commits* pequeños y frecuentes para mantener la trazabilidad.

---

## Procedimiento para modificar el README o la documentación

- Los cambios en la documentación se realizan en el directorio `docs/`.  
  Allí se guardan todos los archivos de documentación detallada:
  - Manual de usuario (más extenso que el `README`).
  - Guías de instalación/despliegue.
  - Diagramas de arquitectura.
  - Tutoriales o ejemplos de uso.
  - Notas técnicas, etc.
- Usar **Markdown** con listas, títulos y ejemplos de código.
- Revisar el formato antes de hacer *merge*.
- **Imágenes:** deben comprimirse antes de subirlas para no sobrecargar el repositorio.  
  - Usar `.jpg` o `.png` comprimido.  
  - Se pueden usar herramientas como [Squoosh](https://squoosh.app/) de Google.

---

## Flujo de trabajo colaborativo con ramas y revisiones

1. Crear rama desde `main`.
2. Implementar los cambios.
3. Hacer *commit*.
4. Subir la rama y abrir un **Pull Request (PR)**.
5. Otro miembro revisa y aprueba (*peer review*), comparando lo anterior con lo modificado.
6. Tras aprobación, se hace *merge* a `main`.

**Notas:**
- Ningún PR se mergea sin revisión inicial (código, pruebas y documentación).
- El compañero revisor NO cambia el código: solo deja comentarios o sugerencias.
- El autor del PR es responsable de resolver los conflictos que surjan.

---

## Estilo de código (PEP-8)

- **Indentación:** 4 espacios (NO tabulador).  
  Se recomienda usar `flake8` para comprobación.
- **Nombres:**
  - Variables y funciones en **minúsculas**.
  - Clases con **Mayúscula inicial**.
- **Líneas:** máximo **79 caracteres**.
- **Comentarios y documentación:**
  - Usar **docstrings** `"""..."""` en funciones, clases y métodos.
  - Explicar objetivo, argumentos y valores de retorno (no describir línea a línea el código).
- **Importaciones:** ordenadas en este orden:
  1. Librerías estándar de Python
  2. Librerías externas
  3. Módulos internos del proyecto

---
