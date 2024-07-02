<div style="text-align:center">
<img style="height: 5cm;" alt="HeatPro App logo" src=logo/heatpro_app_logo.png>
</div>

Streamlit App based on <a href='https://github.com/CEA-Liten/HeatPro'>HeatPro</a>. The app aims to demonstrate HeatPro tool box nby automating some process with a nice interface. HeatPro is usefull to generate hourly features like heat demand by sector or district heating network temperature from aggregate data.

To run the app we recommend to use Poetry :

```
pip install poetry
```

Then you only need enter these commands :

```
poetry install
```
```
poetry run streamlit run app.py
```

If needed use before `poetry install`:
```
poetry lock
```