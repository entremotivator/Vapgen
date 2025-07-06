import streamlit as st
import openai

st.set_page_config(page_title="Vapi Voice Agent Script Generator", layout="wide")
st.title("Vapi Voice Agent Script Generator")

# --- Sidebar ---
with st.sidebar:
    st.header("Agent Identity & API Key")
    openai_api_key = st.text_input("OpenAI API Key", type="password", help="Optional: Use for AI-powered enhancements")
    agent_name = st.text_input("Agent Name", value="Alex")
    company_name = st.text_input("Company Name", value="TechSolutions")
    role = st.text_input("Agent Role", value="customer service voice assistant")
    greeting = st.text_area("First Message", value=f"Hi there, this is {agent_name} from {company_name} customer support. How can I help you today?")

st.header("Persona & System Prompt Details")
personality = st.text_area(
    "Personality Traits",
    value=(
        "- Sound friendly, patient, and knowledgeable without being condescending\n"
        "- Use a conversational tone with natural speech patterns, including occasional \"hmm\" or \"let me think about that\" to simulate thoughtfulness\n"
        "- Speak with confidence but remain humble when you don't know something\n"
        "- Demonstrate genuine concern for customer issues"
    ),
    height=120
)

speech_characteristics = st.text_area(
    "Speech Characteristics",
    value=(
        "- Use contractions naturally (I'm, we'll, don't, etc.)\n"
        "- Vary your sentence length and complexity to sound natural\n"
        "- Include occasional filler words like \"actually\" or \"essentially\" for authenticity\n"
        "- Speak at a moderate pace, slowing down for complex information"
    ),
    height=100
)

conversation_flow = st.text_area(
    "Conversation Flow (YAML/Markdown)",
    value=(
        "### Introduction\n"
        f"Start with: \"{greeting}\"\n\n"
        "If the customer sounds frustrated or mentions an issue immediately, acknowledge their feelings: \"I understand that's frustrating. I'm here to help get this sorted out for you.\"\n\n"
        "### Issue Identification\n"
        "1. Use open-ended questions initially: \"Could you tell me a bit more about what's happening with your [product/service]?\"\n"
        "2. Follow with specific questions to narrow down the issue: \"When did you first notice this problem?\" or \"Does this happen every time you use it?\"\n"
        "3. Confirm your understanding: \"So if I understand correctly, your [product] is [specific issue] when you [specific action]. Is that right?\""
    ),
    height=200
)

knowledge_base = st.text_area(
    "Knowledge Base (YAML/Markdown)",
    value=(
        "### Product Information\n"
        f"- {company_name} offers software services for productivity, security, and business management\n"
        "- Our flagship products include TaskMaster Pro (productivity), SecureShield (security), and BusinessFlow (business management)\n"
        "- All products have desktop and mobile applications\n"
        "- Subscription tiers include Basic, Premium, and Enterprise\n"
        "- Support hours are Monday through Friday, 8am to 8pm Eastern Time, and Saturday 9am to 5pm\n"
        "\n"
        "### Common Solutions\n"
        "- Most connectivity issues can be resolved by signing out completely, clearing browser cache, and signing back in\n"
        "- Performance problems often improve after restarting the application and ensuring the operating system is updated\n"
        "- Data synchronization issues typically resolve by checking internet connection and forcing a manual sync\n"
        "- Most mobile app problems can be fixed by updating to the latest version or reinstalling the application"
    ),
    height=200
)

# --- Optional: Use OpenAI to generate a concise persona summary ---
persona_summary = ""
if openai_api_key and st.button("AI-Generate Persona Summary"):
    try:
        openai.api_key = openai_api_key
        prompt = (
            f"Summarize the following persona traits and speech characteristics for a {role} named {agent_name} at {company_name} in one or two sentences:\n"
            f"Personality Traits:\n{personality}\nSpeech Characteristics:\n{speech_characteristics}"
        )
        with st.spinner("Generating summary with OpenAI..."):
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=60,
                temperature=0.7,
            )
            persona_summary = response.choices[0].message.content.strip()
        st.success("Persona summary generated!")
    except Exception as e:
        st.error(f"OpenAI API error: {e}")

if st.button("Generate Script"):
    script = f"""# Vapi Voice Agent Script

first_message: |
  {greeting}

system_prompt: |
  # {role.capitalize()} Prompt

  ## Identity & Purpose

  You are {agent_name}, a {role} for {company_name}. Your primary purpose is to help customers resolve issues with their products, answer questions about services, and ensure a satisfying support experience.

  ## Voice & Persona

  ### Personality
  {personality}

  ### Speech Characteristics
  {speech_characteristics}

  ## Conversation Flow

  {conversation_flow}

  ## Knowledge Base

  {knowledge_base}

  Remember that your ultimate goal is to resolve customer issues efficiently while creating a positive, supportive experience that reinforces their trust in {company_name}.
"""

    if persona_summary:
        script += f"\n# AI-Generated Persona Summary\n# {persona_summary}\n"

    st.subheader("Generated Script")
    st.code(script, language="yaml")
    st.success("Copy and use this script in your Vapi or LLM voice agent platform!")

else:
    st.info("Fill in the fields and click 'Generate Script' to create your agent script.")

