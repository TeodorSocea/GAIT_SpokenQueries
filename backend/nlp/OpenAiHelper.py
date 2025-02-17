from openai import OpenAI
import os


client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_graphql_query(schema,user_input):
    """Generate a GraphQL query based on user input."""
    schema_text = str(schema)  # Convert schema JSON to string for OpenAI

    prompt = f"""
    Given the following GraphQL schema:
    {schema_text}

    Generate a GraphQL query that matches this user request:
    "{user_input}"
    """

    response = client.chat.completions.create(model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are an expert GraphQL query generator. You need to only show the generated query. Don t wrap it as a Graphql code, provided it so we can run it directly in graphql."},
        {"role": "user", "content": prompt}
    ])

    return response.choices[0].message.content


#print(generate_graphql_query("https://countries.trevorblades.com/", ""))