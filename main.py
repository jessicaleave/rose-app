import streamlit as st
import pandas as pd

st.title(":rose: Find the Perfect Rose  ")
search_query = st.text_input("Search for roses by name", "")


def load_data():
    data = pd.read_csv('Rose_Varieties.csv')
    data['min_height'] = data['min_height'].astype(float)
    data['max_height'] = data['max_height'].astype(float)
    return data

def search_data(data, query):
    if query:  # only filter if there is a query
        query = query.lower()
        return data[data.apply(lambda row: query in row['Common Name'].lower(), axis=1)]
    return data
df = load_data()
# Moving 'Additional Characteristics' to the end
order = [col for col in df.columns if col != 'Additional Characteristics'] + ['Additional Characteristics']
df = df[order]

st.sidebar.header('Filter Options')

# Filter by Flower Color
flower_color = st.sidebar.multiselect(
    'Select Flower Color:',
    options=df['Flower Color'].unique(),
    default=df['Flower Color'].unique()
)
# Filter by Fragrant Level
fragrant_level = st.sidebar.multiselect(
    'Select Fragrant Level:',
    options=df['Fragrant Level'].unique(),
    default=df['Fragrant Level'].unique()
)

# Filter by Fragrant Type
fragrant_type = st.sidebar.multiselect(
    'Select Fragrant Type:',
    options=df['Fragrant Type'].unique(),
    default=df['Fragrant Type'].unique()
)

# Filter by Height Range (Using Min and Max Height)
min_height = df['min_height'].min()
max_height = df['max_height'].max()
height = st.sidebar.slider(
    'Select Height Range:',
    min_value=min_height,
    max_value=max_height,
    value=(min_height, max_height)
)

# Filter by Disease Resistance
disease_resistant = st.sidebar.selectbox(
    'Disease Resistant:',
    options=df['Disease Resistant'].unique(),
    index=0  # Default to first option
)

pre_filtered_data = df[
    (df['Flower Color'].isin(flower_color)) &
    (df['Fragrant Level'].isin(fragrant_level)) &
    (df['Fragrant Type'].isin(fragrant_type)) &
    (df['min_height'] >= height[0]) &
    (df['max_height'] <= height[1]) &
    (df['Disease Resistant'] == disease_resistant)
]

searched_data = search_data(pre_filtered_data, search_query)

display_data = searched_data.drop(columns=['min_height', 'max_height'])

# Display results
st.header('Filtered Rose Varieties')
st.write(display_data)
