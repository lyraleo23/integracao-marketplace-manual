import pandas as pd


def reorder_patients_by_name(file_path, output_path):
    """
    Lê uma planilha com as colunas ['Patient Name', 'Order ID', 'Prescription PDF', 'Receipt Link'],
    reordena as linhas em ordem alfabética de 'Patient Name' e salva o resultado em um novo arquivo.

    Args:
        file_path (str): Caminho para o arquivo da planilha de entrada.
        output_path (str): Caminho para salvar o arquivo da planilha de saída.

    Returns:
        pd.DataFrame: DataFrame reorganizado.
    """
    # Lê a planilha no formato Excel
    df = pd.read_excel(file_path)

    # Verifica se as colunas obrigatórias estão presentes
    required_columns = ['Patient Name', 'Order ID', 'Prescription PDF', 'Receipt Link']
    if not all(column in df.columns for column in required_columns):
        raise ValueError(f"A planilha deve conter as colunas: {', '.join(required_columns)}")

    # Reordena as linhas em ordem alfabética de 'Patient Name'
    df_sorted = df.sort_values(by='Patient Name', ascending=True)

    # Salva o DataFrame ordenado em um novo arquivo
    df_sorted.to_excel(output_path, index=False)

    return df_sorted

def reorder_patients_by_tiny_number(file_path, output_path):
    # Lê a planilha no formato Excel
    df = pd.read_excel(file_path)

    # Verifica se as colunas obrigatórias estão presentes
    required_columns = ['Tiny', 'Patient Name', 'Order ID', 'Prescription PDF', 'Receipt Link']
    if not all(column in df.columns for column in required_columns):
        raise ValueError(f"A planilha deve conter as colunas: {', '.join(required_columns)}")

    # Reordena as linhas em ordem alfabética de 'Patient Name'
    df_sorted = df.sort_values(by='Tiny', ascending=True)

    # Salva o DataFrame ordenado em um novo arquivo
    df_sorted.to_excel(output_path, index=False)

    return df_sorted



