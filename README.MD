# d'abord 

dans le répertoire racine (heatzone)

python -m venv .venv
source .venv/bin/activate    
pip install -r requirements.txt 

# creation de la base de données : 

    python app/db_setup2.py

# puis lancement

    streamlit run app/main.py.py

  