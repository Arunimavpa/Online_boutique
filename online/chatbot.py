import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# FAQ data
faq_data = [
    {"question": "What is your return policy?", "answer": "Our return policy lasts 30 days."},
    {"question": "How can I track my order?",
     "answer": "You can track your order using the tracking number sent via email."},
    {"question": "What payment methods are accepted?", "answer": "We accept credit cards, PayPal, and bank transfers."},
    {"question": "Do you ship internationally?", "answer": "Yes, we ship to most countries worldwide."},
    {"question": "How can I contact customer support?",
     "answer": "You can reach our support team via email at saikadesginst@gmail.com."},
    {"question": "Hi", "answer": "Hello! How can I assist you today?"},
    {"question": "Hello", "answer": "Hi there! How can I help you today?"},
  {"question": "Can I customize my dress?", "answer": "Yes! You can customize your dress by selecting fabric, color, and size on the product page."},
  {"question": "How long does customization take?", "answer": "Customization typically takes 5-7 business days before shipping."},
  {"question": "Can I change my order after placing it?", "answer": "You can modify your order within 24 hours of placing it by contacting our support team."},
  {"question": "What sizes are available?", "answer": "We offer sizes from XS to XXL. You can check our size chart for detailed measurements."},
  {"question": "Do you offer plus-size dresses?", "answer": "Yes, we offer plus-size dresses up to 5XL. Please check our size guide."},
  {"question": "Can I return a customized dress?", "answer": "Customized dresses are non-refundable unless there is a defect. Please review our return policy."},
  {"question": "How much does customization cost?", "answer": "Customization is free for minor changes. Extensive customization may incur additional charges."},
  {"question": "How do I track my order?", "answer": "You can track your order using the tracking link sent to your email."},
  {"question": "What payment methods do you accept?", "answer": "We accept credit/debit cards, PayPal, and other secure payment methods."},
  {"question": "Do you offer international shipping?", "answer": "Yes, we ship worldwide. Shipping times vary by location."}

]

questions = [entry["question"] for entry in faq_data]
answers = [entry["answer"] for entry in faq_data]

vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(questions)


def get_answer(query):
    if query.lower() in ["hi", "hello", "hey"]:
        return "Hello! How can I assist you today?"

    query_vectorized = vectorizer.transform([query])
    similarity_scores = cosine_similarity(query_vectorized, X)

    most_similar_index = np.argmax(similarity_scores)
    highest_similarity_score = similarity_scores[0, most_similar_index]

    if highest_similarity_score > 0.3:
        return answers[most_similar_index]
    else:
        return "Sorry, I didn't understand that. Could you please rephrase your question?"
