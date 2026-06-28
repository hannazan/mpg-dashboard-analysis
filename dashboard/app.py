import pandas as pd
import hvplot.pandas  
import panel as pn

pn.extension('tabulator')  
df = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/mpg.csv")
df = df.dropna(subset=['mpg', 'horsepower', 'weight', 'cylinders', 'origin', 'model_year'])

origin_select = pn.widgets.MultiSelect(
    name='Pilih Origin',
    options=sorted(df['origin'].unique().tolist()),
    value=['usa'],)

year_slider = pn.widgets.IntRangeSlider(
    name='Rentang Tahun',
    start=int(df['model_year'].min()),
    end=int(df['model_year'].max()),
    value=(int(df['model_year'].min()), int(df['model_year'].max())),)

@pn.depends(origin_select, year_slider)
def filtered_data(origin_select, year_slider):
    subset = df[
        (df['origin'].isin(origin_select)) &
        (df['model_year'] >= year_slider[0]) &
        (df['model_year'] <= year_slider[1])    ]
    return subset

@pn.depends(origin_select, year_slider)
def plot_distribusi(origin_select, year_slider):
    data = filtered_data(origin_select, year_slider)
    return data.hvplot.hist(y='mpg', bins=20, color='skyblue', title='Distribusi Nilai MPG')

@pn.depends(origin_select, year_slider)
def plot_hubungan(origin_select, year_slider):
    data = filtered_data(origin_select, year_slider)
    return data.hvplot.scatter(
        x='weight', y='mpg', by='cylinders',
        size=80, alpha=0.6,
        title='Hubungan Antara Berat Mobil dan MPG'    )

@pn.depends(origin_select)
def plot_tren(origin_select):
    data = df[df['origin'].isin(origin_select)]
    avg_mpg = data.groupby('model_year')['mpg'].mean().reset_index()
    return avg_mpg.hvplot.line(
        x='model_year', y='mpg', marker='o',
        title='Tren Rata-rata MPG per Tahun'    )

dashboard = pn.Column(
    pn.pane.Markdown("## 🚗 Dashboard Analisis Data Mobil (MPG Dataset)"),
    pn.pane.Markdown("Gunakan filter di bawah untuk menjelajahi data:"),
    pn.Row(origin_select, year_slider),
    pn.Spacer(height=10),
    pn.Tabs(
        ("Distribusi MPG", plot_distribusi),
        ("Hubungan Weight vs MPG", plot_hubungan),
        ("Tren MPG per Tahun", plot_tren)    ),)

dashboard.servable()