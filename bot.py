!apt-get update
!apt install chromium-chromedriver


from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
#from webdriver_manager.chrome import ChromeDriverManager # This is replaced in the next line
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

# Load the Falcon 7B model and tokenizer
model_name = "tiiuae/falcon-7b-instruct"  # Or "tiiuae/falcon-7b"
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Quantization config with CPU offloading
quantization_config = BitsAndBytesConfig(
    load_in_8bit=True,
    llm_int8_enable_fp32_cpu_offload=True  # Enable CPU offloading
)

# Load model with quantization config and custom device map
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=quantization_config,
    torch_dtype=torch.float16,  # Use lower precision to save VRAM
    device_map="auto",  # Auto-assigns CPU/GPU
    trust_remote_code=True  # This is for falcon models
)

# ... (rest of your code) ...

def generate_falcon_response(user_message):
    """
    Generates a response using the Falcon 7B model.

    Args:
        user_message: The user's input message.

    Returns:
        The AI's generated response.
    """
    # Encode the new user message and append the end-of-string token
    new_user_input_ids = tokenizer.encode(user_message + tokenizer.eos_token, return_tensors='pt').to(model.device)

    # Generate a response
    chat_history_ids = model.generate(new_user_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

    # Decode the generated tokens to get the reply
    ai_response = tokenizer.decode(chat_history_ids[0], skip_special_tokens=True)

    return ai_response

# web driver staartup
# service = Service(ChromeDriverManager().install()) # This line is no longer needed.

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.binary_location = '/usr/bin/chromium-browser'
# driver = webdriver.Chrome(service=service) # This is replaced by the next line
driver = webdriver.Chrome(options=options)
driver.get("https://web.whatsapp.com")
input("Scan QR code and press Enter")

# Set the target contact name isme naam add karna hota hai bas
contact = "YOUR CONTACT"

# Search for the contact using an updated XPath (adjust if necessary)
search_box = driver.find_element(By.XPATH, "//div[@role='textbox']")
search_box.click()
search_box.send_keys(contact)
time.sleep(2)
search_box.send_keys(Keys.ENTER)

# Wait for the chat to load
# fixed time can be changed
time.sleep(2)

# Initialize chat history for DialoGPT
# dont know yeet what tis is
chat_history_ids = None

def get_last_message():

    # Fetch the last received message from the active chat.
    # Adjust the XPath as needed based on WhatsApp's current structure.

    messages = driver.find_elements(By.XPATH, "//div[contains(@class,'message-in')]//span[@dir='ltr']")
    if messages:
        return messages[-1].text
    return None

def send_message(message):

    # Send a message in the active chat.
    # Adjust the XPath for the message input box if needed.

    message_box = driver.find_element(By.XPATH, "//div[@contenteditable='true' and @data-tab='10']")
    message_box.click()
    message_box.send_keys(message)
    message_box.send_keys(Keys.ENTER)

print("AI WhatsApp bot is running...")

i=0

# this is temporaray setting as we have to make tis thing run for longer wide

while i<10:
    last_message = get_last_message()
    if last_message:
        print("Received:", last_message)
        # Get AI response and update chat history
        ai_response, chat_history_ids = generate_falcon_response(last_message)
        print("AI Reply:", ai_response)
        send_message(ai_response)

    i+=1
    time.sleep(10)  # Wait 10 seconds before checking for new messages


