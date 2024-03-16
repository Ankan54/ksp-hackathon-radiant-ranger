from langchain.utils.openai_functions import convert_pydantic_to_openai_function 
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from datetime import datetime
from typing import List
from pydantic import BaseModel, Field
from models import Event
from dotenv import load_dotenv
load_dotenv()

model = ChatOpenAI(temperature=0,model="gpt-3.5-turbo-0125")

class PostAnalysis(BaseModel):
    '''Extract relevant Information from social media posts'''
    sentiment: str = Field(description="""The sentiment of the post based on the type of event mentioned in the post.
                         sentiment will be positive only if the event mentioned is of postive type, otherwise it will be either neutral or negative.
                        Negative sentiment means a negative/worrisome/troubling event has been mentioned in the post.""",enum=["Positive", "Negative", "Neutral"])
    event_type: str = Field(description="The type of event mentioned in the post", enum=["Accident","Violence","Riot"])
    event_place: str = Field(description="""The location mentioned in the post where the event is taking place.
                            The location will always be a place in Bangalore. only one location name to be extracted, it won't be Bangalore but a place within the city.
                            The spelling of the location name needs to be correct and consistent, irrespective of the spelling mentioned in the post.""")
    severity: str = Field(description="""the severity level of the event mentioned in the post
                          if the event can affect large group of people then severity is high, or if the even mentions any blodshed or fatality then it will be high.
                          other than that, It can be classified as medium or low if the event is non-fatal or has smaller affected area.""",
                          enum=["High", "Medium", "Low"])
    hashtags: List = Field(description="Any hashtags that have been mentioned in the post, include the hashtag in the reponse.")

prompt = ChatPromptTemplate.from_messages([
    ("system", "Provided is a social media post posted by a human, reporting some event occuring in a place. Think carefully, and then generate response as instructed. The responses will be analysed by Police perssonels to identify related events, so that they can take prompt action on it."),
    ("human", "{input}")
])

overview_tagging_function = [
    convert_pydantic_to_openai_function(PostAnalysis)
]
tagging_model = model.bind(
    functions=overview_tagging_function,
    function_call={"name":"PostAnalysis"}
)

tagging_chain = prompt | tagging_model | JsonOutputFunctionsParser()


def extract_data(user_input, chain=tagging_chain):
    try:
        result_dict = chain.invoke({"input":f"{user_input}"})
        return result_dict
    except Exception as e:
        print('Error:',str(e))
        return False


def format_date(input_date):
    #dt = datetime.strptime(date_string, '%d-%m-%Y %H:%M:%S')
    dt_formatted = input_date.strftime('%Y-%m-%d %H:%M:%S')
    return dt_formatted

def process_data(user_input,event_timestamp=datetime.now()):
    result_dict = extract_data(user_input)

    if result_dict == False:
        return False

    try:
        event = Event(
                    post_content = user_input,
                    event_place = result_dict["event_place"],
                    timestamp = event_timestamp,
                    sentiment = result_dict['sentiment'],
                    event_type = result_dict['event_type'],
                    severity = result_dict['severity'],
                    hashtags = ",".join([f"#{tag}" for tag in result_dict['hashtags']])
                )
        
        return event.model_dump()
    
    except Exception as e:
        print(result_dict)
        print('Error:',str(e))
        return False