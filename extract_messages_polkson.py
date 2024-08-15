import regex
import os
from bs4 import BeautifulSoup

messages = []
directory = "htmls"  # Where telegram exports lie

for file in os.listdir(directory):
    if file.endswith('.html'):
        with open(os.path.join(directory, file), "r", encoding='utf-8') as html_file:
            content = html_file.read()

            soup = BeautifulSoup(content, "html.parser")

            for message in soup.find_all("div", class_="message default clearfix"):
                from_name_tag = message.find("div", class_="from_name")
                reply_to_tag = message.find("div", class_="reply_to details")
                current_text_tag = message.find("div", class_="text")

                if from_name_tag:
                    if reply_to_tag and current_text_tag:

                        reply_to_link = reply_to_tag.find("a")
                        if reply_to_link:
                            message_id = reply_to_link['href'].split("go_to_message")[-1]

                            referenced_message = soup.find("div", id=f"message{message_id}")
                            if referenced_message:
                                referenced_text_tag = referenced_message.find("div", class_="text")
                                if referenced_text_tag:
                                    referenced_text = regex.sub(r'[^\p{Cyrillic}\d\s.,?!;]', '',
                                                                referenced_text_tag.get_text(strip=True))

                                    referenced_text = regex.sub(r'\s+', ' ', referenced_text)

                                    current_text = regex.sub(r'[^\p{Cyrillic}\d\s.,?!;]', '',
                                                             current_text_tag.get_text(strip=True))
                                    current_text = regex.sub(r'\s+', ' ', current_text)

                                    messages.append(f"<s>PROMPT: {referenced_text}\nREPLY: {current_text}")

with open("texts/output_polkson1.txt", "w", encoding='utf-8') as out_file:
    for message in messages:
        out_file.write(f"{message}\n")
