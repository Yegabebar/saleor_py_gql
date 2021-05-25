import json

import requests


def get_products(headers, number_of_results=100, after_id="", size=100):
    variables_filter = ""
    if after_id != "":
        variables_filter = f"last: {number_of_results}"
    else:
        variables_filter = f'last: {number_of_results} after: "{after_id}"'
    query = f"""query {{
              products({variables_filter}) {{
                edges {{
                  node {{
                    id
                    name
                     pricing{{
                      priceRange{{
                        start{{
                          currency
                          tax{{
                            amount
                            currency
                          }}
                          net{{
                            amount
                            currency
                          }}
                          currency
                        }}
                        stop{{
                          currency
                          tax{{
                            amount
                            currency
                          }}
                          net{{
                            amount
                            currency
                          }}
                        }}
                      }}
                    }}
                    thumbnail(size: {size}) {{
                        url
                        alt
                    }}
                    images {{
                      url(size: {size})
                      alt
                    }}
                  }}
                }}
              }}
            }}"""
    return graphql_request(query, headers)


def get_product_by_id(headers, product_id, size):
    query = f"""query {{
              product(id: "{product_id}") {{
                id
                name
                description
                productType
                pricing{{
                      priceRange{{
                        start{{
                          currency
                          tax{{
                            amount
                            currency
                          }}
                          net{{
                            amount
                            currency
                          }}
                          currency
                        }}
                        stop{{
                          currency
                          tax{{
                            amount
                            currency
                          }}
                          net{{
                            amount
                            currency
                          }}
                        }}
                      }}
                    }}
                thumbnail(size: {size}) {{
                        url
                        alt
                    }}
                    images {{
                      url(size: {size})
                      alt
                    }}
              }}
            }}"""
    return graphql_request(query, headers)


def graphql_request(query, headers={},
                    endpoint="http://localhost:8000/graphql/"):
    response = requests.post(
        endpoint,
        headers=headers,
        json={
            'query': query
        }
    )

    parsed_response = json.loads(response.text)
    if response.status_code != 200:
        raise Exception("{message}\n extensions: {extensions}".format(
            **parsed_response["errors"][0]))
    else:
        return parsed_response


def main():
    gql_endpoint = "http://localhost:8000/graphql/"
    auth_token = "8gAa53gDE9o5xfoTrAbG76nV5eSYB4"
    headers = {"Authorization": "Bearer {}".format(auth_token)}
    product_list = get_products(headers, 100)
    for product in product_list['data']['products']['edges']:
        print(product['node'])


if __name__ == '__main__':
    main()
