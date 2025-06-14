# Career Discovery Chatbot - API Reference

## Overview
This document provides comprehensive API reference for the Career Discovery Chatbot system, including internal APIs, external integrations, and data schemas.

## Table of Contents
1. [Internal APIs](#internal-apis)
2. [External API Integrations](#external-api-integrations)
3. [Data Schemas](#data-schemas)
4. [Authentication](#authentication)
5. [Error Handling](#error-handling)
6. [Rate Limiting](#rate-limiting)
7. [SDK Examples](#sdk-examples)

---

## Internal APIs

### Career Search API

#### Search Careers by Query
**Endpoint**: `POST /api/v1/careers/search`
**Description**: Search for careers using natural language query

**Request Body**:
```json
{
    "query": "software development python programming",
    "top_k": 5,
    "filters": {
        "industry": ["Technology", "Healthcare"],
        "salary_min": 70000,
        "salary_max": 150000,
        "education_level": ["Bachelor's", "Master's"],
        "experience_level": ["Entry", "Mid", "Senior"]
    },
    "user_preferences": {
        "interests": ["technology", "problem-solving"],
        "skills": ["python", "data-analysis"],
        "values": ["work-life-balance", "growth"]
    }
}
```

**Response**:
```json
{
    "status": "success",
    "results": [
        {
            "career_id": "backend_developer",
            "title": "Backend Developer",
            "match_score": 0.87,
            "industry": "Technology",
            "description": "Build server-side applications...",
            "skills": ["Python", "Java", "Node.js"],
            "salary_range": "$70,000 - $140,000",
            "education": ["Computer Science", "Software Engineering"],
            "companies": ["Amazon", "Google", "Microsoft"],
            "explanation": "This career matches your interest in technology and Python programming skills...",
            "confidence": "high"
        }
    ],
    "total_found": 15,
    "search_time_ms": 234,
    "fallback_used": false
}
```

**Error Response**:
```json
{
    "status": "error",
    "error_code": "SEARCH_FAILED",
    "message": "Unable to process search query",
    "details": {
        "reason": "Invalid query format",
        "suggestion": "Please provide a more specific query"
    }
}
```

#### Get Career Details
**Endpoint**: `GET /api/v1/careers/{career_id}`
**Description**: Retrieve detailed information for a specific career

**Path Parameters**:
- `career_id` (string): Unique identifier for the career

**Query Parameters**:
- `include_explanation` (boolean): Include personalized explanation
- `user_context` (string): Base64 encoded user preferences for personalization

**Response**:
```json
{
    "status": "success",
    "career": {
        "id": "frontend_developer",
        "title": "Frontend Developer",
        "description": "Create user-facing web applications...",
        "industry": "Technology",
        "skills": {
            "required": ["JavaScript", "HTML", "CSS"],
            "preferred": ["React", "Vue.js", "TypeScript"],
            "emerging": ["WebAssembly", "Progressive Web Apps"]
        },
        "education": {
            "minimum": "High School",
            "typical": "Bachelor's in Computer Science",
            "alternatives": ["Bootcamp", "Self-taught", "Associate's"]
        },
        "salary": {
            "range": "$65,000 - $130,000",
            "factors": ["location", "experience", "company_size"],
            "by_experience": {
                "entry": "$65,000 - $85,000",
                "mid": "$85,000 - $110,000",
                "senior": "$110,000 - $130,000+"
            }
        },
        "job_outlook": {
            "growth_rate": "8% (faster than average)",
            "demand": "Very High",
            "automation_risk": "Low"
        },
        "work_environment": {
            "typical_setting": "Office or Remote",
            "team_size": "5-15 people",
            "collaboration_level": "High",
            "travel_required": "Minimal"
        },
        "career_paths": [
            "Junior Frontend Developer",
            "Frontend Developer",
            "Senior Frontend Developer",
            "Frontend Tech Lead",
            "Frontend Architect"
        ],
        "related_careers": ["Backend Developer", "Full Stack Developer", "UI/UX Designer"],
        "personality_match": ["Creative", "Detail-oriented", "Problem-solver"],
        "companies": ["Meta", "Netflix", "Shopify", "Stripe", "Atlassian"]
    },
    "personalized_explanation": "Based on your interest in creative technology work..."
}
```

### Preference Extraction API

#### Extract User Preferences
**Endpoint**: `POST /api/v1/preferences/extract`
**Description**: Use LLM to extract structured preferences from conversation

**Request Body**:
```json
{
    "conversation_history": [
        {
            "speaker": "user",
            "message": "I love coding and solving complex problems...",
            "timestamp": "2025-06-15T10:30:00Z"
        }
    ],
    "user_context": {
        "current_stage": "College Student",
        "major": "Computer Science",
        "year": "Junior"
    },
    "extraction_focus": ["interests", "skills", "values", "personality"]
}
```

**Response**:
```json
{
    "status": "success",
    "preferences": {
        "interests": {
            "primary": ["technology", "problem-solving", "innovation"],
            "secondary": ["teamwork", "continuous-learning"],
            "weights": {
                "technology": 0.9,
                "problem-solving": 0.8,
                "innovation": 0.7
            }
        },
        "skills": {
            "technical": ["programming", "data-analysis", "system-design"],
            "soft": ["communication", "critical-thinking", "adaptability"],
            "confidence_levels": {
                "programming": "high",
                "data-analysis": "medium",
                "system-design": "low"
            }
        },
        "values": {
            "work": ["growth", "impact", "autonomy"],
            "life": ["work-life-balance", "financial-security"],
            "priorities": {
                "growth": 1,
                "impact": 2,
                "work-life-balance": 3
            }
        },
        "personality": {
            "traits": ["analytical", "creative", "collaborative"],
            "work_style": "independent-with-collaboration",
            "decision_making": "data-driven"
        }
    },
    "confidence": {
        "overall": "high",
        "by_category": {
            "interests": "high",
            "skills": "medium",
            "values": "high",
            "personality": "medium"
        }
    },
    "missing_info": [],
    "processing_time_ms": 1250
}
```

### Career Mapping API

#### Map Preferences to Careers
**Endpoint**: `POST /api/v1/mapping/preferences-to-careers`
**Description**: Map user preferences to specific career recommendations using LLM

**Request Body**:
```json
{
    "preferences": {
        "interests": ["technology", "healthcare"],
        "skills": ["programming", "data-analysis"],
        "values": ["impact", "growth"]
    },
    "user_context": {
        "stage": "Career Switcher",
        "experience": "5 years in marketing"
    },
    "mapping_strategy": "hybrid",
    "domain_focus": ["stem", "healthcare"],
    "top_k": 10
}
```

**Response**:
```json
{
    "status": "success",
    "recommendations": [
        {
            "career_id": "health_data_analyst",
            "title": "Health Data Analyst",
            "match_score": 0.92,
            "reasoning": "Combines your technical skills with healthcare impact...",
            "domain": "healthcare-tech",
            "transition_feasibility": "high",
            "skill_gaps": ["healthcare-domain-knowledge", "statistical-analysis"],
            "timeline_estimate": "6-12 months"
        }
    ],
    "mapping_strategy_used": "llm_with_vector_fallback",
    "domain_analysis": {
        "best_fit_domains": ["healthcare-tech", "ed-tech", "fin-tech"],
        "domain_scores": {
            "healthcare-tech": 0.89,
            "ed-tech": 0.76,
            "fin-tech": 0.71
        }
    }
}
```

### Report Generation API

#### Generate Career Report
**Endpoint**: `POST /api/v1/reports/generate`
**Description**: Generate comprehensive PDF career report

**Request Body**:
```json
{
    "user_profile": {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "stage": "College Student"
    },
    "session_data": {
        "preferences": { /* extracted preferences */ },
        "recommendations": [ /* career recommendations */ ],
        "explored_careers": ["frontend_developer", "backend_developer"]
    },
    "report_options": {
        "include_action_plan": true,
        "include_learning_resources": true,
        "include_salary_analysis": true,
        "format": "pdf"
    }
}
```

**Response**:
```json
{
    "status": "success",
    "report": {
        "report_id": "rpt_abc123",
        "download_url": "https://api.career-chatbot.com/reports/rpt_abc123/download",
        "expires_at": "2025-06-22T10:30:00Z",
        "pages": 12,
        "sections": [
            "executive_summary",
            "career_recommendations", 
            "skills_analysis",
            "action_plan",
            "resources"
        ]
    },
    "generation_time_ms": 3420
}
```

---

## External API Integrations

### Groq API Integration

#### Configuration
```python
GROQ_CONFIG = {
    "api_key": "gsk_...",
    "base_url": "https://api.groq.com/openai/v1",
    "model": "mixtral-8x7b-32768",
    "timeout": 30,
    "max_retries": 3
}
```

#### Chat Completion Request
```python
async def call_groq_api(messages, **kwargs):
    response = await groq_client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=messages,
        temperature=0.7,
        max_tokens=1000,
        top_p=0.9,
        **kwargs
    )
    return response.choices[0].message.content
```

#### Rate Limiting & Error Handling
```python
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
async def robust_groq_call(messages):
    try:
        return await call_groq_api(messages)
    except RateLimitError:
        logger.warning("Rate limit hit, retrying...")
        raise
    except APIError as e:
        logger.error(f"Groq API error: {e}")
        raise
```

### Sentence Transformers Integration

#### Model Configuration
```python
EMBEDDING_CONFIG = {
    "model_name": "all-MiniLM-L6-v2",
    "dimension": 384,
    "max_seq_length": 512,
    "normalize_embeddings": True,
    "device": "cpu"  # or "cuda" if available
}
```

#### Embedding Generation
```python
def generate_embeddings(texts: List[str]) -> np.ndarray:
    # Batch processing for efficiency
    batch_size = 32
    embeddings = []
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        batch_embeddings = model.encode(
            batch,
            normalize_embeddings=True,
            show_progress_bar=False
        )
        embeddings.extend(batch_embeddings)
    
    return np.array(embeddings)
```

### ChromaDB Integration

#### Client Configuration
```python
CHROMA_CONFIG = {
    "path": "./chroma_db",
    "collection_name": "career-discovery-collection",
    "distance_metric": "cosine",
    "settings": {
        "anonymized_telemetry": False,
        "allow_reset": True
    }
}
```

#### Collection Operations
```python
class ChromaDBClient:
    def search_similar(self, query_embedding, top_k=5, filters=None):
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=filters,
            include=['metadatas', 'documents', 'distances']
        )
        return results
    
    def add_documents(self, documents, metadatas, ids):
        # Batch insert for large datasets
        batch_size = 100
        for i in range(0, len(documents), batch_size):
            batch_docs = documents[i:i + batch_size]
            batch_meta = metadatas[i:i + batch_size]
            batch_ids = ids[i:i + batch_size]
            
            self.collection.add(
                documents=batch_docs,
                metadatas=batch_meta,
                ids=batch_ids
            )
```

---

## Data Schemas

### Career Schema
```typescript
interface Career {
    id: string;
    title: string;
    description: string;
    industry: string;
    skills: {
        required: string[];
        preferred: string[];
        emerging?: string[];
    };
    education: {
        minimum: string;
        typical: string;
        alternatives: string[];
    };
    salary: {
        range: string;
        factors: string[];
        by_experience: {
            entry: string;
            mid: string;
            senior: string;
        };
    };
    job_outlook: {
        growth_rate: string;
        demand: "Low" | "Medium" | "High" | "Very High";
        automation_risk: "Low" | "Medium" | "High";
    };
    work_environment: {
        typical_setting: string;
        team_size: string;
        collaboration_level: "Low" | "Medium" | "High";
        travel_required: "None" | "Minimal" | "Moderate" | "Extensive";
    };
    career_paths: string[];
    related_careers: string[];
    personality_match: string[];
    companies: string[];
    tagline: string;
    emoji: string;
}
```

### User Preferences Schema
```typescript
interface UserPreferences {
    interests: {
        primary: string[];
        secondary: string[];
        weights: Record<string, number>;
    };
    skills: {
        technical: string[];
        soft: string[];
        confidence_levels: Record<string, "low" | "medium" | "high">;
    };
    values: {
        work: string[];
        life: string[];
        priorities: Record<string, number>;
    };
    personality: {
        traits: string[];
        work_style: string;
        decision_making: string;
    };
}
```

### Session State Schema
```typescript
interface SessionState {
    session_id: string;
    user_id?: string;
    created_at: string;
    updated_at: string;
    stage: ConversationStage;
    progress: {
        current_step: number;
        total_steps: number;
        completed_stages: ConversationStage[];
    };
    user_data: {
        current_stage: UserStage;
        selected_interests: string[];
        freeform_interests: string;
        preferences?: UserPreferences;
        recommendations?: CareerRecommendation[];
        explored_careers: string[];
    };
    conversation_history: ConversationMessage[];
    metadata: {
        ip_address?: string;
        user_agent?: string;
        referrer?: string;
        utm_source?: string;
    };
}
```

### API Response Schema
```typescript
interface APIResponse<T> {
    status: "success" | "error";
    data?: T;
    error?: {
        code: string;
        message: string;
        details?: Record<string, any>;
    };
    metadata: {
        request_id: string;
        timestamp: string;
        processing_time_ms: number;
        version: string;
    };
}
```

---

## Authentication

### API Key Authentication
```http
GET /api/v1/careers/search
Authorization: Bearer <api_key>
Content-Type: application/json
```

### Session-based Authentication
```http
POST /api/v1/session/create
Content-Type: application/json

{
    "user_agent": "Career-Chatbot-Client/1.0",
    "client_info": {
        "version": "1.0.0",
        "platform": "web"
    }
}
```

Response:
```json
{
    "session_token": "sess_abc123",
    "expires_at": "2025-06-15T18:30:00Z",
    "rate_limits": {
        "requests_per_minute": 60,
        "requests_per_hour": 1000
    }
}
```

---

## Error Handling

### Standard Error Codes
```typescript
enum ErrorCode {
    // Client Errors (400-499)
    INVALID_REQUEST = "INVALID_REQUEST",
    MISSING_PARAMETERS = "MISSING_PARAMETERS", 
    INVALID_CAREER_ID = "INVALID_CAREER_ID",
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED",
    UNAUTHORIZED = "UNAUTHORIZED",
    
    // Server Errors (500-599)
    INTERNAL_ERROR = "INTERNAL_ERROR",
    LLM_SERVICE_ERROR = "LLM_SERVICE_ERROR",
    DATABASE_ERROR = "DATABASE_ERROR",
    EMBEDDING_SERVICE_ERROR = "EMBEDDING_SERVICE_ERROR",
    
    // Service Specific
    SEARCH_TIMEOUT = "SEARCH_TIMEOUT",
    NO_RESULTS_FOUND = "NO_RESULTS_FOUND",
    PREFERENCE_EXTRACTION_FAILED = "PREFERENCE_EXTRACTION_FAILED"
}
```

### Error Response Format
```json
{
    "status": "error",
    "error": {
        "code": "LLM_SERVICE_ERROR",
        "message": "Failed to process preference extraction",
        "details": {
            "service": "groq",
            "model": "mixtral-8x7b-32768",
            "reason": "rate_limit_exceeded",
            "retry_after": 60
        }
    },
    "metadata": {
        "request_id": "req_xyz789",
        "timestamp": "2025-06-15T10:30:00Z",
        "processing_time_ms": 5000,
        "version": "1.0.0"
    }
}
```

---

## Rate Limiting

### Rate Limit Headers
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1623456789
X-RateLimit-Window: 3600
```

### Rate Limit Tiers
```typescript
interface RateLimitTier {
    name: string;
    requests_per_minute: number;
    requests_per_hour: number;
    requests_per_day: number;
    burst_allowance: number;
}

const RATE_LIMITS: Record<string, RateLimitTier> = {
    free: {
        name: "Free Tier",
        requests_per_minute: 10,
        requests_per_hour: 100,
        requests_per_day: 1000,
        burst_allowance: 20
    },
    pro: {
        name: "Pro Tier", 
        requests_per_minute: 60,
        requests_per_hour: 1000,
        requests_per_day: 10000,
        burst_allowance: 100
    }
};
```

---

## SDK Examples

### Python SDK
```python
from career_chatbot import CareerChatbotClient

# Initialize client
client = CareerChatbotClient(
    api_key="your_api_key",
    base_url="https://api.career-chatbot.com/v1"
)

# Search for careers
results = client.search_careers(
    query="software development python",
    filters={
        "industry": ["Technology"],
        "salary_min": 70000
    }
)

# Extract preferences
preferences = client.extract_preferences(
    conversation="I love coding and solving problems...",
    user_context={"stage": "College Student"}
)

# Get career details
career = client.get_career("frontend_developer")

# Generate report
report = client.generate_report(
    preferences=preferences,
    recommendations=results.careers[:3]
)
```

### JavaScript SDK
```javascript
import { CareerChatbotClient } from '@career-chatbot/sdk';

const client = new CareerChatbotClient({
    apiKey: 'your_api_key',
    baseURL: 'https://api.career-chatbot.com/v1'
});

// Search careers
const searchResults = await client.searchCareers({
    query: 'software development python',
    topK: 5,
    filters: {
        industry: ['Technology'],
        salaryMin: 70000
    }
});

// Extract preferences  
const preferences = await client.extractPreferences({
    conversation: 'I love coding and solving problems...',
    userContext: { stage: 'College Student' }
});

// Map preferences to careers
const recommendations = await client.mapPreferencesToCareers({
    preferences: preferences.data,
    strategy: 'hybrid',
    topK: 10
});
```

### cURL Examples

#### Search Careers
```bash
curl -X POST "https://api.career-chatbot.com/v1/careers/search" \
  -H "Authorization: Bearer your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "software development python",
    "top_k": 5,
    "filters": {
      "industry": ["Technology"],
      "salary_min": 70000
    }
  }'
```

#### Extract Preferences
```bash
curl -X POST "https://api.career-chatbot.com/v1/preferences/extract" \
  -H "Authorization: Bearer your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_history": [
      {
        "speaker": "user",
        "message": "I love coding and solving complex problems"
      }
    ],
    "user_context": {
      "current_stage": "College Student"
    }
  }'
```

---

## API Versioning

### Version Strategy
- **Current Version**: v1
- **Versioning Scheme**: Semantic versioning (MAJOR.MINOR.PATCH)
- **Deprecation Policy**: 12 months notice for breaking changes
- **Backward Compatibility**: Maintained for at least 2 major versions

### Version Headers
```http
Accept: application/vnd.career-chatbot.v1+json
API-Version: 2025-06-15
```

### Migration Guide
When upgrading from v1 to v2:
1. Update base URL from `/v1/` to `/v2/`
2. Update request schemas (see migration documentation)
3. Handle new response formats
4. Update error code handling

---

This API reference provides comprehensive documentation for integrating with the Career Discovery Chatbot system. For additional support, please refer to the main documentation or contact the development team.
