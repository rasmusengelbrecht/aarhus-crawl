import streamlit as st
import random
import requests
import streamlit as st
import pandas as pd
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
import time

st.set_page_config(page_title="Aarhus Crawl", page_icon=":beers:")

st.markdown(
    """
        # Aarhus Crawl 🍻

        Generate a personalised pub crawl in Aarhus! Take up the challenge and add fun rules for each bar
    """
)

import pandas as pd

# Data
data = {
    "Bar": [
        "Vinstuen", "Clemens Bar", "Force Majeure", "Thorkilds", "El Loco", "GBAR", "Lecoq", 
        "Mig og Ølsnedkeren", "Pinot", "Tír na nÓg", "Oops", "Panenka", "Herr Bartels", 
        "Café Under Masken", "ÅBEN", "Cafe Guldhornene", "Bodegaen", "Pustervig", "Heidi's Bier Bar", 
        "Escobar", "Hos Anders", "ZenZa", "Two Socks Ginbar", "Barstart", "Tokio Bar", 
        "Sjovinisten", "Der Kuhstall", "The Old Irish Pub", "Ris Ras Filliongongong", "Erlings Jazz- & Ølbar", 
        "Café Smagløs", "Zanders", "MasVino", "Sherlock Holmes Pub", "Shen Mao", "Rabalder Bar", 
        "Den Gyldne Kro", "Kurts Mor", "Bro Cafeen", "Hos Anton", "Hjorten", "Værtshuset", 
        "Mundhæld", "Flintstone Pub", "Willi's", "Jysk Vin", "Plan B", "Pica Pica", 
        "Vin & Petanque", "Vincaféen", "S'vinbar", "Bar Smil"
    ],
    "Link": [
        "https://maps.app.goo.gl/iddeNS8EaZKxqnZn6",
        "https://maps.app.goo.gl/ttcHVuooQLadU5Mv7",
        "https://maps.app.goo.gl/6nvXjgtMoCU7D6aQ8",
        "https://maps.app.goo.gl/Nsg4kbV7Fto2WrF66",
        "https://maps.app.goo.gl/QJ3iSVz9LYahZiLn9",
        "https://maps.app.goo.gl/2rWsHtjEncjW18JL8",
        "https://maps.app.goo.gl/ptSkM7LukTo1TZFB7",
        "https://maps.app.goo.gl/tRRqjsPtQj9aB2bZA",
        "https://maps.app.goo.gl/3imtZg9kwkBC7Ug58",
        "https://maps.app.goo.gl/MKjRCPkzUDYg4aCs9",
        "https://maps.app.goo.gl/vQktmGXACcZYyEjj9",
        "https://maps.app.goo.gl/mgqsKCG9a1EF4DtTA",
        "https://maps.app.goo.gl/1cvSjrobzaHN7898A",
        "https://maps.app.goo.gl/XhGh9UR4cdZw34GX8",
        "https://maps.app.goo.gl/oRcXyb5shhgLBwEm9",
        "https://maps.app.goo.gl/wDNS19SStrUqc7pY7",
        "https://maps.app.goo.gl/uEKLJ6WnMuPSmijZ8",
        "https://maps.app.goo.gl/6hH4g8VJxLZugjEs7",
        "https://maps.app.goo.gl/sRsYjgYcZpK8AgqeA",
        "https://maps.app.goo.gl/E31RpqvsmBdXeYec6",
        "https://maps.app.goo.gl/sdqwa77gxUEt3W4m6",
        "https://maps.app.goo.gl/uPyv7fGGddWL9Cv1A",
        "https://maps.app.goo.gl/ky27qDVMXBE7PohTA",
        "https://maps.app.goo.gl/Z5i8XFQBizyW1VJ37",
        "https://maps.app.goo.gl/GnRofWNECryjZ7qR8",
        "https://maps.app.goo.gl/BSoHQzeCUXKbpUp89",
        "https://maps.app.goo.gl/A9tNeRjW31CKLumd9",
        "https://maps.app.goo.gl/7Wj3htv5XCKzYBweA",
        "https://maps.app.goo.gl/xTDYni3vmNK3Rk3d8",
        "https://maps.app.goo.gl/7dUHMLppmifzM7KHA",
        "https://maps.app.goo.gl/viGAhNbhEXUqbV4C8",
        "https://maps.app.goo.gl/MkN7ZajprNkKi1hh8",
        "https://maps.app.goo.gl/xbYMriUunmCxfhxv7",
        "https://maps.app.goo.gl/GYPTovABfFgM2bhS9",
        "https://maps.app.goo.gl/7G5Ktpi8fgmtro138",
        "https://maps.app.goo.gl/2JNwJ433SbScj4gn6",
        "https://maps.app.goo.gl/2zo3Bx3UMe4c2SJXA",
        "https://maps.app.goo.gl/9KzkQ1Rugt9pvMySA",
        "https://maps.app.goo.gl/RjVjrb4juNPvG7rz5",
        "https://maps.app.goo.gl/MtFYN4Rhg8UtQJq78",
        "https://maps.app.goo.gl/tuEW2rJFy6ezGZ2S9",
        "https://maps.app.goo.gl/x8LpbAb4ZKJeocTt9",
        "https://maps.app.goo.gl/CmwYwxrEzEH1tdU78",
        "https://maps.app.goo.gl/DL1mqcw5EG6zp1fz5",
        "https://maps.app.goo.gl/G8nTnmo53AV8bJJF7",
        "https://maps.app.goo.gl/YHUyBmVd7gQvBgq47",
        "https://maps.app.goo.gl/a8cDiQbmi5JmCFPg6",
        "https://maps.app.goo.gl/r5Bv5GDewAHz2XrC6",
        "https://maps.app.goo.gl/ntW36Ggm2cA8NPMZ7",
        "https://maps.app.goo.gl/9sW2YvsovcuHHZtv8",
        "https://maps.app.goo.gl/48hauTSfceNz4bTj6",
        "https://maps.app.goo.gl/hipqxGtNzNrzQhAA6"
    ],
    "Tags": [
        "Bodega", "Bar", "Cocktail Bar", "Bodega", "Bar", "Bar", "Bodega", "Brewery",
        "Wine Bar", "Bar", "Bar", "Bar", "Cocktail Bar", "Bodega", "Brewery", "Bar",
        "Bodega", "Bar", "Bar", "Bar", "Bodega", "Cocktail Bar", "Cocktail Bar",
        "Cocktail Bar", "Bar", "Wine Bar", "Bar", "Bar", "Bodega", "Bodega", "Bar",
        "Bar", "Wine Bar", "Bar", "Bar", "Bar", "Bar", "Bodega", "Bodega", "Bodega",
        "Bodega", "Bodega", "Bodega", "Bodega", "Bodega", "Bar", "Wine Bar", "Wine Bar",
        "Wine Bar", "Wine Bar", "Wine Bar", "Bar"    
    ]
}

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

# Creating DataFrame
df = pd.DataFrame(data)

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


# Initialize session state for the pub crawl list
if 'pub_crawl_list' not in st.session_state:
    st.session_state.pub_crawl_list = None

# User Inputs
with st.expander("Settings"):
    number_of_bars = st.number_input('How many bars do you want to visit?', min_value=1, max_value=len(df), value=5)
    include_rules = st.checkbox('Do you want to include a rule for each bar?', value=True)
    bar_types = st.multiselect('Select the types of bars you want to visit', options=all_bar_types, default=all_bar_types)

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


st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")

st.divider()

st.write("Did I miss a bar? Send info to me at: engel_brecht@hotmail.com")