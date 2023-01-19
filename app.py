from datetime import datetime
import dash  # pip install dash
from dash import dcc, Output, Input, State, ctx, no_update
from dash import html
import dash_bootstrap_components as dbc  # pip install dash_bootstrap_components
import base64
import os
import pandas as pd  # version 1.4.3
import io
import uuid
import api  # local file
import helper  # local file
import pickle
import math
import ast  # convert str of list to list
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# dropdowns
catalog_category = pd.read_csv('assets/dropdown_df/dropdown_catalog_category.csv')['options']
catalog_brand = pd.read_csv('assets/dropdown_df/dropdown_catalog_brand.csv')['options']

ajio_category = pd.read_csv('assets/dropdown_df/dropdown_ajio_category.csv')['options']
ajio_brand = pd.read_csv('assets/dropdown_df/dropdown_ajio_brand.csv')['options']

bijnis_category = pd.read_csv('assets/dropdown_df/dropdown_bijnis_category.csv')['options']
bijnis_brand = pd.read_csv('assets/dropdown_df/dropdown_bijnis_brand.csv')['options']

udaan_category = pd.read_csv('assets/dropdown_df/dropdown_udaan_category.csv')['options']
udaan_brand = pd.read_csv('assets/dropdown_df/dropdown_udaan_brand.csv')['options']

client_data = pd.read_csv("store_user_data.csv")


def search_data(index, search_id, api, helper, filename="assets/input_file/file_search/data.csv"):
    global client_data
    # print(search_id)
    pd.DataFrame().to_csv(f"assets/outputs/annotation/{search_id}.csv")
    # print("File saved")
    cat = ""
    brand = ""
    try:
        cat = ast.literal_eval(client_data.loc[index]['category'])
    except:
        pass
    try:
        brand = ast.literal_eval(client_data.loc[index]['brand'])
    except:
        pass

    url = api.url(cat, brand, client_data.loc[index]['catalog'],
                  client_data.loc[index]['scraped'], client_data.loc[index]['ajio'],
                  client_data.loc[index]['bijnis'], client_data.loc[index]['udaan'],
                  client_data.loc[index]['threshold'],
                  client_data.loc[index, 'search_request_id'], client_data.loc[index]['file_search'])
    # print("URL: ", url)
    result = api.get_result(url, filename, client_data.loc[index]['catalog'])
    client_data.loc[index, 'result_list'] = str(result)

    if type(result) == list:
        children1 = []
        product = helper.DisplayImage()
        for search in result[:int(client_data.loc[index]['no_of_search'])]:  # search is a dict
            img_url = search['ImageUrl']
            img_id = search['downloaded_image_path'].split("/")[-1]
            similar_result = search['similar']
            children1.append(product.display_image(img_url, img_id, similar_result))

        if len(result) < int(client_data.loc[index]['no_of_search']):
            show_np = {'display': 'None'}
        else:
            show_np = {}

        client_data.loc[index, 'start'] = 0
        client_data.loc[index, 'end'] = int(client_data.loc[index]['no_of_search'])
        client_data.loc[index, 'page'] = 1
        client_data.loc[index, 'total_page'] = math.ceil(
            len(result) / int(client_data.loc[index]['no_of_search']))
        client_data.loc[index, 'search_item'] = len(result)
        message = f"Total Searched Items: {int(client_data.loc[index]['search_item'])}, Page: {int(client_data.loc[index]['page'])}/{int(client_data.loc[index]['total_page'])}"
        dis_child = children1
        dis_child.insert(0, html.Div(html.H4(message), className="text-center"))
        #         print("Search time: ", datetime.now()-searcht)

        return dis_child, f"Search in process...Internal file location: \"assets/outputs/annotation/{search_id}.csv\"", True, show_np
    else:
        return no_update, result, True, no_update


theme = [dbc.themes.SOLAR]  # page theme
app = dash.Dash(__name__, external_stylesheets=theme, suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}])
server = app.server
app.title = 'KonnectBox Product Recommender'
app._favicon = "kb.png"
app.layout = dbc.Container([
    # navbar
    dbc.NavbarSimple(fixed='top',
                     brand="KonnectBox Fashion Product Recommender",
                     brand_href="/",
                     color="warning",
                     dark=True,
                     className='py-0'),
    html.Br(),
    html.Br(),
    dcc.Store(id="store"),
    dcc.Store(id="store_download_data"),

    # Search Type Radio Button
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.Label("Select Search type"),
                dcc.RadioItems(options=['Image Search', 'File Search', 'Catalog Search'],
                               value='File Search',
                               id="search_radio_btn",
                               inline=True,
                               inputStyle={"margin-left": "10px",
                                           "margin-right": "5px",
                                           "margin-top": "10px"}
                               ),
                dcc.Upload(id='upload_file',
                           children=html.Div(['Drag and Drop or ', html.A('Select a File.',
                                                                          style={'text-decoration': 'underline',
                                                                                 'color': 'blue'})]),
                           style={
                               'width': '90%',
                               'height': '50px',
                               'lineHeight': '50px',
                               'borderWidth': '3%',
                               'borderStyle': 'dashed',
                               'borderRadius': '5px',
                               'textAlign': 'center',
                               'margin': '5%',
                           },
                           multiple=True,  # Allow multiple files to be uploaded
                           ),
            ], className="text-center", style={"height": '150px'})
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Select Database: "),
                    ], className="text-left", width=5),
                    dbc.Col([
                        dcc.RadioItems(options=['Catalog', 'Scraped'],
                                       value='Catalog',
                                       id="database",
                                       inline=False,
                                       inputStyle={"margin-left": "10px",
                                                   "margin-right": "5px",
                                                   "margin-top": "4px"}
                                       ),
                    ], className="text-left")
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Sub-Database: "),
                    ], className="text-left", width=5),
                    dbc.Col([
                        dcc.Checklist(options=['Ajio', 'Ajio_Business', 'Bijnis', 'Udaan'],
                                      # value='Ajio',
                                      id="scraped_from",
                                      inline=True,
                                      inputStyle={"margin-left": "10px",
                                                  "margin-right": "5px",
                                                  "margin-top": "4px"},
                                      )
                    ], className="text-left")
                ], id="sub_data_show", style={"display": "None"}),
                dbc.Row([
                    html.Div(id='dropdown'),
                ]),
            ], className="text-center", style={"height": '150px'})
        ], width=5),
        dbc.Col([
            dbc.Card([
                dbc.Label('Matching Threshold Value %:', className="m-0"),
                dcc.Slider(0, 100, 1, value=80, marks=None, tooltip={"placement": "right", "always_visible": True},
                           id='threshold', className="m-0"),
                dbc.Button('SEARCH',
                           id='search',
                           # href=f"/{client_data.loc[index]['search_request_id']}",
                           n_clicks=0,
                           className="m-1",
                           # style={'width': "100%"}
                           loading_state={'is_loading': 'True'}
                           ),
                dbc.Row([
                    dbc.Col([
                        dbc.Button('Clear',
                                   id='clear',
                                   n_clicks=0,
                                   color="danger",
                                   className="mx-1",
                                   style={'width': "100%"}
                                   ),
                        dcc.ConfirmDialog(id='file_save_alert'),
                    ], width='auto'),
                    dbc.Col([
                        dbc.Button(children=[html.Img(src="assets/delete.svg", width="20px", height="20px")],
                                   id='delete',
                                   n_clicks=0,
                                   color="danger",
                                   className="mx-1",
                                   style={'width': "100%"}
                                   ),
                    ], width='auto'),
                    dbc.Col([
                        dbc.Button('Download',
                                   id='save',
                                   n_clicks=0,
                                   color="danger",
                                   className="mx-1",
                                   style={'width': "100%"}
                                   ),
                    ], width='auto'),

                    dcc.Download(id="download_file")
                ], justify="center", align="center")
            ], className="text-center", style={"height": '150px'}),
        ]),
    ]),
    dcc.ConfirmDialog(id='alert'),
    html.Br(),
    dcc.Loading(id='result', className="m-2 bg-dark bg-gradient", type="default", fullscreen=True, color="#119DFF", ),
    # Result image div
    html.Div(id='data2', style={'display': 'None'}),
    html.Div(id='data3', style={'display': 'None'}),
    html.Div(id='multi_page',
             children=[
                 dbc.Button("Previous", id="prev", href="/", n_clicks=0, className="mx-4"),
                 dbc.Button("Next", id="next", n_clicks=0, href="/", className="mx-4"),
             ],
             className="m-5 text-center", style={'display': 'none'}),

], fluid=True)


@app.callback(
    Output('upload_file', 'disabled'),
    Output('store', 'data'),
    Input("search_radio_btn", 'value')
)
def search_type(stype):
    global client_data
    user_id = str(uuid.uuid4())
    client_data = client_data.append({'id': user_id,
                                      'image_uploaded': 0,
                                      'file_search': None,
                                      'catalog': 0,
                                      'scraped': 0,
                                      'ajio': 0,
                                      'ajio_business': 0,
                                      'bijnis': 0,
                                      'udaan': 0,
                                      'category': None,
                                      'brand': None,
                                      'threshold': 0,
                                      'no_of_search': 5,
                                      'search_request_id': '',
                                      'result_list': None,
                                      'start': 0,
                                      'end': 5,
                                      'page': 1,
                                      'total_page': 0,
                                      'search_item': 0,
                                      'search_type': 'File Search'}, ignore_index=True)
    client_data.to_csv("store_user_data.csv", index=False)
    index = client_data[client_data['id'] == user_id].index[0]
    if stype == "Image Search":
        client_data.loc[index, 'search_type'] = 'Image Search'
        return False, index
    elif stype == 'File Search':
        client_data.loc[index, 'search_type'] = 'File Search'
        return False, index
    else:
        client_data.loc[index, 'search_type'] = 'Catalog Search'
        return True, index


# get radio buttons value
@app.callback(
    Output('dropdown', 'children'),
    Output('sub_data_show', 'style'),
    Input('database', 'value'),
    Input('scraped_from', 'value'),
    Input('store', 'data'),
    # prevent_initial_call=True
)
def update(db, val, index):
    global client_data
    client_data.loc[index, 'ajio'] = 0
    client_data.loc[index, 'ajio_business'] = 0
    client_data.loc[index, 'bijnis'] = 0
    client_data.loc[index, 'udaan'] = 0
    if db == "Catalog":
        client_data.loc[index, 'catalog'] = 1
        client_data.loc[index, 'scraped'] = 0
        client_data.loc[index, 'ajio'] = 0
        client_data.loc[index, 'ajio_business'] = 0
        client_data.loc[index, 'bijnis'] = 0
        client_data.loc[index, 'udaan'] = 0

        return helper.dropdown(catalog_category, catalog_brand), {'display': 'none'}

    else:
        client_data.loc[index, 'catalog'] = 0
        client_data.loc[index, 'scraped'] = 1
        if val is not None and len(val) == 1 and val[0] == 'Ajio':
            client_data.loc[index, 'ajio'] = 1
            client_data.loc[index, 'ajio_business'] = 0
            client_data.loc[index, 'bijnis'] = 0
            client_data.loc[index, 'udaan'] = 0
            return helper.dropdown(ajio_category, ajio_brand), {}
        elif val is not None and len(val) == 1 and val[0] == 'Ajio_Business':
            client_data.loc[index, 'ajio'] = 0
            client_data.loc[index, 'ajio_business'] = 1
            client_data.loc[index, 'bijnis'] = 0
            client_data.loc[index, 'udaan'] = 0
            return helper.dropdown(ajio_category, ajio_brand), {}  # need to change cat and brand
        elif val is not None and len(val) == 1 and val[0] == 'Bijnis':
            client_data.loc[index, 'ajio'] = 0
            client_data.loc[index, 'ajio_business'] = 0
            client_data.loc[index, 'bijnis'] = 1
            client_data.loc[index, 'udaan'] = 0
            return helper.dropdown(bijnis_category, bijnis_brand), {}
        elif val is not None and len(val) == 1 and val[0] == 'Udaan':
            client_data.loc[index, 'ajio'] = 0
            client_data.loc[index, 'ajio_business'] = 0
            client_data.loc[index, 'bijnis'] = 0
            client_data.loc[index, 'udaan'] = 1
            return helper.dropdown(udaan_category, udaan_brand), {}
        elif val is not None and len(val) > 1:
            client_data.loc[index, 'category'] = str(None)
            client_data.loc[index, 'brand'] = str(None)
            opt = ['Ajio', 'Ajio_Business', 'Bijnis', 'Udaan']
            for j in val:
                if j in opt:
                    client_data.loc[index, j.lower()] = 1
            return html.P("Multiple Database Search.", className='my-4'), {}
        else:
            return html.P("For Scraped: Select at least one checkbox", className='text-warning my-4'), {}


# get category, brand and threshold value
@app.callback(
    Output('data2', 'children'),
    Input('category_dpdn', 'value'),
    Input('brand_dpdn', 'value'),
    Input('threshold', 'value'),
    State("store", "data"),
    prevent_initial_call=True
)
def update(cat_val, brand_val, th, index):
    global client_data
    client_data.loc[index, 'category'] = str(cat_val)
    client_data.loc[index, 'brand'] = str(brand_val)
    client_data.loc[index, 'threshold'] = th
    return no_update


# display result.... search button
@app.callback(
    Output('result', 'children'),  # result display div
    Output('alert', 'message'),  # alert message
    Output('alert', 'displayed'),
    Output("multi_page", "style"),
    Input('search', 'n_clicks'),
    Input('clear', 'n_clicks'),
    Input("prev", "n_clicks"),
    Input("next", "n_clicks"),
    State('upload_file', 'contents'),
    State('upload_file', 'filename'),
    State("store", "data"),
    prevent_initial_call=True
)
def update(search_click, clear_click, prev_btn, next_btn, contents, filename, index):
    global client_data

    triggered_id = ctx.triggered_id  # button pressed
    # image search
    if triggered_id == "search":
        radio_val = client_data.loc[index]['search_type']
        fe_request_id = str(uuid.uuid4())  # frontend input file request id
        client_data.loc[index, 'search_request_id'] = fe_request_id
        # client_data.loc[index, 'store_data_df'] = pd.DataFrame()
        if radio_val == "Image Search":
            client_data.loc[index, 'file_search'] = False
            if triggered_id == "search" and contents is not None:
                # save input image
                # image_dir = os.path.join('/home/ubuntu/fashion/DuplicateImage/data/requests', fe_request_id)
                # os.mkdir(image_dir)
                # for idx, (image, name) in enumerate(zip(contents, filename)):
                #     with open(os.path.join(image_dir, f"img_{idx}.jpg"), 'wb') as fp:
                #         fp.write(base64.b64decode((image.split('base64,')[1])))
                #         fp.close()

                path = os.path.join("assets/input_file/image_search", fe_request_id)
                os.mkdir(path)
                for image, name in zip(contents, filename):
                    with open(os.path.join(f'assets/input_file/image_search/{fe_request_id}', f'{name}'), 'wb') as fp:
                        fp.write(base64.b64decode((image.split('base64,')[1])))
                        fp.close()
                return search_data(index, fe_request_id, api, helper, filename="assets/input_file/file_search/data.csv")
            elif search_click > 0 and contents is None:
                return no_update, "No image selected.", True, no_update

        # file search
        elif radio_val == "File Search":
            client_data.loc[index, 'file_search'] = True
            if triggered_id == "search":
                if contents is not None:
                    if len(contents) == 1:
                        if "csv" in contents[0]:
                            try:
                                os.remove(f'assets/input_file/file_search/data.csv')
                            except:
                                pass
                            content_type, content_string = contents[0].split(',')
                            decoded = base64.b64decode(content_string)
                            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
                            df.to_csv("assets/data.csv", index=False)
                            df = df.drop(df.columns[df.columns.str.contains('unnamed', case=False)], axis=1)
                            df = df.rename(columns={'Product_code': 'search_id'})
                            df.drop(['ImageUrl', 'brand'], axis=1).to_csv(f"assets/input_file/file_search/{fe_request_id}.csv", index=False)

                            # print("search request", fe_request_id)
                            return search_data(index, fe_request_id, api, helper, filename="assets/input_file/file_search/data.csv")
                        else:
                            return "", f"Select only a CSV file. Uploaded file : {filename}", True, {'display': 'None'}
                    else:
                        return "", "Select only one file, multiple selected.", True, {'display': 'None'}
                else:
                    return "", "Select a CSV file, no file selected.", True, {'display': 'None'}
        elif radio_val == 'Catalog Search':
            client_data.loc[index, 'file_search'] = False
            return search_data(index, fe_request_id, api, helper, filename="assets/input_file/file_search/data.csv")

    elif triggered_id == "next":
        # print("next search id: ", client_data.loc[index]['search_request_id'])
        try:
            if client_data.loc[index]['end'] < len(ast.literal_eval(client_data.loc[index]['result_list'])):
                client_data.loc[index, 'start'] = client_data.loc[index]['start'] + client_data.loc[index][
                    'no_of_search']
                client_data.loc[index, 'end'] = client_data.loc[index]['end'] + client_data.loc[index]['no_of_search']
                client_data.loc[index, 'page'] = client_data.loc[index]['page'] + 1
                children1 = []
                product = helper.DisplayImage()
                for search in ast.literal_eval(client_data.loc[index]['result_list'])[
                              int(client_data.loc[index]['start']):int(client_data.loc[index]['end'])]:  # search is a dict
                    img_url = search['ImageUrl']
                    img_id = search['downloaded_image_path'].split("/")[-1]
                    similar_result = search['similar']
                    children1.append(product.display_image(img_url, img_id, similar_result))
                message = f"Total Searched Items: {int(client_data.loc[index]['search_item'])}, Page: {int(client_data.loc[index]['page'])}/{int(client_data.loc[index]['total_page'])}"
                dis_child = children1
                dis_child.insert(0, html.Div(html.H4(message), className="text-center"))
                return dis_child, no_update, no_update, {}
            else:
                return no_update, no_update, no_update, {}
        except Exception as e:
            return no_update, e, True, {}

    elif triggered_id == "prev":
        try:
            if client_data.loc[index]['start'] > 0:
                client_data.loc[index, 'start'] = client_data.loc[index]['start'] - client_data.loc[index][
                    'no_of_search']
                client_data.loc[index, 'end'] = client_data.loc[index]['end'] - client_data.loc[index]['no_of_search']
                client_data.loc[index, 'page'] = client_data.loc[index]['page'] - 1
                children1 = []
                product = helper.DisplayImage()
                for search in ast.literal_eval(client_data.loc[index]['result_list'])[
                              int(client_data.loc[index]['start']):int(client_data.loc[index]['end'])]:  # search is a dict
                    img_url = search['ImageUrl']
                    img_id = search['downloaded_image_path'].split("/")[-1]
                    similar_result = search['similar']
                    children1.append(product.display_image(img_url, img_id, similar_result))

                message = f"Total Searched Items: {int(client_data.loc[index]['search_item'])}, Page: {int(client_data.loc[index]['page'])}/{int(client_data.loc[index]['total_page'])}"
                dis_child = children1
                dis_child.insert(0, html.Div(html.H4(message), className="text-center"))
                etime = datetime.now()
                # print("Prev load time: ", etime - stime)
                return dis_child, no_update, no_update, {}
            else:
                return no_update, no_update, no_update, {}
        except Exception as e:
            return no_update, e, True, {}

    elif triggered_id == "clear":
        client_data.loc[index, 'start'] = 0
        client_data.loc[index, 'end'] = client_data.loc[index]['no_of_search']
        client_data.loc[index, 'page'] = 1
        client_data.loc[index, 'total_page'] = 0
        client_data.loc[index, 'store_data_df'] = pd.DataFrame()
        # pyautogui.hotkey('ctrl', 'r')
        return "", no_update, no_update, {"display": 'None'}


# correct/wrong buttons handling
for i in range(400):
    @app.callback(
        Output(f"correct{i}", "disabled"),
        Output(f"correct{i}", "outline"),
        Output(f"wrong{i}", "disabled"),
        Output(f"wrong{i}", "outline"),
        Input(f'correct{i}', 'n_clicks'),
        Input(f'wrong{i}', 'n_clicks'),
        Input(f'correct{i}', 'key'),
        Input(f'wrong{i}', 'key'),
        State("store", "data"),
        prevent_initial_call=True
    )
    def update(correct_click, wrong_click, correct_data, wrong_data, index):
        triggered_id = ctx.triggered_id
        # print(triggered_id)
        global client_data
        sid = client_data.loc[index]['search_request_id']
        if "correct" in triggered_id:
            correct_val = correct_data.split("&&&")
            data = {'search_id': correct_val[0], 'product_id': correct_val[1], 'product_link': correct_val[2],
                    'img_url': correct_val[3], 'score': correct_val[4]}
            df = pd.read_csv(f"assets/outputs/annotation/{sid}.csv")
            df = df.append(data, ignore_index=True)
            df.to_csv(f"assets/outputs/annotation/{sid}.csv", index=False)
            # print("correct")
            return True, False, False, True

        elif "wrong" in triggered_id:
            wrong_val = wrong_data.split("&&&")
            data = {'search_id': wrong_val[0], 'product_id': wrong_val[1], 'product_link': wrong_val[2],
                    'img_url': wrong_val[3], 'score': wrong_val[4], 'result': 'wrong'}
            df = pd.read_csv(f"assets/outputs/annotation/{sid}.csv")
            df = df.append(data, ignore_index=True)
            df.to_csv(f"assets/outputs/annotation/{sid}.csv", index=False)
            # print("wrong")
            return False, True, True, False
        else:
            # print("initial")
            return False, True, False, True


# pkl and df save alert
@app.callback(
    Output("file_save_alert", "message"),
    Output("file_save_alert", "displayed"),
    Output("download_file", "data"),
    Input("save", "n_clicks"),
    Input("delete", "n_clicks"),
    State('store', "data"),
    prevent_initial_call=True
)
def save_data(save, delete, index):
    triggered_id = ctx.triggered_id
    # print('index: ', index)
    sid = client_data.loc[index]['search_request_id']
    if triggered_id == "save":
        if os.path.exists(f"assets/outputs/annotation/{sid}.csv"):
            df = pd.read_csv(f"assets/outputs/annotation/{sid}.csv")
            if not df.empty:
                try:
                    df_mrp = pd.read_csv(f"assets/input_file/file_search/{sid}.csv")
                    df = df.merge(df_mrp, on='search_id')
                    with open(os.path.join('assets/outputs/annotation', f'{sid}.pkl'), 'wb') as f:
                        pickle.dump(df, f)
                    alert_message = f"File Saved!!, internal file location: assets/outputs/annotation/{sid}.csv"
                    # df = df.drop(df.columns[df.columns.str.contains('unnamed', case=False)], axis=1)
                    data = dcc.send_data_frame(df.to_csv, "Matching Results.csv", index=False)
                except Exception as e:
                    alert_message = f'Error: {e}, recovery file location: assets/outputs/annotation/{sid}.csv'
                    # alert_message = f'File saved!!'
                    data = dcc.send_data_frame(df.to_csv, "Matching Results.csv", index=False)
                return alert_message, True, data
            else:
                return "No records to download.", True, no_update
        else:
            return "Search again, something went wrong.", True, no_update

    elif triggered_id == 'delete':
        # print("delete pressed")
        filename = f"assets/outputs/annotation/{sid}.csv"
        if os.path.exists(filename):
            df = pd.read_csv(filename)
            if not df.empty:
                # df = pd.read_csv(f"assets/outputs/output{index}.csv")
                df = df.iloc[:-1]
                df.to_csv(filename, index=False)
                return "Last record deleted", True, no_update
            return "No records to delete", True, no_update
        else:
            return "Search again, something went wrong.", True, no_update


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8085)
    # app.run_server(host='0.0.0.0', port=8085,debug=True)
    # app.run_server(debug=False)
