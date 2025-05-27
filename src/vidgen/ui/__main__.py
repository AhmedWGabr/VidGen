"""
Allow running UI tests or demos directly
Usage: python -m vidgen.ui
"""
if __name__ == "__main__":
    from vidgen.ui.gradio_app import create_gradio_interface
    print("Launching VidGen UI...")
    demo = create_gradio_interface()
    demo.launch()
