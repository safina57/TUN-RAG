# 🇹🇳 Tunisia Constitution Chatbot

Explore and interact with the Tunisian Constitution using this RAG-based chatbot. This project leverages modern AI techniques to provide an intuitive way to navigate constitutional content.

👉 [Test the chatbot here](https://safina57-tun-rag.hf.space)

## 🚀 Getting Started

Follow these steps to set up and run the project:

### 1. 📦 Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 2. 📚 Load the Constitution Data

Run the data loader script to prepare the documents:

```bash
python test/data_loader.py
```

### 3. 🖥️ Start the Backend Server

Start the FastAPI backend:

```bash
uvicorn src.server:app --reload
```

### 4. 🌐 Launch the Chat Interface

Open the Streamlit frontend:

```bash
streamlit run app/app.py
```

---

You're all set!  
Enjoy interacting with the Tunisian Constitution through your chatbot. 🇹🇳
