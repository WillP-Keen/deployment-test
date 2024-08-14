import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

page_names_to_funcs = {}


def authentication():
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
        config["pre-authorized"],
    )

    authenticator.login()

    if st.session_state["authentication_status"]:
        col1, col2 = st.sidebar.columns(2)

        col2.write("# MyKeen MVP")
        col1.image("./PuffinLogo.ico")
        st.sidebar.write("---")

        demo_name = st.sidebar.selectbox("Clients:", page_names_to_funcs.keys())
        authenticator.logout("↪️ Logout", "sidebar")

        st.sidebar.markdown(
            '<a href="mailto:William@keenpayroll.ca?subject=MyKeen%20Issue">Report Issue</a>',
            unsafe_allow_html=True,
        )

        page_names_to_funcs[demo_name]()
    elif st.session_state["authentication_status"] is False:
        st.error("Username/password is incorrect")
    elif st.session_state["authentication_status"] is None:
        st.warning("Please enter your username and password")


authentication()
