import streamlit as st
import sys
import os

# Add the parent directory to the path so we can import from core
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from core.career_counselor import CareerCounselor
    VECTOR_DB_AVAILABLE = True
except ImportError:
    VECTOR_DB_AVAILABLE = False

# Chat UI components

def display_welcome_message():
    """Displays the initial welcome message and onboarding options."""
    st.markdown("### 👋 Hey there! I’m *Brainy*, your AI Career Guide.")
    st.markdown("I’ll help you uncover paths that match your passions, skills, and dreams.")
    
    # Progress Bar (Placeholder - will need actual logic to update)
    st.progress(0, text="0/9 Steps") # Assuming 9 steps based on the flow

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes, let’s explore!", key="start_explore", use_container_width=True):
            st.session_state.conversation_flow = 'context_check'
            st.rerun() # Rerun to reflect state change immediately
    with col2:
        if st.button("Maybe later", key="maybe_later", use_container_width=True):
            st.info("No problem! Feel free to come back anytime you're ready to explore.")
            # Potentially end session or offer minimal info

def display_context_check():
    """Displays the context check question and options."""
    st.markdown("### 📝 Context & Confidence Check")
    st.markdown("Before we dive in, could you share your current stage?")
    
    # Progress Bar
    st.progress(1/9, text="1/9 Steps")

    options = ["School Student", "College Student", "Working Professional", "Career Switcher"]
    
    # Using st.columns to make buttons more visually appealing and spaced
    cols = st.columns(len(options))
    for i, option in enumerate(options):
        if cols[i].button(option, key=f"stage_{option.lower().replace(' ', '_')}", use_container_width=True):
            st.session_state.user_data['current_stage'] = option
            st.session_state.conversation_flow = 'interest_exploration'
            st.success(f"Awesome, got it! I’ll tailor questions for a {option}.")
            st.rerun()

# --- Placeholder for further steps ---

def display_interest_exploration():
    st.markdown("### 🔍 Deep-Dive Interest & Skills Exploration")
    st.markdown("Let's paint a quick picture of you. Which of these activities excite you? (Select all that apply)")
    st.progress(2/9, text="2/9 Steps")
    
    # Initialize interests in session state if not exists
    if 'selected_interests' not in st.session_state.user_data:
        st.session_state.user_data['selected_interests'] = []
    
    # Interest categories with checkboxes
    interests = {
        "🎨 Creative": "design, writing, art",
        "📊 Analytical": "math, coding, puzzles", 
        "🤝 Social": "teaching, counseling, teamwork",
        "🏃 Physical": "sports, crafting, hands-on",
        "💻 Tech": "robotics, gaming, gadgets"
    }
    
    # Display checkboxes in columns for better layout
    cols = st.columns(3)
    for i, (interest, description) in enumerate(interests.items()):
        with cols[i % 3]:
            if st.checkbox(f"{interest}\n({description})", key=f"interest_{i}"):
                if interest not in st.session_state.user_data['selected_interests']:
                    st.session_state.user_data['selected_interests'].append(interest)
            else:
                if interest in st.session_state.user_data['selected_interests']:
                    st.session_state.user_data['selected_interests'].remove(interest)
    
    # Freeform input
    st.markdown("**Anything else? Feel free to type it below:**")
    freeform_input = st.text_area("Additional interests or skills:", key="freeform_interests", height=100)
    if freeform_input:
        st.session_state.user_data['freeform_interests'] = freeform_input
    
    # Continue button
    if st.button("Continue", key="continue_interests", use_container_width=True):
        if st.session_state.user_data['selected_interests'] or freeform_input:
            st.session_state.conversation_flow = 'preference_validation'
            st.rerun()
        else:
            st.warning("Please select at least one interest or add some text to continue.")

def display_preference_validation():
    st.markdown("### 🧠 Preference Extraction & Validation")
    st.progress(3/9, text="3/9 Steps")
    
    # Get conversation history for LLM analysis
    selected_interests = st.session_state.user_data.get('selected_interests', [])
    freeform = st.session_state.user_data.get('freeform_interests', '')
    current_stage = st.session_state.user_data.get('current_stage', 'Student')
    
    # Create conversation history for LLM analysis
    conversation_history = f"""
    User Stage: {current_stage}
    Selected Interest Categories: {', '.join(selected_interests)}
    Additional Details: {freeform}
    """
    
    # Use LLM to extract and analyze preferences
    if 'llm_analysis' not in st.session_state.user_data:
        if VECTOR_DB_AVAILABLE:
            try:
                counselor = st.session_state.get('career_counselor')
                if counselor and counselor.llm_manager:
                    with st.spinner("🤔 Analyzing your preferences..."):
                        # Extract preferences using LLM
                        llm_analysis = counselor.llm_manager.extract_preferences(
                            conversation_history, 
                            analysis_type="interests"
                        )
                        st.session_state.user_data['llm_analysis'] = llm_analysis
                else:
                    # Fallback to basic analysis
                    st.session_state.user_data['llm_analysis'] = {
                        "primary_interests": selected_interests,
                        "extracted_keywords": freeform.split() if freeform else [],
                        "confidence_level": "medium"
                    }
            except Exception as e:
                st.warning(f"Advanced analysis unavailable: {e}")
                st.session_state.user_data['llm_analysis'] = {
                    "primary_interests": selected_interests,
                    "extracted_keywords": freeform.split() if freeform else [],
                    "confidence_level": "medium"
                }
        else:
            # Basic fallback
            st.session_state.user_data['llm_analysis'] = {
                "primary_interests": selected_interests,
                "extracted_keywords": freeform.split() if freeform else [],
                "confidence_level": "medium"
            }
    
    llm_analysis = st.session_state.user_data.get('llm_analysis', {})
    
    # Display intelligent analysis results
    st.markdown("**🔍 Here's what I understand about your interests:**")
    
    # Primary interests
    primary_interests = llm_analysis.get('primary_interests', [])
    if primary_interests:
        st.markdown("**🎯 Primary Interest Areas:**")
        for interest in primary_interests:
            st.markdown(f"• {interest}")
    
    # Extracted keywords
    keywords = llm_analysis.get('extracted_keywords', [])
    if keywords:
        st.markdown("**🔑 Key Themes I Noticed:**")
        keywords_text = ", ".join(keywords[:8])  # Show first 8 keywords
        st.markdown(f"*{keywords_text}*")
    
    # Personality traits (if extracted)
    traits = llm_analysis.get('personality_traits', [])
    if traits:
        st.markdown("**💫 Personality Indicators:**")
        traits_text = ", ".join(traits)
        st.markdown(f"*{traits_text}*")
    
    # Confidence level indicator
    confidence = llm_analysis.get('confidence_level', 'medium')
    confidence_emoji = {"high": "🎯", "medium": "✅", "low": "❓"}
    st.markdown(f"**Analysis Confidence:** {confidence_emoji.get(confidence, '✅')} {confidence.title()}")
    
    # Show missing information if confidence is low
    missing_info = llm_analysis.get('missing_info', [])
    if missing_info and confidence == 'low':
        st.info(f"💡 To improve recommendations, tell me more about: {', '.join(missing_info)}")
    
    st.markdown("---")
    st.markdown("**Does this analysis capture your interests well?**")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("✅ Yes, perfect!", key="confirm_analysis", use_container_width=True):
            st.session_state.conversation_flow = 'career_matching'
            st.success("Great! Let's find careers that match your profile.")
            st.rerun()
    
    with col2:
        if st.button("🔄 Need clarification", key="clarify_analysis", use_container_width=True):
            # Generate clarifying questions using LLM
            st.session_state.conversation_flow = 'fallback_engine'
            st.rerun()
    
    with col3:
        if st.button("✏️ Edit interests", key="edit_analysis", use_container_width=True):
            # Clear LLM analysis to force re-analysis
            if 'llm_analysis' in st.session_state.user_data:
                del st.session_state.user_data['llm_analysis']
            st.session_state.conversation_flow = 'interest_exploration'
            st.rerun()

def display_career_matching():
    st.markdown("### 📊 Career Matching & Discovery")
    st.markdown("**Step 4 of 9**")
    st.markdown("Here are career paths that fit your interests and skills. Tap any to learn more!")
    st.progress(4/9, text="4/9 Steps")
    
    # Get user preferences for intelligent matching
    selected_interests = st.session_state.user_data.get('selected_interests', [])
    freeform_interests = st.session_state.user_data.get('freeform_interests', '')
    llm_analysis = st.session_state.user_data.get('llm_analysis', {})
    current_stage = st.session_state.user_data.get('current_stage', 'Student')
    
    # Create search query from LLM analysis or fallback to basic interests
    if llm_analysis:
        # Use intelligent preferences from LLM analysis
        primary_interests = llm_analysis.get('primary_interests', selected_interests)
        keywords = llm_analysis.get('extracted_keywords', [])
        search_query = " ".join(primary_interests + keywords).strip()
    else:
        # Fallback to basic search
        search_query = " ".join(selected_interests) + " " + freeform_interests
        search_query = search_query.strip()
    
    careers = []
    
    if VECTOR_DB_AVAILABLE and search_query:
        try:
            # Initialize career counselor and search for relevant careers
            if 'career_counselor' not in st.session_state:
                st.session_state.career_counselor = CareerCounselor()
            
            counselor = st.session_state.career_counselor
            vector_results = counselor.search_career_data(search_query, top_k=4)
            
            # Convert vector results to career format
            for career_data in vector_results:
                careers.append({
                    "id": career_data.get("id", "unknown"),
                    "title": f"{career_data.get('emoji', '�')} {career_data.get('title', 'Unknown Career')}",
                    "tagline": career_data.get("tagline", "Explore this career path."),
                    "description": career_data.get("description", "No description available."),
                    "full_data": career_data
                })
            
            st.success(f"✨ Found {len(careers)} careers matching your interests!")
            
        except Exception as e:
            st.warning("Vector database not available. Showing sample careers.")
            careers = get_fallback_careers()
    else:
        # Fallback to sample careers if vector DB not available
        careers = get_fallback_careers()
    
    if not careers:
        st.warning("No careers found. Please try adjusting your interests.")
        return
    
    # Display career cards in a 2x2 grid
    cols = st.columns(2)
    for i, career in enumerate(careers):
        with cols[i % 2]:
            with st.container():
                st.markdown(f"### {career['title']}")
                st.markdown(f"*{career['tagline']}*")
                
                if st.button(f"Learn More", key=f"career_{career['id']}", use_container_width=True):
                    # Store the full career data if available, otherwise use basic data
                    career_to_store = career.get('full_data', career)
                    st.session_state.user_data['selected_career'] = career_to_store
                    st.session_state.conversation_flow = 'detailed_path_exploration'
                    st.rerun()
    
    st.markdown("---")
    
    # Additional options
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎲 Surprise me!", key="surprise_career", use_container_width=True):
            import random
            selected_career = random.choice(careers)
            career_to_store = selected_career.get('full_data', selected_career)
            st.session_state.user_data['selected_career'] = career_to_store
            st.session_state.conversation_flow = 'detailed_path_exploration'
            st.rerun()
    
    with col2:
        if st.button("� Refine Search", key="refine_search", use_container_width=True):
            st.session_state.conversation_flow = 'interest_exploration'
            st.rerun()

def get_fallback_careers():
    """Fallback careers when vector database is not available"""
    return [
        {
            "id": "graphic_designer",
            "title": "🎨 Graphic Designer", 
            "tagline": "Bring ideas to life visually.",
            "description": "Create visual concepts using computer software or by hand to communicate ideas that inspire, inform, and captivate consumers."
        },
        {
            "id": "data_analyst",
            "title": "📊 Data Analyst",
            "tagline": "Find stories in numbers.", 
            "description": "Collect, clean, and interpret data sets to answer questions or solve problems."
        },
        {
            "id": "sports_coach", 
            "title": "🏃 Sports Coach",
            "tagline": "Inspire and train athletes.",
            "description": "Teach athletic skills and strategies while motivating athletes to develop their abilities."
        },
        {
            "id": "ux_researcher",
            "title": "💻 UX Researcher", 
            "tagline": "Understand users to build better products.",
            "description": "Study user behaviors and motivations to inform product design decisions."
        }
    ]

def display_detailed_path_exploration():
    st.markdown("### 📖 Detailed Path Exploration")
    st.progress(5/9, text="5/9 Steps")
    
    selected_career = st.session_state.user_data.get('selected_career', {})
    
    if selected_career:
        # Display career title with emoji if available
        emoji = selected_career.get('emoji', '💼')
        title = selected_career.get('title', 'Unknown Career')
        if not title.startswith(emoji):
            title = f"{emoji} {title}"
            
        st.markdown(f"## {title}")
        st.markdown(selected_career.get('description', 'No description available.'))
        
        # Show personalized LLM explanation if available
        llm_explanation = selected_career.get('llm_explanation')
        if llm_explanation:
            st.markdown("### 🎯 Why This Career Matches You")
            st.info(llm_explanation)
            st.markdown("---")
        
        # Skills section
        skills = selected_career.get('skills', [])
        if skills:
            st.markdown("### 🛠️ Key Skills:")
            # Handle both list format and string format from ChromaDB
            if isinstance(skills, list):
                skills_text = ", ".join(skills)
            else:
                skills_text = str(skills)  # Already a comma-separated string
            st.markdown(f"**{skills_text}**")
        
        # Education section
        education = selected_career.get('education', [])
        if education:
            st.markdown("### 🎓 Typical Education:")
            # Handle both list format and string format from ChromaDB
            if isinstance(education, list):
                education_text = ", ".join(education)
            else:
                education_text = str(education)  # Already a comma-separated string
            st.markdown(f"**{education_text}**")
        
        # Salary section
        salary_range = selected_career.get('salary_range', 'Varies by location and experience')
        st.markdown("### 💰 Expected Salary Range:")
        st.markdown(f"**{salary_range}** annually")
        
        # Job outlook
        job_outlook = selected_career.get('job_outlook', 'Stable')
        st.markdown("### 📈 Job Outlook:")
        st.markdown(f"**{job_outlook}**")
        
        # Companies section
        companies = selected_career.get('companies', [])
        if companies:
            st.markdown("### 🏢 Where You Could Work:")
            # Handle both list format and string format from ChromaDB
            if isinstance(companies, list):
                companies_text = ", ".join(companies[:5])  # Show first 5 companies
            else:
                # Already a string, just limit length if too long
                companies_str = str(companies)
                companies_list = companies_str.split(', ')
                companies_text = ", ".join(companies_list[:5])
            st.markdown(f"**{companies_text}**")
        
        # Career path progression
        career_paths = selected_career.get('career_paths', [])
        if career_paths:
            st.markdown("### 🚀 Career Progression:")
            # Handle both list format and string format from ChromaDB
            if isinstance(career_paths, list):
                paths_list = career_paths
            else:
                paths_list = str(career_paths).split(', ')
            
            for i, path in enumerate(paths_list):
                st.markdown(f"{i+1}. **{path}**")
        
        # Personality match
        personality_match = selected_career.get('personality_match', [])
        if personality_match:
            st.markdown("### 🎯 Perfect for people who are:")
            # Handle both list format and string format from ChromaDB
            if isinstance(personality_match, list):
                personality_text = ", ".join(personality_match)
            else:
                personality_text = str(personality_match)  # Already a comma-separated string
            st.markdown(f"**{personality_text}**")
        
        st.markdown("---")
        st.markdown("**Ready to take the next step?**")
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🚀 How to start?", key="how_to_start", use_container_width=True):
                st.session_state.conversation_flow = 'final_recommendation'
                st.rerun()
        
        with col2:
            if st.button("🔗 See related roles", key="related_roles", use_container_width=True):
                # Show related careers based on industry or skills
                if VECTOR_DB_AVAILABLE:
                    try:
                        counselor = st.session_state.get('career_counselor')
                        if counselor:
                            industry = selected_career.get('industry', '')
                            related_results = counselor.search_career_data(industry, top_k=3)
                            st.markdown("### 🔗 Related Careers:")
                            for career in related_results:
                                if career.get('id') != selected_career.get('id'):
                                    st.markdown(f"- **{career.get('title', 'Unknown')}**: {career.get('tagline', 'No description')}")
                    except:
                        st.info("Related roles feature coming soon!")
                else:
                    st.info("Related roles feature coming soon!")
        
        with col3:
            if st.button("⬅️ Back to list", key="back_to_careers", use_container_width=True):
                st.session_state.conversation_flow = 'career_matching'
                st.rerun()
    else:
        st.error("No career selected. Returning to career matching.")
        st.session_state.conversation_flow = 'career_matching'
        st.rerun()

def display_fallback_engine():
    st.markdown("### 🔄 Fallback & Clarification Engine")
    st.progress(6/9, text="6/9 Steps")
    
    st.markdown("I'd like to understand your preferences better! Let me ask a few targeted questions.")
    
    # Get previous conversation context
    selected_interests = st.session_state.user_data.get('selected_interests', [])
    freeform = st.session_state.user_data.get('freeform_interests', '')
    llm_analysis = st.session_state.user_data.get('llm_analysis', {})
    
    # Generate clarifying questions using LLM if available
    clarifying_questions = []
    
    if VECTOR_DB_AVAILABLE:
        try:
            counselor = st.session_state.get('career_counselor')
            if counselor and counselor.llm_manager:
                # Get missing information from LLM analysis
                missing_info = llm_analysis.get('missing_info', ['interests', 'skills', 'values'])
                user_context = f"Selected: {', '.join(selected_interests)}, Additional: {freeform}"
                
                with st.spinner("🤔 Generating personalized questions..."):
                    question_response = counselor.llm_manager.generate_clarifying_questions(
                        user_context, missing_info, "interest_exploration"
                    )
                    
                    if 'error' not in question_response:
                        clarifying_questions = question_response.get('clarifying_questions', [])
        except Exception as e:
            st.warning(f"Smart question generation unavailable: {e}")
    
    # Fallback questions if LLM not available
    if not clarifying_questions:
        clarifying_questions = [
            "🎯 What activities make you lose track of time?",
            "💡 What subjects or topics naturally interest you?",
            "🤝 Do you prefer working with people, data, or hands-on projects?",
            "🏆 What kind of impact do you want your work to have?"
        ]
    
    # Display clarifying questions as interactive buttons
    st.markdown("**Choose the question that interests you most:**")
    
    for i, question in enumerate(clarifying_questions[:4]):  # Show max 4 questions
        if st.button(question, key=f"clarify_{i}", use_container_width=True):
            # Store the selected question for follow-up
            st.session_state.user_data['selected_clarification'] = question
            
            # Show text input for the answer
            st.markdown(f"**{question}**")
            answer = st.text_area("Your answer:", key="clarification_answer", height=100)
            
            if st.button("Continue with this answer", key="submit_clarification"):
                if answer:
                    # Add the answer to user data
                    if 'clarification_responses' not in st.session_state.user_data:
                        st.session_state.user_data['clarification_responses'] = []
                    
                    st.session_state.user_data['clarification_responses'].append({
                        "question": question,
                        "answer": answer
                    })
                    
                    # Re-analyze with new information
                    if 'llm_analysis' in st.session_state.user_data:
                        del st.session_state.user_data['llm_analysis']
                    
                    st.success("Great answer! Let me re-analyze your preferences.")
                    st.session_state.conversation_flow = 'preference_validation'
                    st.rerun()
                else:
                    st.warning("Please provide an answer to continue.")
            break
    
    # Option to skip clarification
    st.markdown("---")
    if st.button("💫 Skip questions - show me anything interesting!", key="skip_clarification", use_container_width=True):
        # Set some default interests and proceed
        st.session_state.user_data['selected_interests'] = ["🎨 Creative", "💻 Tech"]
        st.session_state.conversation_flow = 'career_matching'
        st.rerun()

def display_final_recommendation():
    st.markdown("### 🚀 Final Recommendation & Next Steps")
    st.progress(7/9, text="7/9 Steps")
    
    selected_career = st.session_state.user_data.get('selected_career', {})
    
    if selected_career:
        st.markdown("## 🎉 All set!")
        st.markdown(f"Based on what you've shared, my top pick is **{selected_career['title']}** because it matches your interests and personality! 🙌")
        
        # Next steps based on career
        st.markdown("### 🛤️ Your Next Steps:")
        
        if selected_career['id'] == 'data_analyst':
            steps = [
                "📚 Learn Python programming basics (try Codecademy or freeCodeCamp)",
                "📊 Practice with Excel and Google Sheets", 
                "🔍 Take an online statistics course",
                "💼 Build a portfolio with sample data projects"
            ]
        elif selected_career['id'] == 'graphic_designer':
            steps = [
                "🎨 Learn Adobe Creative Suite or Figma",
                "📐 Study design principles and color theory",
                "🖼️ Create a portfolio of design projects", 
                "👥 Join design communities online"
            ]
        elif selected_career['id'] == 'sports_coach':
            steps = [
                "🏃 Get certified in your sport of choice",
                "📖 Study sports psychology and training methods",
                "👨‍🏫 Volunteer as an assistant coach",
                "🤝 Network with other coaches and athletes"
            ]
        else:  # UX Researcher
            steps = [
                "🔬 Learn user research methodologies",
                "🛠️ Get familiar with tools like Figma and Miro",
                "📊 Practice conducting user interviews",
                "📚 Read books on UX design and psychology"
            ]
        
        for i, step in enumerate(steps, 1):
            st.markdown(f"{i}. {step}")
        
        st.markdown("---")
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📚 Get Learning Resources", key="learning_resources", use_container_width=True):
                st.session_state.conversation_flow = 'feedback'
                st.success("Learning resources will be provided!")
                st.rerun()
        
        with col2:
            if st.button("🎤 Schedule Mock Interview", key="mock_interview", use_container_width=True):
                st.info("Mock interview scheduling feature coming soon!")
        
        with col3:
            if st.button("🔄 Restart Exploration", key="restart", use_container_width=True):
                # Clear session state
                st.session_state.user_data = {}
                st.session_state.conversation_flow = 'onboarding'
                st.rerun()
    else:
        st.error("No career recommendation available. Let's start over.")
        st.session_state.conversation_flow = 'onboarding'
        st.rerun()

def display_feedback():
    st.markdown("### 🌟 Feedback & Follow-up")
    st.progress(8/9, text="8/9 Steps")
    
    st.markdown("**How helpful was this session?**")
    
    # Star rating using columns
    rating_cols = st.columns(5)
    rating = 0
    
    for i in range(5, 0, -1):
        with rating_cols[5-i]:
            if st.button("⭐" * i, key=f"rating_{i}", use_container_width=True):
                rating = i
                st.session_state.user_data['session_rating'] = rating
                st.success(f"Thank you for rating us {i} star{'s' if i > 1 else ''}!")
    
    # Email capture
    st.markdown("---")
    st.markdown("**Would you like me to send these recommendations to your email?**")
    
    email = st.text_input("Enter your email address (optional):", key="user_email")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📧 Yes, send me an email", key="send_email", use_container_width=True):
            if email:
                st.session_state.user_data['email'] = email
                st.success(f"Great! We'll send your personalized career report to {email}")
                st.balloons()
                st.markdown("### 🎉 Session Complete!")
                st.markdown("Thank you for using Brainy! Your career journey starts now. 🚀")
                st.progress(9/9, text="9/9 Steps Complete!")
            else:
                st.warning("Please enter a valid email address.")
    
    with col2:
        if st.button("❌ No, thanks", key="no_email", use_container_width=True):
            st.success("No problem! You can always come back for more career guidance.")
            st.balloons()
            st.markdown("### 🎉 Session Complete!")
            st.markdown("Thank you for using Brainy! Your career journey starts now. 🚀")
            st.progress(9/9, text="9/9 Steps Complete!")
    
    # Restart option
    st.markdown("---")
    if st.button("🔄 Start New Session", key="new_session", use_container_width=True):
        st.session_state.user_data = {}
        st.session_state.conversation_flow = 'onboarding'
        st.rerun()

# This function will be called from app.py to render the correct UI
def render_chat_interface():
    flow_stage = st.session_state.get('conversation_flow', 'onboarding')

    if flow_stage == 'onboarding':
        display_welcome_message()
    elif flow_stage == 'context_check':
        display_context_check()
    elif flow_stage == 'interest_exploration':
        display_interest_exploration()
    elif flow_stage == 'preference_validation':
        display_preference_validation()
    elif flow_stage == 'career_matching':
        display_career_matching()
    elif flow_stage == 'detailed_path_exploration':
        display_detailed_path_exploration()
    elif flow_stage == 'fallback_engine': # This might be triggered differently
        display_fallback_engine()
    elif flow_stage == 'final_recommendation':
        display_final_recommendation()
    elif flow_stage == 'feedback':
        display_feedback()
    else:
        st.error("Unknown conversation flow stage.")
        display_welcome_message() # Default to welcome
