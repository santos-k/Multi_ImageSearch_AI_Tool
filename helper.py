from dash import dcc, html, no_update
import dash_bootstrap_components as dbc
from datetime import datetime
from operator import itemgetter  # sort list of dictionaries by dict value
import pandas as pd
import ast
import math


class DisplayImage:
    def __init__(self):
        self.btn_count = 0

    def item_card(self, data, search_img_id):
        print("inside item_card")
        # stime = datetime.now()
        # print(data)
        product_id = data['uuid']
        img_link = data['image_link']
        category = data['category']
        price = data['price']
        site = data['site']
        title = data['product_name']
        brand = data['brand']
        product_link = data['product_link']
        score = data['score']

        search_img_id = search_img_id.replace(".jpg","")

        item = dbc.Col([
            html.A([dbc.CardImg(src=img_link,
                                title=title,
                                style={'width': '150px', 'height': '200px'})], href=img_link, target="_blank"),
            dbc.CardBody([
                html.A(f"{title[:20]}...", href=product_link, target="_blank"),
                html.P(f"{brand}, {category[:15]}", className='m-0'),
                html.P(f"Price: {price[:5]}, Score: {score}", className='m-0'),
                html.P(f"Source: {site}", className='m-0'),

                dbc.Col([
                    dbc.Button("Correct",
                               n_clicks=0,
                               disabled=False,
                               key=f"{search_img_id}&&&{product_id}&&&{product_link}&&&{img_link}&&&{score}",
                               id=f"correct{self.btn_count}",
                               outline=True,
                               size='sm',
                               color="danger",
                               style={'height': 'auto'}
                               ),
                    dbc.Button("Wrong",
                               id=f"wrong{self.btn_count}",
                               n_clicks=0,
                               disabled=False,
                               key=f"{search_img_id}&&&{product_id}&&&{product_link}&&&{img_link}&&&{score}",
                               outline=True,
                               size='sm',
                               color="danger",
                               style={'height': 'auto'},
                               ),
                ]),
            ], className=" text-left"),
        ], className="m-2")
        self.btn_count += 1
        # print("Item-card time: ",datetime.now()-stime)
        return item

    def display_image(self, img_url, img_id, similar_result):
        print("inside display_image")
        # stime = datetime.now()
        """
        Creates complete search result of a single input image and pack into row
        :param similar_result: list of dictionary in JSON format
        :param img_id: searched image product code
        :param img_url: image url
        :return: returns row of complete info of a searched result (uploaded image + search result)
        """
        similar_result = sorted(similar_result, key=itemgetter('score'), reverse=True)
        count = 0
        result_children = []  # to store all cards of single result
        for result in similar_result[:30]:
            if len(result) > 0:
                result_children.append(self.item_card(result, img_id))
                count += 1
            else:
                result_children.append(html.Label("No result!!"))
                count += 1

        row = dbc.Row([
            dbc.Row([
                dbc.Col([
                    html.Label('Searched Image'),
                    html.A(dbc.CardImg(src=img_url,
                                       style={'width': '150px', 'height': '200px'}), href=img_url, target="_blank"),
                ], width=2, className="my-5"),
                dbc.Col([
                    html.Label(f'Search Results: {count}'),
                    dbc.Card([
                        dbc.Row([*result_children,
                                 html.Div([
                                     *[
                                         html.Div(id=f"div{i}") for i in range(self.btn_count * 2)
                                     ]
                                 ], style={'display': 'none'}
                                 ),
                                 ], style={"flexWrap": "nowrap"}),
                    ], style={'overflowX': 'scroll'})
                ], width=10)
            ], justify="center"),
        ], justify='center', align='left', className="my-2")
        # print("Display_image time: ", datetime.now()-stime)

        return row


def dropdown(category, brand):
    """
    :param category: column of category options
    :param brand: column of brand options
    :return: return two dropdowns(category and brand) for the given data
    """
    dpdn = dbc.Row([
        dbc.Col([
            dbc.Label("Category"),
            dcc.Dropdown(id="category_dpdn", options=[cat for cat in category],
                         placeholder="Select Category", maxHeight=120, multi=True, className="mx-2",
                         style={'height': '30px'}),
        ]),
        dbc.Col([
            dbc.Label("Brand"),
            dcc.Dropdown(id="brand_dpdn", options=[brand for brand in brand],
                         placeholder="Select Brand", maxHeight=120, multi=True, className="mx-2",
                         style={'height': '30px'})
        ])
    ])

    return dpdn

