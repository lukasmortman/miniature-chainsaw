import json
from collections import Counter
import pandas as pd
import dateutil.parser
import plotly.express as px
import plotly.graph_objects as go


def dataläsare(file):
    with open(file, encoding="utf-8") as f:
        return json.load(f)


def antalgångerfunc(data):
    sånglista = []
    for rad in data["data"]:
        sånglista.append(rad["data"]["name"])
    sånglista = dict(Counter(sånglista))
    return sånglista


def antalgångerochlåtnamn(data):
    låtar = []
    antalgånger = []
    sånglista = antalgångerfunc(data)
    for rad in sånglista:
        låtar.append(rad)
        antalgånger.append(sånglista[rad])
    df1 = pd.DataFrame({'låt': låtar, 'antal gånger': antalgånger})
    df1.sort_values('antal gånger', ascending=False, inplace=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df1["låt"].head(10),
        y=df1["antal gånger"].head(10),
        name='antal gånger låtar blivit spelade'
    ))
    fig.update_layout(title_text="antal gånger låtar blivit spelade")
    fig.update_xaxes(title_text="låtar")
    fig.update_yaxes(title_text="antal gånger spelade")

    fig.update_layout(
        updatemenus=[
            dict(
                buttons=list([
                    dict(
                        label="Top 10 spelade låtar",
                        method="restyle",
                        args=[{"y": [df1["antal gånger"].head(10)], "x": [df1["låt"].head(10)]}],
                    ),
                    dict(
                        label="Top 20 spelade låtar",
                        method="restyle",
                        args=[{"y": [df1["antal gånger"].head(20)], "x": [df1["låt"].head(20)]}]
                    ),
                    dict(
                        label="Top 50 spelade låtar",
                        method="restyle",
                        args=[{"y": [df1["antal gånger"].head(50)], "x": [df1["låt"].head(50)]}]
                    )
                ]),
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=1,
                xanchor="left",
                y=1.1,
                yanchor="top"
            ),
        ]
    )

    fig.show(config={'displaylogo': False})


def datumochantalgånger(data):
    datum = []
    låtar = []
    for rad in data["data"]:
        datum.append(dateutil.parser.isoparse(rad["played_at"]).date())
        låtar.append(rad["data"]["name"])
    datumframe = pd.DataFrame({'datum': pd.to_datetime(datum, infer_datetime_format=True), 'lyssningar': låtar})
    s = datumframe['datum'].value_counts().sort_index()
    nydatumframe = pd.DataFrame({'datum': s.index, 'lyssningar': s.values})
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=nydatumframe["datum"], y=nydatumframe["lyssningar"], fill='tozeroy'))
    fig.update_layout(title_text="antal lyssningar per vecka")
    fig.update_xaxes(title_text="datum")
    fig.update_yaxes(title_text="lyssningar")
    fig.show(config={'displaylogo': False})


def tabellmedalldata(data):
    s = antalgångerfunc(data)
    listamedpopularitet, listamedgångerlyssnade, litstamedlåtnamn, listamedartist, listameddatumsläppt = [], [], [], [], []
    for rad in data["data"]:
        for x, y in s.items():
            if x == rad["data"]["name"]:
                listamedpopularitet.append((rad["data"]["popularity"]))
                litstamedlåtnamn.append(rad["data"]["name"])
                listamedartist.append(rad["data"]["artists"][0]["name"])
                listameddatumsläppt.append(rad["data"]["album"]["release_date"])
                listamedgångerlyssnade.append(y)
                break
    tabellframe = pd.DataFrame(
        {'låttitel': litstamedlåtnamn, 'artistnamn': listamedartist, 'popularitet': listamedpopularitet,
         'datum': listameddatumsläppt, "antal gånger lyssnade": listamedgångerlyssnade})
    tabellframe.sort_values('antal gånger lyssnade', ascending=False, inplace=True)
    tabellframe.drop_duplicates(subset="låttitel", keep="first", inplace=True)
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(tabellframe.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(
            values=[tabellframe["låttitel"], tabellframe["artistnamn"], tabellframe["popularitet"],
                    tabellframe["datum"],
                    tabellframe["antal gånger lyssnade"]],
            fill_color='lavender',
            align='left'))
    ])
    fig.show(config={'displaylogo': False})


data = dataläsare("data.json")

datumochantalgånger(data)
