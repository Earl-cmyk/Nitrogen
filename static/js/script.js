/**
 * AI ENGINE AGENT - Frontend JavaScript
 * Handles all UI interactions, API calls, and dynamic rendering
 */

// ============================================================================
// GLOBAL STATE
// ============================================================================

let subscriptionState = {
    chatgpt: true,
    gemini: true,
    deepseek: true,
    perplexity: true,
    gpai: true,
    codex: true
};

let sidebarCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
let currentAgent = 'chatgpt';

// ============================================================================
// DOM ELEMENTS
// ============================================================================

// Sidebar
const sidebar = document.getElementById('sidebar');
const collapseBtn = document.getElementById('collapseSidebar');

// Search
const searchInput = document.getElementById('contextSearch');
const searchBtn = document.getElementById('searchBtn');
const searchResults = document.getElementById('searchResults');
const resultsContainer = document.getElementById('resultsContainer');
const resultCount = document.getElementById('resultCount');

// Prompt
const promptInput = document.getElementById('promptInput');
const submitBtn = document.getElementById('submitPromptBtn');
const loadingIndicator = document.getElementById('loadingIndicator');

// Response
const responseContent = document.getElementById('responseContent');
const agentBadge = document.getElementById('agentBadge');
const routingReason = document.getElementById('routingReason');
const statusLog = document.getElementById('statusLog');

// History
const historyList = document.getElementById('historyList');
const clearHistoryBtn = document.getElementById('clearHistoryBtn');

// ============================================================================
// INITIALIZATION
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    initializeSidebar();
    initializeSubscriptions();
    initializeEventListeners();
    loadSubscriptionStatus();
    loadHistory();

    // Auto-resize textarea
    promptInput.addEventListener('input', autoResizeTextarea);
});

function initializeSidebar() {
    if (sidebarCollapsed) {
        sidebar.classList.add('collapsed');
    }
}

function initializeSubscriptions() {
    // Load subscription status from localStorage
    const savedSubscriptions = localStorage.getItem('subscriptions');
    if (savedSubscriptions) {
        subscriptionState = JSON.parse(savedSubscriptions);
        updateSubscriptionUI();
    }
}

function initializeEventListeners() {
    // Sidebar collapse
    if (collapseBtn) {
        collapseBtn.addEventListener('click', toggleSidebar);
    }

    // Search
    searchBtn.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') performSearch();
    });

    // Prompt submission
    submitBtn.addEventListener('click', submitPrompt);
    promptInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            submitPrompt();
        }
    });

    // Subscription toggles
    document.querySelectorAll('.toggle-switch input').forEach(toggle => {
        toggle.addEventListener('change', handleSubscriptionToggle);
    });

    // Clear history
    if (clearHistoryBtn) {
        clearHistoryBtn.addEventListener('click', clearHistory);
    }
}

// ============================================================================
// SIDEBAR FUNCTIONS
// ============================================================================

function toggleSidebar() {
    sidebar.classList.toggle('collapsed');
    sidebarCollapsed = sidebar.classList.contains('collapsed');
    localStorage.setItem('sidebarCollapsed', sidebarCollapsed);

    // Update collapse button icon
    const icon = collapseBtn.querySelector('i');
    if (sidebarCollapsed) {
        icon.className = 'fas fa-chevron-right';
    } else {
        icon.className = 'fas fa-chevron-left';
    }
}

// ============================================================================
// SUBSCRIPTION FUNCTIONS
// ============================================================================

async function loadSubscriptionStatus() {
    try {
        const response = await fetch('/subscription/status');
        const data = await response.json();
        subscriptionState = data;
        updateSubscriptionUI();
    } catch (error) {
        console.error('Failed to load subscriptions:', error);
    }
}

function updateSubscriptionUI() {
    for (const [agent, status] of Object.entries(subscriptionState)) {
        const toggle = document.getElementById(`toggle-${agent}`);
        const badge = document.getElementById(`badge-${agent}`);

        if (toggle) {
            toggle.checked = status;
        }

        if (badge) {
            badge.textContent = status ? 'Active' : 'Inactive';
            badge.className = `status-badge ${status ? 'active' : 'inactive'}`;
        }
    }

    // Save to localStorage
    localStorage.setItem('subscriptions', JSON.stringify(subscriptionState));
}

async function handleSubscriptionToggle(event) {
    const toggle = event.target;
    const agent = toggle.id.replace('toggle-', '');
    const status = toggle.checked;

    try {
        const response = await fetch('/subscription', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ agent, status })
        });

        const data = await response.json();

        if (data.success) {
            subscriptionState[agent] = status;
            updateSubscriptionUI();

            // Show status update
            showStatusMessage(`${agent} subscription ${status ? 'activated' : 'deactivated'}`, 'info');
        }
    } catch (error) {
        console.error('Failed to update subscription:', error);
        // Revert toggle
        toggle.checked = !status;
        showStatusMessage('Failed to update subscription', 'error');
    }
}

// ============================================================================
// SEARCH FUNCTIONS - FIXED TO ACTUALLY ROUTE AND DISPLAY RESULTS
// ============================================================================

async function performSearch() {
    const query = searchInput.value.trim();

    if (!query) {
        searchResults.classList.add('hidden');
        return;
    }

    try {
        // Show loading state on search button
        searchBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Routing...';
        searchBtn.disabled = true;

        // Use the new search-and-route endpoint
        const response = await fetch('/search-and-route', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query })
        });

        const data = await response.json();

        // Display search results with router decision prominently shown
        displaySearchResults(data.results, data.routing);

        // ALSO update the main response panel with the AI response
        if (data.agent_response) {
            // Create a response object in the format expected by displayResponse
            const responseData = {
                success: true,
                routing: data.routing,
                response: data.agent_response
            };
            displayResponse(responseData);

            // Update current agent
            currentAgent = data.routing.agent;
        }

        // Show status message
        showStatusMessage(`Routed to ${data.routing.agent.toUpperCase()}`, 'success');

    } catch (error) {
        console.error('Search failed:', error);
        showStatusMessage('Search failed: ' + error.message, 'error');

        // Show error in results
        searchResults.classList.remove('hidden');
        resultsContainer.innerHTML = `
            <div class="error-message">
                <i class="fas fa-exclamation-circle"></i>
                <p>Search failed. Please try again.</p>
            </div>
        `;
    } finally {
        // Restore search button
        searchBtn.innerHTML = 'Search';
        searchBtn.disabled = false;
    }
}

// Update displaySearchResults to highlight router decisions
function displaySearchResults(results, routing) {
    if (!results || results.length === 0) {
        searchResults.classList.add('hidden');
        return;
    }

    resultsContainer.innerHTML = '';
    resultCount.textContent = `${results.length} results`;

    results.forEach((result, index) => {
        const card = document.createElement('div');
        card.className = 'result-card';

        // Add special styling for router result
        if (result.is_router_result) {
            card.style.borderLeft = `4px solid ${result.agent_color || '#40e0d0'}`;
            card.style.background = 'rgba(64, 224, 208, 0.08)';

            // Format the snippet to show router decision clearly
            const snippetParts = result.snippet.split('\n\n');
            const routerDecision = snippetParts[0];
            const agentResponse = snippetParts[1];

            card.innerHTML = `
                <h4 style="color: ${result.agent_color}; display: flex; align-items: center; gap: 8px;">
                    <i class="fas fa-robot"></i> ${result.title}
                </h4>
                <div style="background: rgba(0,0,0,0.3); padding: 12px; border-radius: 8px; margin-bottom: 12px;">
                    <strong style="color: ${result.agent_color};">🤖 ROUTER DECISION:</strong>
                    <p style="color: white; margin-top: 4px;">${escapeHTML(routerDecision.replace('**ROUTER DECISION**:', ''))}</p>
                </div>
                <div style="margin-bottom: 8px;">
                    <strong>AI Response:</strong>
                    <p style="color: var(--text-primary);">${escapeHTML(agentResponse || '')}</p>
                </div>
                <span class="result-source" style="color: ${result.agent_color};">${escapeHTML(result.source)}</span>
            `;
        } else {
            card.innerHTML = `
                <h4>${escapeHTML(result.title)}</h4>
                <p>${escapeHTML(result.snippet)}</p>
                <span class="result-source">Source: ${escapeHTML(result.source)}</span>
            `;
        }

        resultsContainer.appendChild(card);
    });

    searchResults.classList.remove('hidden');

    // Auto-scroll to results
    searchResults.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}
// ============================================================================
// PROMPT FUNCTIONS - IMPROVED VISUAL FEEDBACK
// ============================================================================

async function submitPrompt() {
    const prompt = promptInput.value.trim();

    if (!prompt) {
        showStatusMessage('Please enter a prompt', 'warning');
        return;
    }

    // Show loading state
    loadingIndicator.classList.remove('hidden');
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Routing...';

    try {
        const response = await fetch('/prompt', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ prompt })
        });

        const data = await response.json();

        if (data.success) {
            displayResponse(data);
            currentAgent = data.routing.agent;
            loadHistory(); // Refresh history

            // Also trigger a search to show context
            searchInput.value = prompt;
            performSearch();

            // Show success message
            showStatusMessage(`✓ Routed to ${data.response.agent}`, 'success');
        } else {
            displayError(data.error, data.fallback);
            if (data.routing) {
                currentAgent = data.routing.agent;
            }
            showStatusMessage(`⚠️ ${data.error}`, 'error');
        }

        // Clear input
        promptInput.value = '';
        autoResizeTextarea();

    } catch (error) {
        console.error('Prompt submission failed:', error);
        displayError('Failed to get response from AI agent');
        showStatusMessage('❌ Connection failed', 'error');
    } finally {
        // Hide loading state
        loadingIndicator.classList.add('hidden');
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i><span>Send</span>';
    }
}
// ============================================================================
// HISTORY FUNCTIONS
// ============================================================================

async function loadHistory() {
    try {
        const response = await fetch('/history');
        const history = await response.json();
        displayHistory(history);
    } catch (error) {
        console.error('Failed to load history:', error);
    }
}

function displayHistory(history) {
    if (!historyList) return;

    if (history.length === 0) {
        historyList.innerHTML = '<div class="history-empty">No requests yet</div>';
        return;
    }

    historyList.innerHTML = history.map(item => `
        <div class="history-item">
            <div class="history-prompt">${escapeHTML(item.prompt)}</div>
            <div class="history-meta">
                <span>${escapeHTML(item.agent)}</span>
                <span>${escapeHTML(item.timestamp)}</span>
            </div>
            <small>${escapeHTML(item.routing_reason)}</small>
        </div>
    `).join('');
}

async function clearHistory() {
    try {
        await fetch('/history/clear', { method: 'POST' });
        loadHistory();
        showStatusMessage('History cleared', 'success');
    } catch (error) {
        console.error('Failed to clear history:', error);
        showStatusMessage('Failed to clear history', 'error');
    }
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

function autoResizeTextarea() {
    promptInput.style.height = 'auto';
    promptInput.style.height = (promptInput.scrollHeight) + 'px';
}

function showStatusMessage(message, type = 'info') {
    const statusElement = document.createElement('div');
    statusElement.className = `status-message ${type}`;
    statusElement.textContent = message;

    document.body.appendChild(statusElement);

    setTimeout(() => {
        statusElement.remove();
    }, 3000);
}

function escapeHTML(str) {
    return str.replace(/[&<>"]/g, function(match) {
        const escape = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;'
        };
        return escape[match];
    });
}

// ============================================================================
// ROUTER PREVIEW (LIVE DEMO)
// ============================================================================

let routerPreviewTimer;
promptInput.addEventListener('input', () => {
    clearTimeout(routerPreviewTimer);

    const prompt = promptInput.value.trim();
    if (prompt.length < 3) return;

    routerPreviewTimer = setTimeout(async () => {
        try {
            const response = await fetch('/router-test', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ prompt })
            });

            const data = await response.json();

            // Update live router preview if element exists
            const previewElement = document.querySelector('.router-decision-demo');
            if (previewElement) {
                const agent = data.routing.agent.toUpperCase();
                previewElement.innerHTML = `
                    <span style="color: var(--accent-primary);">Live Router:</span>
                    Would route to <strong>${agent}</strong> — ${data.routing.reason}
                    ${!data.subscription_status ? ' <span style="color: var(--error);">(Not subscribed)</span>' : ''}
                `;
            }
        } catch (error) {
            console.error('Router preview failed:', error);
        }
    }, 500);
});

// ============================================================================
// PERIODIC REFRESH
// ============================================================================

// Refresh subscription status every 30 seconds
setInterval(loadSubscriptionStatus, 30000);