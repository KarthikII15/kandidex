from transformers import pipeline

# Load summarization pipeline using DistilBART
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_text(text, max_tokens=1024, max_chunk_length=150, min_chunk_length=40):
    """
    Summarizes a long text by splitting it into chunks and summarizing each chunk individually.
    
    Args:
        text (str): The input text to be summarized.
        max_tokens (int): Max character length per chunk (approximate).
        max_chunk_length (int): Max summary length per chunk.
        min_chunk_length (int): Min summary length per chunk.

    Returns:
        str: Combined summary text.
    """
    # Split the text into manageable chunks
    chunks = [text[i:i+max_tokens] for i in range(0, len(text), max_tokens)]
    summaries = []

    for i, chunk in enumerate(chunks):
        print(f"Summarizing chunk {i+1}/{len(chunks)}...")
        summary = summarizer(
            chunk,
            max_length=max_chunk_length,
            min_length=min_chunk_length,
            do_sample=False
        )[0]['summary_text']
        summaries.append(summary)

    return " ".join(summaries)
