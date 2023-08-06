import os

import streamlit as st
import streamlit.components.v1 as components

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
_RELEASE = True

if not _RELEASE:
    _streamlit_mermaid = components.declare_component(
        "streamlit_mermaid",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _streamlit_mermaid = components.declare_component("streamlit_mermaid", path=build_dir)


def st_mermaid(code: str, key=None):
    return _streamlit_mermaid(code=code, key=key)


# Test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run st_mermaid/__init__.py`
if not _RELEASE:
    code = """
    graph TD
        A --> B
    """

    mermaid = st_mermaid(code)
    st.write(mermaid)
