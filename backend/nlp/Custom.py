import re

class Custom:
    def __init__(self, schema=None):
        self.schema = schema  # Optionally pass a schema for GraphQL query generation

    def generate_graphql_query(self, user_input):
        """
        Converts a natural language query into a GraphQL query for the Countries API.
        """
        natural_language_query = natural_language_query.lower()
        
        # Define mappings for known entities
        country_codes = {
            "france": "FR", "germany": "DE", "spain": "ES", "italy": "IT", "united states": "US",
            "canada": "CA", "brazil": "BR", "india": "IN", "china": "CN", "japan": "JP"
        }
        currencies = {"euro": "EUR", "dollar": "USD", "yen": "JPY"}
        continents = {"asia": "AS", "europe": "EU", "africa": "AF", "north america": "NA", "south america": "SA"}
        
        # Identify country queries
        country_match = re.search(r"details of (\w+(?: \w+)*)", natural_language_query)
        if country_match:
            country_name = country_match.group(1)
            country_code = country_codes.get(country_name)
            if country_code:
                return f"{{ country(code: \"{country_code}\") {{ name capital currency }} }}"
        
        # Identify currency queries
        currency_match = re.search(r"countries use (\w+)", natural_language_query)
        if currency_match:
            currency_name = currency_match.group(1)
            currency_code = currencies.get(currency_name)
            if currency_code:
                return f"{{ countries(filter: {{ currency: {{ eq: \"{currency_code}\" }} }}) {{ name code }} }}"
        
        # Identify continent queries
        continent_match = re.search(r"countries in (\w+)", natural_language_query)
        if continent_match:
            continent_name = continent_match.group(1)
            continent_code = continents.get(continent_name)
            if continent_code:
                return f"{{ continent(code: \"{continent_code}\") {{ countries {{ name code }} }} }}"
        
        return "Unable to process the query."