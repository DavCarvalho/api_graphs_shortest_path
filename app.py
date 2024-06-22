from fastapi import FastAPI, HTTPException, Query, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from pydantic import BaseModel
import osmnx as ox
import networkx as nx
import geopandas as gpd
from shapely.geometry import LineString, Point
import logging
import json
from plot_grafico import plot_route
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# Define the logger object
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="API para achar o caminho mais curto", description="API para cálculo de rotas mais curta entre os destinos", version="1.0")

# Allow CORS for frontend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carregar dados de amigos e locais de um arquivo JSON
with open('database.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    friends = data["friends"]
    places_salvador = data["places_salvador"]

class Location(BaseModel):  # Criar um modelo de dados para a localização usando o Pydantic
    latitude: float
    longitude: float

@app.get("/friends")  # Criar uma rota para retornar a lista de amigos
def get_friends():
    return friends

@app.get("/places_salvador")  # Criar uma rota para retornar a lista de locais em Salvador
def get_places_salvador():
    return places_salvador

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



@app.post("/shortest_path")
def caminho_mais_curto(latitude: float = Form(...), longitude: float = Form(...), destination: str = Form(...)):
    try:
        location = Location(latitude=latitude, longitude=longitude)
        # Combinar amigos e lugares em um único dicionário
        combined_locations = {**friends, **places_salvador}

        if destination not in combined_locations:
            raise HTTPException(status_code=404, detail="Destino não encontrado")

        # Coordenadas do destino
        dest_coords = combined_locations[destination]

        # Log de coordenadas
        logger.info(f"Origem: ({location.latitude}, {location.longitude})")
        logger.info(f"Destino: ({dest_coords['latitude']}, {dest_coords['longitude']})")

        # aqui em vez de baixar a área de uma cidade ou salvador inteira vamos baixar apenas a área necessária economizando recursos
        # Determinar o ponto central e a distância máxima para a área de interesse
        #O propósito desse cálculo é garantir que a área de interesse 
        # seja grande o suficiente para incluir tanto a origem quanto o destino. Essa área é então usada para baixar a rede viária, 
        # garantindo que ambos os pontos estejam dentro do grafo viário.
        center_lat = (location.latitude + dest_coords["latitude"]) / 2
        center_lon = (location.longitude + dest_coords["longitude"]) / 2
        max_dist = max(abs(location.latitude - dest_coords["latitude"]), abs(location.longitude - dest_coords["longitude"])) * 111320  # Converter para metros

        # Baixar a rede viária dentro do raio calculado ao redor do ponto central
        G = ox.graph_from_point((center_lat, center_lon), dist=max_dist, network_type='drive')

        # Verificar se o grafo foi criado corretamente
        if not G:
            raise HTTPException(status_code=500, detail="Não foi possível criar o grafo da área especificada. Verifique as coordenadas.")

        # adicionar informações adicionais às arestas (ruas) do grafo 
        # Adicionar velocidades às arestas
        G = ox.routing.add_edge_speeds(G)
        #a velocidade é usada para calcular o tempo de viagem, que então se torna o peso final utilizado no algoritmo de Dijkstra
        # Adicionar tempos de viagem às arestas com base nas velocidades
        # Tempo de Viagem como Peso
        #O tempo de viagem é crucial para calcular a rota mais rápida entre dois pontos. 
        # Usar apenas distâncias geográficas não leva em conta a velocidade das ruas, e uma rua mais longa pode ser mais rápida se tiver uma velocidade maior.
       # tempo_de_viagem= velocidade_da_aresta / comprimento_da_aresta
        G = ox.routing.add_edge_travel_times(G)

        # Encontrar os nós mais próximos para origem e destino
        orig_node = ox.distance.nearest_nodes(G, location.longitude, location.latitude)
        dest_node = ox.distance.nearest_nodes(G, dest_coords["longitude"], dest_coords["latitude"])

        # Calcular o caminho mais curto usando o algoritmo de caminho mais curto de networkx
        shortest_path = nx.shortest_path(G, orig_node, dest_node, weight='travel_time')

        # Plotar o gráfico e salvar a imagem
        output_path_html, output_path_png = plot_route(G, shortest_path, location, dest_coords, destination)
        logger.info(f"Generated paths: HTML - {output_path_html}, PNG - {output_path_png}")
        # Retornar os caminhos das imagens como resposta
        return {
           "html_path": f"/static/{output_path_html}",
            "png_path": f"/static/{output_path_png}"
        }
    
    except Exception as e:
        logger.error(f"Erro ao calcular o caminho mais curto: {e}")
        raise HTTPException(status_code=500, detail="Erro ao calcular o caminho mais curto.")
    
# Execução
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", port=8000, reload=True)
