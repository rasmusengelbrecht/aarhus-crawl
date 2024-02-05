import streamlit as st
import random
import requests
import pandas as pd
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
from streamlit_gsheets import GSheetsConnection
import time

st.set_page_config(page_title="Aarhus Crawl", page_icon=":beers:")

st.markdown(
    """
        # Aarhus Crawl 🍻

        Generate a personalised pub crawl in Aarhus! Take up the challenge and add fun rules for each bar
    """
)

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read()

rules = [
    "The Hug or handshake Bar: Everyone have to hug or handshake the bartender",
    "The Moonwalk Bar: Only walk backwards inside the bar",
    "The Digital Detox Bar: No looking at phones. If someone does, they have to buy the next round.",
    "The Mime Bar: No speaking allowed until you’ve ordered your first drink.",
    "The Left Hand Bar: You can only drink with your non-dominant hand.",
    "The Compliments Bar: You must give a compliment to a stranger before placing your drink order",
    "The Whisper Bar: Everyone must speak in whispers. If someone speaks at a normal volume, they buy a round of snacks.",
    "The No-Name Bar: You can’t say anyone’s name. If you do, you have to sing a chorus of a popular song.",
    "The Hat Trick Bar: Everyone must wear something on their head inside the bar.",
    "The High-Five Bar: You must high-five at least three different people in the bar.",
    "The Sock Swap Bar: Everyone swaps one sock with a friend for the duration of the stay in the bar.",
    "The Retro Bar: Everyone talks as if they’re in a past decade while in the bar.",
    "The Dance Move Bar: Each person must perform a dance move before ordering their drink."
]

@st.cache_data
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_progress_url = "https://lottie.host/5e357569-5f59-4d8d-851a-18a5fb7e6acb/1RJiom1Oif.json"
lottie_progress = load_lottieurl(lottie_progress_url)

# List of all unique bar types
all_bar_types = list(set(df['Tags']))

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


# Initialize session state for the pub crawl list
if 'pub_crawl_list' not in st.session_state:
    st.session_state.pub_crawl_list = None

# User Inputs
with st.expander("Settings"):
    number_of_bars = st.number_input('How many bars do you want to visit?', min_value=1, max_value=len(df), value=5)
    include_rules = st.checkbox('Do you want to include a rule for each bar?', value=True)
    bar_types = st.multiselect('Select the types of bars you want to visit', options=all_bar_types, default=['Bar','Bodega','Brewery','Wine Bar'])

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

# Display the pub crawl list if it exists in session state
if st.session_state.pub_crawl_list is not None:
    st.dataframe(
        st.session_state.pub_crawl_list,
        column_config={"Link": st.column_config.LinkColumn("Link", display_text="Maps")},
        hide_index=True, 
        use_container_width=True
    )

    # Display the formatted pub crawl list in a text area for the user to copy
    formatted_list = format_pub_crawl_list(st.session_state.pub_crawl_list)

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
            size=15, 
            color='#0044ff',
            use_container_width=True
        )

    # Use an expander for the textarea
    with st.expander("📝 Copy + Paste in your Notes/Chat"):    
        st.text_area(
        label="Select All, Copy + Paste in Notes or a group chat", 
        value=formatted_list, 
        height=800, 
        help="Copy and paste this list into your notes or send it to your friends.",
    )



st.write("")

st.divider()

st.write("Did I miss a bar? Send info to me at: engel_brecht@hotmail.com")