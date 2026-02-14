# SAfeRoute AI - Intelligent Emergency Navigation Module 

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![License](https://img.shields.io/badge/License-GPL--3.0-red)

## Indice
1. [Panoramica](#1-panoramica)
2. [Scopo del Modulo](#2-scopo-del-modulo)
3. [Architettura dell'IA](#3-architettura-dellia)
4. [Stack Tecnologico](#4-stack-tecnologico)
5. [Struttura del Repository](#5-struttura-del-repository)
6. [Guida all'Avvio](#6-guida-allavvio)
7. [Team di Sviluppo](#7-team-di-sviluppo)

## 1. Panoramica

**SAfeRoute AI** nasce come modulo evolutivo e integrazione avanzata del progetto [**SAfeGuard**](https://github.com/SAfeGuard2025/SAfeGuard), 
dal quale eredita l'infrastruttura di monitoraggio e la base dati delle emergenze. 

Mentre il sistema **SAfeGuard** si occupa della segnalazione e gestione passiva dei pericoli, **SAfeRoute AI** introduce uno strato di **agentività razionale**: trasforma le informazioni statiche in percorsi di evacuazione dinamici, ottimizzando la sicurezza dell'utente attraverso algoritmi di pathfinding su grafi stradali reali.

---

## 2. Scopo del Modulo

Il modulo AI di SAfeRoute serve a:

- **Rilevare emergenze:** Identificare la localizzazione e il tipo di pericolo
- **Localizzare utenti:** Determinare la posizione dell'utente nell'area interessata
- **Calcolare rotte sicure:** Generare il percorso più efficiente verso zone sicure
- **Consigliare in tempo reale:** Fornire navigazione guidata per l'evacuazione

---

## 3. Architettura dell'IA

### 3.1 Flusso dei Dati
Il modulo opera secondo un ciclo di percezione-ragionamento-azione:

- **Percezione:** Interroga Firebase Firestore per ottenere lo stato delle emergenze e l'ultima posizione GPS nota dell'utente.
- **Modellazione Ambientale:** Il Disaster Manager proietta le emergenze sul grafo stradale. Se l'evento è ostruente, viene creata una "Zona Rossa" invalidando i nodi stradali.
- **Calcolo Strategico:** Gli algoritmi di pathfinding elaborano la rotta ottimale pesando la distanza fisica contro il rischio ambientale.

### 3.2 Algoritmi implementati
Il sistema non si affida alla semplice distanza in linea d'aria per la navigazione. Utilizza una pipeline a tre stadi per garantire precisione e velocità computazionale.

1) **Pre-Selezione:** Il sistema esegue una pre-selezione calcolando la distanza lineare tra l'utente e tutti i Safe Points disponibili. Seleziona esclusivamente i 5 punti più vicini per facilitare il calcolo e diminuire i tempi di esecuzione.
2) **Dijkstra Standard:** Viene calcolato il percorso ottimale teorico utilizzando l'algoritmo di Dijkstra classico. In quasto modo si determina il cammino minimo basato unicamente sulla lunghezza fisica degli archi.
3) **Dijkstra Bidirezionale:** Implementa una ricerca simultanea dalla sorgente (utente) e dalla destinazione (punto sicuro). La ricerca si interrompe quando le due frontiere si incontrano e viene soddisfatta la condizione di ottimalità, riducendo il numero di nodi esplorati.

---

## 4. Stack Tecnologico
In questa sezione chiariamo le tecnologie utilizzate specificamente per far girare il "cervello" dell'agente.

| Componente | Tecnologia | Ruolo |
| :--- | :--- | :--- |
| **Backend AI** | FastAPI | Framework ad alte prestazioni per servire i calcoli di routing in formato JSON. |
| **Geospatial Engine** | OSMnx / NetworkX | Modellazione, manipolazione e analisi topologica dei grafi stradali urbani. |
| **Real-time Data** | Firebase Admin SDK | Sincronizzazione asincrona con il database Firestore per la cattura delle emergenze. |
| **Map Data** | OpenStreetMap | Sorgente dei dati topografici ad alta precisione della Provincia di Salerno. |

---

## 5. Struttura del Repository

Il microservizio è organizzato in moduli specializzati per separare la gestione dei dati geografici dalla logica di pathfinding:

* **`main.py`**: Rappresenta l'entry point del server **FastAPI**. Gestisce le richieste POST provenienti dall'app mobile, coordina la fase di **Pre-Selezione** dei punti sicuri e orchestra l'invio dei percorsi calcolati.
* **`enviroment.py`**: È il cuore dell'integrazione dati. Si occupa di:
    * Caricare e normalizzare il grafo stradale della Provincia di Salerno (`.graphml`).
    * Gestire la connessione asincrona con **Firebase Admin SDK**.
    * Implementare il **Disaster Manager** per l'iniezione dinamica dei pesi nelle "Zone Rosse".
* **`algorithms.py`**: Contiene le implementazioni core degli algoritmi di ricerca:
    * **Pipeline 1**: Dijkstra Standard.
    * **Pipeline 2**: **Dijkstra Bidirezionale**, ottimizzato con una condizione di stop basata sulla migliore soluzione attuale per garantire l'ottimalità del percorso sicuro in tempi millesimali.

---

## 6. Guida all'Avvio

Questa sezione descrive i passaggi per configurare ed eseguire il motore di Intelligenza Artificiale basato su Python.

### 6.1. Installazione delle Librerie Core
Assicurati di avere Python (versione 3.8 o superiore) installato. Apri il terminale nella cartella `backend/ai_engine` ed esegui il seguente comando per installare tutti i moduli necessari al funzionamento dell'agente:

```bash
pip install osmnx networkx fastapi uvicorn firebase-admin pandas geopandas matplotlib scipy
```

### 6.2. Navigazione ed Esecuzione
Una volta completata l'installazione delle librerie, è necessario posizionarsi nella directory corretta ed avviare il server. Segui questi passaggi:

```bash
# Entra nella cartella del modulo AI
cd backend/ai_engine

# Avvia lo script principale
python main.py
```

**ATTENZIONE:** Al primo avvio potrebbe volerci qualche minuto a causa del caricamento del file .graphml contenente l'intero grafo della provincia di Salerno.

---

## 7. Team di Sviluppo
Progetto realizzato per il corso di Fondamenti di Intelligenza Artificiale (Prof. Fabio Palomba) presso l'Università degli Studi di Salerno - A.A. 2025/2026.

- **Team composto da:**
  
  - Aquilone Gianpaolo
  - Di Palma Gabriele
  - Zambrino Francesco
  - Zazzerini Giorgio
