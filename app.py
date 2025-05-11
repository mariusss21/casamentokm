import streamlit as st
import base64
import os
from streamlit_pdf_viewer import pdf_viewer


# --- Configuração da Página (Deve ser a primeira chamada Streamlit) ---
st.set_page_config(
    page_title="Nosso Convite de Casamento",
    page_icon="💍",  # Pode ser um emoji ou URL de um ícone .ico/.png
    layout="centered",  # 'centered' ou 'wide'
    initial_sidebar_state="collapsed",  # 'auto', 'expanded', 'collapsed'
)

# --- Configuração de Caminhos dos Arquivos (ajuste se necessário) ---
LOGO_PATH = "logo.jpg"  # Caminho para sua imagem de logo
BUTTON_IMAGE_PATH = "botao.jpg"  # Caminho para a imagem que será o botão (preferencialmente PNG)
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

def display_pdf_from_path(pdf_path, width="100%", height="800px"):
    """Exibe um arquivo PDF embutido no aplicativo Streamlit."""
    if os.path.exists(pdf_path):
        pdf_viewer(input=pdf_path, width=700)


# --- Inicialização do Estado da Sessão ---
# Controla se o PDF do convite deve ser exibido ou não
if 'show_pdf_invite' not in st.session_state:
    st.session_state.show_pdf_invite = False  # Padrão: PDF oculto

# --- Atualiza o estado com base nos parâmetros da URL ---
# Isso permite que o link da imagem (que define ?action=show_invite) acione a visualização do PDF.
# Roda a cada execução do script (ex: ao carregar a página, clicar no link).
if st.query_params.get("action") == "show_invite":
    st.session_state.show_pdf_invite = True

# --- Interface Principal do Aplicativo ---

# 1. Exibir Logo
if os.path.exists(LOGO_PATH):
    st.image(LOGO_PATH, width=200)  # Ajuste a largura conforme necessário
else:
    st.warning(f"Imagem do logo '{LOGO_PATH}' não encontrada. Adicione-a ao diretório do aplicativo ou corrija o caminho no código.")

st.write("---")  # Separador visual

# 2. Exibir conteúdo com base no estado (mostrar PDF ou mostrar imagem-botão)
if st.session_state.show_pdf_invite:
    # Se show_pdf_invite é True, exibe o PDF
    display_pdf_from_path(PDF_PATH)
    if st.button("⬅️ Voltar para o início"):
        st.session_state.show_pdf_invite = False
        # Limpa o parâmetro 'action' da URL para um estado limpo
        if "action" in st.query_params:
            del st.query_params["action"]
        st.rerun()  # Reexecuta o script para refletir a mudança de estado
else:
    # Se show_pdf_invite é False, exibe a imagem clicável (botão)
    button_image_base64 = get_image_as_base64(BUTTON_IMAGE_PATH)
    if button_image_base64:
        # A imagem é um link que adiciona '?action=show_invite' à URL.
        # target="_self" garante que abra na mesma aba.
        # Se sua imagem não for PNG, ajuste 'data:image/png;base64,' para ex: 'data:image/jpeg;base64,'
        invitation_link_html = f'<a href="?action=show_invite" target="_self"><img src="data:image/png;base64,{button_image_base64}" alt="Clique para ver o convite" style="max-width: 350px; cursor: pointer; display: block; margin-left: auto; margin-right: auto;"></a>'
        st.markdown(invitation_link_html, unsafe_allow_html=True)
    elif os.path.exists(BUTTON_IMAGE_PATH): # Imagem existe mas falhou ao carregar/converter
         st.error(f"Não foi possível carregar a imagem do botão '{BUTTON_IMAGE_PATH}'. Verifique o arquivo (idealmente PNG).")
    else:
        # Fallback para um botão de texto se a imagem do botão não for encontrada
        st.warning(f"Imagem do botão '{BUTTON_IMAGE_PATH}' não encontrada. Usando um botão de texto padrão como alternativa.")
        if st.button("💌 Abrir Convite"):
            st.session_state.show_pdf_invite = True
            # Define o parâmetro da URL para consistência, embora o rerun já use o session_state
            st.query_params["action"] = "show_invite"
            st.rerun()

    # Lembrete sobre o PDF se o arquivo estiver faltando na visualização inicial
    if not os.path.exists(PDF_PATH):
        st.error(f"⚠️ Atenção: O arquivo PDF do convite ('{PDF_PATH}') não foi encontrado. O convite não poderá ser exibido ao clicar.")