import pandas as pd
import streamlit as st
from pathlib import Path
import numpy as np

# Set the Streamlit app to wide mode
st.set_page_config(layout="wide")

DATA_PATH = "./data/products.csv"


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [
        col.lower().replace(".", "_").replace(" ", "_").strip() for col in df.columns
    ]

    df["category"] = df["category"].apply(lambda row: str(row).capitalize())

    df["description"] = df["description"].apply(
        lambda row: str(row).capitalize().replace(",", " ")
    )

    return df


@st.cache_data
def import_data(path: str) -> pd.DataFrame | None:
    try:
        if not Path(path).exists():
            raise FileNotFoundError(f"{path} not found")

        data = pd.read_csv(path)
        data = transform_data(data)

        return data
    except FileNotFoundError as e:
        print(e)
        return None

    # Import data to Streamlit session state


if "data" not in st.session_state:
    data = import_data(DATA_PATH)
    st.session_state.data = data

if "product_list" not in st.session_state:
    st.session_state.product_list = []


def add_product(new_product):
    st.session_state.product_list.append(new_product)


def delete_product(product):
    # st.write("Before", st.session_state.product_list)
    st.session_state.product_list.remove(product)
    # st.write("After", st.session_state.product_list)


def show_products_list():
    st.markdown(
        """
        <style>
        .product-container {
            background-color: #f0f0f5;
            # padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            margin-top: 20px;
        }
        .product-item {
            background-color: #ffffff;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .product-text {
            font-size: 18px;
            color: #333;
        }
        .delete-button {
            background-color: #e57373;
            color: white;
            border: none;
            padding: 5px 10px;
            cursor: pointer;
            border-radius: 5px;
            font-size: 14px;
        }
        .delete-button:hover {
            background-color: #c62828;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="product-container">', unsafe_allow_html=True)

    if st.session_state.product_list:
        for product in st.session_state.product_list:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(
                    f'<div class="product-item"><span class="product-text">{product}</span></div>',
                    unsafe_allow_html=True,
                )
            with col2:
                delete_button_key = f"{product}{np.random.randint(0, 1000)}"
                if st.button(
                    "Delete",
                    key=delete_button_key,
                    on_click=delete_product,
                    args=(product,),
                ):
                    st.write("Test")

    st.markdown("</div>", unsafe_allow_html=True)


def app():
    # Title of the application
    st.title("📊 Products Calorie Calculators")

    # Main header for the section
    st.header("🔍 Choose a Product to Calculate Its Calories")

    # Subheader with additional styling and emphasis
    st.subheader(
        "Our extensive database includes:\n"
        "⭐ Thousands of products\n"
        "⭐ Over 1.8 million products available"
    )

    # Additional information or instructions
    st.markdown(
        """
        Use the search bar below to find your product and calculate its calorie content. 
        Our tool is designed to help you make informed choices about your diet and nutrition.
        """
    )

    col1, col2 = st.columns([3, 1])

    with col1:
        if st.session_state.data is not None:
            product = st.selectbox(
                "Select a product you would like to add",
                st.session_state.data["description"],
                placeholder="Select a product",
            )

            st.write("You selected:", product)
            st.button("Add", on_click=add_product, args=(product,))

    with col2:
        if st.session_state.product_list and len(st.session_state.product_list) > 0:
            show_products_list()


app()
#