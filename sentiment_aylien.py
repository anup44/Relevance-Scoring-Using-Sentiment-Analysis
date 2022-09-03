from __future__ import print_function
import csv
import time
from datetime import datetime, timezone
import aylien_news_api
from aylien_news_api.rest import ApiException
import deeppavlov
from pprint import pprint
configuration = aylien_news_api.Configuration()

# Configure API key authorization: app_id
configuration.api_key['X-AYLIEN-NewsAPI-Application-ID'] = '4549c74b'

# Configure API key authorization: app_key
configuration.api_key['X-AYLIEN-NewsAPI-Application-Key'] = 'dee76b905ed2890671cd5b69c969816c'

# Defining host is optional and default to https://api.aylien.com/news
configuration.host = "https://api.aylien.com/news"
# Create an instance of the API class
api_instance = aylien_news_api.DefaultApi(aylien_news_api.ApiClient(configuration))

opts = {
  'text': '"hdfc mutual fund"',
  'sort_by': 'published_at',
  'sort_direction': 'desc',
  'language': ['en'],
  'per_page': 100,
  'cursor': '*',
  'published_at_start': 'NOW-2MONTHS/DAY'
}

'''
opts = {
  'id': [56],
  'not_id': [56],
  'title': 'title_example',
  'body': 'body_example',
  'text': 'text_example',
  'translations_en_title': 'translations_en_title_example',
  'translations_en_body': 'translations_en_body_example',
  'translations_en_text': 'translations_en_text_example',
  'language': ['language_example'],
  'not_language': ['language_example'],
  'published_at_start': 'published_at_start_example',
  'published_at_end': 'published_at_end_example',
  'categories_taxonomy': 'categories_taxonomy_example',
  'categories_confident': True,
  'categories_id': ['categories_id_example'],
  'not_categories_id': ['categories_id_example'],
  'categories_level': [56],
  'not_categories_level': [56],
  'entities_title_text': ['entities_title_text_example'],
  'not_entities_title_text': ['entities_title_text_example'],
  'entities_title_type': ['entities_title_type_example'],
  'not_entities_title_type': ['entities_title_type_example'],
  'entities_title_links_dbpedia': ['entities_title_links_dbpedia_example'],
  'not_entities_title_links_dbpedia': ['entities_title_links_dbpedia_example'],
  'entities_body_text': ['entities_body_text_example'],
  'not_entities_body_text': ['entities_body_text_example'],
  'entities_body_type': ['entities_body_type_example'],
  'not_entities_body_type': ['entities_body_type_example'],
  'entities_body_links_dbpedia': ['entities_body_links_dbpedia_example'],
  'not_entities_body_links_dbpedia': ['entities_body_links_dbpedia_example'],
  'sentiment_title_polarity': 'sentiment_title_polarity_example',
  'not_sentiment_title_polarity': 'sentiment_title_polarity_example',
  'sentiment_body_polarity': 'sentiment_body_polarity_example',
  'not_sentiment_body_polarity': 'sentiment_body_polarity_example',
  'media_images_count_min': 56,
  'media_images_count_max': 56,
  'media_images_width_min': 56,
  'media_images_width_max': 56,
  'media_images_height_min': 56,
  'media_images_height_max': 56,
  'media_images_content_length_min': 56,
  'media_images_content_length_max': 56,
  'media_images_format': ['media_images_format_example'],
  'not_media_images_format': ['media_images_format_example'],
  'media_videos_count_min': 56,
  'media_videos_count_max': 56,
  'author_id': [56],
  'not_author_id': [56],
  'author_name': 'author_name_example',
  'not_author_name': 'author_name_example',
  'source_id': [56],
  'not_source_id': [56],
  'source_name': ['source_name_example'],
  'not_source_name': ['source_name_example'],
  'source_domain': ['source_domain_example'],
  'not_source_domain': ['source_domain_example'],
  'source_locations_country': ['source_locations_country_example'],
  'not_source_locations_country': ['source_locations_country_example'],
  'source_locations_state': ['source_locations_state_example'],
  'not_source_locations_state': ['source_locations_state_example'],
  'source_locations_city': ['source_locations_city_example'],
  'not_source_locations_city': ['source_locations_city_example'],
  'source_scopes_country': ['source_scopes_country_example'],
  'not_source_scopes_country': ['source_scopes_country_example'],
  'source_scopes_state': ['source_scopes_state_example'],
  'not_source_scopes_state': ['source_scopes_state_example'],
  'source_scopes_city': ['source_scopes_city_example'],
  'not_source_scopes_city': ['source_scopes_city_example'],
  'source_scopes_level': ['source_scopes_level_example'],
  'not_source_scopes_level': ['source_scopes_level_example'],
  'source_links_in_count_min': 56,
  'source_links_in_count_max': 56,
  'source_rankings_alexa_rank_min': 56,
  'source_rankings_alexa_rank_max': 56,
  'source_rankings_alexa_country': ['source_rankings_alexa_country_example'],
  'social_shares_count_facebook_min': 56,
  'social_shares_count_facebook_max': 56,
  'social_shares_count_google_plus_min': 56,
  'social_shares_count_google_plus_max': 56,
  'social_shares_count_linkedin_min': 56,
  'social_shares_count_linkedin_max': 56,
  'social_shares_count_reddit_min': 56,
  'social_shares_count_reddit_max': 56,
  'clusters': ['clusters_example'],
  '_return': ['_return_example'],
  'sort_by': 'published_at',
  'sort_direction': 'desc',
  'cursor': '*',
  'per_page': 10
}
'''

try:
    # List Stories
    api_response = api_instance.list_stories(**opts)
    # pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->list_stories: %s\n" % e)


# sentiment_model = deeppavlov.build_model(deeppavlov.configs.classifiers['sentiment_sst_conv_bert'], 
#                                                 download=True)

filename = 'aylien_data_analysis'+(datetime.now().strftime("%Y-%m-%d-%H"))+'.csv'

articles_i = 0
len_stories = -1
with open (filename, 'w', newline='', encoding='utf-8') as csvFile:
    
    csvWriter = csv.writer(csvFile, delimiter=';')
    headers = ['Published', 'Title', 'Content', 'Entities', 'Categories', 'AYLIEN sentiment']
    csvWriter.writerow(headers)
    cursor_prev = ''
    cursor = '*'
    while (len_stories != 0):
        try:
            # List Stories
            api_response = api_instance.list_stories(**opts)
            # pprint(api_response)
            cursor_prev = cursor
            cursor = api_response.next_page_cursor
            opts = {'cursor': cursor,
                    'per_page': 100}
            len_stories = len(api_response.stories)
        except ApiException as e:
            print("Exception when calling DefaultApi->list_stories: %s\n" % e)

        for story in api_response.stories:
            articles_i += 1
            story_encoded = story.body.encode('utf-8')
            story_decoded = story_encoded.decode('utf-8')
            # computed_sentiment = sentiment_model([story.body])
            row = [story.published_at.replace(tzinfo=timezone.utc).astimezone(tz=None).strftime("%Y-%m-%d  %H:%M"),
                    story.title.replace(';', ''),
                    story_decoded.replace(';', ''),
                    str(story.entities),
                    str(story.categories),
                    str(story.sentiment)
                    # computed_sentiment
                    ]
            print (row)
            csvWriter.writerow(row)




