import streamlit as st
import random
import requests
import pandas as pd
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
from streamlit_gsheets import GSheetsConnection
import time
from streamlit_pills import pills

#-------------------------- Page Config --------------------------------

st.set_page_config(page_title="Aarhus Crawl", page_icon=":beers:")


#----------------- Hide Streamlit footer, header -----------------------

hide_streamlit_style = """
            <style>
            [data-testid="stToolbar"] {visibility: hidden !important;}
            footer {visibility: hidden !important;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


#--------------------------------------------------------------------


st.markdown(
    """
        # Aarhus Crawl 🍻

        Generate a personalised pub crawl in Aarhus! Take up the challenge and add fun rules for each bar
    """
)


#-------------------- Load Google Sheet Data --------------------------

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read()


#----------------------- Define Rules -----------------------------

rules = [
    "The Hug or handshake Bar: Everyone have to hug or handshake the bartender",
    "The Moonwalk Bar: Only walk backwards inside the bar",
    "The Digital Detox Bar: No looking at phones. Agree on a punishment, if someone does.",
    "The Mime Bar: No speaking allowed until you’ve ordered your first drink.",
    "The Left Hand Bar: You can only drink with your non-dominant hand.",
    "The Compliments Bar: You must give a compliment to a stranger before placing your drink order",
    "The Whisper Bar: Everyone must speak in whispers.",
    "The No-Name Bar: You can’t say anyone’s name.",
    "The Confession Bar: Make a confession to the group before ordering.",
    "The High-Five Bar: Everyone must high-five at least three different people in the bar.",
    "The Dance Move Bar: Each person must perform a dance move before ordering their drink.",
    "The Compliment Chain Bar: Give a compliment to someone outside your group, and they must pass it on to someone else.",
    "The Group Photo Bar: Take a group photo with new friends you meet at the bar.",
    "The Challenge Bar: Politely challenge someone outside your group to a friendly contest (like rock-paper-scissors).",
    "The Toast Master Bar: Make a toast with a group of strangers.",
    "The Good Deed Bar: Do a small, kind deed for someone in the bar.",
    "The Hidden Talent Bar: Share a hidden talent with a stranger, or discover theirs."
]


#-------------------- Get Lottie Animation --------------------------

@st.cache_data
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_progress_url = "https://lottie.host/5e357569-5f59-4d8d-851a-18a5fb7e6acb/1RJiom1Oif.json"
lottie_progress = load_lottieurl(lottie_progress_url)


#---------------------- Handle Bar Info ----------------------------

# List of all unique bar types excluding 'Uni Friday Bar'
all_bar_types = [tag for tag in set(df['Tags']) if tag != 'Uni Friday Bar']

# Function to format the DataFrame into a string
def format_pub_crawl_list(df):
    formatted_string = ""
    for index, row in df.iterrows():
        bar_name = row['Bar']
        link = row['Link']
        rule = row.get('Rule', '')  # Get the rule if it exists
        formatted_string += f"📍 {bar_name}\n🔗 {link}\n"
        if rule:
            formatted_string += f"🧑‍⚖️ {rule}\n"
        formatted_string += "\n"  # Add an extra newline for spacing between entries
    return formatted_string


#------------------------- Settings -------------------------------

# Initialize session state for the pub crawl list
if 'pub_crawl_list' not in st.session_state:
    st.session_state.pub_crawl_list = None

# User Inputs
with st.expander("Settings"):
    crawl_type = pills("Label", ["City Center", "University Friday Bars"], ["🥳", "👨‍🎓"], label_visibility='collapsed')
    number_of_bars = st.number_input('How many bars do you want to visit?', min_value=1, max_value=len(df), value=5)
    include_rules = st.checkbox('Do you want to include a rule for each bar?', value=True)

    # Conditionally show the multiselect based on crawl_type
    if crawl_type != "University Friday Bars":
        bar_types = st.multiselect('Select the types of bars you want to visit', options=all_bar_types, default=['Bar','Bodega','Brewery'])
    else:
        # Automatically set bar_types to 'Uni Friday Bar' if the crawl type is University Friday Bars
        bar_types = ['Uni Friday Bar']


#--------------------- Generate Pub Crawl ---------------------------

col1, col2, col3 = st.columns(3)

# Button to generate pub crawl
if col2.button('Generate Pub Crawl'):
    with st_lottie_spinner(lottie_progress, loop=True, key="progress", height=200):
        time.sleep(2.5)

    filtered_df = df[df['Tags'].isin(bar_types)]
    number_of_bars = min(number_of_bars, len(filtered_df))
    selected_bars = filtered_df.sample(n=number_of_bars)

    if include_rules:
        random.shuffle(rules)
        selected_rules = rules[:number_of_bars]
        selected_bars['Rule'] = selected_rules

    if include_rules:
        display_columns = ['Bar', 'Link', 'Rule']
    else:
        display_columns = ['Bar', 'Link']
    
    display_df = selected_bars[display_columns].reset_index(drop=True)

    # Store the pub crawl list in session state
    st.session_state.pub_crawl_list = display_df


#-------------------- Display Pub Crawl --------------------------

# Display the pub crawl list if it exists in session state
if st.session_state.pub_crawl_list is not None:

    #-------------------- Dataframe --------------------------
    st.dataframe(
        st.session_state.pub_crawl_list,
        column_config={"Link": st.column_config.LinkColumn("Link",display_text="Maps")},
        hide_index=True, 
        use_container_width=True
    )

    #-------------------- Show Map --------------------------

    # Extract the relevant bars from the original DataFrame based on the selection
    # This assumes that 'Bar' values are unique and can be used to merge/filter DataFrames
    map_data = pd.merge(
        st.session_state.pub_crawl_list[['Bar']], 
        df[['Bar', 'latitude', 'longitude']], 
        on='Bar', 
        how='left'
    )

    # Use an expander for the map
    with st.expander("🗺️ Show Map"):
        # Now display the map with only the selected bars
        st.map(
            map_data,
            size=20, 
            color='#0044ff',
            use_container_width=False,
            zoom=12
        )

    #-------------------- Show Textarea --------------------------
        
    # Display the formatted pub crawl list in a text area for the user to copy
    formatted_list = format_pub_crawl_list(st.session_state.pub_crawl_list)

    # Use an expander for the textarea
    with st.expander("📝 Copy + Paste in your Notes/Chat"):    
        st.text_area(
            label="Select All, Copy + Paste in Notes or a group chat", 
            value=formatted_list, 
            height=800, 
            help="Copy and paste this list into your notes or send it to your friends.",
        )


#-------------------- Add Footer --------------------------
        
st.write("")

st.divider()

st.write("Did I miss a bar? Send info to me at: engel_brecht@hotmail.com")