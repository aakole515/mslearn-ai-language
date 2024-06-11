from dotenv import load_dotenv
import os

# Import namespaces
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

def main():
    try:
        # Get Configuration Settings
        load_dotenv()
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')

        # Create client using endpoint and key
        ai_client = TextAnalyticsClient(
            endpoint=ai_endpoint,
            credential=AzureKeyCredential(ai_key)         
            )

        # Analyze each text file in the reviews folder
        reviews_folder = 'reviews'
        for file_name in os.listdir(reviews_folder):
            # Read the file contents
            print('\n-------------\n' + file_name)
            text = open(os.path.join(reviews_folder, file_name), encoding='utf8').read()
            #print('\n' + text)

            # Get language
            if text != '':
                detected_language = ai_client.detect_language(documents=[text])
                print(f' Detected Language {detected_language[0].primary_language.name}\n')
            
            # Get sentiment
            sentiment = ai_client.analyze_sentiment(documents=[text])[0]
            print(f' Sentiment = {sentiment.sentiment}\n')
            print(f' Confidence score {sentiment.confidence_scores}')
            # Get key phrases
            phrases = ai_client.extract_key_phrases(documents=[text])[0].key_phrases
            if len(phrases)>0:
                print(f'Phrases')
                for pharase in phrases:
                    print(f'{pharase}')
            # Get entities
            entities = ai_client.recognize_entities(documents=[text])[0].entities
            if len(entities) > 0:
                print("\nEntities")
                for entity in entities:
                    # print(entity)
                    print('\t{} ({})'.format(entity.text, entity.category))
            # Get linked entities
            entities = ai_client.recognize_linked_entities(documents=[text])[0].entities
            if len(entities) > 0:
                print("\nLinks")
                for linked_entity in entities:
                    print('\t{} ({})'.format(linked_entity.name, linked_entity.url))


    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()