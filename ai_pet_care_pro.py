import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import random
import datetime

# -------- CONFIG --------
st.set_page_config(page_title="AI Pet Doctor 🐾", page_icon="🐕", layout="centered")

# ✅ Configure Gemini API key
genai.configure(api_key="AIzaSyDdxIu4oaU2lpFJZv5S70fCmA1zgl4zIjQ")

# ✅ Initialize the Gemini model
model = genai.GenerativeModel("gemini-1.5-pro")

# -------- HEADER -------
st.title("🐾 AI Pet Doctor 💙")
st.caption("Smart AI app for pet health, happiness, and emergency care 🐶🐱🐰🐦")

# -------- DAILY TIP --------
tips = [
    "Keep your pet hydrated with fresh, clean water daily.",
    "Don’t skip your pet’s vaccinations.",
    "Give your pet daily exercise or playtime.",
    "Avoid human snacks — some can be toxic to pets!",
    "Keep your pet’s nails trimmed and fur brushed regularly."
]
st.info("💡 Pet Tip of the Day: " + random.choice(tips))

# -------- USER INPUT --------
pet_type = st.selectbox("Select your pet type:", ["Dog", "Cat", "Bird", "Rabbit", "Other"])
symptoms = st.text_area("Describe your pet’s symptoms 👇", height=150)

if "history" not in st.session_state:
    st.session_state.history = []

# -------- AI RESPONSE --------
def generate_response(pet, problem):
    emergencies = ["blood", "poison", "seizure", "choking", "unconscious"]
    if any(word in problem.lower() for word in emergencies):
        return "🚨 Emergency detected! Please take your pet to the nearest vet immediately."

    prompt = (
        f"You are a kind and expert pet doctor AI. "
        f"My {pet} has these symptoms: {problem}. "
        f"Please suggest safe, practical, and friendly advice."
    )

    # ✅ Gemini call (replaced OpenAI part)
    try:
        response = model.generate_content(prompt)
        return response.text.strip() if response and response.text else "Sorry, I couldn’t generate a response."
    except Exception as e:
        return f"⚠️ Error generating response: {e}"

# -------- SAVE CHAT TO PDF --------
def save_chat_to_pdf(chat):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="AI Pet Doctor - Chat History", ln=True, align="C")
    pdf.ln(10)
    for entry in chat:
        pdf.multi_cell(0, 8, f"You: {entry['user']}")
        pdf.multi_cell(0, 8, f"AI: {entry['bot']}")
        pdf.ln(5)
    filename = f"pet_chat_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(filename)
    return filename

# -------- GET ADVICE BUTTON --------
if st.button("💬 Get Pet Advice"):
    if symptoms.strip() == "":
        st.warning("Please describe your pet’s symptoms first.")
    else:
        with st.spinner("Analyzing symptoms... 🩺"):
            reply = generate_response(pet_type, symptoms)
            st.success(reply)
            st.session_state.history.append({"user": symptoms, "bot": reply})

# -------- CHAT HISTORY --------
if st.session_state.history:
    st.subheader("📜 Chat History")
    for chat in st.session_state.history:
        st.markdown(f"**You:** {chat['user']}")
        st.markdown(f"**AI:** {chat['bot']}")
        st.divider()

    if st.button("📥 Download Chat as PDF"):
        pdf_file = save_chat_to_pdf(st.session_state.history)
        with open(pdf_file, "rb") as f:
            st.download_button("Download PDF", f, file_name=pdf_file, mime="application/pdf")

# -------- EXTRA FEATURES --------
st.divider()
st.markdown("🌐 [Find Nearby Vet Clinics](https://www.google.com/maps/search/vet+clinic)")
st.caption("⚠️ This AI provides general suggestions. Always consult a real vet for emergencies.")


