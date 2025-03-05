import numpy as np
import plotly.graph_objects as go

# Define spatial dimensions
x = np.linspace(-10, 10, 20)
y = np.linspace(-10, 10, 20)
z = np.linspace(-10, 10, 20)
X, Y, Z = np.meshgrid(x, y, z)

# Define wave parameters
kx = 1      # Wave number in x-direction
ky = 1     # Wave number in y-direction
kz = 1      # Wave number in z-direction
omega = 1   # Angular frequency

"""
The angular frequency (omega) is set to 1 for simplicity in this visualization.
In general, omega is calculated as omega = 2 * pi * f, where f is the frequency of the wave.
For simplicity, we use omega = 1 to create a clean, consistent wave motion for the animation.
"""

# Number of frames for animation
n_frames = 50
time_values = np.linspace(0, 10, n_frames)  # Time values for each frame

# Create the figure
fig = go.Figure()

# Add the initial isosurface trace (for t=0)
fig.add_trace(go.Isosurface(
    x=X.flatten(),
    y=Y.flatten(),
    z=Z.flatten(),
    value=np.sin(kx * X + ky * Y + kz * Z - omega * 0).flatten(),  # Initial state
    isomin=-1,
    isomax=1,
    surface_count=5,
    colorscale='plasma',
    opacity=0.6,
    colorbar=dict(title="Wave Amplitude")
))

# Create frames for the animation
frames = []
for t in time_values:
    Z_wave = np.sin(kx * X + ky * Y + kz * Z - omega * t)
    print(f"Calculating and creating frame for time t = {t}")  # Print statement added
    frame = go.Frame(
        data=[go.Isosurface(
            x=X.flatten(),
            y=Y.flatten(),
            z=Z.flatten(),
            value=Z_wave.flatten(),
            isomin=-1,
            isomax=1,
            surface_count=5,
            colorscale='plasma',
            opacity=0.6
        )],
        name=f"frame_{t}",
        layout=dict(annotations=[dict(
            text=f"Time = {t:.2f}",  # Display time in annotation
            x=0.1,
            y=0.9,
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(size=14, color="white")
        )])
    )
    frames.append(frame)

# Add frames to the figure
fig.frames = frames

# Add animation controls, main title, and the TIME SLIDER
fig.update_layout(
    title='3D Wavefront Propagation in Space and Time',  # Main title
    annotations=[  # Main title annotation (moved here)
        dict(
            text="3D Wave Propagation Over Time",
            x=0.5,
            y=1.1,             
            xref="paper",  # Now correctly scoped
            yref="paper",  # Now correctly scoped
            showarrow=False,
            font=dict(size=14, color="black")
        )
    ],
    scene=dict(  # Scene layout only for axis titles
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z',
    ),
     sliders=[dict(
        active=0,  # Start at the first frame
        currentvalue={"prefix": "Time: "},  # Label before the time value
        pad={"t": 50},  # Add some padding at the top                   
        steps=[dict(
            label=f"{t:.2f}",  # Label for each step (time value)
            method="animate",
            args=[[f"frame_{t}"],  # Animate to the corresponding frame
                  {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}] #Go to frame without animation
        ) for t in time_values]
    )],
    updatemenus=[dict(
        type="buttons",
        buttons=[dict(label="Play",
                      method="animate",
                      args=[None, {"frame": {"duration": 100, "redraw": True}, "fromcurrent": True}])]
    )]
)

# Add subtitle/description (this is fine where it is)
fig.add_annotation(
    text="This visualization shows a 3D wave propagating through space over time. The wave's amplitude is represented by color, and its shape evolves as time progresses.",
    x=0.5,
    y=-0.1,
    xref="paper",
    yref="paper",
    showarrow=False,
    font=dict(size=12, color="gray")
)

fig.show()