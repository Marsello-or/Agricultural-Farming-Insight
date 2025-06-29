# -*- coding: utf-8 -*-
"""Agriculture Farming Dataset.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1pnv3dY9QVMBzC_r8pcivLpz5xdrP_DvC
"""

!pip install dash pandas plotly
!pip install dash pandas plotly dash-core-components dash-html-components

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# 1. Memuat Dataset
df = pd.read_csv('https://raw.githubusercontent.com/Marsello-or/Agricultural-Farming-Insight/refs/heads/main/agriculture_dataset.csv')

# Menambahkan opsi 'Semua' untuk filter dropdown
all_crops = [{'label': 'Semua Tanaman', 'value': 'all'}] + [{'label': crop, 'value': crop} for crop in df['Crop_Type'].unique()]
all_seasons = [{'label': 'Semua Musim', 'value': 'all'}] + [{'label': season, 'value': season} for season in df['Season'].unique()]


# 2. Inisialisasi Aplikasi Dash
app = dash.Dash(__name__)
server = app.server

# 3. Mendefinisikan Layout Aplikasi
app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#f9f9f9', 'padding': '20px'}, children=[
    # Judul Dashboard
    html.H1(
        'Dashboard Analisis Pertanian',
        style={'textAlign': 'center', 'color': '#333'}
    ),
    html.P(
        'Dashboard interaktif untuk menganalisis faktor-faktor yang mempengaruhi hasil panen.',
        style={'textAlign': 'center', 'color': '#666', 'marginBottom': '30px'}
    ),

    # Kontainer untuk Filter
    html.Div([
        html.Div([
            html.Label('Pilih Jenis Tanaman:', style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='crop-filter',
                options=all_crops,
                value='all', # Nilai default
                clearable=False
            )
        ], style={'width': '48%', 'display': 'inline-block', 'paddingRight': '2%'}),

        html.Div([
            html.Label('Pilih Musim Tanam:', style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='season-filter',
                options=all_seasons,
                value='all', # Nilai default
                clearable=False
            )
        ], style={'width': '48%', 'display': 'inline-block'})
    ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '5px', 'boxShadow': '0 2px 4px #eee', 'marginBottom': '20px'}),

    # Kontainer untuk Grafik
    html.Div([
        # Baris pertama grafik
        html.Div([
            dcc.Graph(id='fertilizer-yield-scatter'),
            dcc.Graph(id='pesticide-yield-scatter'),
        ], style={'display': 'flex', 'width': '100%', 'marginBottom': '20px'}),

        # Baris kedua grafik
        html.Div([
            dcc.Graph(id='yield-by-irrigation-bar'),
            dcc.Graph(id='water-usage-bar'),
        ], style={'display': 'flex', 'width': '100%', 'marginBottom': '20px'}),

        # Baris ketiga untuk Heatmap
        html.Div([
            dcc.Graph(id='yield-heatmap')
        ], style={'width': '100%'})
    ])
])


# 4. Mendefinisikan Callback untuk Interaktivitas
@app.callback(
    [Output('fertilizer-yield-scatter', 'figure'),
     Output('pesticide-yield-scatter', 'figure'),
     Output('yield-by-irrigation-bar', 'figure'),
     Output('water-usage-bar', 'figure'),
     Output('yield-heatmap', 'figure')], # Menambahkan output untuk heatmap
    [Input('crop-filter', 'value'),
     Input('season-filter', 'value')]
)
def update_graphs(selected_crop, selected_season):
    # Filter data berdasarkan pilihan dropdown
    filtered_df = df.copy()
    if selected_crop != 'all':
        filtered_df = filtered_df[filtered_df['Crop_Type'] == selected_crop]
    if selected_season != 'all':
        filtered_df = filtered_df[filtered_df['Season'] == selected_season]

    # Membuat Grafik 1: Pupuk vs Hasil Panen
    fig1 = px.scatter(
        filtered_df, x='Fertilizer_Used(tons)', y='Yield(tons)',
        trendline="ols", title='Pupuk vs Hasil Panen',
        labels={'Fertilizer_Used(tons)': 'Pupuk (ton)', 'Yield(tons)': 'Hasil Panen (ton)'},
        template='plotly_white'
    )
    fig1.update_layout(title_x=0.5)

    # Membuat Grafik 2: Pestisida vs Hasil Panen
    fig2 = px.scatter(
        filtered_df, x='Pesticide_Used(kg)', y='Yield(tons)',
        trendline="ols", title='Pestisida vs Hasil Panen',
        labels={'Pesticide_Used(kg)': 'Pestisida (kg)', 'Yield(tons)': 'Hasil Panen (ton)'},
        template='plotly_white'
    )
    fig2.update_layout(title_x=0.5)

    # Membuat Grafik 3: Rata-rata Hasil Panen berdasarkan Irigasi
    avg_yield_irrigation = filtered_df.groupby('Irrigation_Type')['Yield(tons)'].mean().reset_index()
    fig3 = px.bar(
        avg_yield_irrigation, x='Irrigation_Type', y='Yield(tons)',
        title='Rata-rata Hasil Panen per Jenis Irigasi',
        labels={'Irrigation_Type': 'Jenis Irigasi', 'Yield(tons)': 'Rata-rata Hasil Panen (ton)'},
        template='plotly_white'
    )
    fig3.update_layout(title_x=0.5)

    # Membuat Grafik 4: Rata-rata Penggunaan Air berdasarkan Tanaman
    base_df_water = df.copy()
    if selected_crop != 'all':
         base_df_water = df[df['Crop_Type'] == selected_crop]
    avg_water_usage = base_df_water.groupby('Crop_Type')['Water_Usage(cubic meters)'].mean().reset_index()
    fig4 = px.bar(
        avg_water_usage, x='Crop_Type', y='Water_Usage(cubic meters)',
        title='Rata-rata Penggunaan Air per Jenis Tanaman',
        labels={'Crop_Type': 'Jenis Tanaman', 'Water_Usage(cubic meters)': 'Rata-rata Penggunaan Air (m³)'},
        template='plotly_white'
    )
    fig4.update_layout(title_x=0.5)

    # Membuat Grafik 5: Heatmap Hasil Panen (Berdasarkan data keseluruhan, bukan data terfilter)
    pivot_table = df.pivot_table(values='Yield(tons)', index='Crop_Type', columns='Irrigation_Type', aggfunc='mean')
    fig5 = go.Figure(data=go.Heatmap(
        z=pivot_table.values,
        x=pivot_table.columns,
        y=pivot_table.index,
        colorscale='YlGnBu',
        text=pivot_table.values,
        texttemplate="%{text:.2f}"
    ))
    fig5.update_layout(
        title='Heatmap: Kombinasi Tanaman & Irigasi untuk Hasil Panen Terbaik',
        xaxis_title='Tipe Irigasi',
        yaxis_title='Jenis Tanaman',
        title_x=0.5
    )


    return fig1, fig2, fig3, fig4, fig5


# 5. Menjalankan Server
if __name__ == '__main__':
    app.run(debug=True) # Ganti run_server dengan run

