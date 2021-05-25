import requests
import json


def get_products(headers, number_of_results=100, after_id=""):
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
                  }}
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
    product_list = get_products(headers, 100, "UHJvZHVjdDo4MQ==")
    print(product_list)


if __name__ == '__main__':
    main()
