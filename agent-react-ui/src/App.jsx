import React, { useState, useRef, useEffect } from 'react';
import { marked } from 'marked';

function App() {
  const [messages, setMessages] = useState([
    { id: 'welcome', type: 'system', text: 'Welcome to Aion-ai. Select a target and send a message to start.' }
  ]);
  const [input, setInput] = useState('');
  
  // State for dynamic targets
  const [targets, setTargets] = useState([]);
  const [selectedTarget, setSelectedTarget] = useState('');
  
  const [isTyping, setIsTyping] = useState(false);
  const [sessionId, setSessionId] = useState('');
  const [sessions, setSessions] = useState([]);
  const [intermediateEvents, setIntermediateEvents] = useState([]);
  const chatContainerRef = useRef(null);

  const fetchSessions = async () => {
    try {
      if (targets.length === 0) return;
      
      const fetchPromises = targets.map(target => {
        let url = `/sessions?type=${target.type}`;
        if (target.db_id) {
          url += `&db_id=${target.db_id}`;
        }
        return fetch(url);
      });

      const responses = await Promise.all(fetchPromises);
      let allSessions = [];
      
      for (const res of responses) {
        if (res.ok) {
          const data = await res.json();
          allSessions = allSessions.concat(data.data || []);
        }
      }
      
      // Sort by created_at descending
      allSessions.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
      
      // Deduplicate by session_id in case multiple targets share a db
      const uniqueSessions = [];
      const seenIds = new Set();
      for (const s of allSessions) {
        if (!seenIds.has(s.session_id)) {
          seenIds.add(s.session_id);
          uniqueSessions.push(s);
        }
      }
      
      setSessions(uniqueSessions);
    } catch (e) {
      console.error('Error fetching sessions:', e);
    }
  };

  useEffect(() => {
    fetchSessions();
  }, []);

  const handleLoadSession = async (sid) => {
    if (isTyping) return;
    try {
      const res = await fetch(`/sessions/${sid}/runs`);
      if (res.ok) {
        const runs = await res.json();
        setSessionId(sid);
        
        // Auto-select the target used in this session
        const session = sessions.find(s => s.session_id === sid);
        if (session) {
           if (session.workflow_id) setSelectedTarget(`workflow|${session.workflow_id}`);
           else if (session.team_id) setSelectedTarget(`team|${session.team_id}`);
           else if (session.agent_id) setSelectedTarget(`agent|${session.agent_id}`);
        }
        
        const loadedMessages = [];
        runs.forEach(run => {
          if (run.run_input) {
            loadedMessages.push({ id: `user-${run.run_id}`, type: 'user', text: run.run_input });
          }
          if (run.content) {
            loadedMessages.push({
              id: `agent-${run.run_id}`,
              type: 'agent',
              text: run.content,
              runId: run.run_id,
              sessionId: sid
            });
          }
        });
        
        if (loadedMessages.length === 0) {
          loadedMessages.push({ id: 'welcome', type: 'system', text: 'Resumed empty session.' });
        }
        setMessages(loadedMessages);
      }
    } catch (e) {
      console.error('Error loading session runs:', e);
    }
  };

  const handleClearChat = () => {
    setMessages([{ id: 'welcome', type: 'system', text: 'Welcome to Aion-ai. Select a target and send a message to start.' }]);
    setIntermediateEvents([]);
    setSessionId('');
    fetchSessions();
  };

  // Fetch agents, teams, workflows on mount
  useEffect(() => {
    const fetchTargets = async () => {
      try {
        const fetchJson = async (url) => {
          try {
            const res = await fetch(url);
            if (!res.ok) return [];
            return await res.json();
          } catch (e) {
            console.error(`Error fetching ${url}:`, e);
            return [];
          }
        };

        const [agentsRes, teamsRes, workflowsRes] = await Promise.all([
          fetchJson('/agents'),
          fetchJson('/teams'),
          fetchJson('/workflows')
        ]);
        
        const agents = Array.isArray(agentsRes) ? agentsRes : (agentsRes.data || []);
        const teams = Array.isArray(teamsRes) ? teamsRes : (teamsRes.data || []);
        const workflows = Array.isArray(workflowsRes) ? workflowsRes : (workflowsRes.data || []);
        
        const combinedTargets = [
          ...agents.map(a => ({ id: a.agent_id || a.id, name: a.name || a.agent_id || a.id, type: 'agent', db_id: a.db_id, _value: `agent|${a.id}` })),
          ...teams.map(t => ({ id: t.team_id || t.id, name: t.name || t.team_id || t.id, type: 'team', db_id: t.db_id, _value: `team|${t.team_id || t.id}` })),
          ...workflows.map(w => ({ id: w.workflow_id || w.id, name: w.name || w.workflow_id || w.id, type: 'workflow', db_id: w.db_id, _value: `workflow|${w.id}` }))
        ];
        setTargets(combinedTargets);
        
        if (combinedTargets.length > 0) {
          const defaultWorkflow = combinedTargets.find(t => t.type === 'workflow');
          setSelectedTarget(defaultWorkflow ? defaultWorkflow._value : combinedTargets[0]._value);
        }
      } catch (err) {
        console.error("Error setting up endpoints:", err);
      }
    };
    fetchTargets();
  }, []);

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages, isTyping]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isTyping || !selectedTarget) return;

    const userMessage = input.trim();
    setInput('');
    
    // Add user message
    setMessages(prev => [...prev, { id: Date.now().toString(), type: 'user', text: userMessage }]);
    setIsTyping(true);
    setIntermediateEvents([]);

    try {
      const [type, id] = selectedTarget.split('|');
      let endpoint = '';
      if (type === 'agent') endpoint = `/agents/${id}/runs`;
      else if (type === 'team') endpoint = `/teams/${id}/runs`;
      else if (type === 'workflow') endpoint = `/workflows/${id}/runs`;

      const formData = new FormData();
      formData.append('message', userMessage);
      formData.append('stream', 'true');
      if (sessionId) {
        formData.append('session_id', sessionId);
      }
      formData.append('background', 'false');

      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'accept': 'application/json'
        },
        body: formData
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const agentMsgId = Date.now().toString() + '-agent';
      let agentMsgAdded = false;

      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');
      let accumulatedData = '';
      let markdownBuffer = '';
      let currentStepContent = '';
      let isWorkflow = selectedTarget.startsWith('workflow|');

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        accumulatedData += chunk;

        const events = accumulatedData.split('\n\n');
        accumulatedData = events.pop(); // keep last partial event

        for (const eventStr of events) {
          const lines = eventStr.split('\n');
          let eventType = 'message';
          let data = null;

          for (const line of lines) {
            if (line.startsWith('event: ')) {
              eventType = line.substring(7).trim();
            } else if (line.startsWith('data: ')) {
              try {
                data = JSON.parse(line.substring(6));
              } catch (e) {
                console.warn("Could not parse JSON data", line);
              }
            }
          }

          if (['RunContent', 'RunResponse', 'message', 'ModelResponse'].includes(eventType)) {
            if (data && data.content) {
              if (isWorkflow) {
                // Buffer the content for the current step, do not display yet
                currentStepContent += data.content;
              } else {
                // Live stream for non-workflows
                if (!agentMsgAdded) {
                   setMessages(prev => [...prev, { 
                     id: agentMsgId, 
                     type: 'agent', 
                     text: '',
                     runId: data?.workflow_run_id || data?.run_id || '',
                     sessionId: data?.session_id || '' 
                   }]);
                   agentMsgAdded = true;
                   setIsTyping(false);
                }
                setIntermediateEvents([]);
                markdownBuffer += data.content;
                setMessages(prev => prev.map(m => 
                  m.id === agentMsgId ? { ...m, text: markdownBuffer } : m
                ));
              }
            }
            if (data && data.session_id) {
              setSessionId(data.session_id);
            }
          } else if (eventType === 'WorkflowCompleted') {
            // Workflow finished, now stream the final step's content
            if (!agentMsgAdded) {
               setMessages(prev => [...prev, { 
                 id: agentMsgId, 
                 type: 'agent', 
                 text: '',
                 runId: data?.workflow_run_id || data?.run_id || '',
                 sessionId: data?.session_id || '' 
               }]);
               agentMsgAdded = true;
               setIsTyping(false);
            }
            setIntermediateEvents([]);
            if (data && data.session_id) {
              setSessionId(data.session_id);
            }
            
            // Simulate smooth streaming of the final output
            let i = 0;
            const fullText = currentStepContent;
            const streamInterval = setInterval(() => {
              const chunkSize = Math.max(3, Math.floor(fullText.length / 60));
              markdownBuffer += fullText.substring(i, i + chunkSize);
              setMessages(prev => prev.map(m => 
                m.id === agentMsgId ? { ...m, text: markdownBuffer } : m
              ));
              i += chunkSize;
              if (i >= fullText.length) {
                clearInterval(streamInterval);
                setMessages(prev => prev.map(m => 
                  m.id === agentMsgId ? { ...m, text: fullText } : m
                ));
              }
            }, 15);

          } else if (['RunCompleted', 'RunFinished', 'TeamRunCompleted'].includes(eventType)) {
            if (!isWorkflow) setIntermediateEvents([]);
            if (data && data.session_id) {
              setSessionId(data.session_id);
            }
          } else if (eventType && eventType !== 'RunContentCompleted') {
            let label = '';
            let value = '';
            
            if (eventType === 'StepStarted') {
              label = 'Running step';
              value = data?.step_name;
              currentStepContent = ''; // Reset buffer for new step
            } else if (eventType === 'ToolCallStarted' || eventType === 'TeamToolCallStarted') {
              label = 'Using tool';
              value = data?.tool?.tool_name;
            } else if (eventType === 'RunStarted' && !intermediateEvents.some(e => e.event === 'Running step')) {
              label = 'Agent active';
              value = data?.agent_name;
            }

            if (label && value) {
              setIntermediateEvents(prev => [...prev, { id: Date.now().toString(), event: label, meta: value }]);
            }
          }
        }
      }
      setIsTyping(false);

    } catch (error) {
      console.error('Error fetching agent response:', error);
      setIsTyping(false);
      setMessages(prev => [...prev, { id: Date.now().toString(), type: 'system', text: `Error: ${error.message}. Please check if the server is running.` }]);
    }
  };

  const renderOptions = () => {
    const grouped = targets.reduce((acc, target) => {
      acc[target.type] = acc[target.type] || [];
      acc[target.type].push(target);
      return acc;
    }, {});

    return Object.keys(grouped).map(type => (
      <optgroup key={type} label={`${type.charAt(0).toUpperCase() + type.slice(1)}s`}>
        {grouped[type].map(target => (
          <option key={target._value} value={target._value}>
            {target.name}
          </option>
        ))}
      </optgroup>
    ));
  };

  return (
    <div className="app-layout">
      <aside className="sidebar">
        <div className="sidebar-header">
          <button className="new-chat-btn" onClick={handleClearChat}>
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <line x1="12" y1="5" x2="12" y2="19"></line>
              <line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
            New Chat
          </button>
        </div>
        <div className="session-list">
          {sessions.filter(s => {
             if (!selectedTarget) return true;
             const [type, id] = selectedTarget.split('|');
             if (type === 'workflow') return s.workflow_id === id;
             if (type === 'team') return s.team_id === id;
             if (type === 'agent') return s.agent_id === id;
             return true;
          }).map(s => (
            <div 
              key={s.session_id} 
              className={`session-item ${s.session_id === sessionId ? 'active' : ''}`}
              onClick={() => handleLoadSession(s.session_id)}
            >
              <div className="session-name" title={s.session_name || s.session_id}>
                {s.session_name || 'New Chat'}
              </div>
              <div className="session-date">
                {new Date(s.created_at).toLocaleString(undefined, {
                  month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
                })}
              </div>
            </div>
          ))}
        </div>
      </aside>

      <div className="app-container">
        <header className="app-header">
          <h1>Aion-ai</h1>
          <div className="header-actions" style={{display: 'flex', gap: '12px', alignItems: 'center'}}>
            <div className="agent-selector">
            <select value={selectedTarget} onChange={(e) => setSelectedTarget(e.target.value)}>
              {targets.length > 0 ? renderOptions() : <option value="">Loading...</option>}
            </select>
          </div>
        </div>
      </header>

      <main className="chat-container" ref={chatContainerRef}>
        {messages.map((msg) => {
          let htmlContent = msg.text;
          if (msg.type === 'agent') {
            let cleanText = msg.text || '<span style="opacity: 0.5;">Thinking...</span>';
            // Strip outer markdown blocks if the entire response is wrapped in them
            cleanText = cleanText.replace(/^```(markdown|md)?\s*\n/i, '');
            cleanText = cleanText.replace(/\n?```\s*$/i, '');
            htmlContent = marked.parse(cleanText);
          }
          return (
            <div key={msg.id} className={`message ${msg.type}-message`}>
              <div 
                className="message-content" 
                dangerouslySetInnerHTML={
                  msg.type === 'agent' 
                    ? { __html: htmlContent } 
                    : undefined
                }
              >
                {msg.type !== 'agent' ? msg.text : null}
              </div>
            </div>
          );
        })}
        {isTyping && (
          <div className="message agent typing">
            <div className="thinking-badge" style={{ display: 'flex', alignItems: 'center', color: 'var(--text-color)', background: 'var(--bg-panel)', padding: '12px 16px', borderRadius: '12px', width: 'fit-content', fontSize: '0.9rem' }}>
              <span className="dot-pulse"></span>
              {intermediateEvents.length > 0 
                ? `${intermediateEvents[intermediateEvents.length - 1].event}: ${intermediateEvents[intermediateEvents.length - 1].meta}`
                : 'Starting...'}
            </div>
          </div>
        )}
      </main>

      <footer className="app-footer">
        <form id="chat-form" onSubmit={handleSubmit}>
          <div className="input-wrapper">
            <input 
              type="text" 
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..." 
              autoComplete="off" 
              required 
            />
            <button type="submit" className="send-button" disabled={isTyping || !selectedTarget}>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
              </svg>
            </button>
          </div>
        </form>
      </footer>
      </div>
    </div>
  );
}

export default App;
