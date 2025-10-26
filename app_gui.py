import streamlit as st
from PIL import Image
import time
import os

from main import decidir_accion, _normalize_airline
from peso import determinar_porcentaje
from analisis_vision import analizar_pil_image
from conexionBD import verificar_usuario

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Gategroup Bottle Handling",
    layout="centered",
    initial_sidebar_state="collapsed"
)

hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding: 2rem 1rem 1rem 1rem;}
    .stApp { background-color: #FFFFFF; }
    </style>
    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def show_result_screen(decision, color, emoji):
    st.markdown(f"""
        <style>
        .stApp {{
            background-color: {color};
            transition: background-color 1s;
        }}
        .result-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 80vh;
            color: white;
        }}
        .result-emoji {{
            font-size: 100px;
        }}
        .result-text {{
            font-size: 48px;
            font-weight: bold;
            margin-top: 20px;
        }}
        </style>
        
        <div class="result-container">
            <div class="result-emoji">{emoji}</div>
            <div class="result-text">{decision}</div>
        </div>
    """, unsafe_allow_html=True)

    time.sleep(2) # Pausa dramática
    if st.button("Scan Next Bottle", key="next_bottle"):
        st.session_state.screen = 'scan' # Volver a la pantalla de escaneo
        st.markdown("<style>.stApp { background-color: #FFFFFF; }</style>", unsafe_allow_html=True)
        st.rerun()

# --- Función de Pantalla de Carga ---
def display_loading_page():
    try:
        spinner_img = Image.open("img/analyzing_spinner.png")
        st.image(spinner_img, use_column_width=True)
    except FileNotFoundError:
        st.spinner("Analyzing Bottle... Please wait...")
        
    st.markdown("<h3 style='text-align: center;'>::: ANALYZING BOTTLE :::</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>::: Please wait :::</p>", unsafe_allow_html=True)

    inputs = st.session_state.form_inputs
    airline_norm = st.session_state.airline_norm
    
    try:
        uploaded_file = inputs['image']
        pil_image = Image.open(uploaded_file)
        datos_vision = analizar_pil_image(pil_image)
        porcentaje_real = determinar_porcentaje(
            inputs['name'], 
            inputs['weight'], 
            airline_norm
        )
        datos_completos = {
            "ESTATUS_SELLO": datos_vision.get("sealStatus", "Opened"),
            "ESTATUS_ETIQUETA": datos_vision.get("labelStatus", "Heavily Damaged"),
            "LIMPIEZA": datos_vision.get("cleanliness", "Poor"),
            "PORCENTAJE_CONTENIDO": porcentaje_real
        }
        accion_final = decidir_accion(datos_completos, airline_norm)
        
        st.session_state.result = accion_final
        st.session_state.screen = 'result'
        st.rerun()

    except Exception as e:
        st.error(f"Error during analysis: {e}")
        st.error("Por favor, revisa tu API Key de Gemini, la conexión a la BD o los datos de entrada.")
        if st.button("Try Again"):
            st.session_state.screen = 'scan'
            st.rerun()


# --- Función de Pantalla de Escaneo ---
def display_scan_page():
    try:
        logo = Image.open("img/gategroup_logo.png")
        st.image(logo, width=200)
    except FileNotFoundError:
        st.title("Gategroup")

    st.info(f"Airline: **{st.session_state.airline}** | Flight: **{st.session_state.flight}**")
    st.markdown("---")
    
    try:
        scan_img = Image.open("img/scan_placeholder.png")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(scan_img, width=350)
    except FileNotFoundError:
        st.warning("Poner imagen 'scan_placeholder.png' en carpeta /img")

    st.markdown("<h3 style='text-align: center;'>INSERT THE BOTTLE INTO THE SCANNER</h3>", unsafe_allow_html=True)

    with st.form(key="scan_form"):
        st.write("**(Simulación de hardware)**")
        bottle_name = st.text_input("Bottle Name (from Barcode)", "Kahlúa Liqueur") 
        current_weight = st.number_input("Current Weight (grams)", min_value=0.0, value=500.0, step=0.1)
        uploaded_image = st.file_uploader("Upload Bottle Image (from Camera)", type=["jpg", "png", "jpeg"])
        submit_button = st.form_submit_button(label="ANALYZE BOTTLE")

    if submit_button:
        if not bottle_name or not current_weight or not uploaded_image:
            st.error("Please fill in all fields and upload an image.")
        else:
            st.session_state.form_inputs = {
                "name": bottle_name,
                "weight": current_weight,
                "image": uploaded_image
            }
            st.session_state.screen = 'loading'
            st.rerun()

# --- Función de Pantalla de Bienvenida (Aerolínea) ---
def display_welcome_page():
    try:
        logo = Image.open("img/gategroup_logo.png")
        st.image(logo, width=200)
    except FileNotFoundError:
        st.title("Gategroup")
        st.warning("Poner imagen 'gategroup_logo.png' en carpeta /img")

    st.title("WELCOME!")
    st.subheader("Please select an option...")
    
    airline = st.text_input("Airline:", "PatoVuelo")
    flight = st.text_input("Flight Number:", "PV-123")
    
    if st.button("SEARCH"):
        if not airline or not flight:
            st.error("Please enter Airline and Flight Number.")
        else:
            st.session_state.airline = airline
            st.session_state.flight = flight
            st.session_state.airline_norm = _normalize_airline(airline)
            st.session_state.screen = 'scan'
            st.rerun()

# --- Función de Pantalla de Login ---
def display_login_page():
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        try:
            logo = Image.open("img/gategroup_logo.png")
            st.image(logo, width=200)
        except FileNotFoundError:
            st.title("Gategroup")

        st.subheader("Log in to your account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Log in"):
            
            try:
                if verificar_usuario(username, password):
                    st.session_state.logged_in = True
                    st.session_state.screen = 'welcome'
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
            except Exception as e:
                st.error(f"Error during login: {e}") 
                st.info("Please check database connection and ensure the 'users' table exists.")

    with col2:
        try:
            bg_image = Image.open("img/login_background.png")
            st.image(bg_image, caption="Creating culinary connections")
        except FileNotFoundError:
            st.info("Poner imagen 'login_background.png' en carpeta /img")

# --- Lógica Principal (Router) ---
def main():
    if 'screen' not in st.session_state:
        st.session_state.screen = 'login'
        st.session_state.logged_in = False
        st.session_state.airline = ""
        st.session_state.flight = ""
        st.session_state.airline_norm = ""
        st.session_state.form_inputs = {}
        st.session_state.result = ""

    if not st.session_state.logged_in:
        display_login_page()
    elif st.session_state.screen == 'welcome':
        display_welcome_page()
    elif st.session_state.screen == 'scan':
        display_scan_page()
    elif st.session_state.screen == 'loading':
        display_loading_page()
    elif st.session_state.screen == 'result':
        result = st.session_state.result
        if result == "KEEP":
            show_result_screen("KEEP", "#2ECC71", "✔️") # Verde
        elif result == "REFILL":
            show_result_screen("REFILL", "#3498DB", "💧") # Azul
        elif result == "REPLACE":
            show_result_screen("REPLACE", "#F39C12", "🔄") # Naranja
        elif result == "DISCARD":
            show_result_screen("DISCARD", "#E74C3C", "❌") # Rojo
        else:
            st.error(f"Unknown result: {result}")
            st.session_state.screen = 'scan'
            st.rerun()

if __name__ == "__main__":
    main()