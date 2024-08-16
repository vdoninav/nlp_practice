# NLP Telegram Bots based on ruGPT3Small

## Problem Statement:
The project aims to create Telegram bots capable of engaging in natural language conversations in a specific style or manner. The challenge is to fine-tune a pre-existing language model (ruGPT3Small) on custom datasets to adopt particular communication patterns or personalities. This involves:

Collecting and preprocessing conversation data from specific sources.
Fine-tuning the ruGPT3Small model on this data.
Implementing the fine-tuned models in Telegram bots.
Hosting these bots for user interaction.

## Architecture:

### Base Model:

ruGPT3Small, based on GPT-2 architecture
Pretrained on Russian language texts
125 million parameters


### Fine-tuning Process:

Used Hugging Face's Transformers library
Implemented using PyTorch
Training script: run_clm.py (Causal Language Modeling)


### Data Processing:

Custom scripts (extract_messages_avtobus.py, extract_messages_polkson.py) for data extraction and preprocessing

Tokenization using GPT2Tokenizer


## Bot Implementation:

Python-based Telegram bots (bot_avtobus.py, bot_polkson.py)
Integration with fine-tuned models for response generation


### Hosting:

Bots deployed on an vds server for continuous operation


## Results:

### Model Performance:

Training loss: 1.5335 (as seen in the training output)
Evaluation perplexity: 61.5162
Accuracy: 0.5105


### Bot Functionality:

Two separate bots created: "Avtobus" and "Polkson"

Bots capable of generating responses in their respective styles
Implemented features:

Responding to direct messages

Replying when mentioned in group chats

An "insanity mode", when bots reply to all messages in a group, that can be toggled on/off




### User Interaction:

Bots successfully deployed and accessible via Telegram
Capable of engaging in conversations, mimicking specific communication styles based on their training data


### Limitations:

Response generation limited to 128 tokens
Potential for generating inappropriate content, requiring careful prompt engineering and possibly content filtering



The project successfully demonstrates the ability to fine-tune a pre-existing language model for specific conversational tasks and deploy it in a practical application through Telegram bots. The resulting bots can engage in conversations with users, adopting particular communication styles based on their training data.
For future improvements, considerations could include:

Expanding the training dataset for better performance
Implementing more sophisticated content filtering
Optimizing the model for faster response times
Adding more interactive features to the bots

Link to finetuned models: https://drive.google.com/file/d/1ehw7yZp8GPQvVMrDfFpnkgz9P94T0aMF/view?usp=sharing

Base language model used in this project: https://huggingface.co/ai-forever/rugpt3small_based_on_gpt2
