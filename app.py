import streamlit as st
import base64
import os
from streamlit_pdf_viewer import pdf_viewer
from st_clickable_images import clickable_images


# --- Configuração da Página (Deve ser a primeira chamada Streamlit) ---
st.set_page_config(
    page_title="Nosso Convite de Casamento",
    page_icon="💍",  # Pode ser um emoji ou URL de um ícone .ico/.png
    layout="centered",  # 'centered' ou 'wide'
    initial_sidebar_state="collapsed",  # 'auto', 'expanded', 'collapsed'
)

# --- Configuração de Caminhos dos Arquivos (ajuste se necessário) ---
LOGO_PATH = "logo_sem_fundo.png"  # Caminho para sua imagem de logo
BUTTON_IMAGE_PATH = "bt_pdf.png"  # Caminho para a imagem que será o botão (preferencialmente PNG)
PDF_PATH = "convite.pdf"  # Caminho para o arquivo PDF do convite
BACKGROUND_IMAGE_PATH = "fundo.jpg" # Caminho para sua imagem de fundo (JPG)


# Function to encode image to base64
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Set background image from local file
def set_background(image_path):
    base64_image = get_base64_image(image_path)
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{base64_image}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        #MainMenu {{ visibility: hidden; }} /* Oculta o menu hambúrguer (pode ser redundante se o cabeçalho for oculto) */
        header[data-testid="stHeader"] {{ visibility: hidden; }} /* Oculta o cabeçalho principal */
        footer {{ visibility: hidden; }} /* Oculta o rodapé */
        </style>
        """,
        unsafe_allow_html=True
    )

# Call the function with your local image
set_background(BACKGROUND_IMAGE_PATH)

# --- Funções Auxiliares ---

def get_image_as_base64(path):
    """Lê um arquivo de imagem e retorna sua representação em base64."""
    if not os.path.exists(path):
        # st.error(f"Imagem não encontrada: {path}") # Erro já tratado no local de chamada
        return None
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        st.error(f"Erro ao ler a imagem {path}: {e}")
        return None

def display_pdf_from_path(pdf_path):
    """Exibe um arquivo PDF embutido no aplicativo Streamlit."""
    if os.path.exists(pdf_path):
        pdf_viewer(input=pdf_path,
                   pages_vertical_spacing=0,
                   annotation_outline_size=0)


# --- Inicialização do Estado da Sessão ---
# Controla se o PDF do convite deve ser exibido ou não
if 'show_pdf_invite' not in st.session_state:
    st.session_state.show_pdf_invite = False

def botoes_auxiliares():

    list_images = []
    list_images.append(f"data:image/png;base64,{get_image_as_base64('bt_local.png')}")
    list_images.append(f"data:image/png;base64,{get_image_as_base64('bt_site.png')}")
    list_images.append(f"data:image/png;base64,{get_image_as_base64('bt_pix.png')}")

    bt_local = clickable_images(list_images,
        div_style={
        "display": "flex", 
        "justify-content": "flex-start", 
        "align-items": "flex-start", 
        "flex-wrap": "nowrap", 
        "overflow-x": "auto", 
        "width": "100%" 
    },
    img_style={ 
        "margin": "1.5%", 
        "height": "auto", 
        "max-width": "30%", 
        "object-fit": "contain", 
        "cursor": "pointer",
        "background-color": "transparent"
    },
    key="clickable_inline_images"
    
    )

    if bt_local > -1:
        st.write(bt_local)
        

# --- Interface Principal do Aplicativo ---

# 1. Exibir Logo
if os.path.exists(LOGO_PATH):
    if not st.session_state.show_pdf_invite:
        logo64 = get_image_as_base64(LOGO_PATH)
        if logo64:
            st.markdown(
                f"""
                <div style="text-align: center;">
                <img src="data:image/png;base64,{logo64}" style="max-width: 30%; height: auto;">
            </div>
            """,
            unsafe_allow_html=True
        )

else:
    st.warning(f"Imagem do logo '{LOGO_PATH}' não encontrada. Adicione-a ao diretório do aplicativo ou corrija o caminho no código.")

st.write("---")  # Separador visual

# 2. Exibir conteúdo com base no estado (mostrar PDF ou mostrar imagem-botão)
if st.session_state.show_pdf_invite:
    # Se show_pdf_invite é True, exibe o PDF
    display_pdf_from_path(PDF_PATH)
    botoes_auxiliares()
    if st.button("⬅️ Voltar para o início", use_container_width=True):
        st.session_state.show_pdf_invite = False
        st.rerun()  
else:
    initial_images = []
    initial_images.append(f"data:image/png;base64,{get_image_as_base64(BUTTON_IMAGE_PATH)}")

    bt_convite = clickable_images(initial_images,
        div_style={
        "display": "flex", 
        "justify-content": "flex-start", 
        "align-items": "flex-start", 
        "flex-wrap": "nowrap", 
        "overflow-x": "auto", 
        "width": "100%" 
    },
    img_style={ 
        "margin": "0%", 
        "height": "auto", 
        "max-width": "100%", 
        "object-fit": "contain", 
        "cursor": "pointer",
        "background-color": "transparent"
    },
    key="clickable_inline_imagess"
    
    )

    if bt_convite > -1:
        st.session_state.show_pdf_invite = True
        st.rerun()


    # Lembrete sobre o PDF se o arquivo estiver faltando na visualização inicial
    if not os.path.exists(PDF_PATH):
        st.error(f"⚠️ Atenção: O arquivo PDF do convite ('{PDF_PATH}') não foi encontrado. O convite não poderá ser exibido ao clicar.")