import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

def summarize_text(prompt, max_length=500, max_new_tokens=150):
    
    # Load a pre-trained GPT-2 model for text summarization
    model_name = 'gpt2'
    model = GPT2LMHeadModel.from_pretrained(model_name)
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)

    # Define padding token
    tokenizer.pad_token = tokenizer.eos_token

    # Set the model to evaluation mode
    model.eval()
    
    inputs = tokenizer.encode(prompt, return_tensors='pt', truncation=True,max_length=max_length)
    
    # Create attention mask
    attention_mask = torch.ones(inputs.shape, dtype=torch.long)
    
    with torch.no_grad():
        summary_ids = model.generate(
            inputs,
            attention_mask=attention_mask,
            max_length=max_length + max_new_tokens,
            length_penalty=2.0,
            num_beams=4,
            early_stopping=True,
            pad_token_id=tokenizer.pad_token_id
        )
    # Print the shape of the generated summary tensor
    #print(f"Summary tensor shape: {summary_ids.shape}")    
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

def extract_information(text):
    prompt = f"""
    Extract the technical tools, use cases, and business value mentioned in the following text:
    {text}
    """
    summary = summarize_text(prompt)
    return summary


def create_diagram(extracted_info):
    prompt = f"""
    Create a diagram in markdown to illustrate how the tools are used to build the solution for the use cases mentioned:
    {extracted_info}
    """
    diagram = summarize_text(prompt)
    return diagram

# Example usage


def filter_information(text, filter_type):
    prompt = f"""
    Return only the {filter_type} mentioned in the following text and erase all other information:
    {text}
    """
    filtered_info = summarize_text(prompt)
    return filtered_info
