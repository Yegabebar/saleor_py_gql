import json
import requests


def get_auth_query():
    return """fragment
                User
                on
                User
                {
                    id
                email
                firstName
                lastName
                userPermissions
                {
                    code
                name
                }
                avatar
                {
                    url
                }
                }
                mutation
                TokenAuth($email: String = "admin@admin.admin", $password: String = "P455w0rd") {
                    tokenCreate(email: $email, password: $password) {
                    errors: accountErrors {
                        field
                        message
                }
                csrfToken
                token
                user
                {
                    ...
                User
                }
                }
                }"""


def list_customers():
    return """query customers($first: Int = 10){
              customers(first: $first){
                pageInfo{
                  hasPreviousPage
                  hasNextPage
                    startCursor
                }
                edges{
                  node{
                    id
                    firstName
                    lastName
                    email
                  }
                }
              }
            }"""


def get_products(headers,
                 number_of_results=100,
                 after_id="",
                 size=100,
                 search_string="",
                 sort_method="",
                 direction="DESC"
                 ):
    variables_filter = ""
    if after_id != "":
        variables_filter = f'last: {number_of_results}'
    else:
        variables_filter = f'last: {number_of_results} after: "{after_id}"'
    if search_string != "":
        variables_filter += f'filter: {{search:"{search_string}"}}'

    if sort_method != "":
        if direction != "DESC":
            direction = "ASC"
        variables_filter += f'sortBy: {{field: {sort_method}, direction: {direction}}}'

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
    response = ""
    try:
        response = graphql_request(get_auth_query())
        auth_token = response['data']['tokenCreate']['token']
        headers = {"Authorization": "Bearer {}".format(auth_token)}
        print(graphql_request(list_customers(), headers))

    except Exception as e:
        print("", e)
    print(response)

    # Product list
    # product_list = get_products(headers,  search_string="shirt", sort_method="NAME", direction="DESC")
    # for product in product_list['data']['products']['edges']:
    #     print(product['node'])


if __name__ == '__main__':
    main()
