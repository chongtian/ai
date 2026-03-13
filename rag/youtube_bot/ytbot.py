import gradio as gr
import re  #For extracting video id
from youtube_transcript_api import YouTubeTranscriptApi  
from langchain_text_splitters import RecursiveCharacterTextSplitter  
from langchain_community.vectorstores import FAISS  
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.prompts import PromptTemplate  
from langchain_ollama import ChatOllama, OllamaLLM
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
import logging
import sys

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(stream=sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def get_video_id(url):
    """
    Extract YouTube Video ID from the url

    Args:
        url: Url of YouTube Video, for example, https://www.youtube.com/watch?v=1EAus8qZeyM

    Returns:
        The ID of YouTube video, for example, 1EAus8qZeyM
    """    
    # Regex pattern to match YouTube video URLs
    pattern = r'https:\/\/www\.youtube\.com\/watch\?v=([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None


def get_transcript(url):
    """
    Use YouTubeTranscriptApi to extract transcripts from a video

    The function first looks for and returns manually created transcript. 
    If manual transcript does not exist, it returns the generated transcript.
    
    Args:
        url: Url of YouTube Video, for example, https://www.youtube.com/watch?v=1EAus8qZeyM

    Returns:
        a list of YouTube video transcripts. It only includes English transcripts.
    """
    # Extracts the video ID from the URL
    video_id = get_video_id(url)
 
    # Create a YouTubeTranscriptApi() object
    ytt_api = YouTubeTranscriptApi()
   
    # Fetch the list of available transcripts for the given YouTube video
    transcripts = ytt_api.list(video_id)
   
    # assign blank string to transcript. This does not mean transcript will be a string object
    transcript = ""
    for t in transcripts:
        # Check if the transcript's language is English
        if t.language_code == 'en':
            if t.is_generated:
                # If no transcript has been set yet, use the auto-generated one
                if len(transcript) == 0:
                    transcript = t.fetch()
            else:
                # If a manually created transcript is found, use it (overrides auto-generated)
                transcript = t.fetch()
                break  # Prioritize the manually created transcript, exit the loop
   
    return transcript if transcript else None


def process(transcript):
    """
    Format the transcript so that it can be used by embedding model and LLM.

    Args:
        transcript: a list of YouTube video transcripts

    Returns:
        a string concatenating all lines of transcript, in the format of "Text: {text} Start: {start_time}\n"
    """
    # Initialize an empty string to hold the formatted transcript
    txt = ""
   
    # Loop through each entry in the transcript
    for i in transcript:
        try:
            # Append the text and its start time to the output string
            #txt += f"Text: {i['text']} Start: {i['start']}\n"
            txt += f"Text: {i.text} Start: {i.start}\n"
        except KeyError:
            # If there is an issue accessing 'text' or 'start', skip this entry
            pass
           
    # Return the processed transcript as a single string
    return txt


def chunk_transcript(processed_transcript, chunk_size=200, chunk_overlap=20):
    """
    Use a RecursiveCharacterTextSplitter to split the transript into chunks

    Args:
        processed_transcript: a string of all lines of transcript
        chunk_size: 
        chunk_overlap:

    Returns:
        List of text chunks of transcripts
    """
    # Initialize the RecursiveCharacterTextSplitter with specified chunk size and overlap
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
 
    # Split the transcript into chunks
    chunks = text_splitter.split_text(processed_transcript)
    return chunks

# Set LLM model here
def initialize_llm():
    """
    Initialize and return a llm model
    """
    return OllamaLLM(
        model="qwen3.5:9b"
        )

# Set embedding model here
def setup_embedding_model():
    """
    Initialize and return a embedding model
    """
    return HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")


def create_faiss_index(chunks, embedding_model):
    """
    Create a FAISS index from text chunks using the specified embedding model.

    Args:
        chunks: List of text chunks
        embedding_model: The embedding model to use
    
    Returns: 
        FAISS index
    """
    # Use the FAISS library to create an index from the provided text chunks
    return FAISS.from_texts(chunks, embedding_model)
 
 
def perform_similarity_search(faiss_index, query, k=3):
    """
    Search for specific queries within the embedded transcript using the FAISS index.

    Args:
        faiss_index: The FAISS index containing embedded text chunks
        query: The text input for the similarity search
        k: The number of similar results to return (default is 3)
    
    Returns: 
        List of similar results
    """
    # Perform the similarity search using the FAISS index
    results = faiss_index.similarity_search(query, k=k)
    return results
 
 
def create_summary_prompt():
    """
    Create a PromptTemplate for summarizing a YouTube video transcript.

    Args:
        None
   
    Returns: 
        PromptTemplate object
    """
    # Define the template for the summary prompt
    template = """
    <|begin_of_text|><|start_header_id|>system<|end_header_id|>
    You are an AI assistant tasked with summarizing YouTube video transcripts. Provide concise, informative summaries that capture the main points of the video content.
 
    Instructions:
    1. Summarize the transcript in a single concise paragraph.
    2. Ignore any timestamps in your summary.
    3. Focus on the spoken content (Text) of the video.
 
    Note: In the transcript, "Text" refers to the spoken words in the video, and "start" indicates the timestamp when that part begins in the video.<|eot_id|><|start_header_id|>user<|end_header_id|>
    Please summarize the following YouTube video transcript:
 
    {transcript}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
    """
   
    # Create the PromptTemplate object with the defined template
    prompt = PromptTemplate.from_template(template)
   
    return prompt
 
 
def retrieve(query, faiss_index, k=7):
    """
    Retrieve relevant context from the FAISS index based on the user's query.
 
    Args:
        query (str): The user's query string.
        faiss_index (FAISS): The FAISS index containing the embedded documents.
        k (int, optional): The number of most relevant documents to retrieve (default is 3).
 
    Returns:
        list: A list of the k most relevant documents (or document chunks).
    """
    relevant_context = faiss_index.similarity_search(query, k=k)
    return relevant_context


def create_qa_prompt_template():
    """
    Create a PromptTemplate for question answering based on video content.

    Args:
        None

    Returns:
        PromptTemplate: A PromptTemplate object configured for Q&A tasks.
    """
   
    # Define the template string
    qa_template = """
    <|begin_of_text|><|start_header_id|>system<|end_header_id|>
    You are an expert assistant providing detailed and accurate answers based on the following video content. Your responses should be:
    1. Precise and free from repetition
    2. Consistent with the information provided in the video
    3. Well-organized and easy to understand
    4. Focused on addressing the user's question directly
    If you encounter conflicting information in the video content, use your best judgment to provide the most likely correct answer based on context.
    Note: In the transcript, "Text" refers to the spoken words in the video, and "start" indicates the timestamp when that part begins in the video.<|eot_id|>
 
    <|start_header_id|>user<|end_header_id|>
    Relevant Video Context: {context}
    Based on the above context, please answer the following question:
    {question}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
    """
    # Create the PromptTemplate object
    prompt_template = PromptTemplate.from_template(qa_template)
    return prompt_template
 
 
def generate_answer(llm, question, faiss_index, k=3):
    """
    Retrieve relevant context and generate an answer based on user input.
 
    Args:
        llm: the LLM model
        question (str): The user's question.
        faiss_index (FAISS): The FAISS index containing the embedded documents.
        k (int, optional, default=3): The number of relevant documents to retrieve.
 
    Returns:
        str: The generated answer to the user's question.
    """
 
    # Retrieve relevant context
    gather = RunnableParallel(
        question=RunnablePassthrough(),
        context=lambda q: "\n".join([d.page_content for d in retrieve(q, faiss_index, k=k)])
    )

    # qa_prompt requires two inputs: the user's question and the retrieved context. 
    # The question is passed through unchanged, and the context is produced by a lambda function 
    # that runs a FAISS similarity search using the user's question as the query.
    prompt = create_qa_prompt_template()

    chain = gather | prompt | llm | StrOutputParser()
 
    # Generate answer using the QA chain
    answer = chain.invoke(question)
 
    return answer
 
 
# Initialize an empty string to store the processed transcript after fetching and preprocessing
processed_transcript = ""
 
def summarize_video(video_url):
    """
    Title: Summarize Video
 
    Description:
    This function generates a summary of the video using the preprocessed transcript.
    If the transcript hasn't been fetched yet, it fetches it first.
 
    Args:
        video_url (str): The URL of the YouTube video from which the transcript is to be fetched.
 
    Returns:
        str: The generated summary of the video or a message indicating that no transcript is available.
    """
    global fetched_transcript, processed_transcript
   
   
    if video_url:
        # Fetch and preprocess transcript
        fetched_transcript = get_transcript(video_url)
        processed_transcript = process(fetched_transcript)
    else:
        return "Please provide a valid YouTube URL."
 
    if processed_transcript:
        logger.info(f"processed_transcript: {len(processed_transcript)}")
        llm = initialize_llm()
        summary_prompt = create_summary_prompt()
        chain = summary_prompt | llm | StrOutputParser()
        summary = chain.invoke({"transcript": processed_transcript})
        return summary
    else:
        return "No transcript available. Please fetch the transcript first."
 
 
def answer_question(video_url, user_question):
    """
    Title: Answer User's Question
 
    Description:
    This function retrieves relevant context from the FAISS index based on the user’s query
    and generates an answer using the preprocessed transcript.
    If the transcript hasn't been fetched yet, it fetches it first.
 
    Args:
        video_url (str): The URL of the YouTube video from which the transcript is to be fetched.
        user_question (str): The question posed by the user regarding the video.
 
    Returns:
        str: The answer to the user's question or a message indicating that the transcript
             has not been fetched.
    """
    global fetched_transcript, processed_transcript
 
    # Check if the transcript needs to be fetched
    if not processed_transcript:
        if video_url:
            # Fetch and preprocess transcript
            fetched_transcript = get_transcript(video_url)
            processed_transcript = process(fetched_transcript)
        else:
            return "Please provide a valid YouTube URL."
 
    if processed_transcript and user_question:
        chunks = chunk_transcript(processed_transcript)
        llm = initialize_llm()
        embedding_model = setup_embedding_model()
        faiss_index = create_faiss_index(chunks, embedding_model)
        answer = generate_answer(llm, user_question, faiss_index)
        return answer
    else:
        return "Please provide a valid question and ensure the transcript has been fetched."
 
 
# create gradio user interface 
with gr.Blocks() as interface:
 
    gr.Markdown(
        "<h2 style='text-align: center;'>YouTube Video Summarizer and Q&A</h2>"
    )
 
    # Input field for YouTube URL
    video_url = gr.Textbox(label="YouTube Video URL", placeholder="Enter the YouTube Video URL")
   
    # Outputs for summary and answer
    summary_output = gr.Textbox(label="Video Summary", lines=5)
    question_input = gr.Textbox(label="Ask a Question About the Video", placeholder="Ask your question")
    answer_output = gr.Textbox(label="Answer to Your Question", lines=5)
 
    # Buttons for selecting functionalities after fetching transcript
    summarize_btn = gr.Button("Summarize Video")
    question_btn = gr.Button("Ask a Question")
 
    # Display status message for transcript fetch
    transcript_status = gr.Textbox(label="Transcript Status", interactive=False)
 
    # Set up button actions
    summarize_btn.click(summarize_video, inputs=video_url, outputs=summary_output)
    question_btn.click(answer_question, inputs=[video_url, question_input], outputs=answer_output)
 
# Launch the app with specified server name and port
interface.launch(server_name="127.0.0.1", server_port=7860)
