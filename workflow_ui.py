# Streamlit UI for Content Creation Workflow

import streamlit as st
import requests
import json
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Content Creation Workflow",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .event-card {
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        background-color: #f0f2f6;
        border-left: 4px solid #1f77b4;
    }
    .success-event {
        border-left-color: #28a745;
        background-color: #d4edda;
    }
    .error-event {
        border-left-color: #dc3545;
        background-color: #f8d7da;
    }
    .step-event {
        border-left-color: #ffc107;
        background-color: #fff3cd;
    }
    .metric-card {
        background-color: #e7f3ff;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
    .streaming-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        background-color: #28a745;
        border-radius: 50%;
        animation: pulse 1s infinite;
    }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'events' not in st.session_state:
    st.session_state.events = []
if 'final_content' not in st.session_state:
    st.session_state.final_content = None
if 'is_streaming' not in st.session_state:
    st.session_state.is_streaming = False

def parse_sse_line(line):
    """Parse a single SSE line"""
    if line.startswith('data: '):
        try:
            return json.loads(line[6:])
        except:
            return None
    return None

def call_workflow_api(message, session_id='', user_id='', version=''):
    """Call the workflow API and yield events"""
    url = 'http://localhost:8000/workflows/content-creation-workflow/runs'
    
    data = {
        'message': message,
        'stream': 'true',
        'session_id': session_id,
        'user_id': user_id,
        'version': version
    }
    
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    with requests.post(url, data=data, headers=headers, stream=True) as response:
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                event_data = parse_sse_line(decoded_line)
                if event_data:
                    yield event_data

def extract_event_info(event):
    """Extract relevant info from an event"""
    event_type = event.get('event', 'Unknown')
    created_at = event.get('created_at', '')
    timestamp = datetime.fromtimestamp(created_at).strftime('%H:%M:%S') if created_at else ''
    
    info = {
        'type': event_type,
        'timestamp': timestamp,
        'run_id': event.get('run_id', ''),
        'step_name': event.get('step_name', ''),
        'session_id': event.get('session_id', ''),
    }
    
    # Add metrics if available
    if 'input_tokens' in event:
        info['metrics'] = {
            'input_tokens': event.get('input_tokens', 0),
            'output_tokens': event.get('output_tokens', 0),
            'total_tokens': event.get('total_tokens', 0),
            'reasoning_tokens': event.get('reasoning_tokens', 0),
        }
    
    # Add model info if available
    if 'model' in event:
        info['model'] = event.get('model', '')
        info['model_provider'] = event.get('model_provider', '')
    
    # Add tool info if available
    if 'tool' in event:
        info['tool'] = event['tool']
    
    return info

def get_event_class(event_type):
    """Get CSS class based on event type"""
    if 'Completed' in event_type or 'Success' in event_type:
        return 'success-event'
    elif 'Error' in event_type or 'Failed' in event_type:
        return 'error-event'
    elif 'Step' in event_type:
        return 'step-event'
    return ''

def strip_code_fences(s):
    """Remove surrounding triple-backtick code fences if present"""
    if not s:
        return s
    if s.startswith('```'):
        # drop the first fence line which may include language
        idx = s.find('\n')
        if idx != -1:
            s = s[idx+1:]
    if s.endswith('```'):
        s = s[:-3]
    return s

# Main UI
st.markdown('<div class="main-header">🤖 Content Creation Workflow</div>', unsafe_allow_html=True)

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    message = st.text_area(
        "Message",
        value="machine learning in 2026",
        height=100,
        placeholder="Enter your message..."
    )
    
    session_id = st.text_input("Session ID (optional)", value="")
    user_id = st.text_input("User ID (optional)", value="")
    version = st.text_input("Version (optional)", value="")
    
    st.divider()
    st.markdown("Press the **Run Workflow** button in the main panel to start.")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📊 Events")
    run_workflow = st.button("🚀 Run Workflow", type="primary", use_container_width=True)
    
    if run_workflow:
        st.session_state.events = []
        st.session_state.final_content = None
        st.session_state.is_streaming = True

        # Placeholder for streaming events
        events_placeholder = st.empty()
        status_placeholder = st.empty()

        try:
            for event in call_workflow_api(message, session_id, user_id, version):
                st.session_state.events.append(event)

                # accumulate streamed content chunks when present
                evt_name = event.get('event', '')
                if evt_name == 'RunContent' and 'content' in event:
                    if st.session_state.final_content is None:
                        st.session_state.final_content = ''
                    st.session_state.final_content += event.get('content', '')

                # if run completed or content completed, set final content (overwrite with final payload if present)
                if evt_name in ('RunCompleted', 'RunContentCompleted'):
                    content = event.get('content')
                    if not content and isinstance(event.get('step_response'), dict):
                        content = event['step_response'].get('content')
                    if not content and isinstance(event.get('step_output'), dict):
                        content = event['step_output'].get('content')
                    if content:
                        st.session_state.final_content = content

                # Update the display
                with events_placeholder.container():
                    st.markdown("### 📡 Live Events Stream")
                    for i, evt in enumerate(st.session_state.events[-10:]):  # Show last 10 events
                        evt_info = extract_event_info(evt)
                        event_type = evt_info['type']
                        css_class = get_event_class(event_type)

                        with st.expander(f"🔹 {event_type} - {evt_info['timestamp']}", expanded=True):
                            st.markdown(f"""
                            <div class="event-card {css_class}">
                                <p><strong>Event:</strong> {event_type}</p>
                                <p><strong>Time:</strong> {evt_info['timestamp']}</p>
                                <p><strong>Run ID:</strong> <code>{evt_info['run_id'][:20]}...</code></p>
                                {f'<p><strong>Step:</strong> {evt_info["step_name"]}</p>' if evt_info.get('step_name') else ''}
                                {f'<p><strong>Model:</strong> {evt_info["model"]} ({evt_info["model_provider"]})</p>' if evt_info.get('model') else ''}
                            </div>
                            """, unsafe_allow_html=True)

                            # Show metrics if available
                            if evt_info.get('metrics'):
                                metrics = evt_info['metrics']
                                m_col1, m_col2, m_col3, m_col4 = st.columns(4)
                                with m_col1:
                                    st.metric("Input Tokens", metrics['input_tokens'])
                                with m_col2:
                                    st.metric("Output Tokens", metrics['output_tokens'])
                                with m_col3:
                                    st.metric("Total Tokens", metrics['total_tokens'])
                                with m_col4:
                                    st.metric("Reasoning Tokens", metrics['reasoning_tokens'])

                            # Show tool info if available
                            if evt_info.get('tool'):
                                tool = evt_info['tool']
                                st.json(tool)

                # Update status
                status_placeholder.info(f"📡 Streaming... {len(st.session_state.events)} events received")

            st.session_state.is_streaming = False
            status_placeholder.success("✅ Streaming completed!")

        except Exception as e:
            st.session_state.is_streaming = False
            status_placeholder.error(f"❌ Error: {str(e)}")

    if st.session_state.events and not st.session_state.is_streaming:
        # Event statistics
        event_types = {}
        for evt in st.session_state.events:
            event_type = evt.get('event', 'Unknown')
            event_types[event_type] = event_types.get(event_type, 0) + 1
        
        # Display event type distribution
        st.subheader("Event Distribution")
        for event_type, count in sorted(event_types.items(), key=lambda x: x[1], reverse=True):
            st.progress(count / len(st.session_state.events), text=f"{event_type}: {count}")
        
        # Display all events in a table
        st.subheader("All Events")
        event_data = []
        for evt in st.session_state.events:
            evt_info = extract_event_info(evt)
            event_data.append({
                "Time": evt_info['timestamp'],
                "Event": evt_info['type'],
                "Step": evt_info.get('step_name', '-'),
                "Run ID": evt_info['run_id'][:8] + "..." if evt_info['run_id'] else "-"
            })
        
        if event_data:
            st.dataframe(event_data, use_container_width=True)
        
        # Show raw events
        with st.expander("🔍 Raw Events JSON"):
            st.json(st.session_state.events)

        # Final output if present
        if st.session_state.final_content:
            with st.expander("🎯 Final Output", expanded=True):
                clean = strip_code_fences(st.session_state.final_content)
                try:
                    parsed = json.loads(clean)
                    st.json(parsed)
                except Exception:
                    st.code(clean)

    elif not st.session_state.is_streaming:
        st.info("👈 Configure inputs in the sidebar and run the workflow from the main panel")

with col2:
    st.header("📈 Summary")
    
    if st.session_state.events:
        # Calculate summary statistics
        total_events = len(st.session_state.events)
        
        # Count different event types
        run_started = sum(1 for e in st.session_state.events if e.get('event') == 'RunStarted')
        run_completed = sum(1 for e in st.session_state.events if e.get('event') == 'RunCompleted')
        step_started = sum(1 for e in st.session_state.events if e.get('event') == 'StepStarted')
        step_completed = sum(1 for e in st.session_state.events if e.get('event') == 'StepCompleted')
        
        # Total tokens
        total_input = sum(e.get('input_tokens', 0) for e in st.session_state.events if 'input_tokens' in e)
        total_output = sum(e.get('output_tokens', 0) for e in st.session_state.events if 'output_tokens' in e)
        
        # Display metrics
        st.metric("Total Events", total_events)
        st.metric("Runs Started", run_started)
        st.metric("Runs Completed", run_completed)
        st.metric("Steps Started", step_started)
        st.metric("Steps Completed", step_completed)
        
        st.divider()
        
        st.metric("Total Input Tokens", total_input)
        st.metric("Total Output Tokens", total_output)
        st.metric("Total Tokens", total_input + total_output)
        
        # Streaming status
        st.divider()
        if st.session_state.is_streaming:
            st.markdown('<div class="streaming-indicator"></div> <strong>Streaming...</strong>', unsafe_allow_html=True)
        else:
            st.success("✅ Completed")
    
    else:
        st.info("No events yet")

# Clear button
if st.session_state.events:
    if st.button("🗑️ Clear Results"):
        st.session_state.events = []
        st.session_state.final_content = None
        st.rerun()