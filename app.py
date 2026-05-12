import streamlit as st
from PIL import Image
import requests
import base64
import io

#API url
SERVICE_URL = ""

#API token
# TOKEN =

#Colors
#------
ROUGE = '#FF4B4B'
BLEU = '#1f77b4'
VERT = '#2ECC71'
ORANGE = '#F39C12'
BLEU_FONCE = "#1F4E79"
JAUNE = '#F1C40F'
VIOLET = '#8E44AD'
CYAN = '#1ABC9C'
GRIS_CLAIR = '#F5F7FA'
GRIS_FONCE = '#34495E'
NOIR = '#000000'
BLANC = '#FFFFFF'

# Maximum image size
#####################
MAX_SIZE = 4000  #pixels in height or width


#Test image
TEST_IMG_BW = 'images/image0001_bw.jpg'
TEST_IMG_COLOR = 'images/image0001.jpg'

#####################
# Page configuration
#####################

st.set_page_config(
    page_title="COLOR-RISE",
    layout="wide",
    initial_sidebar_state="expanded"
)
#st.title("D-FAKE")
st.markdown("""
<h1 style='text-align:center; color:BLACK;'>
COLOR-RISE
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<p style='text-align:center; font-size:25px;'>
<b>Bringing color back</b>
</p>
""", unsafe_allow_html=True)

st.markdown("---")



##########################################
#Image verification before sending to API
##########################################

def validate_image(uploaded_file, max_size=MAX_SIZE):
    try:
        image = Image.open(uploaded_file)
        image.verify()  # checking file integrity
    except Exception:
        st.error("⚠️ Corrupted image file")
        st.stop()
        return None

    #Open again after verification
    image = Image.open(uploaded_file)

    #Checking format to prevent viruses with extension replacement
    allowed_formats = ["JPG","JPEG","PNG","GIF","BMP","MPO"]
    if image.format not in allowed_formats:
        st.error(f" 🟡 Unsupported format: {image.format}")
        st.stop()
        return None
    #Checking size of loaded image
    if image.width > max_size or image.height > max_size:
        st.error(f"⚠️ Image too large : Max size is {max_size} x {max_size}")
        st.stop()
        return None

    return image



#First version with placeholders
uploaded_file = TEST_IMG_BW

if uploaded_file is not None:
    image = validate_image(uploaded_file)

    initial_uploaded_image = image
    img_reconstructed = Image.open(TEST_IMG_COLOR)
    #Affichage des images côte à côte (loadée et heatmap)
    col1, col2 = st.columns(2)
    col1.image(initial_uploaded_image, caption="Uploaded image", width='stretch')
    col2.image(img_reconstructed, caption=f"Colorized image", width='stretch')
