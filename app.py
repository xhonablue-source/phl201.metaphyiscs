import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="PHL 201: Metaphysics Visuals", layout="wide")

st.title("🌌 PHL 201: Metaphysics - Wave-Perturbed Reality")

st.markdown("""
### Metaphysical Context
This visualization demonstrates the **epsilon-scale revelation**: that even seemingly perfect spheres dissolve into wave-like perturbations when examined closely. 

- The **perfect sphere** reflects Plato's *ideal Forms*.
- The **wave-perturbed sphere** reveals reality's true vibrational foundation.

💡 **Insight**: Geometry itself is an approximation. Reality at its deepest level is **sinusoidal and relational**.
""")

# Create a sphere
phi = np.linspace(0, np.pi, 50)   # polar angle
theta = np.linspace(0, 2*np.pi, 50)  # azimuthal angle
phi, theta = np.meshgrid(phi, theta)

# Base radius
r = 1

# Perturb the radius with a sinusoidal function
perturb = 0.2 * np.sin(5*theta) * np.sin(5*phi)
r_perturbed = r + perturb

# Convert spherical to Cartesian coordinates
x = r_perturbed * np.sin(phi) * np.cos(theta)
y = r_perturbed * np.sin(phi) * np.sin(theta)
z = r_perturbed * np.cos(phi)

# Create 3D surface plot
fig = go.Figure(data=[go.Surface(x=x, y=y, z=z, colorscale="Viridis")])
fig.update_layout(scene=dict(aspectmode="data"),
                  title="Wave-Perturbed Spherical Reality")

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption("PHL 201 | CognitiveCloud.ai – Exploring logic, geometry, and infinitesimal reality")
