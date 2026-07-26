import streamlit as st
import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Menova - Period Tracker & Chatbot",
    page_icon="🩸",
    layout="centered"
)

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
""", unsafe_allow_html=True)

# --- The Prompts ---
FAQ_RESPONSES = {
    # Greetings & Essentials
    "hi": "Hello! 👋 I'm Menova, your period tracking assistant. How can I help you today? ✨",
    "hello": "Hi there! 👋 Hope you're doing well. What's on your mind today?",
    "hey": "Hey! 😊 I'm here to answer any period or tracking questions you have.",
    "bye": "Goodbye! 👋 Take care of yourself, and see you next month! ✨",
    "goodbye": "Bye! 👋 Remember to stay hydrated 💧 and rest up 😴.",
    "thanks": "You're very welcome! 🥰 Let me know if you need anything else.",
    "thank you": "Happy to help! 💕 Take care.",
    
    # Cramps & Pain
    "cramps": "Menstrual cramps are very common 😣. Try using a warm heating pad on your abdomen, taking a warm bath, or drinking herbal teas like chamomile or ginger 🍵. To avoid cramps, do regular exercise, yoga 🧘‍♀️ and eat fresh veggies 🥦!",
    "bad cramps": "Severe cramps can be tough 🥺. If over-the-counter pain relievers or heat pads don't help, or if the pain prevents you from doing daily activities, it's a good idea to consult a doctor 🩺.",
    "stomach pain": "Lower abdominal pain is standard during periods due to the uterus contracting 🌸. Light stretching and staying warm can help ease the tension.",
    "back pain": "Lower back pain during periods is caused by hormonal shifts (progestins) 💆‍♀️. Gentle yoga poses like Child's Pose or Cat-Cow can offer relief.",
    "headache": "Hormonal headaches are common before or during your period due to dropping estrogen levels 🤕. Stay hydrated and rest in a dim room 🌙.",
    "migraine": "Menstrual migraines can be intense 😣. Avoid bright screens 📱, drink plenty of water, and speak to a healthcare professional if they are regular and severe 🩺.",
    "head": "A heavy spinning head is a classic 🌀. Drink water and take rest 😴. Take a pain reliever or go to a doctor if serious 🩺.",
    "pain": "Pain is usual during periods 💕. Use pain killers or hot bags. Drink hot water or green tea 🍵 for comfort. To avoid pain in your next periods, do light exercises, yoga 🧘‍♀️ and eat fruits and veggies everyday! 🍎🥦",
    "pelvic pain": "Pelvic discomfort is frequent as your uterine lining sheds. However, if it's sharp or sudden, monitor it closely and get some rest 🛋️.",
    
    # Blood Color & Texture
    "dark": "Dark brown or black blood is completely normal! 🤎 It usually means the blood is older and took longer to exit the uterus, often happening at the very beginning or end of your period.",
    "brown": "Brown blood is just old blood that has oxidized 🤎. It is very common at the start or end of your cycle.",
    "bright red": "Bright red blood means the blood is fresh and flowing quickly ❤️. This is normal, especially during the heaviest days of your period.",
    "pink": "Pinkish discharge or blood often happens at the very beginning of your period when fresh blood mixes with regular vaginal fluids 🌸.",
    "orange": "Orange-tinged discharge can sometimes happen when blood mixes with cervical fluid, but it can also be a sign of an infection ⚠️. Keep an eye on it!",
    "grey": "Greyish discharge, especially if accompanied by a strong odor or clumps, can be a sign of an infection like BV 🩺. It is best to see a doctor.",
    "clots": "Passing small blood clots (size of a dime or smaller) is totally normal, especially on heavy days 🩸. It's just your body's anti-coagulants keeping up with a fast flow.",
    "large clots": "If you are consistently passing blood clots larger than a quarter, it's recommended to consult a doctor or gynecologist 🩺.",
    "stringy": "Stringy or jelly-like blood is just a mix of blood and endometrial tissue/mucus, which is standard during a period 🌸.",
    "black": "Black blood is just the older blood getting expelled during slow flow days 🖤. Your body is just cleaning itself, however if the flow is heavy, please consult a gynecologist.",
    "blood": "Please tell me which color, texture, or clots of blood you see 🩸👀.",

    # Flow Vagaries
    "heavy": "A heavy flow is common in the first 2-3 days 🌊. However, if you soak through a pad or tampon every hour for several consecutive hours, consult a healthcare provider 🩺.",
    "light": "A light flow or 'scanty period' is common, especially if you are on hormonal birth control, stressed 😰, or near the end of your cycle ✨.",
    "spotting": "Spotting is light bleeding that happens outside your normal period 🩸. It can be caused by ovulation, stress, or starting a new birth control.",
    "no period": "A missed period can happen due to stress 😰, sudden weight changes, intense exercise, hormonal imbalances, or pregnancy 🤰. See a doctor if it misses for 3 cycles 🩺.",
    "late period": "Cycles can fluctuate! ⏳ A period is generally considered late if it hasn't started 5 or more days after it was expected. Stress is a huge factor 💭!",
    "early period": "An early period can happen occasionally due to hormonal fluctuations, travel ✈️, stress, or lifestyle changes ✨.",
    "irregular period": "Irregular cycles are common, especially in teenagers or those approaching menopause 🌸. If your cycle is consistently shorter than 21 days or longer than 35 days, check with a doctor 🩺.",
    "long period": "A typical period lasts 3 to 7 days 🗓️. If your bleeding lasts longer than 7 days consistently, it's a good idea to get it checked out.",
    "short period": "Periods lasting only 1-2 days can happen due to stress, hormonal shifts, or birth control. It's usually nothing to worry about if it happens occasionally 😊.",

    # Symptoms & Mood
    "burning sensation": "A burning sensation during your period or while urinating is not typical for a period and often indicates a UTI or infection. Please consult a doctor for a quick checkup! 🩺",
    "cold": "Feeling unusually cold during your period is common! Drops in estrogen can mess with your body's thermostat, and low iron (from blood loss) can also make you feel chilly. Stay warm with hot teas, cozy blankets, and iron-rich foods ☕ blankets!",
    "chilly": "Feeling chilly during your period is often due to shifting hormone levels or mild iron dips from bleeding. Grab a hot water bottle, sip warm drinks 🍵, and keep your feet extra warm 🧦!",
    "bloating": "Bloating is caused by water retention due to changing progesterone levels 💧. Reducing salt intake and drinking more water can surprisingly help reduce it!",
    "pms": "Premenstrual Syndrome (PMS) includes mood swings, bloating, and fatigue 💆‍♀️. Be gentle with yourself, practice self-care 🧘‍♀️, and get enough sleep 😴.",
    "mood swings": "Feeling emotional, irritable, or anxious is normal due to shifting estrogen and progesterone 💖. Remember, it's just your hormones talking!",
    "irritated": "Feeling frustrated is just due to your hormones 😤. Have some dark chocolate 🍫 or just sleep for a while, everything is gonna be okay! 💕",
    "sad": "Awww! Cheer up girl! 🥹 These hormones trouble you a lot I see. Before your next period, try to be more active and eat healthy food 🥗. For now, just Netflix and chill for a while! 🍿🎬 :D",
    "depressed": "Hey girl, this is no time to be depressed! Check this out: 😂\n Q: Why are tampon commercials so unrealistic?\n A: Nobody does cartwheels in white pants during a crime scene! 👖🩸",
    "happy": "Good to hear that! 🥳 Hope the happiness stays forever! ✨ :D",
    "fatigue": "Feeling exhausted? 😴 Your body is working hard! Prioritize sleep, eat iron-rich foods 🥬, and avoid over-exerting yourself.",
    "acne": "Hormonal breakouts along the jawline and chin are classic before a period 🧴. Keep your skin clean and hydrated, and try not to pop them! 🙅‍♀️",
    "pimple": "Hormonal breakouts along the jawline and chin are classic before a period ✨. Keep your skin clean and hydrated, and try not to pop them!",
    "vomiting": "It is completely normal due to hormonal changes 🤢. Try smelling some lemons 🍋 to stop the sensation and consult a doctor if severe 🩺.",
    "sensation": "Stop everything for a while and sit or sleep 🛋️. Drink plenty of water 💧.",
    "nausea": "Nausea can be caused by prostaglandins 🤢. Ginger tea 🍵 or peppermint can calm your stomach nicely.",
    "diarrhea": "'Period poops' are real! 😅 Prostaglandins can cause your bowels to contract along with your uterus. Stay hydrated 💧 and eat bland foods 🍞.",
    "constipation": "High progesterone levels before your period can slow down digestion 🥑. Eat fiber-rich foods and drink plenty of water 💧!",
    "breasts": "Breast tenderness or swelling is a classic PMS symptom caused by hormonal surges 🌸. Wearing a supportive, wire-free bra can help 👙.",
    "cravings": "Craving carbs or chocolate? 🍫 Your basal metabolic rate rises slightly before your period, making you hungrier 🍕! Enjoy your treats in moderation ✨.",
    "insomnia": "Difficulty sleeping can happen right before your period due to drops in progesterone 🌙. Try a relaxing bedtime routine without screens 📱.",
    "dizziness": "Mild dizziness can happen due to dehydration, cramping pain, or a slight drop in blood pressure 💧. Sit down, drink water, and rest 🛋️.",
    
    # Menopause & Perimenopause
    "burning": "Chronically low estrogen during menopause tricks the brain's thermostat into thinking you're overheating, causing hot flashes 🔥!",
    "menopause": "Menopause marks the end of menstrual cycles, officially diagnosed after 12 months without a period 🌸. Common symptoms include hot flashes 🔥, mood changes, and sleep disruptions 🌙.",
    "perimenopause": "Perimenopause is the transition phase leading up to menopause ✨. Cycles may become irregular, and symptoms like hot flashes or mood swings can begin.",
    "hot flashes": "Hot flashes are sudden feelings of heat, mostly in the face, neck, and chest 🔥. Wearing layered clothing 🧥, staying cool, and avoiding spicy foods 🌶️ can help ease them.",
    "night sweats": "Night sweats are severe hot flashes that happen during sleep 🌙. Keeping your bedroom cool, using breathable cotton bedding 🛌, and staying hydrated 💧 can provide relief.",
    "vaginal dryness": "Decreased estrogen during menopause can cause dryness 🧴. Using over-the-counter water-based moisturizers or lubricants can significantly improve comfort.",
    "bone density": "Lower estrogen levels can affect bone strength 🦴. Gentle weight-bearing exercises 🏋️‍♀️ and ensuring adequate calcium and vitamin D intake support bone health.",
    "sleep problems": "Sleep disturbances during menopause are often linked to hot flashes or hormonal shifts 😴. Establishing a calm bedtime routine and keeping the room cool can help 🌙.",
    "joint pain": "Hormonal changes during menopause can cause joint stiffness or pain 🦴. Staying active with low-impact exercises like walking 🚶‍♀️ or swimming 🏊‍♀️ can keep joints flexible.",
    "brain fog": "Mild forgetfulness or trouble concentrating can happen during perimenopause due to changing hormone levels 🧠. Prioritizing rest, exercise, and staying mentally active helps ✨.",
    "remedies": "Menopause symptoms can be managed through lifestyle adjustments 🥗 (regular exercise, balanced diet, cool environments) or medical options like HRT (Hormone Replacement Therapy) after consulting a doctor 🩺.",
    "gained weight": "Metabolic changes and dropping estrogen levels during menopause can make it easier to gain weight, especially around the trunk and waist. Staying active helps! 🏃‍♀️",
    "weight gain": "Metabolic changes and dropping estrogen levels during menopause can make it easier to gain weight, especially around the midsection. Staying active helps! 🏃‍♀️",
    "dry skin": "As collagen decreases during menopause, skin might feel drier or lose elasticity 🧴. Keeping skin hydrated and using gentle moisturizers can help ✨.",
    "moody": "Frequent mood shifts or irritability are very common during perimenopause due to fluctuating estrogen levels affecting brain chemistry 💖.",
    "hot": "Feeling hot during menopausal stages is due to dropping estrogen levels confuse the thermostat in the brain, causing a false alarm that the body is overheating🔥",
    "forget": "Mild forgetfulness during perimenopause is due to hormonal imbalances. Just rest well, stay mentally active, and do light exercises. Don't overdo anything!",
    "swell": "Hormonal shifts during menopause can cause fluid retention, leading to temporary swelling in your stomach, fingers, underarms or ankles 💧. Staying hydrated and reducing salt helps!",
    "size": "As estrogen drops during menopause, fat distribution changes toward the trunk, which can make your body size feel different even without major diet changes.",
    "low estrogen": "Estrogen levels naturally decline as you approach menopause 📉. This decrease is the primary driver behind hot flashes 🔥, sleep shifts 🌙, and cycle changes 🌸.",

    # General Tracking & Questions
    "how long is a cycle": "A normal menstrual cycle averages 28 days 🗓️, but anything between 21 and 35 days is considered perfectly healthy and normal!",
    "what is ovulation": "Ovulation is when an egg is released from the ovary 🥚. It usually happens around 14 days before your next period starts, marking your most fertile window ✨.",
    "can i get pregnant on my period": "While the chances are low, it is still possible to get pregnant during your period, especially if you have a short menstrual cycle 🗓️.",
    "exercise": "Yes! 🏃‍♀️ Light exercise like walking, swimming, or yoga 🧘‍♀️ can actually help reduce cramps and boost your mood via endorphins ✨!",
    "swim": "Absolutely! 🏊‍♀️ You can swim safely by using a tampon, menstrual cup, or period-proof swimwear. Pads will absorb water and won't work ❌.",
    "hygiene": "Change your pads or tampons every 4-6 hours (or sooner if heavy) to prevent bacteria buildup and stay fresh 🧼✨.",
    "smell": "A mild metallic smell is completely normal because of iron in the blood 🩸. However, a strong fishy or foul odor might point to an infection 🩺.",
}

# APPLICATION INTERFACE
st.title("🩸 Menova")
st.subheader("Your Period Tracker & Friendly Chat Assistant ✨")
st.write("Track your cycles easily and ask Menova any questions about your period or symptoms 💬.")

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

# --- SECTION 2: CHATBOT ---
st.header("💬 Ask Menova")
st.caption("Type in keywords like *'cramps'*, *'blood is dark'*, *'mood swings'*, or just say *'hi'*! 👋")

# 1. Initialize chat history in session state if it doesn't exist yet
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Display all previous messages from history on rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 3. Handle new user input
user_query = st.chat_input("Type your question or symptom here...")

if user_query:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.write(user_query)
        
    # Clean up the input to match keys easily
    clean_query = user_query.lower().strip().replace("?", "").replace(".", "")
    
    bot_response = None

    # Dynamic check for upcoming period questions using tracker data
    upcoming_triggers = ["period in", "starting in", "what should i do", "upcoming period", "period coming", "periods in"]
    if any(trigger in clean_query for trigger in upcoming_triggers):
        if days_left > 0:
            bot_response = (
                f"Your period is expected in about **{days_left} day(s)**! ⏳ Here is how you can prepare and help prevent severe cramps:\n\n"
                "**Precautions & Preparation:** 🌸\n"
                "* **Stay Hydrated:** Drink plenty of water 💧 to reduce bloating and muscle tightness.\n"
                "* **Adjust Diet:** Limit excessive salt, caffeine ☕, and sugar to lessen fluid retention.\n"
                "* **Stock Up:** Ensure you have pads, tampons, or period products ready 🩸.\n\n"
                "**Exercises to Prevent Cramps:** 🧘‍♀️\n"
                "* **Light Yoga:** Poses like *Child's Pose*, *Cat-Cow*, and *Bound Angle Pose* gently stretch the lower back and pelvis.\n"
                "* **Brisk Walking:** Low-impact cardio 🚶‍♀️ boosts circulation and releases endorphins (natural pain relievers ✨).\n"
                "* **Gentle Stretching:** Focus on relaxation and light stretching 🛋️."
            )
        elif days_left == 0:
            bot_response = "Your period is expected **today**! 🚨 Wear comfortable clothing 🧘‍♀️, keep heat packs handy 🧺, stay hydrated 💧, and try light stretching."
        else:
            bot_response = f"According to your tracker, your period is potentially **{abs(days_left)} days late** ⚠️. Minor variations are common due to stress or routine shifts ✨."

    # Keyword matching system
    if not bot_response:
        for key, response in FAQ_RESPONSES.items():
            if key in clean_query:
                bot_response = response
                break

    # Default fallback
    if not bot_response:
        bot_response = "I'm not quite sure about that specific phrase 🤔. Try asking Menova about symptoms like *cramps*, *heavy flow*, *dark blood*, *bloating*, or ask *'what should I do before my period?'* 🌸"

    # Display and save response
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    with st.chat_message("assistant"):
        st.write(bot_response)

# --- DISCLAIMER ---
st.divider()
st.caption("⚠️ **Disclaimer:** Menova is an informational tool and does not replace professional medical advice. If you experience severe pain, extremely irregular cycles, or have health concerns, please consult a healthcare professional.")
