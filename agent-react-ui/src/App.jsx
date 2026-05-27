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
  const [intermediateEvents, setIntermediateEvents] = useState([]);
  const chatContainerRef = useRef(null);

  const handleClearChat = () => {
    setMessages([{ id: 'welcome', type: 'system', text: 'Welcome to Aion-ai. Select a target and send a message to start.' }]);
    setIntermediateEvents([]);
    setSessionId('');
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

        const [agents, teams, workflows] = await Promise.all([
          fetchJson('/agents'),
          fetchJson('/teams'),
          fetchJson('/workflows')
        ]);

        let newTargets = [];

        if (agents && agents.length > 0) {
          newTargets = [...newTargets, ...agents.map(a => ({ ...a, _type: 'agent', _value: `agent|${a.id}` }))];
        }
        if (teams && teams.length > 0) {
          newTargets = [...newTargets, ...teams.map(t => ({ ...t, _type: 'team', _value: `team|${t.team_id || t.id}` }))];
        }
        if (workflows && workflows.length > 0) {
          newTargets = [...newTargets, ...workflows.map(w => ({ ...w, _type: 'workflow', _value: `workflow|${w.id}` }))];
        }

        setTargets(newTargets);
        if (newTargets.length > 0) {
          const defaultWorkflow = newTargets.find(t => t._type === 'workflow');
          setSelectedTarget(defaultWorkflow ? defaultWorkflow._value : newTargets[0]._value);
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
                   setMessages(prev => [...prev, { id: agentMsgId, type: 'agent', text: '' }]);
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
               setMessages(prev => [...prev, { id: agentMsgId, type: 'agent', text: '' }]);
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
              setIntermediateEvents([{ id: Date.now().toString(), event: label, meta: value }]);
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
      acc[target._type] = acc[target._type] || [];
      acc[target._type].push(target);
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
    <div className="app-container">
      <header className="app-header">
        <h1>Aion-ai</h1>
        <div className="header-actions" style={{display: 'flex', gap: '12px', alignItems: 'center'}}>
          <button className="clear-btn" onClick={handleClearChat} title="Clear Chat">
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M3 6h18"></path><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
            </svg>
          </button>
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
          <div className="message agent-message" style={{flexDirection: 'column', alignItems: 'flex-start', background: 'transparent', border: 'none', boxShadow: 'none'}}>
            <div className="typing-indicator" style={{marginBottom: intermediateEvents.length > 0 ? '8px' : '0'}}>
              <div className="typing-dot"></div>
              <div className="typing-dot"></div>
              <div className="typing-dot"></div>
            </div>
            {intermediateEvents.length > 0 && (
              <div className="intermediate-events-container">
                {intermediateEvents.map(ev => (
                  <div key={ev.id} className="intermediate-event">
                    <span className="event-name">{ev.event}</span>
                    {ev.meta && <span className="event-meta">{ev.meta}</span>}
                  </div>
                ))}
              </div>
            )}
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
  );
}

export default App;
