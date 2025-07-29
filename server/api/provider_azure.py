import os
import traceback
from datetime import datetime
from openai import AzureOpenAI

azure_image_model_option = None
azure_text_model_option = None
azure_api_version = None
image_llm_client = None
text_llm_client = None

def init_azure():
    """Initialize Azure OpenAI configuration"""
    global azure_image_model_option, azure_text_model_option, azure_api_version, image_llm_client, text_llm_client
    
    os.environ['AZURE_OPENAI_API_KEY'] = os.environ.get('AZURE_OPENAI_API_KEY')
    os.environ['AZURE_OPENAI_ENDPOINT'] = os.environ.get('AZURE_OPENAI_ENDPOINT')
    azure_image_model_option = os.environ.get('AZURE_IMAGE_MODEL_OPTION')
    azure_text_model_option = os.environ.get('AZURE_TEXT_MODEL_OPTION')
    azure_api_version = os.environ.get('AZURE_API_VERSION')

    text_api_base = os.environ['AZURE_OPENAI_ENDPOINT']
    text_llm_client = AzureOpenAI(
        api_key=os.environ['AZURE_OPENAI_API_KEY'],  
        api_version=azure_api_version,
        azure_endpoint=text_api_base
    )
    image_api_base = os.environ['AZURE_OPENAI_ENDPOINT']
    image_llm_client = AzureOpenAI(
        api_key=os.environ['AZURE_OPENAI_API_KEY'],  
        api_version=azure_api_version,
        base_url=f"{image_api_base}openai/deployments/{azure_image_model_option}/extensions",
    )

def get_azure_gpt_response(primer_message, user_message, analyser_format, analyser_type, prompt_examples=None):
    """Get response from Azure OpenAI"""
    print("GETTING AZURE")

    try:
        chat_settings = {
            "model": azure_image_model_option if (analyser_format == "image") or (analyser_format == "textimage") else azure_text_model_option
        }

        messages = []

        if analyser_format == "text":
            messages.append({
                "role": "system",
                "content": primer_message
            })
        elif (analyser_format == "image") or (analyser_format == "textimage"):
            
            prompt_messages = []

            primer = {
                "type": "text",
                "text": primer_message + "-----\n\nExamples:\n\n""-----\n\n"
            }
            prompt_messages.append(primer)

            for i, ex in enumerate(prompt_examples):

                if (analyser_format == "textimage"):
                    text = {
                        "type": "text",
                        "text": f"TEXT-{str(i)}:{ex['text']}\n"
                    }
                    prompt_messages.append(text)

                imagetag = {
                    "type": "text",
                    "text": f"\nIMAGE-{str(i)}:" 
                }
                prompt_messages.append(imagetag)

                img_data = ex['image']
                img_url = f"data:image/png;base64,{img_data}"
                image = {
                    "type": "image_url",
                    "image_url": {
                        "url": img_url,
                        "detail":"low"
                    }
                }
                prompt_messages.append(image)

                if analyser_type == 'binary':
                    result_text = f"\nRESULT-{str(i)}:" + ('positive' if ex['label'] == 1 else 'negative')
                else: #score
                    result_text = f"\nRESULT-{str(i)}:" + str(ex['label'])
                rationale_text = ("" if (len(ex['rationale']) == 0) else "\nREASON:" + ex['rationale'])

                label = {
                    "type": "text",
                    "text": result_text + rationale_text
                }
                prompt_messages.append(label)

                print(result_text)
            
            messages.append({
                "role": "system",
                "content": prompt_messages
            })

        messages.append({
            "role": "user",
            "content": user_message
        })

        body = {
            "messages": messages
        }

        completion = None

        if (analyser_format == "image") or (analyser_format == "textimage"):
            try:
                completion = image_llm_client.chat.completions.create(
                    model=chat_settings["model"],
                    messages=body["messages"]
                )
            except Exception as e:
                res = e.response.json()
                if res['error']['code'] == "content_filter":
                    error_msg = res['error']['message']
                    error_obj = res['error']['inner_error']['content_filter_results']
                    return {
                        "status":"400",
                        "error":res['error'],
                        "message":error_msg,
                        "content_filter_data":error_obj
                    }
                else:
                    return {
                        "status":"400",
                        "error":res
                    }
                
        elif analyser_format == "text":
            try:
                completion = text_llm_client.chat.completions.create(
                    model=chat_settings["model"],
                    messages=body["messages"]
                )
            except Exception as e:
                res = e.response.json()
                if res['error']['code'] == "content_filter":
                    error_msg = res['error']['message']
                    error_obj = res['error']['inner_error']['content_filter_results']
                    return {
                        "status":"400",
                        "error":res['error'],
                        "message":error_msg,
                        "content_filter_data":error_obj
                    }
                else:
                    return {
                        "status":"400",
                        "error":res
                    }

        llm_end_time_ms = round(datetime.now().timestamp() * 1000)
        response_text = completion.choices[0].message.content
        token_usage = completion.usage
        return {
            "status":"200",
            "res":response_text,
            "end":llm_end_time_ms, 
            "token":token_usage 
        }

    except Exception as e:
        print("exception in get_azure_gpt_response")
        print(e)
        print(traceback.format_exc())


