# ----------------------------------
#         LOCAL SET UP
# ----------------------------------

install_requirements:
	@pip install -r requirements.txt

# ----------------------------------
#         STREAMLIT COMMANDS
# ----------------------------------

streamlit:
	-@streamlit run app.py
