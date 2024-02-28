
import os
from dotenv import load_dotenv

from ai_utils import (
    airtable_to_csv,
    run_agent,
    extract_ids_from_base_url,
    get_airtable_table
)

from pyairtable import Table

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
AIRTABLE_PAT_KEY = os.getenv('AIRTABLE_PAT_KEY')

models = ["gpt-3.5-turbo", "gpt-4", "gpt-4-0613", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k-0613"]
airtable_urls = {
    "advisor-startup": {
        "advisors": "https://airtable.com/appJMudX309AJmXBz/tblgPH95zhmXfu08O/viwm8oCDS0PU8J8ca",
        "startups": "https://airtable.com/appJMudX309AJmXBz/tblOTZtugYYtG66JX/viwFzBgREhDqHlH3f",
        "advisor-matches": "https://airtable.com/appJMudX309AJmXBz/tbl8JCYJa9LpBXk2q/viw0Nm83WNsLDKPkj",
        "startup-matches": "https://airtable.com/appJMudX309AJmXBz/tbl2mzPAUIeCz09ES"
    }
}

selected_model = models[1]

advisors_file = airtable_to_csv(AIRTABLE_PAT_KEY, airtable_urls["advisor-startup"]["advisors"])

# Get Table for startups
startups_table = get_airtable_table(AIRTABLE_PAT_KEY, airtable_urls["advisor-startup"]["startups"])

# Get Table for startup-matches
startup_matches_table = get_airtable_table(AIRTABLE_PAT_KEY, airtable_urls["advisor-startup"]["startup-matches"])

# Iterate through startups Table
for records in startups_table.iterate(page_size=1, max_records=1):
    for record in records:
        id = record["id"]
        fields = record["fields"]

        query = 
        """If each row in the table represents an advisor, give me the names of the top 3 advisors that are best suited to advise this startup based on Description and Key Areas of Interest. 
             Return only an array of the list of advisors.
            Return NO other text.
            This is an example of the output format:\n
            ['Austin Hwang', 'Nate Mason', 'Maxim Dressler']
            \n
            Do not write code or tell me how to do it. Output on the names of the advisors in the specified format.
            This is the startup: \n
            """ + \
                "Description of the startup: " + fields['Description'] + "\n" + \
                "Industry of the startup: " + fields['Industry'] + "\n" + \
                "Current Stage of the startup: " + fields['Current Stage'] + "\n" + \
                "Tags" + ", ".join(fields["Tags"])
        print(query)

        '''agent_response = run_agent(advisors_file, query, OPENAI_API_KEY, selected_model)

        new_record = {'Startup Name': fields["Startup Name"], 'Matched Text': agent_response, 'Startup': [id]}
        startup_matches_table.create(new_record)'''


'''
query = "How many advisors are in the enterprise space?"
url = airtable_urls["advisor-startup"]["advisors"]

agent_response = run_agent(airtable_to_csv(AIRTABLE_PAT_KEY, url), query, OPENAI_API_KEY, models[1])

print("\n\n")
print(agent_response)
'''


