# 🧠 CodingGiants Auto-Booking Bot

Este script automatiza la reserva de clases *DemonstrationLesson1On1Online* en la plataforma de [CodingGiants España](https://registration.codinggiants.es/), seleccionando automáticamente las clases según los filtros indicados y omitiendo aquellas ya reservadas (resaltadas en amarillo) o en fines de semana.

---

## 🚀 Funcionalidades

- Inicia sesión automáticamente en tu cuenta.
- Selecciona el semestre **Summer 2025** y el tipo de curso **DemonstrationLesson1On1Online**.
- Elige el día del mes que vos indiques.
- Reserva todas las clases disponibles, **evitando**:
  - Las que ya están reservadas (fondo amarillo).
  - Las que caen en sábado o domingo.
- Navega por múltiples páginas de resultados.

---

## 🛠️ Requisitos

- Python 3.7 o superior
- Google Chrome instalado
- ChromeDriver compatible con tu versión de Chrome

### Instalación de dependencias

```bash
pip install selenium
