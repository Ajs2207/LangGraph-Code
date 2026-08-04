## Sample Streamlit Code


import streamlit as st
import threading
import time

# ---- Mock Simulation Job for UI Testing ----
class MockSimulationJob:
    def __init__(self, job_id, prompt, geometry):
        self.job_id = job_id
        self.prompt = prompt
        self.geometry = geometry
        self.state = "running"
        self.logs = ["Initializing simulation engine...", "Reading geometry file..."]
        self.start_time = time.time()

    def run(self):
        for i in range(1, 6):
            time.sleep(2)
            self.logs.append(f"Processing step {i}/5... Step Name in progress.")
        self.logs.append("Simulation finished successfully.")
        self.state = "completed"

    def get_status(self):
        return {
            "state": self.state,
            "logs": self.logs
        }

    def get_results(self):
        return {
            "Job ID": self.job_id,
            "Prompt Provided": self.prompt,
            "Status": "Success",
            "Max Stress": "240 MPa",
            "Displacement": "1.2 mm"
        }

# ---- Session State Initialization ----
if "job" not in st.session_state:
    st.session_state.job = None
if "show_results" not in st.session_state:
    st.session_state.show_results = False

# ---- Sidebar Setup ----
with st.sidebar:
    st.title("⚙️ Controls & History")
    
    # Show active job metadata if a simulation is running or completed
    if st.session_state.job:
        st.info("🔄 Active Job Running")
        if st.button("Cancel & Reset Job", type="primary", use_container_width=True):
            st.session_state.job = None
            st.session_state.show_results = False
            st.rerun()
    else:
        st.success("🟢 System Ready")
        
    st.markdown("---")
    st.markdown("### 📊 Workspace Info")
    st.caption("Environment: Mock UI Test Mode")
    st.caption("Ansys Version: 2025 R1")


# ---- Page 1: Setup ----
if not st.session_state.job:
    st.title("Engineering Copilot")
    with st.form("setup_form"):
        uploaded_file = st.file_uploader("Upload Geometry")
        prompt = st.text_area("Describe your simulation")
        submitted = st.form_submit_button("Run Simulation")

        if submitted:
            if not uploaded_file:
                st.error("⚠️ Please upload a geometry file to proceed with the simulation.")
            else:
                # Instantiate the mock job instead
                job = MockSimulationJob(job_id=int(time.time()), prompt=prompt, geometry=uploaded_file.read())
                thread = threading.Thread(target=job.run)
                thread.start()
                st.session_state.job = job
                st.session_state.show_results = False
                st.rerun()
        
        if submitted and uploaded_file:
            job = MockSimulationJob(job_id=int(time.time()), prompt=prompt, geometry=uploaded_file.read())
            thread = threading.Thread(target=job.run)
            thread.start()
            st.session_state.job = job
            st.session_state.show_results = False  # Reset view state
            st.rerun()

# ---- Page 2: Progress / Results ----
else:
    st.title("Simulation Progress")
    job = st.session_state.job
    status = job.get_status()
    
    # Live logs
    log_placeholder = st.empty()
    log_placeholder.code("\n".join(status.get("logs", [])), language="bash")
    
    if status.get("state") == "completed":
        st.success("Simulation Complete!")
        
        # Persistent layout using columns for action buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("View Results", use_container_width=True):
                st.session_state.show_results = True
                
        with col2:
            if st.button("Run Another Simulation", use_container_width=True):
                # Complete state wipeout forces a clean return to screen 1
                st.session_state.job = None
                st.session_state.show_results = False
                st.rerun()
                
        # Display results below buttons if activated
        if st.session_state.show_results:
            st.write("### Simulation Metrics")
            results = job.get_results()
            st.json(results)
    else:
        st.spinner("Simulation running in background...")
        time.sleep(2)
        st.rerun()
