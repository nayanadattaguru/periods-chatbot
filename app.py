import streamlit as st
import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Monthly Friend" - Period Tracker & Chatbot",
    page_icon="🩸",
    layout="centered")

# --- CUSTOM CSS FOR BETTER VISUALS ---
st.markdown("""
    <style>
    .main { background-color: #fff5f5; }
    .stButton>button {
        background-color: #ff4d6d;
        color: white;
        border-radius: 20px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #c9184a;
        color: white;
    }
    div.stDateInput > div {
        border-radius: 10px;
    }
    </style>
""", unsafe-allowed_html=True)

# --- The Prompts ---
FAQ_RESPONSES = {
    # Greetings & Essentials
    "hi": "Hello! I'm FlowBuddy, your period tracking assistant. How can I help you today?",
    "hello": "Hi there! Hope you're doing well. What's on your mind today?",
    "hey": "Hey! I'm here to answer any period or tracking questions you have.",
    "bye": "Goodbye! Take care of yourself, and see you next month!",
    "goodbye": "Bye! Remember to stay hydrated and rest up.",
    "thanks": "You're very welcome! Let me know if you need anything else.",
    "thank you": "Happy to help! Take care.",
    
    # Cramps & Pain
    "i have cramps": "Menstrual cramps are very common. Try using a warm heating pad on your abdomen, taking a warm bath, or drinking herbal teas like chamomile or ginger.",
    "bad cramps": "Severe cramps can be tough. If over-the-counter pain relievers or heat pads don't help, or if the pain prevents you from doing daily activities, it's a good idea to consult a doctor.",
    "stomach pain": "Lower abdominal pain is standard during periods due to the uterus contracting. Light stretching and staying warm can help ease the tension.",
    "back pain": "Lower back pain during periods is caused by hormonal shifts (progestins). Gentle yoga poses like Child's Pose or Cat-Cow can offer relief.",
    "headache": "Hormonal headaches are common before or during your period due to dropping estrogen levels. Stay hydrated and rest in a dim room.",
    "migraine": "Menstrual migraines can be intense. Avoid bright screens, drink water, and speak to a healthcare professional if they are regular and severe.",
    "pelvic pain": "Pelvic discomfort is frequent as your uterine lining sheds. However, if it's sharp or sudden, monitor it closely and rest.",
    
    # Blood Color & Texture
    "blood is dark": "Dark brown or black blood is completely normal. It usually means the blood is older and took longer to exit the uterus, often happening at the very beginning or end of your period.",
    "brown blood": "Brown blood is just old blood that has oxidized. It is very common at the start or end of your cycle.",
    "bright red blood": "Bright red blood means the blood is fresh and flowing quickly. This is normal, especially during the heaviest days of your period.",
    "pink blood": "Pinkish discharge or blood often happens at the very beginning of your period when fresh blood mixes with regular vaginal fluids.",
    "orange blood": "Orange-tinged discharge can sometimes happen when blood mixes with cervical fluid, but it can also be a sign of an infection. Keep an eye on it.",
    "grey blood": "Greyish discharge, especially if accompanied by a strong odor or clumps, can be a sign of an infection like BV. It is best to see a doctor.",
    "clots": "Passing small blood clots (size of a dime or smaller) is totally normal, especially on heavy days. It's just your body's anti-coagulants keeping up with a fast flow.",
    "large clots": "If you are consistently passing blood clots larger than a quarter, it's recommended to consult a doctor or gynecologist.",
    "stringy blood": "Stringy or jelly-like blood is just a mix of blood and endometrial tissue/mucus, which is standard during a period.",

    # Flow Vagaries
    "heavy flow": "A heavy flow is common in the first 2-3 days. However, if you soak through a pad or tampon every hour for several consecutive hours, consult a healthcare provider.",
    "light flow": "A light flow or 'scanty period' is common, especially if you are on hormonal birth control, stressed, or near the end of your cycle.",
    "spotting": "Spotting is light bleeding that happens outside your normal period. It can be caused by ovulation, stress, or starting a new birth control.",
    "no period": "A missed period can happen due to stress, sudden weight changes, intense exercise, hormonal imbalances, or pregnancy. See a doctor if it misses for 3 cycles.",
    "late period": "Cycles can fluctuate. A period is generally considered late if it hasn't started 5 or more days after it was expected. Stress is a huge factor!",
    "early period": "An early period can happen occasionally due to hormonal fluctuations, travel, stress, or lifestyle changes.",
    "irregular period": "Irregular cycles are common, especially in teenagers or those approaching menopause. If your cycle is consistently shorter than 21 days or longer than 35 days, check with a doctor.",
    "long period": "A typical period lasts 3 to 7 days. If your bleeding lasts longer than 7 days consistently, it's a good idea to get it checked out.",
    "short period": "Periods lasting only 1-2 days can happen due to stress, hormonal shifts, or birth control. It's usually nothing to worry about if it happens occasionally.",

    # Symptoms & Mood
    "bloating": "Bloating is caused by water retention due to changing progesterone levels. Reducing salt intake and drinking more water can surprisingly help reduce it.",
    "pms": "Premenstrual Syndrome (PMS) includes mood swings, bloating, and fatigue. Be gentle with yourself, practice self-care, and get enough sleep.",
    "mood swings": "Feeling emotional, irritable, or anxious is normal due to shifting estrogen and progesterone. Remember, it's just your hormones talking!",
    "fatigue": "Feeling exhausted? Your body is working hard! Prioritize sleep, eat iron-rich foods, and avoid over-exerting yourself.",
    "acne": "Hormonal breakouts along the jawline and chin are classic before a period. Keep your skin clean and hydrated, and try not to pop them.",
    "nausea": "Nausea can be caused by prostaglandins, the same chemicals that cause uterine contractions. Ginger tea or peppermint can calm your stomach.",
    "diarrhea": "Period poops' are real! Prostaglandins can cause your bowels to contract along with your uterus. Stay hydrated and eat bland foods.",
    "constipation": "High progesterone levels before your period can slow down digestion. Eat fiber-rich foods and drink plenty of water.",
    "sore breasts": "Breast tenderness or swelling is a classic PMS symptom caused by hormonal surges. Wearing a supportive, wire-free bra can help.",
    "cravings": "Craving carbs or chocolate? Your basal metabolic rate rises slightly before your period, making you hungrier. Enjoy your treats in moderation!",
    "insomnia": "Difficulty sleeping can happen right before your period due to drops in progesterone. Try a relaxing bedtime routine without screens.",
    "dizziness": "Mild dizziness can happen due to dehydration, cramping pain, or a slight drop in blood pressure. Sit down, drink water, and rest.",

    # General Tracking & Questions
    "how long is a cycle": "A normal menstrual cycle averages 28 days, but anything between 21 and 35 days is considered perfectly healthy and normal.",
    "what is ovulation": "Ovulation is when an egg is released from the ovary. It usually happens around 14 days before your next period starts, marking your most fertile window.",
    "can i get pregnant on my period": "While the chances are low, it is still possible to get pregnant during your period, especially if you have a short menstrual cycle.",
    "exercise on period": "Yes! Light exercise like walking, swimming, or yoga can actually help reduce cramps and boost your mood via endorphins.",
    "swim on period": "Absolutely! You can swim safely by using a tampon, menstrual cup, or period-proof swimwear. Pads will absorb water and won't work.",
    "hygiene": "Change your pads or tampons every 4-6 hours (or sooner if heavy) to prevent bacteria buildup and stay fresh.",
    "smell": "A mild metallic smell is completely normal because of iron in the blood. However, a strong fishy or foul odor might point to an infection.",
}

# APPLICATION INTERFACE
st.title("🩸 Monthly Friend")
st.subheader("Your Period Tracker & Friendly Chat Assistant")
st.write("Track your cycles easily and ask Monthly Friend any questions about your period or symptoms.")

st.divider()

# PERIOD TRACKER SECTION
st.header("📅 Period Tracker")

col1, col2 = st.columns(2)

with col1:
    last_period = st.date_input("When did your last period start?", datetime.date.today())
with col2:
    cycle_length = st.number_input("Average length of your cycle (in days):", min_value=15, max_value=45, value=28)

# Calculate next expected period
next_period = last_period + datetime.timedelta(days=int(cycle_length))
days_left = (next_period - datetime.date.today()).days

# Display tracker insights
st.info(f"✨ Your next expected period will start around: **{next_period.strftime('%B %d, %Y')}**")

if days_left > 0:
    st.success(f"⏳ Approximately **{days_left} days** until your next cycle.")
elif days_left == 0:
    st.warning("🚨 Your period is expected **today**!")
else:
    st.error(f"⚠️ Your period is potentially **{abs(days_left)} days late**. (Note: Minor irregularities are common!)")


st.divider()

# SECTION CHATBOT
st.header("💬 Ask FlowBuddy")
st.caption("Type in keywords like *'cramps'*, *'blood is dark'*, *'mood swings'*, or just say *'hi'*!")

# Chat Input Component
user_query = st.chat_input("Type your question or symptom here...")

if user_query:
    # Display user message
    with st.chat_message("user"):
        st.write(user_query)
        
    # Clean up the input to match keys easily
    clean_query = user_query.lower().strip().replace("?", "").replace(".", "")
    
    # Generate bot response
    bot_response = "I'm not quite sure about that specific phrase. Try asking about symptoms like *cramps*, *heavy flow*, *dark blood*, *bloating*, or *mood swings*!"
    
    # Keyword matching system
    for key, response in FAQ_RESPONSES.items():
        if key in clean_query:
            bot_response = response
            break # Stop at the first matched keyword
            
    # Display bot response
    with st.chat_message("assistant"):
        st.write(bot_response)

# DISCLAIMER(to not trust the AI completely)
st.divider()
st.caption("⚠️ **Disclaimer:** Monthly Friend is an informational tool and does not replace professional medical advice.If you experience severe pain, extremely irregular cycles, or have health concerns, please consult a healthcare professional.")
