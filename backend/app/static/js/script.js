function clearText() {
    const source = document.getElementById("source_text");
    const translation = document.getElementById("translation");

    if (source) source.value = "";
    if (translation) translation.value = "";
}
