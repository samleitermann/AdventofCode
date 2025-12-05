import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import copy
import sys


def generate_animation():
    # --- 1. Load and Parse Input ---
    input_filename = 'real_input.txt'
    try:
        with open(input_filename, 'r') as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        print(f"Error: Could not find '{input_filename}'. Please ensure it is in the same directory.")
        return

    # Determine grid dimensions dynamically
    rows_count = len(lines)
    cols_count = len(lines[0])

    # Initialize grid with padding (0 = empty, 1 = roll/@)
    # We add a border of 0s around the entire grid to handle edge cases easily
    grid = []
    padding_row = [0] * (cols_count + 2)

    grid.append(list(padding_row))  # Top padding

    for line in lines:
        row = [0]  # Left padding
        for char in line:
            # Map '@' to 1 (roll) and '.' to 0 (empty)
            if char == '.':
                row.append(0)
            else:
                row.append(1)
        row.append(0)  # Right padding
        grid.append(row)

    grid.append(list(padding_row))  # Bottom padding

    print(f"Grid loaded: {len(grid)} rows x {len(grid[0])} columns")

    # --- 2. Run Simulation ---
    frames = []
    # Save the initial state
    frames.append(copy.deepcopy(grid))

    reachable = 1
    iteration = 0
    max_iterations = 1000  # Safety break

    print("Starting simulation...")

    while reachable > 0 and iteration < max_iterations:
        reachable = 0

        # Iterate over the valid grid area (excluding the padding border)
        for i in range(1, len(grid) - 1):
            for j in range(1, len(grid[0]) - 1):
                if grid[i][j] == 1:
                    # Sum the 8 neighbors
                    # (i-1, j-1) (i-1, j) (i-1, j+1)
                    # (i,   j-1)          (i,   j+1)
                    # (i+1, j-1) (i+1, j) (i+1, j+1)
                    count = (grid[i - 1][j - 1] + grid[i - 1][j] + grid[i - 1][j + 1] +
                             grid[i][j - 1] + grid[i][j + 1] +
                             grid[i + 1][j - 1] + grid[i + 1][j] + grid[i + 1][j + 1])

                    # If fewer than 4 neighbors, it is "reachable" and gets removed
                    if count < 4:
                        reachable += 1
                        grid[i][j] = 0

                        # If changes occurred, save the frame
        if reachable > 0:
            frames.append(copy.deepcopy(grid))

        iteration += 1
        sys.stdout.write(f"\rIteration {iteration}: Removed {reachable} rolls")
        sys.stdout.flush()

    print(f"\nSimulation finished in {iteration} iterations. Total frames captured: {len(frames)}")

    # --- 3. Generate GIF ---
    print("Generating GIF... (this might take a moment)")

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.axis('off')  # Hide axes for a cleaner look

    def update(frame_idx):
        ax.clear()
        ax.axis('off')
        g = np.array(frames[frame_idx])
        # 'Greys' colormap: 0 is white, 1 is black
        ax.imshow(g, cmap='Greys', interpolation='nearest')
        ax.set_title(f"Iteration: {frame_idx}")

    # Create animation
    # interval=200 means 200ms per frame (5 frames per second)
    ani = animation.FuncAnimation(fig, update, frames=len(frames), interval=200)

    output_file = 'grid_evolution.gif'
    ani.save(output_file, writer='pillow')

    print(f"Done! Animation saved to '{output_file}'")


if __name__ == "__main__":
    generate_animation()