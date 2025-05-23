import pandas as pd
import folium
import numpy as np
import branca

# Leer el archivo erasmus.xlsx
df = pd.read_excel('erasmus.xlsx')

# Centrar el mapa entre España peninsular y Canarias
m = folium.Map(location=[36.5, -6.0], zoom_start=6, tiles='OpenStreetMap')

def get_offset_coords(lat, lon, n, i, offset=0.0005):
    """Devuelve coordenadas desplazadas en círculo para n puntos, el i-ésimo marcador."""
    angle = 2 * np.pi * i / n
    return lat + offset * np.cos(angle), lon + offset * np.sin(angle)

# Agrupa por lat/lon para desplazar si hay solapamiento
grouped = df.groupby(['lat', 'long'])

for (lat, lon), group in grouped:
    n = len(group)
    for i, (_, row) in enumerate(group.iterrows()):
        # Si hay más de un marcador en el mismo punto, desplázalos
        if n > 1:
            lat_offset, lon_offset = get_offset_coords(lat, lon, n, i)
        else:
            lat_offset, lon_offset = lat, lon
        popup_html = (
            f"<b>Nombre:</b> {row['nombre']}<br>"
            f"<b>Universidad:</b> {row['universidad']}<br>"
            f"<b>Latitud:</b> {row['lat']}<br>"
            f"<b>Longitud:</b> {row['long']}"
        )
        folium.Marker(
            location=[lat_offset, lon_offset],
            popup=folium.Popup(popup_html, max_width=350, min_width=200),
            tooltip=row['universidad'],
            icon=folium.Icon(color='orange', icon='globe-europe', prefix='fa')
        ).add_to(m)

# Limitar el área visible (opcional)
m.fit_bounds([[27.5, -18.5], [44, 4]])

# Título flotante alineado a la izquierda
titulo_principal = "Movilidad Erasmus - HU Berlin"
titulo_html = f'''
<div style="
    position: fixed;
    top: 20px;
    left: 100px;
    z-index: 9999;
    background: rgba(255,255,255,0.95);
    padding: 10px 30px 6px 30px;
    border-radius: 10px;
    box-shadow: 2px 2px 8px #888;
    font-size: 18px;
    font-family: Arial, sans-serif;
    font-weight: bold;
    text-align: left;
    line-height: 1.2;
">
    {titulo_principal}
</div>
'''
m.get_root().html.add_child(branca.element.Element(titulo_html))

# HTML de las tablas actualizado, más pequeña y más abajo
# (el CSS se incluye en el div para que se aplique solo a las tablas flotantes)
tablas_html = """
<div id="tablas-erasmus" style="
    position: fixed;
    top: 90px;
    left: 60px;
    z-index: 9999;
    background: rgba(255,255,255,0.95);
    padding: 10px;
    border-radius: 10px;
    box-shadow: 2px 2px 8px #888;
    max-width: 400px;
    min-width: 320px;
    font-size: 12px;
    font-family: Arial, sans-serif;
">
<style>
#tablas-erasmus .table-container {
    background-color: rgba(255, 255, 255, 0.8);
    padding: 10px;
    margin-bottom: 18px;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
    width: fit-content;
}
#tablas-erasmus table {
    border-collapse: collapse;
    width: 100%;
    min-width: 300px;
}
#tablas-erasmus th, #tablas-erasmus td {
    border: 1px solid #333;
    padding: 5px 8px;
    text-align: center;
}
#tablas-erasmus th {
    background-color: #dddddd;
}
#tablas-erasmus caption, #tablas-erasmus .footnote {
    margin-top: 8px;
    font-size: 0.85em;
    text-align: left;
}
#tablas-erasmus h2 {
    margin-top: 0;
}
</style>
<h2 style="margin: 12px 0 8px 12px; font-size: 15px;">Spanien gesamt</h2>
<div class="table-container">
    <table>
        <caption><strong>Studierendenmobilität Erasmus+</strong></caption>
        <thead>
            <tr>
                <th></th>
                <th></th>
                <th>2021/22</th>
                <th>2022/23</th>
                <th>2023/24*</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td rowspan="3"><strong>Outgoing</strong></td>
                <td>Studium</td>
                <td>38</td>
                <td>72</td>
                <td>71</td>
            </tr>
            <tr>
                <td>Praktikum</td>
                <td>23</td>
                <td>11</td>
                <td>7</td>
            </tr>
            <tr>
                <td><strong>Gesamt</strong></td>
                <td><strong>61</strong></td>
                <td><strong>83</strong></td>
                <td><strong>78</strong></td>
            </tr>
            <tr>
                <td colspan="2"><strong>Incoming**</strong></td>
                <td>18</td>
                <td>18</td>
                <td>13</td>
            </tr>
        </tbody>
    </table>
    <div class="footnote">
        * Stand 04/2024, laufender Jahrgang<br>
        ** Praktika Incoming sind nicht erfasst
    </div>
</div>
<div class="table-container">
    <table>
        <caption><strong>Mitarbeitendenmobilität Erasmus+</strong></caption>
        <thead>
            <tr>
                <th></th>
                <th></th>
                <th>2021/22</th>
                <th>2022/23</th>
                <th>2023/24*</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td rowspan="3"><strong>Outgoing**</strong></td>
                <td>Lehre</td>
                <td>12</td>
                <td>1</td>
                <td>9</td>
            </tr>
            <tr>
                <td>Fort- und Weiterbildung</td>
                <td>9</td>
                <td>3</td>
                <td>1</td>
            </tr>
            <tr>
                <td><strong>Gesamt</strong></td>
                <td><strong>21</strong></td>
                <td><strong>4</strong></td>
                <td><strong>10</strong></td>
            </tr>
        </tbody>
    </table>
    <div class="footnote">
        * Stand 04/2024, laufender Jahrgang<br>
        ** Mobilitäten Incoming sind nicht erfasst<br>
        (Stand September 2024)
    </div>
</div>
</div>
"""

m.get_root().html.add_child(branca.element.Element(tablas_html))

# Guardar el mapa como HTML
m.save('maps/mapa_erasmus.html')

print("¡Mapa Erasmus+ generado a partir de erasmus.xlsx! Abre 'maps/mapa_erasmus.html' para verlo.")
