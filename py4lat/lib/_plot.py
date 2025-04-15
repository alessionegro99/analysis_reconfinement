import matplotlib.pyplot as plt

IBM_COLORS = {
    "blue": "#0061F2", 
    "red": "#D30000", 
    "green": "#1BC800", 
    "yellow": "#FFAA00", 
    "black": "#000000", 
    "gray": "#9A9A9A",
    "light_gray": "#D5D5D5",
    }
    
plt.rcParams.update({
    "text.usetex": True,  # Enable LaTeX rendering for text
    "font.family": "serif",  # Use a serif font family (for LaTeX)
    "axes.labelsize": 14,  # Set label size
    "axes.titlesize": 16,  # Set title size
    "xtick.labelsize": 12,  # X-axis tick size
    "ytick.labelsize": 12,  # Y-axis tick size
    "font.size": 12,  # Global font size
    })