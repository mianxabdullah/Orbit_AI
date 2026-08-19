def extract_text(uploaded_file):

    if uploaded_file is None:
        return ""

    file_type = uploaded_file.name.split(".")[-1].lower() # extract the file extension and convert it to lowercase

# .txt
    if file_type == "txt":
        return uploaded_file.read().decode("utf-8")

    return ""

