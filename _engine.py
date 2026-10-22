import sys
import turtle

# Check if the --svg flag was passed in the terminal execution
USE_SVG = "--svg" in sys.argv

# Set standard canvas dimensions for the aquarium
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600

if USE_SVG:
    try:
        # Python 3.14+ compatibility patch for svg_turtle on macOS
        import svg_turtle.canvas
        if hasattr(svg_turtle.canvas, "DummyWindow"):
            if not hasattr(svg_turtle.canvas.DummyWindow, "wm_attributes"):
                svg_turtle.canvas.DummyWindow.wm_attributes = lambda *args, **kwargs: None
        if not hasattr(svg_turtle.canvas.Canvas, "winfo_toplevel"):
            class _DummyRoot:
                def wm_attributes(self, *args, **kwargs):
                    pass
            svg_turtle.canvas.Canvas.winfo_toplevel = lambda self: _DummyRoot()

        
        from svg_turtle import SvgTurtle
        # Initialize the SVG drawing engine with the standard dimensions
        t = SvgTurtle(CANVAS_WIDTH, CANVAS_HEIGHT)
    except ImportError:
        print("Error: The 'svg_turtle' package is missing.")
        print("Make sure you activated your virtual environment and ran:")
        print("pip install -r requirements.txt")
        sys.exit(1)
else:
    # Initialize the standard interactive graphical window
    screen = turtle.Screen()
    screen.setup(width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
    screen.title("PA1: Python Aquarium")
    
    t = turtle.Turtle()

# Apply common configurations regardless of which engine is running
t.speed(0)       # 0 is the fastest animation speed
t.hideturtle()   # Hides the turtle cursor while drawing so it doesn't ruin the final image