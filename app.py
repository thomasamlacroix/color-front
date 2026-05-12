import streamlit as st
from PIL import Image
import requests
import base64
import io

#API url
SERVICE_URL = "http://127.0.0.1:8000"

#API token
# TOKEN =

#Colors
#------
RED = '#FF4B4B'
BLUE = '#1f77b4'
GREEN = '#2ECC71'
ORANGE = '#F39C12'
DARK_BLUE = "#1F4E79"
YELLOW = '#F1C40F'
PURPLE = '#8E44AD'
CYAN = '#1ABC9C'
LIGHT_GREY = '#F5F7FA'
DARK_GREY = '#34495E'
BLACK = '#000000'
WHITE = '#FFFFFF'

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
<b>Bringing color back to life</b>
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


st.markdown("### How does it work?")
st.write("""
1. Upload your image
2. AI based on deep learning reconstructs color channels
""")


#First version with placeholders
# uploaded_file = TEST_IMG_BW

uploaded_file = st.file_uploader(
        "📷 Upload your image",
        type=["jpg","jpeg","png","gif","bmp","MPO"], #filtering at interface level
        key = "file"
)


if uploaded_file is not None:
    image = validate_image(uploaded_file)

    # initial_uploaded_image = image
    # img_reconstructed = Image.open(TEST_IMG_COLOR)
    # col1, col2 = st.columns(2)
    # col1.image(initial_uploaded_image, caption="Uploaded image", width='stretch')
    # col2.image(img_reconstructed, caption=f"Colorized image", width='stretch')

    if image is not None :
            #Resetting pointer after image verification to avoid empty file and API error
            uploaded_file.seek(0)
            #Sending file to API
            with st.spinner("🔍 Reconstructing colors..."): #hourglass if taking too long
                files = {"file" : uploaded_file }
                #headers = {'token' : TOKEN}
                response = requests.post(SERVICE_URL, files=files)  #, headers=headers)

    if response.status_code == 200:
        data  = response.json()
        #Decoding binary image
        img_bw_resized_data = base64.b64decode(data["img_bw_resized"])
        img_reconstructed_data = base64.b64decode(data["img_reconstructed"]) #decoding binary image

        #Turning into actual images
        img_bw_resized = Image.open(io.BytesIO(img_bw_resized_data))
        img_reconstructed = Image.open(io.BytesIO(img_reconstructed_data))

        col1, col2 = st.columns(2)
        col1.image(img_bw_resized, caption="Uploaded image", width='stretch')
        col2.image(img_reconstructed, caption="Colorized image", width='stretch')

    else:
        st.error("Error calling the API")

else:
    st.write("No file uploaded yet")
