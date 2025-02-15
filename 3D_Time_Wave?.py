import numpy as np
import plotly.graph_objects as go

# Define time dimensions
t_x = np.linspace(-10, 10, 30)
t_y = np.linspace(-10, 10, 30)
t_z = np.linspace(-10, 10, 30)
T_x, T_y, T_z = np.mgrid[-10:10:30j, -10:10:30j, -10:10:30j]  # Use mgrid for structured grid

# Define wave parameters
omega_x = 1  # Angular frequency in T_x direction
omega_y = 1  # Angular frequency in T_y direction
omega_z = 1  # Angular frequency in T_z direction

# Choose which axis to animate: "x", "y", or "z"
animated_axis = "x"  # Change this to "x", "y", or "z"

# Select the correct time array based on user choice
if animated_axis == "x":
    time_values = t_x
    wave_function = lambda tx: np.sin(omega_x * tx + omega_y * T_y + omega_z * T_z)
elif animated_axis == "y":
    time_values = t_y
    wave_function = lambda ty: np.sin(omega_x * T_x + omega_y * ty + omega_z * T_z)
else:  # Default to "z"
    time_values = t_z
    wave_function = lambda tz: np.sin(omega_x * T_x + omega_y * T_y + omega_z * tz)

# Create the figure
fig = go.Figure()

# Compute initial wave state (at first time value)
initial_wave = wave_function(time_values[0])

fig.add_trace(go.Isosurface(
    x=T_x.flatten(),
    y=T_y.flatten(),
    z=T_z.flatten(),
    value=initial_wave.flatten(),
    isomin=-1,
    isomax=1,
    surface_count=5,
    colorscale='plasma',
    opacity=0.6,
    colorbar=dict(title="Wave Amplitude")
))

# Create frames for animation
frames = []
for t_val in time_values:
    wave_3d_time = wave_function(t_val)
    frame = go.Frame(
        data=[go.Isosurface(
            x=T_x.flatten(),
            y=T_y.flatten(),
            z=T_z.flatten(),
            value=wave_3d_time.flatten(),
            isomin=-1,
            isomax=1,
            surface_count=5,
            colorscale='plasma',
            opacity=0.6
        )],
        name=f"frame_{t_val:.2f}"
    )
    frames.append(frame)

# Add frames to the figure
fig.frames = frames

# Add animation controls
fig.update_layout(
    title=f"Wave in 3D Time (Animated along {animated_axis.upper()})",
    scene=dict(
        xaxis_title="T_x (Time Dimension 1)",
        yaxis_title="T_y (Time Dimension 2)",
        zaxis_title="T_z (Time Dimension 3)",
    ),
    updatemenus=[dict(                
        type="buttons",
        buttons=[
            dict(
                label="Play",
                method="animate",
                args=[None, {"frame": {"duration": 100, "redraw": True}, "fromcurrent": True}]
            )
        ]
    )],
    sliders=[
        dict(
            steps=[
                dict(
                    method="animate",
                    args=[[f"frame_{t_val:.2f}"], {"frame": {"duration": 100, "redraw": True}, "mode": "immediate"}],
                    label=f"{t_val:.2f}"
                ) for t_val in time_values
            ]
        )
    ]
)

# Show the figure
fig.show()


