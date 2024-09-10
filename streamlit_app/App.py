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


# @st.cache_data
def import_data(path: str) -> pd.DataFrame | None:
    try:
        if not Path(path).exists():
            raise FileNotFoundError(f"{path} not found")

        data = pd.read_csv(path)

        st.write(data.columns)
        data = transform_data(data)


        ##  medianę, min, maximum , std, itp , mean

        # rows, column -> dataframe
        # dataframe['description'] -> pandas Series
        st.write(data["data_kilocalories"].describe())

        ### wyswietlic sama kolumne, wyswietl 10 jej pierwszych rzedow  i robisz to za pomoca .head(10)
        st.write('Testing arrays')
        # category + calories

        # .loc -> location
        # dataframe.loc[rows, columns]
        #      0 1 2 3 4
        lst = [1,2,3,4,6]
        # 0 -> 3(nie właczając)
        # 4
        # [:-1]
        # lst[start_index:end_index(nie wlaczamy)]
        st.write(lst[0:-1])
        st.write("ddd",lst[:])
        # data.loc[:, ["description"]]


        # st.write(data.loc[:10,["category",'description',"data_kilocalories"]])

        st.write(data.loc[:6, :])
        # zwrocil dane tylko z  kolumnami które nas interesują
        st.write(data[:])
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
# Index(['Category', 'Description', 'Nutrient Data Bank Number',
#        'Data.Alpha Carotene', 'Data.Ash', 'Data.Beta Carotene',
#        'Data.Beta Cryptoxanthin', 'Data.Carbohydrate', 'Data.Cholesterol',
#        'Data.Choline', 'Data.Fiber', '`Data.Kilocalories',
#        'Data.Lutein and Zeaxanthin', 'Data.Lycopene', 'Data.Manganese',
#        'Data.Niacin', 'Data.Pantothenic Acid', 'Data.Protein',
#        'Data.Refuse Percentage', 'Data.Retinol', 'Data.Riboflavin',
#        'Data.Selenium', 'Data.Sugar Total', 'Data.Thiamin', 'Data.Water',
#        'Data.Fat.Monosaturated Fat', 'Data.Fat.Polysaturated Fat',
#        'Data.Fat.Saturated Fat', 'Data.Fat.Total Lipid',
#        'Data.Household Weights.1st Household Weight',
#        'Data.Household Weights.1st Household Weight Description',
#        'Data.Household Weights.2nd Household Weight',
#        'Data.Household Weights.2nd Household Weight Description',
#        'Data.Major Minerals.Calcium', 'Data.Major Minerals.Copper',
#        'Data.Major Minerals.Iron', 'Data.Major Minerals.Magnesium',
#        'Data.Major Minerals.Phosphorus', 'Data.Major Minerals.Potassium',
#        'Data.Major Minerals.Sodium', 'Data.Major Minerals.Zinc',
#        'Data.Vitamins.Vitamin A - IU', 'Data.Vitamins.Vitamin A - RAE',
#        'Data.Vitamins.Vitamin B12', 'Data.Vitamins.Vitamin B6',
#        'Data.Vitamins.Vitamin C', 'Data.Vitamins.Vitamin E',
#        'Data.Vitamins.Vitamin K'],
#       dtype='object')


###

#
# Category (Kategoria): Typ lub grupa żywności.
# Description (Opis): Szczegółowy opis produktu żywnościowego.
# Nutrient Data Bank Number (Numer bazy danych składników odżywczych): Unikalny numer identyfikujący składnik odżywczy.
# Data.Alpha Carotene (Dane. Alfa-karoten): Ilość alfa-karotenu; związek, który jest źródłem witaminy A.
# Data.Ash (Dane. Popiół): Całkowita zawartość substancji mineralnych.
# Data.Beta Carotene (Dane. Beta-karoten): Ilość beta-karotenu; przekształca się w witaminę A.
# Data.Beta Cryptoxanthin (Dane. Beta-kryptoksantyna): Ilość beta-kryptoksantyny; źródło witaminy A.
# Data.Carbohydrate (Dane. Węglowodany): Całkowita ilość węglowodanów.
# Data.Cholesterol (Dane. Cholesterol): Zawartość cholesterolu.
# Data.Choline (Dane. Cholina): Ilość choliny; ważna dla funkcji mózgu i nerwów.
# Data.Fiber (Dane. Błonnik): Ilość błonnika; wspomaga trawienie.
# Data.Kilocalories (Dane. Kilokalorie): Ilość kalorii dostarczanych przez żywność.
# Data.Lutein and Zeaxanthin (Dane. Luteina i zeaksantyna): Ilość luteiny i zeaksantyny; dobre dla zdrowia oczu.
# Data.Lycopene (Dane. Likopen): Ilość likopenu; przeciwutleniacz.
# Data.Manganese (Dane. Mangan): Ilość manganu; ważny dla metabolizmu.
# Data.Niacin (Dane. Niacyna): Ilość niacyny (witamina B3); wspiera układ nerwowy.
# Data.Pantothenic Acid (Dane. Kwas pantotenowy): Ilość kwasu pantotenowego (witamina B5); ważny dla produkcji energii.
# Data.Protein (Dane. Białko): Ilość białka; kluczowe dla wzrostu i naprawy tkanek.
# Data.Refuse Percentage (Dane. Procent odpadów): Procent odpadów, które nie są spożywane.
# Data.Retinol (Dane. Retinol): Ilość retinolu; forma witaminy A.
# Data.Riboflavin (Dane. Ryboflawina): Ilość ryboflawiny (witamina B2); wspiera produkcję energii.
# Data.Selenium (Dane. Selen): Ilość selenu; przeciwutleniacz.
# Data.Sugar Total (Dane. Całkowita zawartość cukru): Ilość wszystkich cukrów.
# Data.Thiamin (Dane. Tiamina): Ilość tiaminy (witamina B1); wspiera metabolizm.
# Data.Water (Dane. Woda): Zawartość wody.
# Data.Fat.Monosaturated Fat (Dane. Tłuszcze jednonienasycone): Ilość tłuszczów jednonienasyconych; korzystne dla zdrowia serca.
# Data.Fat.Polysaturated Fat (Dane. Tłuszcze wielonienasycone): Ilość tłuszczów wielonienasyconych; wspierają zdrowie serca.
# Data.Fat.Saturated Fat (Dane. Tłuszcze nasycone): Ilość tłuszczów nasyconych; może wpływać na poziom cholesterolu.
# Data.Fat.Total Lipid (Dane. Całkowita zawartość tłuszczu): Całkowita ilość tłuszczu.
# Data.Household Weights.1st Household Weight (Dane. Waga 1): Waga produktu w standardowej jednostce domowej (np. filiżanka).
# Data.Household Weights.1st Household Weight Description (Opis wagi 1): Opis jednostki miary (np. filiżanka, łyżka).
# Data.Household Weights.2nd Household Weight (Dane. Waga 2): Inna waga produktu w standardowej jednostce domowej.
# Data.Household Weights.2nd Household Weight Description (Opis wagi 2): Opis drugiej jednostki miary.
# Data.Major Minerals.Calcium (Dane. Wapń): Ilość wapnia; ważny dla kości.
# Data.Major Minerals.Copper (Dane. Miedź): Ilość miedzi; wspiera układ odpornościowy.
# Data.Major Minerals.Iron (Dane. Żelazo): Ilość żelaza; potrzebne do transportu tlenu.
# Data.Major Minerals.Magnesium (Dane. Magnez): Ilość magnezu; ważny dla mięśni i nerwów.
# Data.Major Minerals.Phosphorus (Dane. Fosfor): Ilość fosforu; kluczowy dla kości i zębów.
# Data.Major Minerals.Potassium (Dane. Potas): Ilość potasu; wspiera funkcje serca.
# Data.Major Minerals.Sodium (Dane. Sód): Ilość sodu; regulacja ciśnienia krwi.
# Data.Major Minerals.Zinc (Dane. Cynk): Ilość cynku; wspiera układ odpornościowy.
# Data.Vitamins.Vitamin A - IU (Dane. Witamina A - IU): Ilość witaminy A w jednostkach międzynarodowych (IU).
# Data.Vitamins.Vitamin A - RAE (Dane. Witamina A - RAE): Ilość witaminy A w równoważnikach retinolu (RAE).
# Data.Vitamins.Vitamin B12 (Dane. Witamina B12): Ilość witaminy B12; ważna dla krwinek.
# Data.Vitamins.Vitamin B6 (Dane. Witamina B6): Ilość witaminy B6; wspiera układ nerwowy.
# Data.Vitamins.Vitamin C (Dane. Witamina C): Ilość witaminy C; ważna dla układu odpornościowego.
# Data.Vitamins.Vitamin E (Dane. Witamina E): Ilość witaminy E; przeciwutleniacz.
# Data.Vitamins.Vitamin K (Dane. Witamina K): Ilość witaminy K; ważna dla krzepnięcia krwi.