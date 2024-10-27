import flet as ft
import undetected_chromedriver as uc
import os
import tempfile
import base64
import requests
import json
import nltk

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain_community.document_loaders import UnstructuredHTMLLoader
from langchain.docstore.document import Document
from unstructured.cleaners.core import remove_punctuation,clean,clean_extra_whitespace
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

def process_article(url):
    def save_website_to_html(url, output_file):

        # Get the HTML content of the page using chromedriver which will launch a browser window
        options = uc.ChromeOptions()
        options.headless = False
        driver = uc.Chrome(
            options=options,
            use_subprocess=False)
        driver.get(url)
        html = driver.page_source
        driver.quit()

        # Parse the HTML content
        soup = BeautifulSoup(html, 'html.parser')

        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Save the parsed HTML to a file
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(str(soup.prettify()))

        image_links = [img['src'] for img in soup.find_all('img') if 'src' in img.attrs or 'srcset' in img.attrs]

        return image_links

    output_file = "./incar_temp.html"

    # Not currently used, getting images requires more thought on how to handle them.
    image_links = save_website_to_html(url, output_file)

    model = ChatAnthropic(model="claude-3-sonnet-20240229")

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an AI assistant analyzing news articles about police killing people and answering questions."),
        ("human", "Here is a document: {document}\n\nQuestion: {question}")
    ])

    chain = (
        {"document": RunnablePassthrough(), "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )

    # Load and preprocess the document
    loader = UnstructuredHTMLLoader(
        output_file, mode="elements", strategy="fast",
    )
    document = loader.load()


    # Commented out for now, might be needed if the article is very long.
    # Split the document into chunks if it's too long
    #text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    #splits = text_splitter.split_documents(document)

    document_content = document

    # Define your question
    question = "You should extract victim's name as victim_name (often referred to as the deceased, or as 'identified', or as 'named'), gender as victim_gender (try to determine based on first name if possible), age as victim_age, race as victim_race, date of the incident as incident_date, address broken down into street as incident_street, city as incident_city, state as incident_state, county as incident_county, Which police agencies were involved as agency_involved, officer's name if available as officer_name, cause of death as cause_of_death, and a paragraph summary of the incident as incident_summary include in the summary statements from both the victim's family and friends as well as the police. You should output this as a SQL insert statement into table police_incidents. Keep the sql statements to a single line. If a field is not provided, set it to null. And fix any punctuation, grammar, and spelling errors. Finally output the original url as source_url."

    response = chain.invoke({"document": document_content, "question": question})

    return response, image_links

def main(page: ft.Page):
    page.title = "Incarcernation Article Processor"

    def copy_output(e):
        # Join all the output lines into a single string
        output_text = "\n".join([text.value for text in output_area.controls])

        page.set_clipboard(output_text)

        page.snack_bar = ft.SnackBar(ft.Text("Output copied to clipboard!"))
        page.snack_bar.open = True
        copy_button.visible = True
        page.update()

    def save_file_result(e: ft.FilePickerResultEvent):
        if e.path:
            output_text = "\n".join([text.value for text in output_area.controls])
            with open(e.path, 'w') as f:
                f.write(output_text)
            page.snack_bar = ft.SnackBar(ft.Text(f"File saved to {e.path}"))
            page.snack_bar.open = True
            page.update()

    save_file_dialog = ft.FilePicker(on_result=save_file_result)
    page.overlay.append(save_file_dialog)

    def save_file(e):
        save_file_dialog.save_file(
            dialog_title="Save SQL file",
            file_name="output.sql",
            allowed_extensions=["sql"]
        )

    def process_input(e):
        # Get the text from the multi-line input
        text = input_field.value

        lines = text.split('\n')

        # Clear the output area
        output_area.controls.clear()

        for i, line in enumerate(lines, 1):
            response, image_links = process_article(line)
            output_area.controls.append(ft.Text(f"{response}"))

        download_button.disabled = False

        # Update the page to reflect changes
        page.update()

    # Create UI elements
    input_field = ft.TextField(
        multiline=True,
        min_lines=1,
        max_lines=1000,
        hint_text="Paste the URLS of the articles here...",
    )

    process_button = ft.ElevatedButton("Process", on_click=process_input)
    output_area = ft.Column()
    copy_button = ft.ElevatedButton("Copy Output", on_click=copy_output, visible=True)

    download_button = ft.ElevatedButton(
        "Download as SQL",
        on_click=save_file,
        disabled=True
    )

    # Add elements to the page
    page.add(
        ft.Text("Enter article URLs, one per line:"),
        input_field,
        process_button,
        ft.Text("Output:"),
        ft.Container(content=output_area, height=200, border=ft.border.all(1, ft.colors.GREY_400), border_radius=5),
        ft.Row([copy_button, download_button])
    )

if __name__ == "__main__":
    load_dotenv()

    nltk.download('punkt')
    nltk.download('punkt_tab')

    ft.app(target=main)
