# d'abord 

python -m venv .venv
source .venv/bin/activate    
pip install -r requirements.txt 

# peut être aussi car cet api est soumise à de fréquents changements
pip install --upgrade pytube

# puis au choix 

    streamlit run webcam_app.py

# ou bien 

    streamlit run youtube_scan.py
  