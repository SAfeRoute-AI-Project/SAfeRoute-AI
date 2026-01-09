import os
import osmnx as ox
import firebase_admin
from firebase_admin import credentials, firestore

class SafeGuardEnv:
    def __init__(self):
        # Percorso dinamico per la chiave Firebase
        current_dir = os.path.dirname(os.path.abspath(__file__))
        key_path = os.path.join(current_dir, "safeguard-c08-firebase-adminsdk-fbsvc-54e53643c3.json")

        try:
            firebase_admin.get_app()
        except ValueError:
            # Inizializzazione connessione al database Firestore
            cred = credentials.Certificate(key_path)
            firebase_admin.initialize_app(cred)
            print("Connessione a Firebase stabilita!")

        self.db = firestore.client()
        self.graph = None

    # Genera e salva la mappa GIS della Provincia di Salerno
    def download_salerno_map(self):
        print("Scaricamento mappa (Provincia di Salerno)...")
        # Download grafo stradale guidabile
        self.graph = ox.graph_from_place("Provincia di Salerno, Italy", network_type='drive')

        # Esportazione in formato GraphML per uso offline del team
        ox.save_graphml(self.graph, "salerno_map.graphml")
        print("Mappa salvata con successo!")

    # Recupera ospedali e zone sicure mappandoli sui nodi del grafo
    def get_points_from_firestore(self):
        punti_mappati = []
        collezioni = ['hospitals', 'safe_points']

        for col in collezioni:
            docs = self.db.collection(col).stream()
            for doc in docs:
                d = doc.to_dict()
                lat, lng, nome = d.get('lat'), d.get('lng'), d.get('name')

                if lat and lng:
                    try:
                        # Associa coordinate GPS al nodo stradale più vicino
                        node = ox.nearest_nodes(self.graph, X=lng, Y=lat)
                        punti_mappati.append({
                            'id': doc.id,
                            'name': nome,
                            'type': col,
                            'node_id': node,
                            'coords': (lat, lng)
                        })
                    except Exception as err:
                        print(f"Errore mapping per {nome}: {err}")
        return punti_mappati

    # Simula l'ambiente dinamico basandosi sulle segnalazioni reali di emergenza
    def apply_disaster_manager(self):
        print("Analisi tipologia emergenze in corso...")
        emergenze = self.db.collection('active_emergencies').where('status', '==', 'active').stream()

        # Reset pesi standard (distanza reale)
        for u, v, k, attr in self.graph.edges(data=True, keys=True):
            attr['final_weight'] = attr['length']

        # Lista delle cause che rendono le strade impraticabili
        cause_bloccanti = ['terremoto', 'incendio', 'tsunami', 'alluvione', 'bomba']

        for doc in emergenze:
            em = doc.to_dict()
            tipo = em.get('type', '').lower() # Usiamo il minuscolo per evitare errori

            # Blocchiamo la viabilità solo per disastri ambientali
            if tipo in cause_bloccanti:
                e_lat, e_lng = em.get('lat'), em.get('lng')
                danger_node = ox.nearest_nodes(self.graph, X=e_lng, Y=e_lat)

                # Rendiamo le strade connesse molto "costose" per i navigatori
                for u, v, k, attr in self.graph.edges(danger_node, keys=True, data=True):
                    attr['final_weight'] = attr['length'] * 100

                print(f"ALLERTA {tipo.upper()}: Viabilità modificata presso nodo {danger_node}.")
            else:
                # Caso 'malessere' o 'sos generico': nessuna modifica al traffico
                print(f"INFO {tipo.upper()}: Segnalazione puntuale, nessuna restrizione stradale.")

        print("Disaster Manager: Grafo aggiornato correttamente.")

if __name__ == "__main__":
    try:
        # Esecuzione del setup dell'ambiente IA
        env = SafeGuardEnv()
        env.download_salerno_map()

        # Sincronizzazione POI (Punti di Interesse)
        punti = env.get_points_from_firestore()
        print(f"\nSincronizzazione completata! Trovati {len(punti)} punti totali.")

        # Simulazione dinamica per test algoritmi
        env.apply_disaster_manager()
        print("\nAmbiente IA pronto per il calcolo dei percorsi sicuri.")

    except Exception as e:
        print(f"ERRORE CRITICO: {e}")