from datetime import datetime
import requests
import json


# api request
def get_result2(api_url, filename, catalog):
    start = datetime.now()
    """
    :param api_url: complete url
    :param filename: uploaded file
    :param catalog: True or False
    :return: response.text(JSON)
    """
    payload = {}
    files = [
        ('file', (filename, open(filename, 'rb'), 'text/csv'))
    ]
    headers = {'enctype': 'multipart/form-data ; Content-Type:multipart/form-data'}
    starttime = datetime.now()
    try:
        # print("requesting...")
        response = requests.request("POST", api_url, headers=headers, data=payload, files=files)
        # print("got response")
        if json.loads(response.text)['status'] == 'success':
            if catalog == 0:
                result = json.loads(response.text)['scraped']

            else:
                result = json.loads(response.text)['catalog']
            # print(result)
            # with open("sample.json", "w") as outfile:
            #     json.dump(result, outfile)
        else:
            result = f"API Response Status: {json.loads(response.text)['status']}"
        # print("API Time: ", datetime.now()-start)

    except requests.exceptions.ConnectionError as con:
        # print(con)
        result = f"API Connection Error: {con}"
    except requests.exceptions.Timeout as t:
        result = f"API Timeout Error: Time out, {t}"
        # print(t)
    except requests.exceptions.TooManyRedirects as too:
        result = f"API Too Many Redirects Error: Bad URL, {too}"
        # print(type(too))
    except requests.exceptions.RequestException as e:
        # print(type(e))
        result = f"API Error: Request Exception"
    return result


def get_result(api_url, filename,catalog):
    file_name = 'result.json'
    with open(file_name, 'r', encoding='utf-8') as f:
        result = json.load(f)
    return result


# generate url
def url(category, brand, catalog, scraped, ajio, bijnis, udaan, threshold, fe_request_id, file_search):
    # print(category,type(category), brand, catalog, scraped, ajio, bijnis, udaan, threshold, fe_request_id, file_search)
    """
    generate url as per input values
    :param file_search: Image or File type
    :param category: list of category options
    :param brand: list of brand options
    :param catalog: 0 or 1
    :param scraped: 0 or 1
    :param ajio: 0 or 1
    :param bijnis: 0 or 1
    :param udaan: 0 or 1
    :param threshold: score of matching result
    :param fe_request_id: unique search id
    :return: url
    """
    if category is None and brand is None:
        return f"http://3.111.148.117:8084/v1/upload?catalog={catalog}&scraped={scraped}&ajio={ajio}" \
               f"&bijnis={bijnis}&udaan={udaan}&category=&brand=&threshold={threshold / 100}&fe_request_id={fe_request_id}&file_search={file_search}"
    elif category is not None and brand is not None:
        cat = '~'.join(category)
        brand = '~'.join(brand)
        return f"http://3.111.148.117:8084/v1/upload?catalog={catalog}&scraped={scraped}&ajio={ajio}&bijnis={bijnis}&" \
               f"udaan={udaan}&category={cat}&brand={brand}&threshold={threshold / 100}&fe_request_id={fe_request_id}&file_search={file_search}"

    elif category is None and brand is not None:
        brand = '~'.join(brand)
        return f"http://3.111.148.117:8084/v1/upload?catalog={catalog}&scraped={scraped}&ajio={ajio}&bijnis={bijnis}&" \
               f"udaan={udaan}&category=&brand={brand}&threshold={threshold / 100}&fe_request_id={fe_request_id}&file_search={file_search}"
    elif category is not None and brand is None:
        cat = '~'.join(category)
        return f"http://3.111.148.117:8084/v1/upload?catalog={catalog}&scraped={scraped}&ajio={ajio}&bijnis={bijnis}&" \
               f"udaan={udaan}&category={cat}&brand=&threshold={threshold / 100}&fe_request_id={fe_request_id}&file_search={file_search}"

