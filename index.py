# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser (npx kill-port 8050)
import io
import base64
from dash import Dash, html, dcc,  Input, Output, no_update
import plotly.express as px
import pandas as pd
from PIL import Image

app = Dash(__name__)
colors = {
    'background': '#1f2132',
    'text': '#5dc8aa',
    'bar': '#f9d824'
}

df = pd.read_csv('Reporte_C_02_Et.csv')
rows= []
for i in range(0,len(df)):
    rows.append(i)

fig = px.scatter(df, x=rows,y="RT",
                 size="Area MI R", hover_name="Compound Name", color="RT",
                 labels={"x": "Compound Number", "RT": "Retention Time"})

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

fig.update_layout(title_text='Relative Area Compound (%)',title_y=0.95,title_x=0.5)

fig2 = px.scatter(df, x=rows,y=" Match Score",
                 size="Area MI R", hover_name="Compound Name", color=" Match Score",
                 labels={"x": "Compound Number"})

fig2.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

fig2.update_layout(title_text='Compound Match',title_y=0.95,title_x=0.5)

df2 = pd.read_csv('clasificacion.csv') 
fig3 = px.pie(df2, values="number1", names="Amino acids", hole=.3)
fig3.update_traces(hoverinfo='name', textinfo='label')
fig3.update_layout(showlegend=False)
fig3.update_layout(title_text="Amino acids",title_y=0.95,title_x=0.5)
fig3.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

labels = ["Amino acids",	"Alkaloids",	"Carbohydrates",	
"Saturated",	"Unsaturated",	"Terpenes",	"Acids",	"Bases",	
"Polyalcohols",	"Amino derivatives",	"Diamines",	
"Amides",	"Alcohols",	"Aldehydes"]
values = [18.5185185185185,	6.17283950617284,	9.25925925925926,	22.2222222222222,	12.962962962963, 0.617283950617284,	63.5802469135803,	4.32098765432099,		25.9259259259259,	12.962962962963,	0.617283950617284,	2.46913580246914,	10.4938271604938,	0.617283950617284]
fig4 = px.bar(x=labels,y=values,labels={"x": " ", "y": "Percentage (%)"},text=values)
fig4.update_traces(texttemplate='%{text:.2}%', textposition='outside')
fig4.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
fig4.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
fig4.update_layout(title_text="Compound Classification",title_y=0.95,title_x=0.5)

fig5 = px.pie(df2, values="number2", names="Alkaloids", hole=.3)
fig5.update_traces(hoverinfo='name', textinfo='label')
fig5.update_layout(showlegend=False)
fig5.update_layout(title_text="Alkaloids",title_y=0.95,title_x=0.5)
fig5.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
image_filename = 'khoka.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app.layout = html.Div(
    className="contenedor",
    children=[
     html.Div(
         className="header",
         children=[
         html.Div(children =[ 
         html.Div(className="image"),
         #html.H2('Khoka Extracts',className="app-header"),
         #html.H5('A web application for your chromatography data.',className="app-header"),
         ])
         ]),
     html.Div(
        className="area1",
        children=[
         dcc.Graph(
            id='area',
            figure=fig,
            clear_on_unhover=True),
         dcc.Tooltip(id="graph-tooltip-2", direction='bottom')
        ]),    
     html.Div(
        className="class",
        children=[
            dcc.Graph(
            id='class',
            figure=fig4,
            clear_on_unhover=True
        )]),
     html.Div(
        className="match1",
        children=[
            dcc.Graph(
            id='match',
            figure=fig2
       )]),
    html.Div(
    className="classsification",
    children=[
        dcc.Graph(
        id='classification1',
        figure=fig3,
        clear_on_unhover=True
    )]),
    html.Div(
    className="classsification",
    children=[
        dcc.Graph(
        id='classification2',
        figure=fig5,
        clear_on_unhover=True
    )]),
    html.Div(
         className="footer",
         children=[
         html.H2('Exlonk Gil',className="footer"),
         ]),
])

@app.callback(
    Output("graph-tooltip-2", "show"),
    Output("graph-tooltip-2", "bbox"),
    Output("graph-tooltip-2", "children"),
    Output("graph-tooltip-2", "direction"),
    Input("area", "hoverData"),

)

def display_hover(hoverData):

    if hoverData is None:
        return False, no_update, no_update, no_update

    # demo only shows the first point, but other points may also be available
    hover_data = hoverData["points"][0]
    bbox = hover_data["bbox"]
    # Fragmento que permite cambiar la imagen en función del hover #
    compound = str(hoverData["points"][0].get("hovertext"))
    if compound == "Glycine, 3TMS derivative" or compound == "Trigonelline TMS" or compound == "quinicacid(5TMS)":
        pass
    else:
      compound = "benzene"
    
    # Load image with pillow
    image_path = '/media/Particion_E/1_Proyectos/Amenity/Cromatogramas/Copia/Aplicacion/'+compound+'.png' 
    im = Image.open(image_path)

    # dump it to base64
    buffer = io.BytesIO()
    im.save(buffer, format="png")
    encoded_image = base64.b64encode(buffer.getvalue()).decode()
    im_url = "data:image/png;base64, " + encoded_image

    # control the position of the tooltip
    y = hover_data["y"]
    direction = "bottom" if y > 1.5 else "top"

    children = [
        html.Img(
            src=im_url,
            style={"width": "100px"},
        ),
    ]

    return True, bbox, children, direction


if __name__ == '__main__':
    app.run_server(debug=True)