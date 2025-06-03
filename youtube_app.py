import streamlit as st

st.set_page_config(page_title="Lecteur YouTube", layout="centered")
st.title("📺 Lecteur YouTube avec Streamlit")

# Initialisation de l'état pour lecture/pause
if "play_video" not in st.session_state:
    st.session_state.play_video = False

# Entrée de l'URL YouTube
video_url = st.text_input("🔗 Collez l'URL d'une vidéo YouTube :", "")

# Choix de la taille d'affichage
width = st.slider("📐 Largeur du lecteur (en pixels)", min_value=300, max_value=1280, value=640)
height = int(width * 9 / 16)

# Fonction de validation d'URL YouTube
def is_valid_youtube_url(url):
    return "youtube.com/watch" in url or "youtu.be/" in url

# Bouton de démarrage / arrêt
if video_url and is_valid_youtube_url(video_url):
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("▶️ Start" if not st.session_state.play_video else "⏸️ Pause"):
            st.session_state.play_video = not st.session_state.play_video

    # Affichage conditionnel de la vidéo
    if st.session_state.play_video:
        st.markdown("### 🎞️ Aperçu de la vidéo :")
        st.video(video_url, format="video/mp4", start_time=0)
else:
    if video_url:
        st.error("❌ Lien non valide. Veuillez entrer une URL YouTube.")
    else:
        st.info("💡 Entrez une URL de vidéo YouTube pour commencer.")
