# AI Chatbot Project

## Overview
This AI Chatbot project is designed to provide a conversational interface for users to interact with. It uses natural language processing techniques to understand user queries and provide relevant responses. The chatbot can also read data from long paragraphs, CSV files, and PDF files to enhance its knowledge base.

## Technologies Used
- **Python**: The primary programming language used for developing the chatbot.
- **Tkinter**: A standard GUI library in Python used for creating the graphical user interface.
- **FuzzyWuzzy**: A library used for fuzzy string matching to find similarities between user queries and stored data.
- **Python-Levenshtein**: A library that provides fast computation of Levenshtein distance, which is used by FuzzyWuzzy for better performance.
- **PdfPlumber**: A library used for extracting text from PDF files.

## Installation
To run this project, you need to have Python installed on your system. You can download Python from [python.org](https://www.python.org/).

1. **Clone the repository**:
   ```sh
   git clone https://github.com/noamanayub/ai-chatbot.git
   cd ai-chatbot
   ```

2. **Install the required dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

## How to Run
1. **Navigate to the project directory**:
   ```sh
   cd ai-chatbot
   ```

2. **Run the chatbot**:
   ```sh
   python chatbot.py
   ```

## Advantages of the AI Chatbot
- **User-Friendly Interface**: The chatbot provides a simple and intuitive GUI for users to interact with.
- **Fuzzy Matching**: Uses fuzzy string matching to understand user queries even if they are not phrased exactly as stored data.
- **Multi-Format Data Support**: Can read and process data from long paragraphs, CSV files, and PDF files, making it versatile and adaptable.
- **Feedback Mechanism**: Allows users to provide feedback on the responses, which can be used to improve the chatbot's performance over time.

## How the AI Works
1. **Data Loading**: The chatbot loads its knowledge base from a `chatbot_data.txt` file, which contains questions and answers in a simple format.
2. **User Input**: Users can input their queries through the GUI. The chatbot checks if the input contains any bad words and filters them out.
3. **Response Generation**: The chatbot uses fuzzy matching to find the closest match to the user's query in its knowledge base. If a match is found, it provides the corresponding answer.
4. **File Upload**: Users can upload CSV and PDF files to update the chatbot's knowledge base. The chatbot reads the files and extracts relevant information.
5. **Feedback**: Users can provide feedback on the responses, which is stored and can be used to improve the chatbot's responses in the future.

## Future Enhancements
- **Machine Learning Integration**: Incorporate machine learning models to improve the chatbot's understanding and response accuracy.
- **Natural Language Processing**: Use advanced NLP techniques to handle more complex queries and provide more nuanced responses.
- **Multi-Lingual Support**: Extend the chatbot's capabilities to support multiple languages.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any bugs or feature requests.
