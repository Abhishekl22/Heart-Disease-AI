"""All written content in one place (easy to edit / translate)."""

DAILY_TIPS = [
    ("Walk after meals", "A 10–15 minute walk after eating lowers blood sugar and blood pressure and helps digestion."),
    ("Swap salt for spice", "Use garlic, lemon, pepper, cumin and herbs to flavour food. Less salt means a calmer blood pressure."),
    ("Add one fruit today", "Berries, oranges, apples and bananas are rich in fibre and potassium that your heart loves."),
    ("Breathe for 5 minutes", "Slow breathing (inhale 4s, exhale 6s) reduces stress hormones and relaxes blood vessels."),
    ("Drink water first", "Replace one sugary drink with water. Staying hydrated keeps blood flowing smoothly."),
    ("Take the stairs", "Two to three flights of stairs a day is a free cardio workout for your heart."),
    ("Sleep 7–8 hours", "Poor sleep is linked to high blood pressure and heart disease. Keep a fixed bedtime."),
    ("Go nuts (a handful!)", "A small handful of almonds or walnuts daily can improve cholesterol levels."),
    ("Stand up every hour", "Sitting for long periods hurts circulation. Stand and stretch for 2 minutes every hour."),
    ("Check your numbers", "Know your blood pressure, sugar and cholesterol. You can't fix what you don't measure."),
    ("Eat the rainbow", "Colourful vegetables give antioxidants that protect your arteries."),
    ("Laugh & connect", "Time with friends and family lowers stress and is linked to a longer, healthier life."),
]

CATEGORIES = [
    ("🥗", "green", "Heart-healthy eating", "Fill half your plate with vegetables, a quarter with whole grains and a quarter with lean protein.",
     ["Choose whole grains: oats, brown rice, millets", "Eat fish twice a week (or flax/walnuts)", "Use olive, mustard or groundnut oil in small amounts", "Limit packaged snacks and sweets"]),
    ("🏃", "red", "Move every day", "Adults need about 150 minutes of moderate exercise per week — that's just 30 minutes, 5 days.",
     ["Brisk walking, cycling, swimming, dancing", "Add 2 days of light strength training", "Warm up and cool down for 5 minutes", "Stop and rest if you feel chest pain or dizziness"]),
    ("😌", "violet", "Manage stress", "Long-term stress raises blood pressure and encourages unhealthy habits.",
     ["Try yoga, meditation or pranayama", "Spend time outdoors in nature", "Keep a hobby that you enjoy", "Talk to someone you trust"]),
    ("🚭", "amber", "Say no to tobacco", "Smoking damages blood vessels and doubles heart-attack risk. Quitting helps at any age.",
     ["Set a quit date and tell your family", "Ask your doctor about nicotine replacement", "Avoid second-hand smoke", "Keep alcohol within safe limits"]),
    ("⚖️", "green", "Healthy weight", "Extra weight around the waist makes the heart work harder.",
     ["Aim for a BMI of 18.5 – 24.9", "Waist: under 90 cm (men), 80 cm (women)", "Lose weight slowly: 0.5 kg a week", "Eat slowly and stop when 80% full"]),
    ("🩺", "", "Regular check-ups", "Early detection saves lives. Many heart problems show no symptoms at first.",
     ["BP check at least once a year", "Cholesterol & sugar test from age 30", "ECG if you have risk factors", "Keep a record of your reports"]),
]

EAT_MORE = ["Leafy greens & vegetables", "Fruits (not juices)", "Oats, millets, brown rice", "Lentils, beans, chickpeas", "Fish, eggs, skinless chicken", "Nuts & seeds (a handful)", "Curd, low-fat milk", "Garlic, turmeric, flaxseed"]
EAT_LESS = ["Salt & pickles", "Sugary drinks & sweets", "Deep-fried foods", "Bakery items (trans-fat)", "Processed & red meat", "White bread & maida", "Excess butter, ghee, cream", "Alcohol & energy drinks"]

MEAL_PLAN = [
    ("🌅 Breakfast", "Vegetable oats or poha with a fruit and a handful of nuts"),
    ("🍎 Mid-morning", "One seasonal fruit or coconut water"),
    ("🍛 Lunch", "2 rotis (multigrain), dal, a big bowl of vegetables, salad and curd"),
    ("🥜 Evening", "Roasted chana or green tea with a few almonds"),
    ("🍲 Dinner", "Grilled fish / paneer / sprouts with sautéed vegetables and soup"),
]

WEEK_PLAN = [
    ("Mon", "30 min brisk walk"), ("Tue", "20 min yoga + stretching"), ("Wed", "30 min cycling or swimming"),
    ("Thu", "Rest or gentle walk"), ("Fri", "30 min brisk walk + light weights"), ("Sat", "45 min fun activity (sport, dance, trek)"),
    ("Sun", "Rest, meditation, family time"),
]

WARNING_SIGNS = [
    ("😣", "Chest pain or pressure", "Tightness, squeezing or heaviness in the centre of the chest lasting more than a few minutes."),
    ("💪", "Pain spreading", "Pain that moves to the left arm, shoulder, jaw, neck or back."),
    ("😮‍💨", "Shortness of breath", "Struggling to breathe while resting or doing light activity."),
    ("🥶", "Cold sweat, nausea", "Sudden sweating, vomiting or feeling faint along with chest discomfort."),
    ("😵", "Dizziness", "Sudden light-headedness, blackouts or an irregular, racing heartbeat."),
    ("🦶", "Swollen feet", "Swelling in ankles or legs and unusual tiredness can indicate heart failure."),
]

MYTHS = [
    ("Heart disease only affects old people.", "Myth. Poor diet, stress, smoking and inactivity are causing heart problems in people in their 20s and 30s."),
    ("If I feel fine, my heart is fine.", "Myth. High blood pressure and cholesterol are 'silent' — you may feel nothing until a serious event."),
    ("Heart attacks always start with severe chest pain.", "Myth. Some people, especially women and diabetics, feel only breathlessness, nausea or fatigue."),
    ("Exercise is dangerous if you have a heart condition.", "Mostly myth. Doctor-approved exercise strengthens the heart. Always ask your doctor first."),
    ("Ghee and coconut oil are 'heart-healthy' for everyone.", "Myth. Saturated fats should be limited. Small amounts are fine but they are not a cure."),
    ("Only overweight people get heart disease.", "Myth. Thin people can have high cholesterol and blood pressure too."),
]

BP_TABLE = [
    ("Normal", "< 120 and < 80", "#18a864"),
    ("Elevated", "120–129 and < 80", "#8bc34a"),
    ("High (Stage 1)", "130–139 or 80–89", "#f5a524"),
    ("High (Stage 2)", "≥ 140 or ≥ 90", "#ef6c3d"),
    ("Crisis — call doctor", "> 180 and/or > 120", "#e5384f"),
]

FAQS = [
    ("How does the Heart Check work?", "You enter 13 simple health details. A machine-learning model trained on 920 real patient records from the UCI Heart Disease dataset compares your numbers with patterns seen in people with and without heart disease and returns a risk percentage."),
    ("Is the result a medical diagnosis?", "No. It is an educational screening tool. Only a qualified doctor can diagnose heart disease after proper tests such as ECG, echo and stress tests."),
    ("I don't know some of my values — can I still use it?", "Yes! Cholesterol, fasting sugar, ST slope, major vessels and thalassemia all have a 'Don't know' option. The model fills the gaps using typical values, but results are more reliable with more information."),
    ("Where do I find my blood pressure, cholesterol and ECG values?", "Look at your latest lab report or prescription. Blood pressure can be measured at any pharmacy; cholesterol needs a lipid profile blood test; ECG results come from a cardiology visit."),
    ("Is my data stored or shared?", "Your inputs are used only to calculate the result and are kept in your browser session. Nothing is uploaded or sold. Support messages you send are saved only to the app owner's local file."),
    ("What does 'Moderate' risk mean?", "Some of your readings are borderline. It is a nudge to improve lifestyle and arrange a routine check-up — not a cause for panic."),
    ("How accurate is the model?", "On unseen test data it reaches roughly 85% accuracy and about 0.91 ROC-AUC (see the Insights page). No model is perfect, so always treat results as guidance."),
    ("Can I download my result?", "Yes. After a prediction, click 'Download report' to save a printable health report. You can also export your session history as CSV."),
    ("What should I do in an emergency?", "If you have chest pain, breathlessness or fainting, stop using the app and call your local emergency number immediately (112 in India, 911 in the US, 999 in the UK)."),
]
