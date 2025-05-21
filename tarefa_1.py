import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import pydeck as pdk

def plota_pivot_table(df, value, index, func, ylabel, xlabel, opcao='nada'):
    if opcao == 'nada':
        pd.pivot_table(df, values=value, index=index,aggfunc=func).plot(figsize=[15, 5])
    elif opcao == 'unstack':
        pd.pivot_table(df, values=value, index=index,aggfunc=func).unstack().plot(figsize=[15, 5])
    elif opcao == 'sort':
        pd.pivot_table(df, values=value, index=index,aggfunc=func).sort_values(value).plot(figsize=[15, 5])
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    st.pyplot(fig=plt)
    return None

st.set_page_config(page_title = 'Sinasc RO - 2019', 
                   page_icon = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ__uwtZnbxNRdhFe5UctTZc8ruHFiFTkVgrw&s',
                   layout='wide')

sinasc = pd.read_csv(r"C:\Users\Meu Computador\anaconda3\EBAC\M15_Streamlit\Tarefa\sinasc.csv")
sinasc['DTNASC'] = pd.to_datetime(sinasc['DTNASC'])
limite = len(sinasc) * 1 
sinasc = sinasc.dropna(thresh=limite, axis=1)

st.markdown("<h1 style='text-align: center; color: red;'> Análise Sinasc 2019 </h1>", unsafe_allow_html=True)
st.markdown("[Linkedin](https://www.linkedin.com/in/jos%C3%A9-eduardo-souza-leite-192405288/)")
st.markdown("[Portfólio](https://github.com/jeduardosleite)")
st.markdown("Primeiro exercício utilizando streamlit e VS Code como IDES.")
st.markdown("<h3 style='text-align: center; color: white;'> Banco de dados SINASC_2019 </h3>", unsafe_allow_html=True)

st.write(sinasc)

min_data = sinasc.DTNASC.min()
max_data = sinasc.DTNASC.max()

datas = pd.DataFrame(sinasc.DTNASC.unique(), columns=['DTNASC'])
datas.sort_values(by='DTNASC', inplace=True, ignore_index=True)

data_inicial = st.sidebar.date_input("Data inicial",
                           value = min_data,
                           min_value = min_data,
                           max_value = max_data)
data_final = st.sidebar.date_input("Data final",
                           value = max_data,
                           min_value = min_data,
                           max_value = max_data)

st.sidebar.write("Data inicial é: ", data_inicial)
st.sidebar.write("Data final é: ", data_final)


sinasc = sinasc[(sinasc['DTNASC'] <= pd.to_datetime(data_final)) &
                (sinasc['DTNASC'] >= pd.to_datetime(data_inicial))]
sim_nao = st.sidebar.selectbox(
    'Aceita passar seu contato?', ('Sim', 'Não'))

if sim_nao == 'Sim':
    contato = st.sidebar.selectbox(
        'Como você gostaria de ser contatado?',
        ('Email', 'Whatsapp', 'Telefone')
    )
    info = st.sidebar.text_input(f"Digite aqui o {contato.lower()}:")
else:
    st.sidebar.write("Você optou por não fornecer contato.")


st.markdown("<h3 style='text-align: center; color: white;'> Gráficos </h3>", unsafe_allow_html=True)
sinasc['DTNASC'] = pd.to_datetime(sinasc['DTNASC'])

plota_pivot_table(sinasc, 'IDADEMAE', 'DTNASC', 'mean', 'média idade mãe por data', 'data nascimento', 'unstack')
plota_pivot_table(sinasc, 'IDADEMAE', ['DTNASC', 'CONSULTAS'], 'mean', 'media idade mae','data de nascimento','unstack')
plota_pivot_table(sinasc, 'PESO', ['DTNASC', 'CONSULTAS'], 'mean', 'media peso bebe','data de nascimento','unstack')
plota_pivot_table(sinasc, 'PESO', 'DTNASC', 'median', 'PESO mediano','data nascimento')
plota_pivot_table(sinasc, 'CONSULTAS', 'DTNASC', 'mean', 'Consultas média','data nascimento')


st.markdown("<h3 style='text-align: center; color: white;'> Nascimentos em 2019 </h3>", unsafe_allow_html=True)

sinasc_map = pd.read_csv(r"C:\Users\Meu Computador\anaconda3\EBAC\M15_Streamlit\Tarefa\sinasc.csv")

sinasc_map = sinasc_map.dropna(subset=['munResLat', 'munResLon'])
sinasc_map = sinasc_map.rename(columns={'munResLat': 'lat', 'munResLon': 'lon'})

nascimentos_por_local = sinasc_map.groupby(['lat', 'lon']).size().reset_index(name='nascimentos')


layer = pdk.Layer(
    "ScatterplotLayer",
    data=nascimentos_por_local,
    get_position='[lon, lat]',
    get_fill_color='[255, 0, 0, 140]',
    get_radius='nascimentos * 7',
    pickable=True,
)

view_state = pdk.ViewState(
    latitude=nascimentos_por_local['lat'].mean(),
    longitude=nascimentos_por_local['lon'].mean(),
    zoom=5.5,
    pitch=0,
)

st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style='mapbox://styles/mapbox/outdoors-v9',
    tooltip={"text": "{nascimentos} nascimentos"},
))


x = st.slider("De 0 a 100, qual nota você dá para esta apresentação?")
st.write("Sua nota é: ", x)

if "counter" not in st.session_state:
    st.session_state.counter = 0

st.session_state.counter += 1

st.header(f"Esta página foi visitada {st.session_state.counter} vezes.")
st.button("Ir novamente")