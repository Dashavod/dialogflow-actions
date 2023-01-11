def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    CLIENT_API_KEY = "api_key.json"
    from google.cloud import dialogflow

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    for text in texts:
        text_input = dialogflow.TextInput(text=text, language_code=language_code)

        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        print("=" * 20)
        print("Query text: {}".format(response.query_result.query_text))
        print(
            "Detected intent: {} (confidence: {})\n".format(
                response.query_result.intent.display_name,
                response.query_result.intent_detection_confidence,
            )
        )
        print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))

import json
from PyDictionary import PyDictionary

dictionary=PyDictionary()
list_health = ["Dental","Vaccination","General medical examination","checkup","Coinsurance","inpatient","outpatient","medical specialists","therapeutic","operative treatment","surgical intervention","anesthetic","glass lenses","Biologically active dietary","Covid tests",
             "Dermatologist","critical diseases","Emergency medical care","tumors", "tuberculosis", "diabete mellitus", "cirrhosis of the liver", "chronic renal failure", "gynecology", "urology" ,
             "emergency medical services ","Reanimation measures","Diagnostic", "Medical supplies"]
list_item = ["benefits"
"Sport", "Health","group activities","lunch","birth of a child","marriage","death of close relative","english classes"]
a = [{ "value": item, "synonyms": [item] } for item in list_item]
# for item in a:
#     if len(item["value"].split(' '))>2:
#         continue;
#     else:
#         item["synonyms"] = dictionary.synonym(item["value"])

print(json.dumps(a,indent=2))
with open("sample.json", "w") as outfile:
    outfile.write(json.dumps(a,indent=2))