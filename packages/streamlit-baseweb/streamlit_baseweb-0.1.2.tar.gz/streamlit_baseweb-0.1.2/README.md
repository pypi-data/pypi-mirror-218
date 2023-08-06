# Streamlit Baseweb

Streamlit Baseweb is a Python package that provides custom components from the Baseweb framework, allowing you to enhance your Streamlit applications with beautiful and interactive UI elements.

## Installation

You can install Streamlit Baseweb using pip:

```shell
pip install streamlit-baseweb
```

## Usage

To use the Baseweb components in your Streamlit application, you need to import the necessary components from the '**streamlit_baseweb**' module and utilize them in your code. Here's an example:

```python
import streamlit as st
from streamlit_baseweb import base_web_modal, base_web_button

st.title("Testing Streamlit Baseweb")
if base_web_button(size="large", shape="pill", kind="secondary"):
    base_web_modal(
        title="This is a test modal",
        body="""
                Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium 
                doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae 
                vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, 
                sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est,
    """,
        key="modal",
    )
if st.session_state.get("modal"):
    st.success("Confirmation received from modal")

```

For more details on available components and their usage, refer to the package documentation.

## Roadmap
Elements will be integrated as per the below priority ranking:
1. modal
2. buttons
3. button groups
4. navbar
5. tooltip
6. alerts
7. pop-over cards

Additional elements have not yet been prioritized 

## Contributing
Contributions to Streamlit Baseweb are welcome! If you find any issues or have suggestions for improvements, please open an issue on the [GitHub repository](https://github.com/thomasbs17/streamlit-contributions/tree/master/baseweb_components). If you'd like to contribute code, you can fork the repository, make your changes, and submit a pull request.

Before contributing, please review the [Contributing Guidelines](https://github.com/thomasbs17/streamlit-contributions/blob/master/baseweb_components/README.md) for more information.

## License
This package is licensed under the MIT License. See the [LICENSE file](https://github.com/thomasbs17/streamlit-contributions/blob/master/baseweb_components/LICENSE) for more information.

## Credits
Streamlit Baseweb is created and maintained by Thomas Bouamoud. 
It utilizes the Baseweb framework by [Uber](https://baseweb.design/).

## Contact
If you have any questions or inquiries, feel free to reach out to thomas.bouamoud@gmail.com.

## 👩‍💻 Happy Streamlit Baseweb coding! 👨‍💻