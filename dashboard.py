#C:\Users\Maxi\AppData\Local\Programs\Python\Python312\Scripts\streamlit.exe run "c:/Users/Maxi/uni/semester 4/dashboard.py"

import streamlit as st
import requests
from datetime import datetime, timedelta, date
import pandas as pd

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

#dashboard title
st.title(f'Interaktives Wetterdashboard von Maxi')

# sidebar

st.sidebar.title("Navigation")
seite = st.sidebar.selectbox("Wähle eine Seite:",["Dashboard","Über mich"])
datum = st.sidebar.date_input("Wähle den Startzeitpunkt der betrachtung",
                            value=datetime.today().date() - timedelta(days=90))
stadtname = st.sidebar.text_input("Wähle eine Stadt aus.")


#Api für Stadt in Koordinaten konvertieren
#bekomme stadtname über sidebar
geo_url = "https://geocoding-api.open-meteo.com/v1/search"
geo_params = {"name": stadtname, "count":1, "language":"de", "format":"json"}
geo_response = requests.get(geo_url,params=geo_params)
geo_data = geo_response.json()

if not geo_data.get("results"):
    display_data = False
else:
    result = geo_data["results"][0]
    lat, lon = result["latitude"], result["longitude"]
    name = result["name"]
    country = result.get("country", "")

#Zeitraum berechnen:
    tage = (date.today() - datum).days
    end_date = datetime.utcnow().date()
    start_date = end_date  - timedelta(days=tage)

# Api für Wetterdaten:
    wetter_url = "https://api.open-meteo.com/v1/forecast"
    wetter_hist_url = "https://archive-api.open-meteo.com/v1/archive"
    wetter_params = {
        "latitude": lat,
        "longitude": lon,
        "current": [
            "temperature_2m",
            "precipitation",
            "wind_speed_10m",
            "relative_humidity_2m",
            "weather_code"
        ],
        "timezone": "Europe/Berlin"
    }
    wetter_hist_params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "hourly": [
            "temperature_2m",
            "precipitation",
            "wind_speed_10m",
            "relative_humidity_2m"
        ],
        "timezone": "Europe/Berlin"
    }

    wetter_response = requests.get(wetter_url,params=wetter_params)
    wetter_data = wetter_response.json()

    wetter_hist_response = requests.get(wetter_hist_url,params= wetter_hist_params)
    wetter_hist_data = wetter_hist_response.json()
    #aktuelle wetterdaten laden
    aktuell = wetter_data.get("current",{})

    # historische tägliche daten laden
    stündlich = pd.DataFrame({
    "date": wetter_hist_data["hourly"]["time"],
    "temp": wetter_hist_data["hourly"]["temperature_2m"],
    "precipitation": wetter_hist_data["hourly"]["precipitation"],
    "wind_speed_10m": wetter_hist_data["hourly"]["wind_speed_10m"],
    "relative_humidity_2m": wetter_hist_data["hourly"]["relative_humidity_2m"]
    })
    stündlich["date"] = pd.to_datetime(stündlich["date"])
    stündlich = stündlich.sort_values("date").reset_index(drop=True)


#inhalt

if 'aktuell' in locals() and seite == 'Dashboard':
# Metriken Reihe 1 mit 3 parallelen Anzeigen
# Titel
    st.subheader('Aktuelles Wetter')
    col1, col2, col3,col4 = st.columns(4)

# Daten für Metriken berechnen
    current_time = pd.to_datetime(aktuell.get("time")).floor('h')
    vor_24h = stündlich.loc[stündlich["date"] == current_time - pd.Timedelta(days=1), ["temp", "wind_speed_10m","precipitation","relative_humidity_2m"]]
    temp_diff = aktuell.get("temperature_2m") - vor_24h["temp"].values[0]
    wind_diff = aktuell.get("wind_speed_10m") - vor_24h["wind_speed_10m"].values[0]
    rain_diff = aktuell.get("precipitation") - vor_24h["precipitation"].values[0]
    hum_diff = aktuell.get("relative_humidity_2m") - vor_24h["relative_humidity_2m"].values[0]

    col1.metric(F"Temperatur in {stadtname}",f"{aktuell.get('temperature_2m')} °C",round(temp_diff,2))
    col2.metric(F"Wind in {stadtname}",f"{aktuell.get('wind_speed_10m')} km/h",round(wind_diff,2))
    col3.metric(F"Regen in {stadtname}",f"{aktuell.get('precipitation')} mm",round(rain_diff,2))
    col4.metric(F"Luftfeuchtigkeit in {stadtname}", f"{aktuell.get("relative_humidity_2m") } %",round(hum_diff,2))

# wetter diagramm

    st.subheader(f"Historischer Wetterverlauf der letzten {tage} Tage")

    täglich = stündlich.copy()
    täglich["date_only"] = täglich["date"].dt.date
    percip_täglich = täglich.copy()
    percip_täglich = percip_täglich.groupby("date_only").agg({"precipitation" : "sum"})
    täglich = täglich.set_index("date")[["temp"]]

    st.subheader("Temperatur")
    st.line_chart(täglich["temp"])
    st.subheader("Niederschlag")
    st.line_chart(percip_täglich["precipitation"])


elif seite == 'Über mich':
    st.subheader('Über mich')
    st.text('Hallo ich bin Maxi.\n' \
    'Ich bin aktuell Data Science Student im Bachelor an der Hochschule Karlsruhe.\n' \
    'Das dashboard war/ist ein kleines Projekt um mich schonmal mit einer Form von Datenanalyse zu beschäftigen.\n' \
    'Es spiegelt meine ersten Erfahrungen mit streamlit wieder. mögliche erweiterungen sind geplant, wenn ich die Zeit und die Skills dazu habe.')
else: 
    st.subheader("Die Stadt wurde nicht gefunden. Bitte versuche eine andere")

