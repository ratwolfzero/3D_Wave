import numpy as np
import plotly.graph_objects as go

# Define spatial and time dimensions
x = np.linspace(-10, 10, 10)  # Spatial dimension X
y = np.linspace(-10, 10, 10)  # Spatial dimension Y
z = np.linspace(-10, 10, 10)  # Spatial dimension Z (used for amplitude)
t_x = np.linspace(-10, 10, 10)  # Time dimension T_x
t_y = np.linspace(-10, 10, 10)  # Time dimension T_y
t_z = np.linspace(-10, 10, 10)  # Time dimension T_z
t = np.linspace(-10, 10, 20)  # Shared time dimension t

# Create 6D grid using meshgrid
X, Y, Z, T_x, T_y, T_z, T = np.meshgrid(x, y, z, t_x, t_y, t_z, t, indexing='ij')

# Define wave parameters
kx = 1  # Wave number in X direction
ky = 1  # Wave number in Y direction
kz = 1  # Wave number in Z direction
omega_x = 1  # Angular frequency in T_x direction
omega_y = 1  # Angular frequency in T_y direction
omega_z = 1  # Angular frequency in T_z direction
gamma = 1  # Coupling constant for shared time dimension t

# Define the wave function with time as intersection
def wave_function(X, Y, Z, T_x, T_y, T_z, T):
    return np.sin(kx * X + ky * Y + kz * Z + omega_x * T_x + omega_y * T_y + omega_z * T_z + gamma * T)

# Function to create a frame for a given slice
def create_frame(X, Y, wave_amplitude, t_val, fixed_dims, animated_dim):
    return go.Frame(
        data=[go.Surface(
            x=X,
            y=Y,
            z=wave_amplitude,  # Use Z-axis for wave amplitude
            colorscale='plasma',
            cmin=-1,
            cmax=1,
            colorbar=dict(title="Wave Amplitude")
        )],
        name=f"frame_{t_val:.2f}",
        layout=dict(
            annotations=[
                dict(
                    text=f"Fixed: {fixed_dims}<br>Animated: {animated_dim} = {t_val:.2f}",
                    x=0.1,
                    y=0.9,
                    xref="paper",
                    yref="paper",
                    showarrow=False,
                    font=dict(size=12, color="white")
                )
            ]
        )
    )

# Function to update the figure based on user selection
def update_figure(fixed_dims, animated_dims, animated_values):
    # Fix the selected dimensions
    fixed_Z = fixed_dims.get('Z', 0)
    fixed_T_x = fixed_dims.get('T_x', 0)
    fixed_T_y = fixed_dims.get('T_y', 0)
    fixed_T_z = fixed_dims.get('T_z', 0)
    fixed_T = fixed_dims.get('T', 0)

    # Create the figure
    fig = go.Figure()

    # Add the initial surface trace
    initial_wave = wave_function(X[:, :, 0, 0, 0, 0, 0], Y[:, :, 0, 0, 0, 0, 0], fixed_Z, fixed_T_x, fixed_T_y, fixed_T_z, fixed_T)
    fig.add_trace(go.Surface(
        x=X[:, :, 0, 0, 0, 0, 0],
        y=Y[:, :, 0, 0, 0, 0, 0],
        z=initial_wave,  # Use Z-axis for wave amplitude
        colorscale='plasma',
        cmin=-1,
        cmax=1,
        colorbar=dict(title="Wave Amplitude")
    ))

    # Create frames for animation
    frames = []
    for animated_dim, animated_values in animated_dims.items():
        for t_val in animated_values:
            if animated_dim == 'T_x':                                                                                               
                wave_amplitude = wave_function(X[:, :, 0, 0, 0, 0, 0], Y[:, :, 0, 0, 0, 0, 0], fixed_Z, t_val, fixed_T_y, fixed_T_z, fixed_T)
            elif animated_dim == 'T_y':
                wave_amplitude = wave_function(X[:, :, 0, 0, 0, 0, 0], Y[:, :, 0, 0, 0, 0, 0], fixed_Z, fixed_T_x, t_val, fixed_T_z, fixed_T)
            elif animated_dim == 'T_z':
                wave_amplitude = wave_function(X[:, :, 0, 0, 0, 0, 0], Y[:, :, 0, 0, 0, 0, 0], fixed_Z, fixed_T_x, fixed_T_y, t_val, fixed_T)
            elif animated_dim == 'Z':
                wave_amplitude = wave_function(X[:, :, 0, 0, 0, 0, 0], Y[:, :, 0, 0, 0, 0, 0], t_val, fixed_T_x, fixed_T_y, fixed_T_z, fixed_T)
            elif animated_dim == 'T':
                wave_amplitude = wave_function(X[:, :, 0, 0, 0, 0, 0], Y[:, :, 0, 0, 0, 0, 0], fixed_Z, fixed_T_x, fixed_T_y, fixed_T_z, t_val)
            else:
                raise ValueError("Invalid animated dimension")

            frame = create_frame(X[:, :, 0, 0, 0, 0, 0], Y[:, :, 0, 0, 0, 0, 0], wave_amplitude, t_val, fixed_dims, animated_dim)
            frames.append(frame)

    # Add frames to the figure
    fig.frames = frames

    # Add animation controls
    fig.update_layout(
        title=f"6D Wave Propagation with Oscillation Between Time and Space",
        scene=dict(
            xaxis_title="X (Spatial Dimension 1)",
            yaxis_title="Y (Spatial Dimension 2)",
            zaxis_title="Wave Amplitude",
            zaxis=dict(range=[-1, 1])  # Set Z-axis range for wave amplitude
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
                    ) for t_val in np.concatenate(list(animated_dims.values()))
                ]
            )
        ]
    )

    return fig

# Example usage
fixed_dims = {'Z': 0, 'T_x': 0, 'T_y': 0, 'T_z': 0}  # Fix Z, T_x, T_y, T_z
animated_dims = {
    'T': t,  # Animate shared time dimension T
    'Z': z,  # Animate spatial dimension Z
    'T_x': t_x  # Animate time dimension T_x
}

fig = update_figure(fixed_dims, animated_dims, animated_values=None)
fig.show()
