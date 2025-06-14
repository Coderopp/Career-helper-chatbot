# LLM Manager for handling multiple AI providers (Groq + Mixtral integration)
import os
import json
from typing import Dict, Any, Optional, List
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class LLMManager:
    """
    Manages multiple LLM providers for different tasks.
    - Groq: Fast responses, real-time chat
    - Mixtral: Complex reasoning, preference analysis
    """
    
    def __init__(self):
        self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        # Available models
        self.models = {
            "groq_fast": "mixtral-8x7b-32768",  # Fast Groq model
            "groq_detailed": "llama3-70b-8192",  # More detailed Groq model
            "mixtral": "mixtral-8x7b-32768"  # Using Groq's Mixtral for now
        }
        
    def load_prompt_template(self, prompt_path: str) -> str:
        """Load a prompt template from the prompts directory"""
        try:
            with open(prompt_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except FileNotFoundError:
            print(f"Warning: Prompt template not found at {prompt_path}")
            return ""
    
    def extract_preferences(self, conversation_history: str, analysis_type: str = "interests") -> Dict[str, Any]:
        """
        Extract user preferences from conversation using specialized prompts.
        
        Args:
            conversation_history: Full conversation text
            analysis_type: "interests", "skills", or "values"
        """
        
        prompt_files = {
            "interests": "prompts/preference_extraction/interest_extraction.txt",
            "skills": "prompts/preference_extraction/skill_assessment.txt", 
            "values": "prompts/preference_extraction/values_identification.txt"
        }
        
        prompt_template = self.load_prompt_template(prompt_files[analysis_type])
        if not prompt_template:
            return {"error": f"Could not load {analysis_type} extraction prompt"}
        
        # Format the prompt with conversation history
        formatted_prompt = prompt_template.format(conversation_history=conversation_history)
        
        try:
            response = self.groq_client.chat.completions.create(
                model=self.models["groq_detailed"],
                messages=[
                    {"role": "system", "content": "You are an expert career counselor. Always respond with valid JSON."},
                    {"role": "user", "content": formatted_prompt}
                ],
                temperature=0.3,
                max_tokens=1500
            )
            
            result = response.choices[0].message.content
            
            # Try to parse as JSON
            try:
                return json.loads(result)
            except json.JSONDecodeError:
                # If JSON parsing fails, return the raw text
                return {"raw_analysis": result, "parsing_error": True}
                
        except Exception as e:
            return {"error": f"LLM request failed: {str(e)}"}
    
    def map_to_career_categories(self, user_preferences: Dict[str, Any], category: str = "general") -> Dict[str, Any]:
        """
        Map user preferences to specific career categories.
        
        Args:
            user_preferences: Extracted preferences from previous analysis
            category: "stem", "arts", "sports", or "general"
        """
        
        prompt_files = {
            "stem": "prompts/career_mapping/stem_careers.txt",
            "arts": "prompts/career_mapping/arts_careers.txt",
            "sports": "prompts/career_mapping/sports_careers.txt",
            "general": "prompts/career_mapping/general_mapping.txt"
        }
        
        if category in prompt_files:
            prompt_template = self.load_prompt_template(prompt_files[category])
        else:
            # Use general mapping approach
            prompt_template = self.load_prompt_template(prompt_files["general"])
        
        if not prompt_template:
            return {"error": f"Could not load {category} career mapping prompt"}
        
        # Format preferences as string for the prompt
        preferences_str = json.dumps(user_preferences, indent=2)
        formatted_prompt = prompt_template.format(user_preferences=preferences_str)
        
        try:
            response = self.groq_client.chat.completions.create(
                model=self.models["mixtral"],  # Use Mixtral for complex reasoning
                messages=[
                    {"role": "system", "content": "You are a career mapping specialist. Always respond with valid JSON."},
                    {"role": "user", "content": formatted_prompt}
                ],
                temperature=0.4,
                max_tokens=2000
            )
            
            result = response.choices[0].message.content
            
            try:
                return json.loads(result)
            except json.JSONDecodeError:
                return {"raw_analysis": result, "parsing_error": True}
                
        except Exception as e:
            return {"error": f"Career mapping failed: {str(e)}"}
    
    def generate_career_explanation(self, career_name: str, user_profile: Dict[str, Any], 
                                   match_score: float, user_stage: str = "Student") -> str:
        """
        Generate a personalized explanation for why a career matches the user.
        """
        
        prompt_template = self.load_prompt_template("prompts/explanation_generation/career_explanation.txt")
        if not prompt_template:
            return f"This career matches your interests and skills based on our analysis."
        
        # Format the prompt with career details
        formatted_prompt = prompt_template.format(
            career_name=career_name,
            user_profile=json.dumps(user_profile, indent=2),
            match_score=match_score,
            user_stage=user_stage
        )
        
        try:
            response = self.groq_client.chat.completions.create(
                model=self.models["groq_fast"],  # Use fast model for explanations
                messages=[
                    {"role": "system", "content": "You are an encouraging career counselor. Write in a conversational, supportive tone."},
                    {"role": "user", "content": formatted_prompt}
                ],
                temperature=0.6,
                max_tokens=800
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"I believe {career_name} would be a great fit for you based on your interests and skills!"
    
    def generate_clarifying_questions(self, user_response: str, missing_info: List[str], 
                                     conversation_stage: str = "interest_exploration") -> Dict[str, Any]:
        """
        Generate clarifying questions when user preferences are unclear.
        """
        
        prompt_template = self.load_prompt_template("prompts/fallback/clarifying_questions.txt")
        if not prompt_template:
            return {
                "clarifying_questions": [
                    "What activities do you enjoy most in your free time?",
                    "What subjects or topics naturally interest you?",
                    "Do you prefer working with people, data, or hands-on projects?"
                ],
                "question_type": "general_exploration"
            }
        
        # Format the prompt
        formatted_prompt = prompt_template.format(
            user_context=user_response,
            missing_info=", ".join(missing_info),
            conversation_stage=conversation_stage
        )
        
        try:
            response = self.groq_client.chat.completions.create(
                model=self.models["groq_fast"],
                messages=[
                    {"role": "system", "content": "You are a helpful career counselor. Always respond with valid JSON."},
                    {"role": "user", "content": formatted_prompt}
                ],
                temperature=0.5,
                max_tokens=800
            )
            
            result = response.choices[0].message.content
            
            try:
                return json.loads(result)
            except json.JSONDecodeError:
                return {
                    "clarifying_questions": [
                        "Could you tell me more about what interests you?",
                        "What kind of work environment appeals to you?",
                        "What are your strongest skills or talents?"
                    ],
                    "question_type": "fallback"
                }
                
        except Exception as e:
            return {
                "clarifying_questions": [
                    "What activities make you feel most engaged and energized?",
                    "If you could solve any problem in the world, what would it be?",
                    "What does your ideal workday look like?"
                ],
                "question_type": "fallback",
                "error": str(e)
            }
    
    def chat_response(self, user_input: str, conversation_context: str = "", 
                     system_prompt: str = "") -> str:
        """
        Generate a conversational response for general chat interactions.
        """
        
        if not system_prompt:
            system_prompt = """You are Brainy, a friendly and encouraging AI career counselor. 
            Help users explore career options in a conversational, supportive way. 
            Ask thoughtful questions and provide helpful guidance."""
        
        try:
            messages = [{"role": "system", "content": system_prompt}]
            
            if conversation_context:
                messages.append({"role": "assistant", "content": f"Context: {conversation_context}"})
            
            messages.append({"role": "user", "content": user_input})
            
            response = self.groq_client.chat.completions.create(
                model=self.models["groq_fast"],
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return "I'm here to help you explore career options! Could you tell me a bit about your interests?"
