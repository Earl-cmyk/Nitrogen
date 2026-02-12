"""
AI ENGINE AGENT - Flask Web Application
Single-file implementation with modular structure
Routes user requests to different AI providers based on intent classification
"""

from flask import Flask, render_template, request, jsonify, session
import re
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'ai-engine-agent-secret-key-2024'  # Required for session memory

# ============================================================================
# IN-MEMORY STORAGE
# ============================================================================

# Subscription status storage
subscriptions = {
    'chatgpt': True,
    'gemini': True,
    'deepseek': True,
    'perplexity': True,
    'gpai': True,
    'codex': True
}

# Request history storage (session-based)
request_history = []


# ============================================================================
# PROMPT CLASSIFICATION ENGINE
# ============================================================================

def route_prompt(prompt_text):
    """
    Classify user intent and route to appropriate AI agent

    Args:
        prompt_text (str): User input prompt

    Returns:
        dict: Contains agent name and classification reason
    """
    prompt_lower = prompt_text.lower()

    # Intent classification rules
    classification_rules = [
        # Codex/Programming
        {
            'agent': 'codex',
            'patterns': [
                r'\b(code|program|function|script|debug|compile|syntax|api|app|software|develop)\b',
                r'\b(react|vue|angular|django|flask|node|express|python|java|javascript|html|css)\b',
                r'\b(algorithm|data structure|class|object|method|variable|loop|array)\b',
                r'\b(programming|coding|software development|web dev)\b'
            ],
            'keywords': ['write code', 'fix bug', 'create function', 'program', 'debug', 'build app'],
            'reason': 'Programming/code request detected'
        },

        # Perplexity/Links and sources
        {
            'agent': 'perplexity',
            'patterns': [
                r'\b(link|source|reference|citation|article|research|paper|find|search|google|look up)\b',
                r'\b(where can I|find me|search for|give me sources|list of resources)\b'
            ],
            'keywords': ['sources', 'references', 'links', 'citations', 'research'],
            'reason': 'Source/link request detected'
        },

        # Gemini/Factual knowledge
        {
            'agent': 'gemini',
            'patterns': [
                r'\b(fact|history|date|location|famous|population|culture|definition|meaning)\b',
                r'\b(who|what|where|when)\s+(is|are|was|were|did|does)\b',
                r'\b(factual|knowledge|google|search|information|dictionary)\b'
            ],
            'keywords': ['tell me about', 'what is', 'who is', 'when did', 'where is', 'define'],
            'reason': 'Factual knowledge/lookup request detected'
        },

        # DeepSeek/Long explanations
        {
            'agent': 'deepseek',
            'patterns': [
                r'\b(explain in detail|comprehensive|thorough|in-depth|elaborate|detailed)\b',
                r'\b(long form|essay|extensive|complete guide|full explanation)\b'
            ],
            'keywords': ['explain thoroughly', 'detailed analysis', 'comprehensive guide', 'in depth'],
            'reason': 'Long-form explanation requested'
        },

        # GPAI/Math logic
        {
            'agent': 'gpai',
            'patterns': [
                r'[\d\+\-\*\/\=\%\(\)]+',  # Contains numbers and operators
                r'\b(calculate|solve|equation|math|algebra|calculus|geometry|puzzle|logic)\b',
                r'\b(compute|sum|difference|product|quotient|modulo|derivative|integral)\b'
            ],
            'keywords': ['solve this', 'calculate', 'math problem', 'equation', 'formula'],
            'reason': 'Math/logic/puzzle request detected'
        },

        # ChatGPT/General knowledge (default)
        {
            'agent': 'chatgpt',
            'patterns': [
                r'\b(opinion|thoughts|perspective|general|anyway|basically|overall)\b'
            ],
            'keywords': [],
            'reason': 'General knowledge/conversational query'
        }
    ]

    # Score each agent
    scores = {rule['agent']: 0 for rule in classification_rules}

    for rule in classification_rules:
        agent = rule['agent']

        # Check regex patterns
        for pattern in rule['patterns']:
            if re.search(pattern, prompt_lower):
                scores[agent] += 3

        # Check keywords
        for keyword in rule['keywords']:
            if keyword in prompt_lower:
                scores[agent] += 5

    # Add default score to ChatGPT for fallback
    scores['chatgpt'] += 1

    # Find highest scoring agent
    max_score = max(scores.values())

    if max_score == 0:
        # Default fallback
        return {
            'agent': 'chatgpt',
            'reason': 'No specific intent detected - routing to general assistant'
        }

    # Get all agents with max score
    top_agents = [agent for agent, score in scores.items() if score == max_score]

    # Select first top agent (can be enhanced with ML later)
    selected_agent = top_agents[0]

    # Get reason from classification rules
    for rule in classification_rules:
        if rule['agent'] == selected_agent:
            return {
                'agent': selected_agent,
                'reason': rule['reason']
            }

    # Fallback
    return {
        'agent': 'chatgpt',
        'reason': 'Default routing'
    }


# ============================================================================
# MOCK AI AGENT RESPONSES
# ============================================================================

def call_chatgpt(prompt):
    """Mock ChatGPT response generator"""
    responses = [
        f"Based on general knowledge: '{prompt[:50]}...' relates to various perspectives. ChatGPT would provide a balanced overview considering multiple viewpoints.",
        f"ChatGPT analysis: The query '{prompt[:40]}...' touches on general concepts. Here's what I know from my training data...",
        f"General assistant response: I understand you're asking about '{prompt[:30]}...'. Let me share some general information on this topic."
    ]
    return {
        'agent': 'ChatGPT',
        'agent_color': '#10a37f',
        'response': random.choice(responses),
        'timestamp': datetime.now().strftime('%H:%M:%S')
    }


def call_gemini(prompt):
    """Mock Gemini response generator"""
    responses = [
        f"Gemini factual lookup: Searching for '{prompt[:50]}...'. According to verified sources, this involves several key facts and data points.",
        f"Based on factual knowledge: '{prompt[:40]}...' - this is documented in multiple authoritative sources. Let me summarize the key information.",
        f"Gemini knowledge search: I've found relevant information about '{prompt[:30]}...'. Here are the verified facts."
    ]
    return {
        'agent': 'Gemini',
        'agent_color': '#1a73e8',
        'response': random.choice(responses),
        'timestamp': datetime.now().strftime('%H:%M:%S')
    }


def call_deepseek(prompt):
    """Mock DeepSeek response generator"""
    responses = [
        f"DeepSeek detailed analysis: Let me provide a comprehensive explanation of '{prompt[:40]}...' This topic has several layers to explore...",
        f"In-depth explanation requested for: '{prompt[:30]}...' I'll break this down into detailed components and elaborate on each aspect.",
        f"DeepSeek long-form response: Your query about '{prompt[:35]}...' requires thorough examination. Let me provide a complete guide."
    ]
    return {
        'agent': 'DeepSeek',
        'agent_color': '#4b6bfb',
        'response': random.choice(responses),
        'timestamp': datetime.now().strftime('%H:%M:%S')
    }


def call_perplexity(prompt):
    """Mock Perplexity response generator"""
    responses = [
        f"Perplexity sources: I found multiple references for '{prompt[:45]}...'. Here are relevant sources with citations and links.",
        f"Source compilation for: '{prompt[:35]}...' - I've gathered information from academic papers, articles, and verified references.",
        f"Perplexity research: Regarding '{prompt[:40]}...', here are the key sources and references with their credibility assessments."
    ]
    return {
        'agent': 'Perplexity',
        'agent_color': '#5436da',
        'response': random.choice(responses),
        'timestamp': datetime.now().strftime('%H:%M:%S')
    }


def call_gpai(prompt):
    """Mock GPAI response generator"""
    responses = [
        f"GPAI logical reasoning: Analyzing '{prompt[:40]}...' through mathematical frameworks. The solution involves several computational steps.",
        f"Math/Logic processing: For '{prompt[:35]}...', I've computed the result using formal logic and mathematical operations.",
        f"GPAI puzzle solver: Your query '{prompt[:30]}...' requires logical deduction. Here's my step-by-step reasoning."
    ]
    return {
        'agent': 'GPAI',
        'agent_color': '#ff6b4a',
        'response': random.choice(responses),
        'timestamp': datetime.now().strftime('%H:%M:%S')
    }


def call_codex(prompt):
    """Mock Codex response generator"""
    responses = [
        f"Codex programming: For '{prompt[:40]}...', here's a code solution with implementation details and best practices.",
        f"Software development: Analyzing '{prompt[:35]}...' - I'll provide a clean, efficient implementation with documentation.",
        f"Codex assistance: Your coding request '{prompt[:30]}...' can be solved with this optimized approach."
    ]
    return {
        'agent': 'Codex',
        'agent_color': '#ff6e4a',
        'response': random.choice(responses),
        'timestamp': datetime.now().strftime('%H:%M:%S')
    }


# ============================================================================
# FLASK ROUTES
# ============================================================================

@app.route('/')
def index():
    """Render main application page"""
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    """Handle contextual keyword search"""
    data = request.get_json()
    query = data.get('query', '')

    # Generate mock search results
    search_results = []

    if query:
        # Create varied results based on query
        for i in range(3):
            search_results.append({
                'title': f"{query.capitalize()} - Key Concept {i + 1}",
                'snippet': f"Comprehensive information about {query}. This includes relevant details and contextual understanding of the topic.",
                'source': ['Wikipedia', 'Academic Journal', 'Technical Documentation'][i]
            })

        # Add a specific result about AI routing
        routing = route_prompt(query)
        search_results.append({
            'title': f"AI Agent Routing Result",
            'snippet': f"This query was classified as: {routing['agent'].upper()}. Reason: {routing['reason']}",
            'source': 'Engine Agent'
        })

    return jsonify({'results': search_results})


@app.route('/prompt', methods=['POST'])
def handle_prompt():
    """Process main AI prompt and route to appropriate agent"""
    data = request.get_json()
    prompt_text = data.get('prompt', '')

    # Check if agent is subscribed
    routing = route_prompt(prompt_text)
    agent_name = routing['agent']

    if not subscriptions.get(agent_name, False):
        # Agent is not subscribed, route to ChatGPT as fallback
        return jsonify({
            'success': False,
            'error': f'{agent_name.capitalize()} is not subscribed',
            'fallback': True,
            'routing': {
                'agent': 'chatgpt',
                'original_agent': agent_name,
                'reason': 'Fallback due to subscription status'
            },
            'response': call_chatgpt(prompt_text)
        })

    # Route to appropriate agent
    agent_functions = {
        'chatgpt': call_chatgpt,
        'gemini': call_gemini,
        'deepseek': call_deepseek,
        'perplexity': call_perplexity,
        'gpai': call_gpai,
        'codex': call_codex
    }

    agent_function = agent_functions.get(agent_name, call_chatgpt)
    response = agent_function(prompt_text)

    # Add to request history
    history_entry = {
        'prompt': prompt_text[:60] + ('...' if len(prompt_text) > 60 else ''),
        'agent': response['agent'],
        'timestamp': response['timestamp'],
        'routing_reason': routing['reason']
    }

    # Initialize session history if not exists
    if 'request_history' not in session:
        session['request_history'] = []

    # Add to beginning of list (newest first) and keep last 10
    session['request_history'].insert(0, history_entry)
    session['request_history'] = session['request_history'][:10]
    session.modified = True

    return jsonify({
        'success': True,
        'routing': routing,
        'response': response
    })


@app.route('/subscription', methods=['POST'])
def update_subscription():
    """Toggle subscription status for AI agents"""
    data = request.get_json()
    agent = data.get('agent')
    status = data.get('status')

    if agent in subscriptions:
        subscriptions[agent] = status
        return jsonify({
            'success': True,
            'agent': agent,
            'status': status
        })

    return jsonify({
        'success': False,
        'error': 'Invalid agent'
    })


@app.route('/subscription/status', methods=['GET'])
def get_subscriptions():
    """Get current subscription status"""
    return jsonify(subscriptions)


@app.route('/router-test', methods=['POST'])
def router_test():
    """Debug route for testing classification"""
    data = request.get_json()
    prompt_text = data.get('prompt', '')

    routing = route_prompt(prompt_text)

    return jsonify({
        'prompt': prompt_text,
        'routing': routing,
        'subscription_status': subscriptions.get(routing['agent'], False),
        'available_agents': list(subscriptions.keys())
    })


@app.route('/history', methods=['GET'])
def get_history():
    """Get request history from session"""
    if 'request_history' not in session:
        session['request_history'] = []

    return jsonify(session['request_history'])


@app.route('/history/clear', methods=['POST'])
def clear_history():
    """Clear request history"""
    session['request_history'] = []
    session.modified = True
    return jsonify({'success': True})


@app.route('/search-and-route', methods=['POST'])
def search_and_route():
    """Handle search that also routes to AI agent"""
    data = request.get_json()
    query = data.get('query', '')

    # Generate mock search results
    search_results = []

    if query:
        # Create varied results based on query
        for i in range(3):
            search_results.append({
                'title': f"{query.capitalize()} - Key Concept {i + 1}",
                'snippet': f"Comprehensive information about {query}. This includes relevant details and contextual understanding of the topic.",
                'source': ['Wikipedia', 'Academic Journal', 'Technical Documentation'][i]
            })

        # ROUTE THE SEARCH QUERY TO AN AI AGENT
        routing = route_prompt(query)

        # Get response from the routed agent
        agent_functions = {
            'chatgpt': call_chatgpt,
            'gemini': call_gemini,
            'deepseek': call_deepseek,
            'perplexity': call_perplexity,
            'gpai': call_gpai,
            'codex': call_codex
        }

        agent_function = agent_functions.get(routing['agent'], call_chatgpt)
        agent_response = agent_function(query)

        # Add routing result as first result
        search_results.insert(0, {
            'title': f"🔍 AI ENGINE AGENT: Routed to {routing['agent'].upper()}",
            'snippet': f"**ROUTER DECISION**: {routing['reason']}\n\n{agent_response['response']}",
            'source': f"Agent: {agent_response['agent']} at {agent_response['timestamp']}",
            'is_router_result': True,
            'agent': routing['agent'],
            'agent_color': agent_response.get('agent_color', '#40e0d0'),
            'full_response': agent_response['response']
        })

    return jsonify({
        'results': search_results,
        'routing': routing if query else None,
        'agent_response': agent_response if query else None
    })


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)