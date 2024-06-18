import folium
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import contextily as ctx
import geopandas as gpd
from shapely.geometry import LineString, Point
import os
import osmnx as ox

def plot_route(G, shortest_path, location, dest_coords, destination):
    # Converter o caminho mais curto para um GeoDataFrame
    nodes, edges = ox.graph_to_gdfs(G)
    route_nodes = nodes.loc[shortest_path]
    route_line = LineString(list(route_nodes.geometry.apply(lambda point: (point.x, point.y))))
    route_gdf = gpd.GeoDataFrame(geometry=[route_line], crs=nodes.crs)

    # Garantir que o diretório 'static' existe
    if not os.path.exists("static"):
        os.makedirs("static")

    # Criar o mapa base com Folium
    m = folium.Map(location=[location.latitude, location.longitude], zoom_start=12)

    # Adicionar a rota ao mapa
    folium.GeoJson(route_gdf).add_to(m)

    # Adicionar pontos de início e fim ao mapa
    folium.Marker([location.latitude, location.longitude], tooltip='Minha Localização', icon=folium.Icon(color='green')).add_to(m)
    folium.Marker([dest_coords["latitude"], dest_coords["longitude"]], tooltip=destination, icon=folium.Icon(color='blue')).add_to(m)

    # Salvar o mapa em um arquivo HTML
    output_path_html = "static/route.html"
    m.save(output_path_html)

    # Agora, também criar o gráfico com Matplotlib
    fig, ax = plt.subplots(figsize=(10, 10), dpi=100)

    # Reprojetar para coordenadas Web Mercator
    route_gdf = route_gdf.to_crs(epsg=3857)
    edges = edges.to_crs(epsg=3857)
    nodes = nodes.to_crs(epsg=3857)

    # Adicionar mapa de fundo detalhado
    ctx.add_basemap(ax, crs=route_gdf.crs.to_string(), source=ctx.providers.OpenStreetMap.Mapnik, zoom=12)

    # Plotar a rota
    route_gdf.plot(ax=ax, color='red', linewidth=2, zorder=5)

    # Plotar todos os nós e arestas do grafo para depuração
    edges.plot(ax=ax, linewidth=1, alpha=0.3, color='gray')
    nodes.plot(ax=ax, markersize=2, color='black')

    # Plotar a localização atual e a localização do destino
    location_point = gpd.GeoDataFrame(geometry=[Point(location.longitude, location.latitude)], crs="EPSG:4326")
    dest_point = gpd.GeoDataFrame(geometry=[Point(dest_coords["longitude"], dest_coords["latitude"])], crs="EPSG:4326")

    location_point = location_point.to_crs(epsg=3857)
    dest_point = dest_point.to_crs(epsg=3857)

    ax.scatter(location_point.geometry.x, location_point.geometry.y, color='green', marker='o', s=100, zorder=5)
    ax.scatter(dest_point.geometry.x, dest_point.geometry.y, color='blue', marker='o', s=100, zorder=5)

    # Adicionar rótulos para as localizações
    ax.text(location_point.geometry.x.iloc[0], location_point.geometry.y.iloc[0], 'Minha Localização', fontsize=12, ha='right', zorder=6, bbox=dict(facecolor='white', alpha=0.6, edgecolor='none', pad=1))
    ax.text(dest_point.geometry.x.iloc[0], dest_point.geometry.y.iloc[0], destination, fontsize=12, ha='right', zorder=6, bbox=dict(facecolor='white', alpha=0.6, edgecolor='none', pad=1))

    # Ajustar a visualização para garantir que a rota esteja visível
    ax.set_xlim(route_gdf.total_bounds[0] - 1000, route_gdf.total_bounds[2] + 1000)
    ax.set_ylim(route_gdf.total_bounds[1] - 1000, route_gdf.total_bounds[3] + 1000)

    # Salvar a imagem do caminho
    output_path_png = "static/route.png"
    plt.savefig(output_path_png)
    plt.close()

    return output_path_html, output_path_png
