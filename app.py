# ============================================================================
# STREAMLIT MULTI-AGENT DEEPAGENT
# Beautiful web interface with panels for building apps
# ============================================================================

import streamlit as st
import anthropic
from datetime import datetime
import base64
import re

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Multi-Agent DeepAgent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS
# ============================================================================

st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px;
        border-radius: 8px;
        font-weight: 600;
    }
    
    .agent-card {
        background: white;
        padding: 16px;
        border-radius: 12px;
        margin: 8px 0;
        border-left: 4px solid #667eea;
    }
    
    .success-box {
        background: #d1fae5;
        border: 2px solid #10b981;
        padding: 16px;
        border-radius: 8px;
        margin: 12px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'current_app' not in st.session_state:
    st.session_state.current_app = None

if 'build_history' not in st.session_state:
    st.session_state.build_history = []

if 'agent_outputs' not in st.session_state:
    st.session_state.agent_outputs = {}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_anthropic_client():
    """Get Anthropic client with API key"""
    try:
        api_key = st.secrets["ANTHROPIC_API_KEY"]
    except:
        api_key = st.sidebar.text_input("Enter Anthropic API Key", type="password")
        if not api_key:
            st.warning(⚠️ Please enter your API key in the sidebar")
            st.stop()
    
    return anthropic.Anthropic(api_key=api_key)


def agent_work(client, role, goal, backstory, task, context=""):
    """Execute agent task"""
    
    prompt = f"""You are a {role}.

Your goal: {goal}
Your background: {backstory}

{f'Context from previous agents: {context[:1500]}' if context else ''}

Task: {task}

Execute this task professionally and concisely."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2500,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.content[0].text


# ============================================================================
# MAIN APP
# ============================================================================

def main():
    # Get client
    client = get_anthropic_client()
    
    # Header
    st.markdown("""
    <div style="text-align:center;padding:20px;background:white;border-radius:16px;margin-bottom:20px;">
        <h1 style="color:#667eea;margin:0;">🤖 Multi-Agent DeepAgent</h1>
        <p style="color:#666;margin:10px 0 0 0;">5 AI Agents Building Apps Together</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create two columns
    col1, col2 = st.columns([1, 1])
    
    # ===== LEFT PANEL: INPUT =====
    with col1:
        st.markdown("### 💬 Describe Your App")
        
        user_request = st.text_area(
            "What do you want to build?",
            height=150,
            placeholder="Example: Create a todo app with categories and priority levels...",
            key="user_input"
        )
        
        if st.button("🚀 Build with AI Crew", type="primary"):
            if user_request:
                with st.spinner("Building your app..."):
                    build_app_with_crew(client, user_request)
            else:
                st.warning("Please describe what you want to build")
        
        # Quick examples
        st.markdown("#### 💡 Quick Examples:")
        
        examples = [
            "Simple calculator",
            "Todo list with categories",
            "Countdown timer",
            "Note-taking app",
            "Expense tracker"
        ]
        
        for example in examples:
            if st.button(f"📌 {example}", key=f"ex_{example}"):
                st.session_state.user_input = example
                with st.spinner("Building your app..."):
                    build_app_with_crew(client, example)
                st.rerun()
    
    # ===== RIGHT PANEL: RESULTS =====
    with col2:
        st.markdown("### 📊 Build Progress & Results")
        
        if st.session_state.current_app:
            # Show tabs for different outputs
            tab1, tab2, tab3, tab4 = st.tabs(["📱 App", "📋 Requirements", "🏗️ Architecture", "🔍 QA"])
            
            with tab1:
                if st.session_state.current_app.get('code'):
                    st.markdown("#### ✨ Your App is Ready!")
                    
                    filename = st.session_state.current_app.get('filename', 'app.html')
                    code = st.session_state.current_app['code']
                    
                    # Download button
                    st.download_button(
                        label="📥 Download App",
                        data=code,
                        file_name=filename,
                        mime="text/html",
                        type="primary"
                    )
                    
                    st.success("💡 Download and open in your browser to use it!")
                    
                    # Stats
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("Lines of Code", len(code.splitlines()))
                    with col_b:
                        st.metric("Characters", len(code))
                    
                    # Code preview
                    with st.expander("👨‍💻 View Source Code"):
                        st.code(code, language="html", line_numbers=True)
            
            with tab2:
                if 'requirements' in st.session_state.agent_outputs:
                    st.markdown(st.session_state.agent_outputs['requirements'])
                else:
                    st.info("No requirements yet")
            
            with tab3:
                if 'architecture' in st.session_state.agent_outputs:
                    st.markdown(st.session_state.agent_outputs['architecture'])
                else:
                    st.info("No architecture yet")
            
            with tab4:
                if 'qa_report' in st.session_state.agent_outputs:
                    st.markdown(st.session_state.agent_outputs['qa_report'])
                else:
                    st.info("No QA report yet")
        else:
            st.info("👈 Enter your app idea on the left and click 'Build with AI Crew'")
            st.markdown("""
            **The crew will:**
            - 👔 Create requirements
            - 🏗️ Design architecture
            - 💻 Write code
            - 🔍 Review quality
            - 📦 Package for download
            """)


def build_app_with_crew(client, user_request):
    """Build app using multi-agent crew"""
    
    # Clear previous outputs
    st.session_state.agent_outputs = {}
    
    # Agent 1: Product Manager
    with st.status("👔 Product Manager - Creating Requirements", expanded=False) as status:
        requirements = agent_work(
            client,
            role="Product Manager",
            goal="Create clear, actionable requirements",
            backstory="Expert at turning ideas into specifications",
            task=f"Create concise requirements (under 800 words) for: {user_request}. Focus on key features and functionality."
        )
        st.session_state.agent_outputs['requirements'] = requirements
        status.update(label="👔 Product Manager - ✅ Complete", state="complete")
    
    # Agent 2: Architect
    with st.status("🏗️ Software Architect - Designing System", expanded=False) as status:
        architecture = agent_work(
            client,
            role="Software Architect",
            goal="Design simple, effective architecture",
            backstory="Expert in clean, maintainable design",
            task=f"Design a simple single-file HTML app (under 600 words). Focus on component structure and key technical decisions.",
            context=requirements[:1000]
        )
        st.session_state.agent_outputs['architecture'] = architecture
        status.update(label="🏗️ Software Architect - ✅ Complete", state="complete")
    
    # Agent 3: Developer
    with st.status("💻 Full-Stack Developer - Writing Code", expanded=False) as status:
        code_prompt = f"""Build a SIMPLE, COMPLETE app for: {user_request}

Keep it under 250 lines total!

Requirements summary: {requirements[:400]}

CRITICAL INSTRUCTIONS:
1. Single HTML file with embedded CSS and JavaScript
2. Use addEventListener for ALL events (NO inline onclick)
3. Wrap ALL JS in DOMContentLoaded
4. Make it FULLY FUNCTIONAL
5. Clean, modern design
6. MUST be COMPLETE with all closing tags
7. Simple but working

Return ONLY the complete HTML code. No explanations."""

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            messages=[{"role": "user", "content": code_prompt}]
        )
        
        code = response.content[0].text
        
        # Clean code
        if "```html" in code:
            code = code.split("```html")[1].split("```")[0].strip()
        elif "```" in code:
            code = code.split("```")[1].split("```")[0].strip()
        
        # Ensure completion
        if not code.strip().endswith("</html>"):
            code += "\n</body>\n</html>"
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"app_{timestamp}.html"
        
        st.session_state.agent_outputs['code'] = code
        status.update(label=f"💻 Developer - ✅ Complete ({len(code.splitlines())} lines)", state="complete")
    
    # Agent 4: QA Analyst
    with st.status("🔍 QA Analyst - Reviewing Code", expanded=False) as status:
        qa_report = agent_work(
            client,
            role="QA Analyst",
            goal="Quick quality check",
            backstory="Expert at finding issues fast",
            task=f"Quick review (under 400 words): Is the code complete and functional? Any critical issues? Code sample: {code[:800]}"
        )
        st.session_state.agent_outputs['qa_report'] = qa_report
        status.update(label="🔍 QA Analyst - ✅ Complete", state="complete")
    
    # Save to session state
    st.session_state.current_app = {
        'filename': filename,
        'code': code,
        'timestamp': timestamp
    }
    
    # Success message
    st.success("✅ **BUILD COMPLETE!** Check the 'App' tab to download.")
    st.balloons()


# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("## 👥 The Crew")
    
    agents = [
        ("👔", "Product Manager", "Creates requirements"),
        ("🏗️", "Software Architect", "Designs system"),
        ("💻", "Full-Stack Developer", "Writes code"),
        ("🔍", "QA Analyst", "Reviews quality"),
        ("📦", "Deployer", "Packages app")
    ]
    
    for icon, role, desc in agents:
        st.markdown(f"""
        <div style="background:white;padding:12px;border-radius:8px;margin:8px 0;border-left:4px solid #667eea;">
            <div style="font-weight:600;color:#1f2937;">{icon} {role}</div>
            <div style="font-size:12px;color:#6b7280;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📚 How It Works")
    st.markdown("""
    1. **Describe** your app
    2. **Watch** agents collaborate
    3. **Download** working app
    4. **Open** in browser
    
    **No coding needed!**
    """)
    
    st.markdown("---")
    
    if st.session_state.current_app:
        st.markdown("### 📊 Current Project")
        st.info(f"**File:** {st.session_state.current_app.get('filename', 'N/A')}")
        st.info(f"**Lines:** {len(st.session_state.current_app.get('code', '').splitlines())}")
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    **Version:** 1.0.0
    
    Built with Streamlit & Claude AI
    
    [GitHub](https://github.com) | [Docs](https://docs.streamlit.io)
    """)

# ============================================================================
# RUN MAIN APP
# ============================================================================

if __name__ == "__main__":