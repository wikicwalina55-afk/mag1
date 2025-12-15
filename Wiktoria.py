import streamlit as st
import uuid

# --- Inicjalizacja stanu sesji ---
# Używamy st.session_state do przechowywania danych, 
# dzięki czemu lista towarów jest zachowywana pomiędzy interakcjami użytkownika.
if 'towary' not in st.session_state: 
    # Struktura listy: [{'id': unique_id, 'nazwa': 'Nazwa Towaru', 'ilosc': 10}]
    st.session_state['towary'] = []

# --- Funkcje do zarządzania magazynem ---

def dodaj_towar(nazwa, ilosc):
    """Dodaje nowy towar do listy."""
    try:
        ilosc_int = int(ilosc)
        if ilosc_int <= 0:
            st.error("Ilość musi być liczbą całkowitą większą od zera.")
            return
    except ValueError:
        st.error("Ilość musi być liczbą całkowitą.")
        return

    if nazwa:
        nowy_towar = {
            'id': str(uuid.uuid4()),  # Generowanie unikalnego ID dla łatwego usuwania
            'nazwa': nazwa,
            'ilosc': ilosc_int
        }
        st.session_state['towary'].append(nowy_towar)
        st.success(f"Dodano towar: **{nazwa}** w ilości **{ilosc_int}**.")
    else:
        st.error("Nazwa towaru nie może być pusta.")

def usun_towar(towar_id):
    """Usuwa towar z listy po jego unikalnym ID."""
    st.session_state['towary'] = [
        towar for towar in st.session_state['towary'] 
        if towar['id'] != towar_id
    ]
    st.info("Towar usunięty.")
    # Po usunięciu warto ponownie wyświetlić aktualną listę
    st.rerun() 

# --- Interfejs użytkownika Streamlit ---

st.title("📦 Prosty Magazyn (Streamlit)")
st.caption("Dane są przechowywane tylko w pamięci aplikacji (session state).")

# --- Sekcja Dodawania Towaru ---
st.header("➕ Dodaj Nowy Towar")

# Używamy formularza (st.form) do grupowania elementów, 
# co zapewnia, że kod dodawania towaru jest wykonywany tylko po kliknięciu przycisku 'Dodaj'.
with st.form("dodaj_formularz", clear_on_submit=True):
    nowa_nazwa = st.text_input("Nazwa Towaru")
    nowa_ilosc = st.number_input("Ilość", min_value=1, step=1, value=1)
    
    dodaj_przycisk = st.form_submit_button("Dodaj Towar do Magazynu")
    
    if dodaj_przycisk:
        dodaj_towar(nowa_nazwa, nowa_ilosc)

# --- Sekcja Aktualnego Stanu Magazynu ---
st.header("📋 Aktualny Stan Magazynu")

if not st.session_state['towary']:
    st.write("Magazyn jest pusty. Dodaj pierwszy towar powyżej!")
else:
    # Tworzenie kolumn do wyświetlania i zarządzania listą
    
    # Wyświetlamy towary w formie tabeli lub listy z przyciskami do usuwania
    for towar in st.session_state['towary']:
        col1, col2, col3, col4 = st.columns([0.4, 0.2, 0.3, 0.1])
        
        with col1:
            st.markdown(f"**{towar['nazwa']}**")
        with col2:
            st.write(f"{towar['ilosc']} szt.")
        with col3:
            # Używamy st.button z unikalnym kluczem (key)
            if st.button("🗑 Usuń", key=f"delete_{towar['id']}"):
                usun_towar(towar['id'])
        # Dodatkowa kolumna dla wyrównania - opcjonalnie
        # with col4:
        #     st.empty()

    # Alternatywnie, można wyświetlić dane w formie tabeli Streamlit, ale wtedy trudniej dodać przycisk usuwania obok każdego wiersza.
    # st.dataframe(st.session_state['towary'], hide_index=True)
