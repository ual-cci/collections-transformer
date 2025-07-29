import os
import traceback
from datetime import datetime
from io import BytesIO
from PIL import Image
import base64
import torch
from transformers import AutoProcessor, MllamaForConditionalGeneration, MllamaConfig
from huggingface_hub import login

huggingface_model_option = None
huggingface_model = None
huggingface_processor = None

def init_huggingface():
    """Initialize Hugging Face configuration"""
    global huggingface_model_option, huggingface_model, huggingface_processor
    
    huggingface_model_option = "meta-llama/Llama-3.2-11B-Vision-Instruct"
    os.environ['HUGGINGFACE_API_KEY'] = os.environ.get('HUGGINGFACE_API_KEY')
    
    login(token = os.environ['HUGGINGFACE_API_KEY']) #llama repo permission

    print('Downloading ' + huggingface_model_option + '...')
    config = MllamaConfig()
    config._attn_implementation_autoset = True
    config._name_or_path = "meta-llama/Llama-3.2-11B-Vision-Instruct"
    config.architectures = ["MllamaForConditionalGeneration"]
    config.torch_dtype = "bfloat16"
    config.text_config.eos_token_id = [128001,128008,128009]
    config.text_config.rope_scaling = {
        "factor": 8.0,
        "high_freq_factor": 4.0,
        "low_freq_factor": 1.0,
        "original_max_position_embeddings": 8192,
        "rope_type": "llama3"
    }
    config.text_config.rope_theta = 500000.0
    config.text_config.torch_dtype = "bfloat16"
    config.text_config.max_position_embeddings = int(1e30) #increase context size
    config.vision_config.image_size = 560
    config.vision_config.torch_dtype = "bfloat16"
    huggingface_model = MllamaForConditionalGeneration.from_pretrained("meta-llama/Llama-3.2-11B-Vision-Instruct", device_map="auto", torch_dtype=torch.bfloat16, config=config, low_cpu_mem_usage=True)
    huggingface_processor = AutoProcessor.from_pretrained(huggingface_model_option)

def get_huggingface_response(primer_message, user_message, analyser_format, analyser_type, prompt_examples=None, test_batch=None):
    """Get response from Hugging Face model"""
    try:
        image_data = None
        messages = []

        if analyser_format == "text":
            messages.append({
                "role": "system",
                "content": [{
                    'type': 'text',
                    'text': primer_message
                }]
            })
        elif (analyser_format == "image") or (analyser_format == "textimage"):

            prompt_messages = []

            primer = {
                "type": "text",
                "text": primer_message
            }
            prompt_messages.append(primer)

            train_images = []
            train_messages = []

            train_content = [
                {
                    "type": "text",
                    "text": "-----\n\nExamples:\n\n""-----\n\n"
                }
            ]

            train_messages.append(train_content)

            for i, ex in enumerate(prompt_examples):

                if (analyser_format == "textimage"):
                    text = {
                        "type": "text",
                        "text": f"TEXT-{str(i)}:{ex['text']}\n"
                    }
                    train_messages.append(text)

                imagetag = {
                    "type": "text",
                    "text": f"\nIMAGE-{str(i)}:"
                }
                train_messages.append(imagetag)

                img_data = ex['image']
                train_images.append(Image.open(BytesIO(base64.b64decode(img_data))))

                image = {
                    "type": "image"
                }
                train_messages.append(image)

                if analyser_type == 'binary':
                    result_text = f"\nRESULT-{str(i)}:" + ('positive' if ex['label'] == 1 else 'negative')
                else:
                    result_text = f"\nRESULT-{str(i)}:" + str(ex['label'])

                rationale_text = ("" if (len(ex['rationale']) == 0) else "\nREASON:" + ex['rationale'])

                label = {
                    "type": "text",
                    "text": result_text + rationale_text
                }
                train_messages.append(label)

            messages.append({
                "role": "system",
                "content": prompt_messages
            })

            messages.append({
                "role": "user",
                "content": train_messages
            })

            test_images = []
            for i in test_batch:  
                test_images.append(Image.open(BytesIO(base64.b64decode(i if analyser_format == 'image' else i['image']))))

            image_data = train_images + test_images

        messages.append({
            "role": "user",
            "content": user_message
        })

        completion = None 

        try:
            prompt = huggingface_processor.apply_chat_template(messages, add_generation_prompt=True)
            inputs = huggingface_processor(images=image_data, text=prompt, padding=True, return_tensors="pt").to(huggingface_model.device) 
            completion = huggingface_model.generate(**inputs, min_new_tokens=len(test_batch)*2, max_new_tokens=len(test_batch)*2, use_cache=False, do_sample=True)
            response = huggingface_processor.decode(completion[0], skip_special_tokens=True, clean_up_tokenization_spaces=False) 
            response_text = response.split('assistant')[-1].strip()

        except RuntimeError as e:
            print("Runtime exception in get_huggingface_response")
            print(e)
            print(traceback.format_exc())
            return {
                "status":"400",
                "error":"Runtime error: Your device is out of memory."
            }

        except Exception as e:
            return {
                "status":"400",
                "error":e
            }

        llm_end_time_ms = round(datetime.now().timestamp() * 1000)
        token_usage = len(prompt) 

        return {
            "status":"200",
            "res":response_text,
            "end":llm_end_time_ms,
            "token":token_usage
        }

    except RuntimeError as e:
        print("Runtime exception in get_huggingface_response")
        print(e)
        print(traceback.format_exc())
        return {
            "status":"400",
            "error":"Runtime error: Your device is out of memory."
        }

    except Exception as e:
        print("exception in get_huggingface_response")
        print(e)
        print(traceback.format_exc())
        return {
            "status":"400",
            "error":e
        }
