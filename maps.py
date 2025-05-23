import pandas as pd
import folium
import branca
from folium.plugins import MarkerCluster

# Leer el archivo principal
df = pd.read_excel('database_con_coordenadas.xlsx')

# Definir áreas y colaboraciones
areas = ['Lingüística', 'Literatura y didáctica']
colab_types = ['Docencia', 'Investigación']

def get_marker_style(colab_type):
    style_map = {
        'Docencia':      {'color': 'blue',    'icon': 'chalkboard-teacher'},
        'Investigación': {'color': 'cadetblue', 'icon': 'flask'},
    }
    return style_map.get(colab_type, {'color': 'gray', 'icon': 'university'})

for area in areas:
    for colab in colab_types:
        df_filtered = df[(df['área'] == area) & (df['colaboración'] == colab)]
        if df_filtered.empty:
            continue

        m = folium.Map(location=[36.5, -6.0], zoom_start=6, tiles='OpenStreetMap')

        # Create a MarkerCluster for this map
        marker_cluster = MarkerCluster().add_to(m)

        # Add markers to the cluster
        for _, row in df_filtered.iterrows():
            marker_style = get_marker_style(colab)

            popup_html = (
                f"<b>Área:</b> {area}<br>"
                f"<b>Universidad:</b> {row['universidad']}<br>"
                f"<b>Colaboración:</b> {colab}<br>"
                f"<b>Nombre:</b> {row['nombre']}<br>"
                f"<b>Detalle:</b> {row['detalle']}"
            )

            folium.Marker(
                location=[row['lat'], row['long']],
                popup=folium.Popup(popup_html, max_width=350, min_width=200),
                tooltip=row['universidad'],
                icon=folium.Icon(color=marker_style['color'], icon=marker_style['icon'], prefix='fa')
            ).add_to(marker_cluster)

        m.fit_bounds([[27.5, -18.5], [44, 4]])

        # Título principal y subtítulo
        # titulo_principal = "Proyectos / cooperaciones del Institut für Romanistik con colegas en España"
        # subtitulo = f"{area} – {colab}"
        # titulo_html = f'''
        # <div style="
        #     position: fixed;
        #     top: 20px;
        #     left: 110px;
        #     z-index: 9999;
        #     background: rgba(255,255,255,0.95);
        #     padding: 10px 30px 6px 30px;
        #     border-radius: 10px;
        #     box-shadow: 2px 2px 8px #888;
        #     font-size: 18px;
        #     font-family: Arial, sans-serif;
        #     font-weight: bold;
        #     text-align: left;
        #     line-height: 1.2;
        # ">
        #     {titulo_principal}<br>
        #     <span style="font-size: 15px; font-weight: bold; color: #2a4d8f;">{subtitulo}</span>
        # </div>
        # '''
        # m.get_root().html.add_child(branca.element.Element(titulo_html))

        # Guardar el mapa con nombre descriptivo
        filename = f"maps/mapa_{area.lower().replace(' ', '_')}_{colab.lower().replace(' ', '_')}.html"
        m.save(filename)
        print(f"¡Mapa generado: {filename}!")
