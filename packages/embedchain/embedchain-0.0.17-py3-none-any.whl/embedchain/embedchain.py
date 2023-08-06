import openai
import os
from string import Template

from chromadb.utils import embedding_functions
from dotenv import load_dotenv
from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from embedchain.config import InitConfig, AddConfig, QueryConfig, ChatConfig
from embedchain.config.QueryConfig import DEFAULT_PROMPT

from embedchain.loaders.youtube_video import YoutubeVideoLoader
from embedchain.loaders.pdf_file import PdfFileLoader
from embedchain.loaders.web_page import WebPageLoader
from embedchain.loaders.local_qna_pair import LocalQnaPairLoader
from embedchain.loaders.local_text import LocalTextLoader
from embedchain.loaders.docx_file import DocxFileLoader
from embedchain.chunkers.youtube_video import YoutubeVideoChunker
from embedchain.chunkers.pdf_file import PdfFileChunker
from embedchain.chunkers.web_page import WebPageChunker
from embedchain.chunkers.qna_pair import QnaPairChunker
from embedchain.chunkers.text import TextChunker
from embedchain.chunkers.docx_file import DocxFileChunker
from embedchain.vectordb.chroma_db import ChromaDB


gpt4all_model = None

load_dotenv()

ABS_PATH = os.getcwd()
DB_DIR = os.path.join(ABS_PATH, "db")

memory = ConversationBufferMemory()


class EmbedChain:
    def __init__(self, config: InitConfig):
        """
        Initializes the EmbedChain instance, sets up a vector DB client and
        creates a collection.

        :param config: InitConfig instance to load as configuration.
        """

        self.config = config
        self.db_client = self.config.db.client
        self.collection = self.config.db.collection
        self.user_asks = []

    def _get_loader(self, data_type):
        """
        Returns the appropriate data loader for the given data type.

        :param data_type: The type of the data to load.
        :return: The loader for the given data type.
        :raises ValueError: If an unsupported data type is provided.
        """
        loaders = {
            'youtube_video': YoutubeVideoLoader(),
            'pdf_file': PdfFileLoader(),
            'web_page': WebPageLoader(),
            'qna_pair': LocalQnaPairLoader(),
            'text': LocalTextLoader(),
            'docx': DocxFileLoader(),
        }
        if data_type in loaders:
            return loaders[data_type]
        else:
            raise ValueError(f"Unsupported data type: {data_type}")

    def _get_chunker(self, data_type):
        """
        Returns the appropriate chunker for the given data type.

        :param data_type: The type of the data to chunk.
        :return: The chunker for the given data type.
        :raises ValueError: If an unsupported data type is provided.
        """
        chunkers = {
            'youtube_video': YoutubeVideoChunker(),
            'pdf_file': PdfFileChunker(),
            'web_page': WebPageChunker(),
            'qna_pair': QnaPairChunker(),
            'text': TextChunker(),
            'docx': DocxFileChunker(),
        }
        if data_type in chunkers:
            return chunkers[data_type]
        else:
            raise ValueError(f"Unsupported data type: {data_type}")

    def add(self, data_type, url, config: AddConfig = None):
        """
        Adds the data from the given URL to the vector db.
        Loads the data, chunks it, create embedding for each chunk
        and then stores the embedding to vector database.

        :param data_type: The type of the data to add.
        :param url: The URL where the data is located.
        :param config: Optional. The `AddConfig` instance to use as configuration options.
        """
        if config is None:
            config = AddConfig()
        loader = self._get_loader(data_type)
        chunker = self._get_chunker(data_type)
        self.user_asks.append([data_type, url])
        self.load_and_embed(loader, chunker, url)

    def add_local(self, data_type, content, config: AddConfig = None):
        """
        Adds the data you supply to the vector db.
        Loads the data, chunks it, create embedding for each chunk
        and then stores the embedding to vector database.

        :param data_type: The type of the data to add.
        :param content: The local data. Refer to the `README` for formatting.
        :param config: Optional. The `AddConfig` instance to use as configuration options.
        """
        if config is None:
            config = AddConfig()
        loader = self._get_loader(data_type)
        chunker = self._get_chunker(data_type)
        self.user_asks.append([data_type, content])
        self.load_and_embed(loader, chunker, content)

    def load_and_embed(self, loader, chunker, src):
        """
        Loads the data from the given URL, chunks it, and adds it to the database.

        :param loader: The loader to use to load the data.
        :param chunker: The chunker to use to chunk the data.
        :param src: The data to be handled by the loader. Can be a URL for remote sources or local content for local loaders.
        """
        embeddings_data = chunker.create_chunks(loader, src)
        documents = embeddings_data["documents"]
        metadatas = embeddings_data["metadatas"]
        ids = embeddings_data["ids"]
        # get existing ids, and discard doc if any common id exist.
        existing_docs = self.collection.get(
            ids=ids,
            # where={"url": src}
        )
        existing_ids = set(existing_docs["ids"])

        if len(existing_ids):
            data_dict = {id: (doc, meta) for id, doc, meta in zip(ids, documents, metadatas)}
            data_dict = {id: value for id, value in data_dict.items() if id not in existing_ids}

            if not data_dict:
                print(f"All data from {src} already exists in the database.")
                return

            ids = list(data_dict.keys())
            documents, metadatas = zip(*data_dict.values())

        self.collection.add(
            documents=documents,
            metadatas=list(metadatas),
            ids=ids
        )
        print(f"Successfully saved {src}. Total chunks count: {self.collection.count()}")

    def _format_result(self, results):
        return [
            (Document(page_content=result[0], metadata=result[1] or {}), result[2])
            for result in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
            )
        ]

    def get_llm_model_answer(self, prompt):
        raise NotImplementedError

    def retrieve_from_database(self, input_query):
        """
        Queries the vector database based on the given input query.
        Gets relevant doc based on the query

        :param input_query: The query to use.
        :return: The content of the document that matched your query.
        """
        result = self.collection.query(
            query_texts=[input_query,],
            n_results=1,
        )
        result_formatted = self._format_result(result)
        if result_formatted:
            content = result_formatted[0][0].page_content
        else:
            content = ""
        return content

    def generate_prompt(self, input_query, context, template: Template = None):
        """
        Generates a prompt based on the given query and context, ready to be passed to an LLM

        :param input_query: The query to use.
        :param context: Similar documents to the query used as context.
        :param template: Optional. The `Template` instance to use as a template for prompt.
        :return: The prompt
        """
        prompt = template.substitute(context = context, query = input_query)
        return prompt

    def get_answer_from_llm(self, prompt):
        """
        Gets an answer based on the given query and context by passing it
        to an LLM.

        :param query: The query to use.
        :param context: Similar documents to the query used as context.
        :return: The answer.
        """
        answer = self.get_llm_model_answer(prompt)
        return answer

    def query(self, input_query, config: QueryConfig = None):
        """
        Queries the vector database based on the given input query.
        Gets relevant doc based on the query and then passes it to an
        LLM as context to get the answer.

        :param input_query: The query to use.
        :param config: Optional. The `QueryConfig` instance to use as configuration options.
        :return: The answer to the query.
        """
        if config is None:
            config = QueryConfig()
        context = self.retrieve_from_database(input_query)
        prompt = self.generate_prompt(input_query, context, config.template)
        answer = self.get_answer_from_llm(prompt)
        return answer

    def generate_chat_prompt(self, input_query, context, chat_history=''):
        """
        Generates a prompt based on the given query, context and chat history
        for chat interface. This is then passed to an LLM.

        :param input_query: The query to use.
        :param context: Similar documents to the query used as context.
        :param chat_history: User and bot conversation that happened before.
        :return: The prompt
        """
        prefix_prompt = f"""You are a chatbot having a conversation with a human. You are given chat history and context. You need to answer the query considering context, chat history and your knowledge base. If you don't know the answer or the answer is neither contained in the context nor in history, then simply say "I don't know"."""
        chat_history_prompt = f"""\n----\nChat History: {chat_history}\n----"""
        suffix_prompt = f"""\n####\nContext: {context}\n####\nQuery: {input_query}\nHelpful Answer:"""
        prompt = prefix_prompt
        if chat_history:
            prompt += chat_history_prompt
        prompt += suffix_prompt
        return prompt

    def chat(self, input_query, config: ChatConfig = None):
        """
        Queries the vector database on the given input query.
        Gets relevant doc based on the query and then passes it to an
        LLM as context to get the answer.

        Maintains last 5 conversations in memory.
        :param input_query: The query to use.
        :param config: Optional. The `ChatConfig` instance to use as configuration options.
        :return: The answer to the query.
        """
        if config is None:
            config = ChatConfig()
        context = self.retrieve_from_database(input_query)
        global memory
        chat_history = memory.load_memory_variables({})["history"]
        prompt = self.generate_chat_prompt(
            input_query,
            context,
            chat_history=chat_history,
        )
        answer = self.get_answer_from_llm(prompt)
        memory.chat_memory.add_user_message(input_query)
        memory.chat_memory.add_ai_message(answer)
        return answer

    def dry_run(self, input_query, config: QueryConfig = None):
        """
        A dry run does everything except send the resulting prompt to
        the LLM. The purpose is to test the prompt, not the response.
        You can use it to test your prompt, including the context provided
        by the vector database's doc retrieval.
        The only thing the dry run does not consider is the cut-off due to
        the `max_tokens` parameter.

        :param input_query: The query to use.
        :param config: Optional. The `QueryConfig` instance to use as configuration options.
        :return: The prompt that would be sent to the LLM
        """
        if config is None:
            config = QueryConfig()
        context = self.retrieve_from_database(input_query)
        prompt = self.generate_prompt(input_query, context)
        return prompt

    def count(self):
        """
        Count the number of embeddings.

        :return: The number of embeddings.
        """
        return self.collection.count()


    def reset(self):
        """
        Resets the database. Deletes all embeddings irreversibly.
        `App` has to be reinitialized after using this method.
        """
        self.db_client.reset()


class App(EmbedChain):
    """
    The EmbedChain app.
    Has two functions: add and query.

    adds(data_type, url): adds the data from the given URL to the vector db.
    query(query): finds answer to the given query using vector database and LLM.
    dry_run(query): test your prompt without consuming tokens.
    """

    def __init__(self, config: InitConfig = None):
        """
        :param config: InitConfig instance to load as configuration. Optional.
        """
        if config is None:
            config = InitConfig()
        super().__init__(config)

    def get_llm_model_answer(self, prompt):
        messages = []
        messages.append({
            "role": "user", "content": prompt
        })
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
            temperature=0,
            max_tokens=1000,
            top_p=1,
        )
        return response["choices"][0]["message"]["content"]


class OpenSourceApp(EmbedChain):
    """
    The OpenSource app.
    Same as App, but uses an open source embedding model and LLM.

    Has two function: add and query.

    adds(data_type, url): adds the data from the given URL to the vector db.
    query(query): finds answer to the given query using vector database and LLM.
    """

    def __init__(self, config: InitConfig = None):
        """
        :param config: InitConfig instance to load as configuration. Optional. `ef` defaults to open source.
        """
        print("Loading open source embedding model. This may take some time...")
        if not config:
            config = InitConfig(
                ef = embedding_functions.SentenceTransformerEmbeddingFunction(
                    model_name="all-MiniLM-L6-v2"
                )
            )
        elif not config.ef:
            config._set_embedding_function(
                    embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2"
            ))
        print("Successfully loaded open source embedding model.")
        super().__init__(config)

    def get_llm_model_answer(self, prompt):
        from gpt4all import GPT4All

        global gpt4all_model
        if gpt4all_model is None:
            gpt4all_model = GPT4All("orca-mini-3b.ggmlv3.q4_0.bin")
        response = gpt4all_model.generate(
            prompt=prompt,
        )
        return response


class EmbedChainPersonApp:
    """
    Base class to create a person bot.
    This bot behaves and speaks like a person.

    :param person: name of the person, better if its a well known person.
    :param config: InitConfig instance to load as configuration.
    """
    def __init__(self, person, config: InitConfig = None):
        self.person = person
        self.person_prompt = f"You are {person}. Whatever you say, you will always say in {person} style."
        self.template = Template(
            self.person_prompt + " " + DEFAULT_PROMPT
        )
        if config is None:
            config = InitConfig()
        super().__init__(config)


class PersonApp(EmbedChainPersonApp, App):
    """
    The Person app.
    Extends functionality from EmbedChainPersonApp and App
    """
    def query(self, input_query, config: QueryConfig = None):
        query_config = QueryConfig(
            template=self.template,
        )
        return super().query(input_query, query_config)

    def chat(self, input_query, config: ChatConfig = None):
        chat_config = ChatConfig(
            template = self.template,
        )
        return super().chat(input_query, chat_config)


class PersonOpenSourceApp(EmbedChainPersonApp, OpenSourceApp):
    """
    The Person app.
    Extends functionality from EmbedChainPersonApp and OpenSourceApp
    """
    def query(self, input_query, config: QueryConfig = None):
        query_config = QueryConfig(
            template=self.template,
        )
        return super().query(input_query, query_config)

    def chat(self, input_query, config: ChatConfig = None):
        chat_config = ChatConfig(
            template = self.template,
        )
        return super().chat(input_query, chat_config)