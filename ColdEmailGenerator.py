import streamlit as st
import os

# Now import CrewAI and other dependencies
from crewai import Agent, Task, Crew, LLM
from crewai_tools import ScrapeWebsiteTool
from dotenv import load_dotenv

load_dotenv()

# Page config
st.set_page_config(page_title="Cold Email Generator", page_icon="📧", layout="wide")

# Title and description
st.title("📧 Cold Email Generator")
st.markdown("Generate personalized cold emails by analyzing target company websites")

# Sidebar for inputs
with st.sidebar:
    st.header("🔑 API Configuration")
    
    groq_api_key_input = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="Enter your Groq API key (or set in Streamlit secrets)",
        value=os.getenv("GROQ_API_KEY", "")
    )
    
    # Set API key from input if provided
    if groq_api_key_input:
        os.environ["GROQ_API_KEY"] = groq_api_key_input
    
    st.markdown("---")
    st.header("🎯 Target Information")
    
    target_website = st.text_input(
        "Target Website URL",
        placeholder="https://example.com",
        help="Enter the company website to analyze"
    )
    
    agency_services = st.text_area(
        "Your Agency Services",
        placeholder="Web Development, AI Solutions, Digital Marketing...",
        help="List the services your agency provides"
    )
    
    ceo_name = st.text_input(
        "CEO/Decision Maker Name",
        placeholder="John Doe",
        help="Name of the person you're reaching out to"
    )
    
    your_name = st.text_input(
        "Your Name",
        placeholder="Jane Smith",
        help="Your name for email signature"
    )
    
    your_company = st.text_input(
        "Your Company Name",
        placeholder="Your Agency Inc.",
        help="Your company name"
    )
    
    generate_button = st.button("🚀 Generate Cold Email", type="primary", use_container_width=True)

# Main content area
if generate_button:
    if not all([target_website, agency_services, ceo_name, your_name, your_company]):
        st.error("⚠️ Please fill in all fields in the sidebar")
    else:
        with st.spinner("🔍 Analyzing website and generating personalized email..."):
            try:
                # Check for API key
                groq_api_key = os.getenv("GROQ_API_KEY")
                if not groq_api_key:
                    st.error("❌ GROQ_API_KEY not found. Please set it in your Streamlit secrets or .env file")
                    st.stop()
                
                # Initialize tools and LLM
                scraper = ScrapeWebsiteTool()
                
                llm = LLM(
                    model="groq/llama-3.3-70b-versatile",
                    api_key=groq_api_key
                )
                
                # Create agents
                research_agent = Agent(
                    role="Website Research Specialist",
                    goal=f"Analyze {target_website} and extract key business information, pain points, and opportunities",
                    backstory="You are an expert at analyzing company websites to understand their business model, services, and potential needs",
                    tools=[scraper],
                    llm=llm,
                    verbose=True
                )
                
                email_writer_agent = Agent(
                    role="Cold Email Copywriter",
                    goal="Write compelling, personalized cold emails that get responses",
                    backstory="You are a master copywriter specializing in B2B cold outreach with a proven track record of high response rates",
                    llm=llm,
                    verbose=True
                )
                
                # Create tasks
                research_task = Task(
                    description=f"""
                    Analyze the website {target_website} and extract:
                    1. Company's main services and offerings
                    2. Target market and industry
                    3. Recent updates or news
                    4. Potential pain points or areas for improvement
                    5. Company culture and values
                    
                    Provide a comprehensive analysis that can be used for personalized outreach.
                    """,
                    expected_output="Detailed analysis of the company including services, market, pain points, and opportunities",
                    agent=research_agent
                )
                
                email_writing_task = Task(
                    description=f"""
                    Using the research findings, write a personalized cold email to {ceo_name}.
                    
                    Context:
                    - Sender: {your_name} from {your_company}
                    - Our services: {agency_services}
                    - Target: {ceo_name} at the researched company
                    
                    Requirements:
                    1. Personalized subject line (creative and attention-grabbing)
                    2. Brief, engaging opening that shows you've researched their company
                    3. Clear value proposition aligned with their needs
                    4. Specific examples of how our services can help
                    5. Soft call-to-action
                    6. Professional signature
                    
                    Keep it concise (150-200 words), conversational, and focused on their needs, not just our services.
                    Avoid generic phrases and make it feel human and authentic.
                    """,
                    expected_output="A complete cold email with subject line and body text, ready to send",
                    agent=email_writer_agent,
                    context=[research_task]
                )
                
                # Create and run crew
                crew = Crew(
                    agents=[research_agent, email_writer_agent],
                    tasks=[research_task, email_writing_task],
                    verbose=True
                )
                
                result = crew.kickoff()
                
                # Display results
                st.success("✅ Email generated successfully!")
                
                # Display the generated email
                st.markdown("---")
                st.markdown("### 📬 Generated Cold Email")
                
                # Create a nice card for the email
                with st.container():
                    st.markdown(f"""
                    <div style="background-color: #1e1e1e; padding: 20px; border-radius: 10px; border-left: 5px solid #1f77b4; color: #ffffff;">
                    {result}
                    </div>
                    """, unsafe_allow_html=True)
                
                # Copy to clipboard button
                st.markdown("---")
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    st.download_button(
                        label="📋 Download Email",
                        data=str(result),
                        file_name=f"cold_email_{ceo_name.replace(' ', '_')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.info("💡 Tip: Make sure all API keys are set in your .env file")

else:
    # Welcome message when no email is generated
    st.info("👈 Fill in the target information in the sidebar and click 'Generate Cold Email' to get started")
    
    st.markdown("---")
    st.markdown("### 🎯 How it works:")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 1️⃣ Research")
        st.write("AI analyzes the target website to understand their business, services, and potential needs")
    
    with col2:
        st.markdown("#### 2️⃣ Personalize")
        st.write("Combines research insights with your services to create relevant value propositions")
    
    with col3:
        st.markdown("#### 3️⃣ Generate")
        st.write("Crafts a compelling, personalized cold email ready to send")
    
    st.markdown("---")
    st.markdown("### ✨ Features:")
    st.markdown("""
    - 🔍 **Intelligent Website Analysis**: Extracts key business information
    - 🎨 **Personalized Content**: Tailored to each prospect's needs
    - ✍️ **Professional Copy**: Written by AI trained on high-converting emails
    - ⚡ **Fast Generation**: Get your email in seconds
    - 📋 **Easy Export**: Download and use immediately
    """)
