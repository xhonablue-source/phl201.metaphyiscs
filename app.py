import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import List, Dict, Optional

# 🔐 SECURE API KEY HANDLING
# Your API key is stored in Streamlit secrets - students never see it
try:
    ANTHROPIC_API_KEY = st.secrets["ANTHROPIC_API_KEY"]
except KeyError:
    ANTHROPIC_API_KEY = None

# Fallback: Allow manual API key input for testing
if not ANTHROPIC_API_KEY:
    ANTHROPIC_API_KEY = st.sidebar.text_input("🔑 Anthropic API Key (for testing)", type="password")

st.set_page_config(page_title="PHL 201: Metaphysics CognitiveCloud.ai", layout="wide", initial_sidebar_state="expanded")

# Define questions from our metaphysics CognitiveCloud.ai framework
questions = [
    ("The conjunction symbol ∧ geometrically represents:", 
     ["Two lines diverging from a point", "Two lines converging to a single point of truth", "A circular boundary", "An infinite loop"], 
     "Two lines converging to a single point of truth"),
    
    ("In metaphysical terms, the disjunction symbol ∨ embodies:", 
     ["Unity through convergence", "Possibility branching from actuality", "The negation of being", "Temporal causation"], 
     "Possibility branching from actuality"),
    
    ("The geometric form of the negation symbol ¬ represents:", 
     ["Simple denial", "The active principle that defines boundaries of being", "Mathematical subtraction", "Circular reasoning"], 
     "The active principle that defines boundaries of being"),
    
    ("The material implication arrow → metaphysically represents:", 
     ["Spatial direction only", "The arrow of time and causation flowing from conditions to consequences", "Mathematical greater-than relationships", "Religious symbolism"], 
     "The arrow of time and causation flowing from conditions to consequences"),
    
    ("The Greek letter epsilon (ε) in our metaphysical framework represents:", 
     ["A specific numerical value", "The infinitely small that approaches zero but never reaches it", "The largest possible number", "A type of logical operator"], 
     "The infinitely small that approaches zero but never reaches it"),
    
    ("According to string theory's metaphysical implications, the most fundamental level of reality consists of:", 
     ["Point particles", "Sinusoidal vibrating strings", "Linear geometric forms", "Static mathematical objects"], 
     "Sinusoidal vibrating strings"),
    
    ("When we examine any seemingly linear phenomenon at the epsilon (ε) scale, we discover:", 
     ["Perfect straight lines", "Sinusoidal wave patterns", "Empty space", "Circular motions"], 
     "Sinusoidal wave patterns"),
    
    ("The statement 'linearity is infinitely small' means:", 
     ["Lines are very short", "Linear relationships exist only as macroscopic approximations that dissolve into wave-functions at quantum scales", "Geometry doesn't exist", "Mathematics is incorrect"], 
     "Linear relationships exist only as macroscopic approximations that dissolve into wave-functions at quantum scales"),
    
    ("A 2D graph of a sinusoidal function is metaphysically limited because:", 
     ["It uses the wrong mathematical formulas", "It shows only a projection of higher-dimensional wave-reality", "Sine waves don't exist in 2D", "Mathematics cannot describe reality"], 
     "It shows only a projection of higher-dimensional wave-reality"),
    
    ("When we add the z-plane to create true 3D visualization, sinusoidal functions become:", 
     ["Straight lines", "Spherical or helical forms revealing relational interdependence", "Perfect circles", "Mathematical impossibilities"], 
     "Spherical or helical forms revealing relational interdependence"),
    
    ("In 3D spherical reality, every point exists:", 
     ["Independently and separately", "Only in relation to every other point within the totality", "As a perfect mathematical abstraction", "Without any connections"], 
     "Only in relation to every other point within the totality"),
    
    ("In advanced mathematics, when we 'cancel out' infinitesimal quantities (ε → 0), this metaphysically demonstrates:", 
     ["Mathematical error", "That linear causation is a 'non-event' - an approximation rather than fundamental reality", "The importance of very small numbers", "That mathematics is purely abstract"], 
     "That linear causation is a 'non-event' - an approximation rather than fundamental reality"),
    
    ("The universal quantifier ∀ (inverted triangle) geometrically represents:", 
     ["Mathematical multiplication", "Universality 'pouring down' from the Platonic realm into particulars", "Simple logical conjunction", "Temporal sequence"], 
     "Universality 'pouring down' from the Platonic realm into particulars"),
    
    ("The existential quantifier ∃ (backwards E) symbolizes:", 
     ["The letter E written incorrectly", "Emergence from non-being - existence as reflection of possibility becoming actual", "Mathematical division", "Alphabetical order"], 
     "Emergence from non-being - existence as reflection of possibility becoming actual"),
    
    ("The empty set symbol ∅ (circle with diagonal line) paradoxically shows:", 
     ["That nothing exists", "That even 'nothingness' requires bounded structure to be conceivable", "Mathematical error", "The absence of geometry"], 
     "That even 'nothingness' requires bounded structure to be conceivable"),
    
    ("The 'element of' symbol ∈ (stylized epsilon) with its gap represents:", 
     ["Broken mathematics", "How particulars participate in universals without losing individual identity", "Simple membership", "Incomplete knowledge"], 
     "How particulars participate in universals without losing individual identity"),
    
    ("The convertibility of being and truth means:", 
     ["Everything is the same", "Thinking and being share the same underlying geometric/logical structure", "Truth doesn't exist", "Being is purely mental"], 
     "Thinking and being share the same underlying geometric/logical structure"),
    
    ("String theory confirms which ancient metaphysical insight?", 
     ["The world is flat", "Reality is mathematical/musical at its foundation, composed of relationships rather than substances", "Only matter exists", "Time is linear"], 
     "Reality is mathematical/musical at its foundation, composed of relationships rather than substances"),
    
    ("The transition from linear to sinusoidal to spherical reveals the progression:", 
     ["From simple to complex mathematics", "From illusion of separation → wave-like interconnection → holographic totality", "From ancient to modern thinking", "From religion to science"], 
     "From illusion of separation → wave-like interconnection → holographic totality"),
    
    ("In Indra's Net metaphor, each jewel reflects all others, which corresponds to our framework's principle that:", 
     ["Jewelry is valuable", "Each point in spherical reality contains the pattern of the whole", "Reflection is optical illusion", "Networks are technological"], 
     "Each point in spherical reality contains the pattern of the whole"),
    
    ("When linearity collapses at the epsilon scale, what emerges as the fundamental structure?", 
     ["Chaos and randomness", "Sinusoidal wave-patterns revealing relational interdependence", "Perfect geometric forms", "Empty space"], 
     "Sinusoidal wave-patterns revealing relational interdependence"),
    
    ("The deepest metaphysical insight of our framework is that:", 
     ["Mathematics is purely abstract", "Logic symbols encode geometric intuitions about reality's relational structure", "Thinking has no connection to being", "Only material objects exist"], 
     "Logic symbols encode geometric intuitions about reality's relational structure"),
    
    ("The 'meta-geometric principle' suggests that:", 
     ["Geometry is just human invention", "The visual forms of logic symbols embody metaphysical relationships like convergence, divergence, and boundary", "Mathematics and reality are unrelated", "Only linear thinking is valid"], 
     "The visual forms of logic symbols embody metaphysical relationships like convergence, divergence, and boundary"),
    
    ("The biconditional symbol ↔ (double-headed arrow) represents:", 
     ["Two separate directions", "Perfect reciprocity and identity - mutual definition", "Mathematical addition", "Temporal flow"], 
     "Perfect reciprocity and identity - mutual definition"),
    
    ("The ultimate metaphysical revelation of our CognitiveCloud.ai framework is that:", 
     ["Reality is chaotic", "Being is fundamentally relational, wave-like, and holographic rather than linear and mechanical", "Nothing exists", "Only human perception matters"], 
     "Being is fundamentally relational, wave-like, and holographic rather than linear and mechanical")
]

# Session state for quiz control
if 'questions' not in st.session_state:
    st.session_state.questions = questions
if 'current' not in st.session_state:
    st.session_state.current = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'feedback' not in st.session_state:
    st.session_state.feedback = None
if 'selected_answer' not in st.session_state:
    st.session_state.selected_answer = None
if 'answered' not in st.session_state:
    st.session_state.answered = False

def show_question():
    """Display current question with enhanced UI"""
    if st.session_state.current < len(st.session_state.questions):
        q, opts, correct = st.session_state.questions[st.session_state.current]
        
        # Progress bar
        progress = (st.session_state.current + 1) / len(st.session_state.questions)
        st.progress(progress, text=f"Question {st.session_state.current + 1} of {len(st.session_state.questions)}")
        
        st.subheader(f"Question {st.session_state.current + 1}")
        st.write(f"**{q}**")
        
        # Radio button for answers
        if not st.session_state.answered:
            ans = st.radio("Choose your answer:", opts, key=f"q{st.session_state.current}")
            st.session_state.selected_answer = ans
            
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                if st.button("Submit Answer", type="primary"):
                    if ans == correct:
                        st.session_state.feedback = ("success", "✅ Correct! +10 XP")
                        st.session_state.score += 10
                    else:
                        st.session_state.feedback = ("error", f"❌ Incorrect. The answer is: **{correct}**")
                    st.session_state.answered = True
                    st.rerun()
        else:
            # Show the question and selected answer when answered
            st.write(f"**Your answer:** {st.session_state.selected_answer}")
            show_feedback()
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Next Question", type="primary"):
                    st.session_state.current += 1
                    st.session_state.answered = False
                    st.session_state.feedback = None
                    st.session_state.selected_answer = None
                    st.rerun()
            with col2:
                if st.button("Skip to End"):
                    st.session_state.current = len(st.session_state.questions)
                    st.rerun()

def show_feedback():
    """Display feedback with enhanced styling"""
    if st.session_state.feedback:
        typ, msg = st.session_state.feedback
        if typ == "success":
            st.success(msg)
        else:
            st.error(msg)

def show_score():
    """Display current score with styling"""
    col1, col2, col3 = st.columns(3)
    with col2:
        st.metric("Current Score", f"{st.session_state.score} XP", 
                 delta=f"{st.session_state.current} answered")

def restart_quiz():
    """Reset quiz state"""
    if st.button("🔄 Restart Quiz", type="secondary"):
        st.session_state.current = 0
        st.session_state.score = 0
        st.session_state.feedback = None
        st.session_state.selected_answer = None
        st.session_state.answered = False
        st.rerun()

def create_visualizations():
    """Create the metaphysical visualizations"""
    st.header("📊 Metaphysical Visualizations")
    
    # Tabs for different visualizations
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Linear vs Sinusoidal", "3D Spherical Reality", "Wave-Perturbed Reality", "Epsilon Scale", "Interactive Explorer"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Linear Illusion (Macro Scale)")
            x_linear = np.linspace(0, 10, 100)
            y_linear = np.ones_like(x_linear) * 0.5
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(x=x_linear, y=y_linear, mode="lines", 
                                    name="Apparent Linearity", line=dict(color="blue", width=3)))
            fig1.update_layout(title="Linear Approximation", xaxis_title="x", yaxis_title="y")
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            st.subheader("Sinusoidal Reality (True Nature)")
            x_sin = np.linspace(0, 10, 500)
            y_sin = np.sin(x_sin * 2) * 0.5
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=x_sin, y=y_sin, mode="lines", 
                                    name="Wave Reality", line=dict(color="red", width=2)))
            fig2.update_layout(title="Sinusoidal Foundation", xaxis_title="x", yaxis_title="sin(x)")
            st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        st.subheader("3D Spherical Totality")
        phi = np.linspace(0, np.pi, 30)
        theta = np.linspace(0, 2 * np.pi, 30)
        phi, theta = np.meshgrid(phi, theta)
        r = 1
        X = r * np.sin(phi) * np.cos(theta)
        Y = r * np.sin(phi) * np.sin(theta)
        Z = r * np.cos(phi)
        
        fig3 = go.Figure(data=[go.Surface(x=X, y=Y, z=Z, colorscale="Viridis", opacity=0.8)])
        fig3.update_layout(title="Holographic Sphere of Relational Being", 
                          scene=dict(aspectmode="cube"))
        st.plotly_chart(fig3, use_container_width=True)
        st.info("💡 **Insight**: Every point on this sphere exists only in relation to all other points - no isolated existence possible.")
    
    with tab3:
        st.subheader("Wave-Perturbed Reality: Perfect Forms Dissolve")
        
        # Controls for the perturbation
        col1, col2 = st.columns(2)
        with col1:
            wave_frequency = st.slider("Wave Frequency", 1, 10, 5, 1, 
                                     help="How many waves appear on the sphere surface")
        with col2:
            perturbation_strength = st.slider("Perturbation Strength", 0.0, 0.5, 0.2, 0.05,
                                            help="How much the waves distort the perfect sphere")
        
        # Create the perturbed sphere
        phi = np.linspace(0, np.pi, 50)   # polar angle
        theta = np.linspace(0, 2*np.pi, 50)  # azimuthal angle
        phi, theta = np.meshgrid(phi, theta)
        
        # Base radius
        r = 1
        
        # Perturb the radius with sinusoidal function
        perturb = perturbation_strength * np.sin(wave_frequency*theta) * np.sin(wave_frequency*phi)
        r_perturbed = r + perturb
        
        # Convert spherical to Cartesian coordinates
        x = r_perturbed * np.sin(phi) * np.cos(theta)
        y = r_perturbed * np.sin(phi) * np.sin(theta)
        z = r_perturbed * np.cos(phi)
        
        # Create comparison: perfect vs perturbed
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Perfect Sphere (Platonic Ideal)**")
            # Perfect sphere
            x_perfect = 1 * np.sin(phi) * np.cos(theta)
            y_perfect = 1 * np.sin(phi) * np.sin(theta)
            z_perfect = 1 * np.cos(phi)
            
            fig_perfect = go.Figure(data=[go.Surface(x=x_perfect, y=y_perfect, z=z_perfect, 
                                                   colorscale="Blues", opacity=0.8)])
            fig_perfect.update_layout(scene=dict(aspectmode="cube", 
                                               xaxis=dict(range=[-1.5, 1.5]),
                                               yaxis=dict(range=[-1.5, 1.5]),
                                               zaxis=dict(range=[-1.5, 1.5])),
                                    title="Geometric Ideal")
            st.plotly_chart(fig_perfect, use_container_width=True)
        
        with col2:
            st.write("**Wave-Perturbed Reality (ε-Scale Truth)**")
            # Perturbed sphere
            fig_perturbed = go.Figure(data=[go.Surface(x=x, y=y, z=z, 
                                                     colorscale="Plasma", opacity=0.8)])
            fig_perturbed.update_layout(scene=dict(aspectmode="cube",
                                                 xaxis=dict(range=[-1.5, 1.5]),
                                                 yaxis=dict(range=[-1.5, 1.5]),
                                                 zaxis=dict(range=[-1.5, 1.5])),
                                      title="Sinusoidal Reality")
            st.plotly_chart(fig_perturbed, use_container_width=True)
        
        # Metaphysical explanation
        if perturbation_strength > 0.1:
            st.success("🌊 **Epsilon Revelation**: Even 'perfect' geometric forms dissolve into wave patterns when examined closely!")
        else:
            st.info("💡 Increase perturbation strength to see how geometric ideals become wave-reality at the ε-scale.")
        
        st.markdown("""
        **Metaphysical Insight**: This demonstrates that what Plato called "perfect Forms" are actually 
        sinusoidal perturbations when examined at the epsilon (ε) scale. The "perfect sphere" is a 
        macroscopic approximation - reality's foundation is wave-like vibration.
        
        - **Left**: The Platonic ideal - what we think reality should be
        - **Right**: Actual reality - waves perturbing perfect forms
        - **Truth**: Geometry itself emerges from underlying sinusoidal patterns
        """)
    
    with tab4:
        st.subheader("Epsilon (ε) Scale Revelation")
        epsilon_scale = st.slider("Zoom to Epsilon Scale", 0.01, 1.0, 0.1, 0.01)
        
        x_eps = np.linspace(-epsilon_scale, epsilon_scale, 1000)
        frequency = 1 / (epsilon_scale * 0.1)
        y_eps = np.sin(frequency * x_eps)
        
        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(x=x_eps, y=y_eps, mode="lines", 
                                name=f"ε = {epsilon_scale}", line=dict(color="purple")))
        fig4.update_layout(title=f"Infinitesimal Scale (ε = {epsilon_scale})", 
                          xaxis_title="ε-scale position", yaxis_title="Wave amplitude")
        st.plotly_chart(fig4, use_container_width=True)
        
        if epsilon_scale < 0.05:
            st.success("🎯 **Linearity Collapses!** At this scale, everything is wave-like.")
    
    with tab5:
        st.subheader("Interactive Metaphysical State Explorer")
        mode = st.selectbox("Choose metaphysical perspective:", [
            "Linear Illusion (Macroscopic)",
            "Sinusoidal Emergence (ε Scale)",
            "3D Transcendence (Dimensional)",
            "Point Interdependence (Relational)",
            "Spherical Totality (Holographic)",
            "Wave-Perturbed Forms (Epsilon Reality)"
        ])
        
        if mode == "Linear Illusion (Macroscopic)":
            st.write("**State**: Conventional reality - straight lines and linear causation")
            # Show linear visualization
        elif mode == "Sinusoidal Emergence (ε Scale)":
            st.write("**State**: Wave nature revealed - linearity dissolves into oscillation")
            # Show sinusoidal visualization
        elif mode == "3D Transcendence (Dimensional)":
            st.write("**State**: Breaking free from 2D projections into true dimensional reality")
            # Show 3D visualization
        elif mode == "Point Interdependence (Relational)":
            st.write("**State**: No isolated points - everything exists through relationships")
            # Show network visualization
        elif mode == "Spherical Totality (Holographic)":
            st.write("**State**: Complete holographic reality where each part contains the whole")
            # Show sphere visualization
        elif mode == "Wave-Perturbed Forms (Epsilon Reality)":
            st.write("**State**: Perfect geometric forms reveal their sinusoidal foundation")
            # Quick perturbed sphere
            phi_quick = np.linspace(0, np.pi, 25)
            theta_quick = np.linspace(0, 2*np.pi, 25)
            phi_quick, theta_quick = np.meshgrid(phi_quick, theta_quick)
            r_quick = 1 + 0.15 * np.sin(4*theta_quick) * np.sin(4*phi_quick)
            x_quick = r_quick * np.sin(phi_quick) * np.cos(theta_quick)
            y_quick = r_quick * np.sin(phi_quick) * np.sin(theta_quick)
            z_quick = r_quick * np.cos(phi_quick)
            
            fig_quick = go.Figure(data=[go.Surface(x=x_quick, y=y_quick, z=z_quick, 
                                                 colorscale="Plasma", opacity=0.8)])
            fig_quick.update_layout(scene=dict(aspectmode="cube"), 
                                  title="Geometric Forms at Epsilon Scale")
            st.plotly_chart(fig_quick, use_container_width=True)

# Main Application Layout
st.title("🧠 PHL 201: Metaphysics CognitiveCloud.ai")
st.markdown("**Xavier Honablue M.Ed. | Wayne County Community College District**")

# Sidebar for navigation
with st.sidebar:
    st.header("📚 Navigation")
    page = st.radio("Choose Section:", [
        "Course Overview", 
        "Interactive Quiz", 
        "Visualizations", 
        "Logic Symbol Reference",
        "Resources & Further Reading",
        "🤖 AI Philosophy Assistant"
    ])
    
    st.markdown("---")
    st.subheader("📈 Your Progress")
    if st.session_state.questions:
        progress_pct = (st.session_state.current / len(st.session_state.questions)) * 100
        st.metric("Completion", f"{progress_pct:.1f}%")
        st.metric("Score", f"{st.session_state.score} XP")

# Main content based on page selection
if page == "Course Overview":
    st.header("🌟 Metaphysics Through Logic Symbol Geometry")
    
    st.markdown("""
    Welcome to **CognitiveCloud.ai's** revolutionary approach to metaphysics! This course explores how the **geometry of logic symbols** 
    encodes deep metaphysical truths about the nature of reality.
    
    ## 🎯 Core Insights
    
    **Logic Symbols as Geometric Intuitions:**
    - **∧ (AND)**: Convergence - two paths meeting at truth
    - **∨ (OR)**: Divergence - one reality branching into possibilities  
    - **¬ (NOT)**: Boundary creation - the active principle of negation
    - **→ (IMPLIES)**: Directional flow - the arrow of causation
    - **ε (Epsilon)**: The infinitely small that reveals wave-reality
    
    ## 🌊 The Epsilon Revolution
    
    At the **epsilon (ε) scale**, linearity collapses! What appears as straight lines at human scale 
    dissolves into **sinusoidal wave patterns** - confirming string theory's insight that reality 
    is fundamentally vibrational and relational.
    
    ## 🔮 Dimensional Transcendence
    
    - **1D**: Linear illusion (macro view)
    - **2D**: Sinusoidal projections (partial truth)  
    - **3D**: Spherical totality (holographic reality)
    
    **Meta-Geometric Principle**: The visual forms of logic symbols embody the structure of reality itself.
    """)
    
elif page == "Interactive Quiz":
    st.header("🎯 Test Your Metaphysical Understanding")
    
    show_score()
    
    if st.session_state.current < len(st.session_state.questions):
        show_question()
    else:
        st.balloons()
        st.success(f"🎉 **Quiz Complete!** Final Score: {st.session_state.score} XP")
        
        # Performance analysis
        total_possible = len(st.session_state.questions) * 10
        percentage = (st.session_state.score / total_possible) * 100
        
        if percentage >= 90:
            st.success("🏆 **Metaphysical Master!** You've transcended linear thinking.")
        elif percentage >= 80:
            st.info("🎓 **Advanced Understanding** - You grasp the epsilon principle!")
        elif percentage >= 70:
            st.warning("📚 **Good Progress** - Continue exploring dimensional transcendence.")
        else:
            st.error("🔄 **Keep Learning** - The path to geometric wisdom continues.")
        
        restart_quiz()

elif page == "Visualizations":
    create_visualizations()

elif page == "Logic Symbol Reference":
    st.header("📖 Logic Symbol Geometry Reference")
    
    symbols_data = {
        "∧": ("Conjunction (AND)", "Two lines converging", "Unity through convergence - multiple conditions aligning"),
        "∨": ("Disjunction (OR)", "Two lines diverging", "Possibility branching from actuality"),
        "¬": ("Negation (NOT)", "Line with perpendicular hook", "Active principle defining boundaries of being"),
        "→": ("Material Implication", "Arrow pointing forward", "Directional flow of causation through time"),
        "↔": ("Biconditional", "Double-headed arrow", "Perfect reciprocity and mutual definition"),
        "∀": ("Universal Quantifier", "Inverted triangle", "Universality flowing down into particulars"),
        "∃": ("Existential Quantifier", "Backwards E", "Emergence from non-being into existence"),
        "∅": ("Empty Set", "Circle with diagonal slash", "Bounded nothingness - emptiness with structure"),
        "∈": ("Element Of", "Curved line with gap", "Participation without complete absorption"),
        "ε": ("Epsilon", "Curved line almost closing", "The infinitely small revealing wave-reality"),
        "∞": ("Infinity", "Figure-8 rotated", "Eternal return and self-containment"),
        "≡": ("Equivalence", "Three parallel lines", "Identity across multiple modes of being")
    }
    
    for symbol, (name, geometry, meaning) in symbols_data.items():
        with st.expander(f"**{symbol}** - {name}"):
            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown(f"## {symbol}")
            with col2:
                st.write(f"**Geometric Form**: {geometry}")
                st.write(f"**Metaphysical Meaning**: {meaning}")

elif page == "Resources & Further Reading":
    st.header("🎯 Interactive Philosophy Resources")
    
    # Create tabs for different resource categories
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Quick Start", "Interactive Logic", "Philosophy Videos", "Research Tools", "Practice Hub"])
    
    with tab1:
        st.subheader("🚀 Jump Into Philosophy")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📚 Essential First Reads")
            
            # Stanford Encyclopedia button - opens link
            if st.button("📖 Stanford Encyclopedia: Metaphysics", use_container_width=True):
                st.markdown("**Opening Stanford Encyclopedia of Philosophy...**")
                st.markdown("**[Click here to access: Stanford Encyclopedia - Metaphysics](https://plato.stanford.edu/entries/metaphysics/)**")
                st.success("Authoritative overview of metaphysical concepts - perfect for understanding the foundations behind our symbolic framework.")
            
            # Nagel PDF button  
            if st.button("🧠 What Does It All Mean? (Free PDF)", use_container_width=True):
                st.markdown("**Thomas Nagel's Classic Introduction**")
                st.markdown("**[Access through Internet Archive](https://archive.org/details/whatdoesitallmea0000nage)**")
                st.success("Essential 100-page introduction to philosophy. Check your university library's digital access for the latest edition.")
            
            # Philosophy Bites button
            if st.button("🎭 Philosophy Bites Podcast", use_container_width=True):
                st.markdown("**[Listen to Philosophy Bites](https://www.philosophybites.com/)**")
                st.success("15-minute philosophy podcasts with world-class philosophers. Start with their logic and metaphysics episodes.")
                
                # Show recent episode suggestions
                st.markdown("**Recommended episodes:**")
                st.markdown("- 'Logic and Language' with Susan Haack")
                st.markdown("- 'Metaphysics' with Peter van Inwagen") 
                st.markdown("- 'What is Philosophy?' with Simon Critchley")
        
        with col2:
            st.markdown("### 🔗 Logic Foundations")
            
            # Interactive Logic Tutorial
            if st.button("⚡ Interactive Logic Tutorial", use_container_width=True):
                st.markdown("**[Open Logitext - MIT's Visual Logic Tool](https://logitext.mit.edu/main)**")
                st.success("MIT's interactive logic tool. Practice the symbols we explore in class with immediate feedback.")
                
                # Embed a simple logic exercise
                st.markdown("**Try this in Logitext:**")
                st.code("P ∧ Q → R")
                st.info("This reads: 'If P and Q, then R' - notice how ∧ shows convergence leading to implication →")
            
            # Truth Table Generator  
            if st.button("🎯 Truth Table Generator", use_container_width=True):
                st.markdown("**[Open Stanford Truth Table Tool](https://web.stanford.edu/class/cs103/tools/truth-table-tool/)**")
                st.success("Stanford's tool for testing logical expressions. Input ∧, ∨, ¬ and see how they work.")
                
                # Show embedded truth table example
                st.markdown("**Quick example - try this expression: `P ∧ Q`**")
                col_a, col_b, col_c, col_d = st.columns(4)
                with col_a:
                    st.write("**P**")
                    st.write("T")
                    st.write("T") 
                    st.write("F")
                    st.write("F")
                with col_b:
                    st.write("**Q**")
                    st.write("T")
                    st.write("F")
                    st.write("T") 
                    st.write("F")
                with col_c:
                    st.write("**P∧Q**")
                    st.write("T")
                    st.write("F")
                    st.write("F")
                    st.write("F")
                with col_d:
                    st.write("**Meaning**")
                    st.write("Both true")
                    st.write("P true, Q false")
                    st.write("P false, Q true")
                    st.write("Both false")
            
            # Argument Mapper
            if st.button("📊 Argument Mapper", use_container_width=True):
                st.markdown("**[Open Rationale Online](https://www.rationaleonline.com/)**")
                st.success("Visual argument analysis - see how premises connect to conclusions geometrically.")
                
                # Show argument structure example
                st.markdown("**Example argument structure:**")
                st.markdown("""
                ```
                Premise 1: All logic symbols have geometric meaning
                Premise 2: ∧ is a logic symbol
                ────────────────────────────────────────────────
                Conclusion: Therefore, ∧ has geometric meaning
                ```
                """)
                st.info("Notice the geometric flow from premises to conclusion - just like ∧ shows convergence!")
    
    with tab2:
        st.subheader("🔧 Interactive Logic Practice")
        
        st.markdown("### Quick Logic Challenges")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🎮 Logic Game 1: Symbol Matching", use_container_width=True):
                st.markdown("**Challenge: Match symbols to meanings**")
                symbols = ["∧", "∨", "¬", "→", "↔"]
                meanings = ["AND", "OR", "NOT", "IMPLIES", "IF AND ONLY IF"]
                
                # Simple matching exercise
                st.write("**Symbols:** " + " | ".join(symbols))
                st.write("**Meanings:** " + " | ".join(meanings))
                
                answer = st.text_input("Type your matches (e.g., ∧=AND, ∨=OR...)")
                if st.button("Check Answer"):
                    if "∧=AND" in answer and "∨=OR" in answer:
                        st.success("Correct! You understand the basic geometric intuitions.")
                    else:
                        st.error("Try again - think about convergence vs divergence.")
        
        with col2:
            if st.button("🧩 Logic Game 2: Truth Tables", use_container_width=True):
                st.markdown("**Challenge: Complete the truth table**")
                
                # Simple truth table practice
                st.write("**P ∧ Q (P AND Q)**")
                st.write("P=True, Q=True → ?")
                st.write("P=True, Q=False → ?")
                st.write("P=False, Q=True → ?")
                st.write("P=False, Q=False → ?")
                
                answers = st.multiselect("Select correct outputs:", ["True", "False", "True", "False", "True", "False", "True", "False"])
                if st.button("Check Truth Table"):
                    if answers == ["True", "False", "False", "False"]:
                        st.success("Perfect! ∧ requires both conditions to converge.")
                    else:
                        st.error("Remember: ∧ is true only when both inputs are true.")
        
        with col3:
            if st.button("🌊 Epsilon Challenge", use_container_width=True):
                st.markdown("**Challenge: Epsilon intuition**")
                
                epsilon_input = st.slider("What happens as ε approaches 0?", 0.01, 1.0, 0.5)
                
                if epsilon_input < 0.1:
                    st.success("Exactly! As ε→0, linearity collapses into wave patterns.")
                    st.write("🌊 You're grasping the infinitesimal principle!")
                else:
                    st.info("Try moving the slider closer to zero...")
    
    with tab3:
        st.subheader("🎬 Philosophy in Action")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📺 Essential Philosophy Videos")
            
            if st.button("🏛️ Plato's Cave (Animated)", use_container_width=True):
                st.markdown("**[TED-Ed: Plato's Allegory of the Cave](https://www.youtube.com/watch?v=1RWOpQXTltA)**")
                st.info("4-minute animated explanation - connects to our dimensional transcendence concepts.")
            
            if st.button("🧠 What is Consciousness?", use_container_width=True):
                st.markdown("**[Crash Course Philosophy #8](https://www.youtube.com/watch?v=GDrBFu5diBs)**")
                st.info("Explores the hard problem of consciousness - relates to our being/thinking unity.")
            
            if st.button("⚖️ Kant in 90 Seconds", use_container_width=True):
                st.markdown("**[Philosophy Tube: Kant](https://www.youtube.com/watch?v=xwOCmJevigw)**")
                st.info("Quick intro to transcendental idealism - connects to our meta-geometric principles.")
        
        with col2:
            st.markdown("### 🎓 Academic Lectures")
            
            if st.button("🔬 MIT: Metaphysics Lecture", use_container_width=True):
                st.markdown("**[MIT OpenCourseWare](https://ocw.mit.edu/courses/linguistics-and-philosophy/24-221-metaphysics-fall-2005/)**")
                st.info("Full university-level metaphysics course materials available free.")
            
            if st.button("📐 Logic & Mathematics", use_container_width=True):
                st.markdown("**[Stanford: Mathematical Logic](https://www.youtube.com/playlist?list=PL_onPhFCkVQiZgE9U539_QmKLJV_0YvlQ)**")
                st.info("Deep dive into formal logic systems - foundation for symbolic reasoning.")
            
            if st.button("🌀 String Theory & Philosophy", use_container_width=True):
                st.markdown("**[Royal Institution Lectures](https://www.youtube.com/watch?v=YtdE662eY_M)**")
                st.info("Physics meets philosophy - explores the mathematical nature of reality.")
    
    with tab4:
        st.subheader("🔍 Research & Analysis Tools")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🗃️ Academic Databases")
            
            if st.button("📚 PhilPapers Search", use_container_width=True):
                st.markdown("**[PhilPapers.org](https://philpapers.org/)**")
                st.info("Search over 2.9 million philosophy papers. Try searching 'logic symbolism' or 'metaphysics mathematics'.")
                
                search_term = st.text_input("Quick search term:")
                if search_term:
                    st.markdown(f"**[Search PhilPapers for '{search_term}'](https://philpapers.org/s/{search_term})**")
            
            if st.button("🎓 Stanford Encyclopedia", use_container_width=True):
                st.markdown("**[Stanford Encyclopedia of Philosophy](https://plato.stanford.edu/)**")
                st.info("Gold standard for philosophical information - peer-reviewed and authoritative.")
            
            if st.button("📖 Internet Encyclopedia", use_container_width=True):
                st.markdown("**[Internet Encyclopedia of Philosophy](https://iep.utm.edu/)**")
                st.info("Comprehensive philosophy articles - good for getting different perspectives.")
        
        with col2:
            st.markdown("### 🛠️ Analysis Tools")
            
            if st.button("🗺️ Argument Mapping", use_container_width=True):
                st.markdown("**[Rationale Online](https://www.rationaleonline.com/)**")
                st.info("Visual argument analysis - map premises and conclusions like geometric structures.")
            
            if st.button("📊 Logic Checker", use_container_width=True):
                st.markdown("**[Logic & Arguments](https://logic.stanford.edu/)**")
                st.info("Stanford's logic tools - verify symbolic logic expressions.")
            
            if st.button("🔬 Citation Builder", use_container_width=True):
                st.markdown("**[ZBib by Zotero](https://zbib.org/)**")
                st.info("Auto-generate citations for philosophy papers - just paste URLs.")
    
    with tab5:
        st.subheader("💪 Philosophy Practice Hub")
        
        st.markdown("### Quick Philosophy Workouts")
        
        practice_type = st.selectbox("Choose your practice:", [
            "Argument Analysis",
            "Symbol Translation", 
            "Thought Experiments",
            "Definition Building"
        ])
        
        if practice_type == "Argument Analysis":
            st.markdown("**Practice: Break down this argument**")
            argument = st.text_area("Paste an argument here:", 
                                   "All logic symbols have geometric meaning. ∧ is a logic symbol. Therefore, ∧ has geometric meaning.")
            
            if st.button("Analyze Structure"):
                if argument:
                    st.write("**Premise 1:** All logic symbols have geometric meaning")
                    st.write("**Premise 2:** ∧ is a logic symbol") 
                    st.write("**Conclusion:** Therefore, ∧ has geometric meaning")
                    st.write("**Form:** Valid syllogism (All A are B, X is A, therefore X is B)")
        
        elif practice_type == "Symbol Translation":
            st.markdown("**Practice: Translate to symbols**")
            english = st.text_input("English statement:", "If it rains, then the ground gets wet")
            
            if st.button("Show Translation"):
                if "if" in english.lower() and "then" in english.lower():
                    st.write("**Symbolic form:** P → Q")
                    st.write("**Where:** P = 'it rains', Q = 'ground gets wet'")
                    st.write("**Geometric meaning:** Arrow shows causal flow")
        
        elif practice_type == "Thought Experiments":
            experiments = [
                "🧠 **Ship of Theseus**: If you replace every part of a ship, is it still the same ship?",
                "🏛️ **Plato's Cave**: What if everything you think is real is just shadows?", 
                "🤖 **Chinese Room**: Can a computer truly understand, or just manipulate symbols?",
                "∞ **Infinite Hotel**: A hotel with infinite rooms gets a new guest..."
            ]
            
            selected = st.selectbox("Choose a thought experiment:", experiments)
            if st.button("Explore This"):
                st.info("Think through the implications... what does this reveal about reality's nature?")
        
        elif practice_type == "Definition Building":
            st.markdown("**Practice: Define key terms**")
            term = st.selectbox("Define:", ["Metaphysics", "Logic", "Epsilon", "Being", "Truth"])
            
            definition = st.text_area(f"Your definition of {term}:")
            
            if st.button("Compare with Standard"):
                definitions = {
                    "Metaphysics": "The branch of philosophy that examines the nature of reality, being, and existence itself.",
                    "Logic": "The study of valid reasoning and argument structure.",
                    "Epsilon": "In mathematics, an arbitrarily small positive quantity; in our framework, the infinitesimal scale where linearity dissolves.",
                    "Being": "The quality or state of existence; what it means for something to exist.",
                    "Truth": "Correspondence between statements and reality; in our framework, convertible with being itself."
                }
                st.write(f"**Standard definition:** {definitions[term]}")
                if definition:
                    st.write(f"**Your definition:** {definition}")
    
    st.markdown("---")
    st.warning("**Academic Note**: This course presents an interpretive framework connecting logic symbols to metaphysical concepts. While this can stimulate philosophical thinking, distinguish between established scholarship and speculative frameworks when conducting research.")
    
    # Quick access footer
    st.markdown("### 🔗 Quick Links")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("**[Stanford Phil](https://plato.stanford.edu/)**")
    with col2:
        st.markdown("**[PhilPapers](https://philpapers.org/)**")
    with col3:
        st.markdown("**[MIT Logic](https://logitext.mit.edu/)**")
    with col4:
        st.markdown("**[Philosophy Bites](https://www.philosophybites.com/)**")

elif page == "🤖 AI Philosophy Assistant":
    st.header("🤖 AI Philosophy Assistant")
    st.markdown("**Ask deep questions about metaphysics, logic symbols, and the nature of reality**")
    
    # Check if API key is available
    if not ANTHROPIC_API_KEY:
        st.error("🔑 API key required. Please add your Anthropic API key in the sidebar to use the AI assistant.")
        st.info("This feature requires an Anthropic API key to function. Contact your instructor if you need access.")
    else:
        try:
            import anthropic
            
            # Initialize Anthropic client
            client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
            
            # Suggested important questions
            st.subheader("💡 Suggested Philosophical Questions")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Logic & Symbols:**")
                if st.button("Why do logic symbols have geometric shapes?", use_container_width=True):
                    st.session_state.current_question = "Why do logic symbols have geometric shapes? How does their visual form relate to their meaning?"
                
                if st.button("What is the epsilon (ε) principle?", use_container_width=True):
                    st.session_state.current_question = "Explain the epsilon principle and how it reveals that linearity is infinitely small."
                
                if st.button("How does ∧ embody convergence?", use_container_width=True):
                    st.session_state.current_question = "How does the conjunction symbol ∧ geometrically represent convergence and unity in metaphysics?"
            
            with col2:
                st.markdown("**Metaphysical Foundations:**")
                if st.button("What is the relationship between being and truth?", use_container_width=True):
                    st.session_state.current_question = "What does it mean that being and truth are convertible? How do thinking and reality share the same structure?"
                
                if st.button("Why is reality wave-like rather than linear?", use_container_width=True):
                    st.session_state.current_question = "How does string theory confirm that reality is fundamentally wave-like and relational rather than linear and mechanical?"
                
                if st.button("What is spherical totality?", use_container_width=True):
                    st.session_state.current_question = "Explain the concept of spherical totality where each point contains the pattern of the whole."
            
            # Initialize chat history in session state
            if 'chat_history' not in st.session_state:
                st.session_state.chat_history = []
            
            # Handle suggested questions
            if 'current_question' in st.session_state:
                st.session_state.user_input = st.session_state.current_question
                del st.session_state.current_question
            
            # Chat interface
            st.subheader("💬 Philosophy Chat")
            
            # Display chat history
            for i, (question, answer) in enumerate(st.session_state.chat_history):
                with st.container():
                    st.markdown(f"**🧠 You:** {question}")
                    st.markdown(f"**🤖 Assistant:** {answer}")
                    st.markdown("---")
            
            # User input
            user_question = st.text_area(
                "Ask your philosophical question:",
                value=st.session_state.get('user_input', ''),
                height=100,
                placeholder="e.g., How do logic symbols encode the structure of reality?"
            )
            
            col1, col2 = st.columns([1, 4])
            with col1:
                ask_button = st.button("🔮 Ask Assistant", type="primary")
            with col2:
                if st.button("🗑️ Clear Chat History"):
                    st.session_state.chat_history = []
                    st.rerun()
            
            if ask_button and user_question.strip():
                with st.spinner("🤔 Contemplating your philosophical question..."):
                    try:
                        # Create context-aware prompt
                        system_prompt = """You are a philosophical assistant specializing in metaphysics and logic. You're helping students in a course that explores how logic symbols encode geometric intuitions about reality's structure. The course framework includes:

1. Logic symbols as geometric forms (∧ = convergence, ∨ = divergence, ¬ = boundary creation)
2. The epsilon (ε) principle: linearity is infinitely small and dissolves into wave patterns
3. String theory connections to sinusoidal foundations of reality
4. Dimensional transcendence from linear to spherical totality
5. The convertibility of being and truth

Provide thoughtful, academically rigorous responses that connect to these themes while acknowledging when ideas are interpretive frameworks versus established scholarship. Be clear about distinguishing between metaphorical/pedagogical frameworks and empirical claims."""

                        # Get response from Claude
                        message = client.messages.create(
                            model="claude-3-haiku-20240307",
                            max_tokens=1000,
                            temperature=0.7,
                            system=system_prompt,
                            messages=[{
                                "role": "user", 
                                "content": user_question
                            }]
                        )
                        
                        response = message.content[0].text
                        
                        # Add to chat history
                        st.session_state.chat_history.append((user_question, response))
                        
                        # Clear input
                        st.session_state.user_input = ""
                        
                        # Rerun to show new response
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error getting response: {str(e)}")
                        st.info("Please check your API key and try again.")
        
        except ImportError:
            st.error("📦 Missing required library. Please install: `pip install anthropic`")
            st.info("The Anthropic library is required for the AI assistant functionality.")
    
    # Philosophy tips
    st.markdown("---")
    st.subheader("💡 Tips for Philosophical Inquiry")
    
    tip_cols = st.columns(3)
    with tip_cols[0]:
        st.markdown("""
        **🤔 Ask Deep Questions**
        - Why does this concept exist?
        - What assumptions am I making?
        - How do the pieces connect?
        """)
    
    with tip_cols[1]:
        st.markdown("""
        **🔍 Examine Closely**
        - What exactly does this mean?
        - Can I think of counterexamples?
        - What would critics say?
        """)
    
    with tip_cols[2]:
        st.markdown("""
        **🌐 Connect Ideas**
        - How does this relate to other concepts?
        - What are the implications?
        - Where does this lead?
        """)

# Footer
st.markdown("---")
st.markdown("**Built with 💭 by CognitiveCloud.ai | PHL 201 - Introduction to Philosophy**")
st.caption("© 2024 Wayne County Community College District")
