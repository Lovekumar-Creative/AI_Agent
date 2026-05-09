def compare_assessments(message, catalog):

    text = message.lower()

    first = None
    second = None

    # --------------------------------
    # Find OPQ
    # --------------------------------
    if "opq" in text:
        for item in catalog:
            name = item.get("name", "").lower()
            if ("occupational personality questionnaire" in name):
                first = item
                break

    # --------------------------------
    # Find GSA
    # --------------------------------
    if "gsa" in text or "global skills" in text:
        for item in catalog:
            name = item.get("name", "").lower()
            if "global skills" in name:
                second = item
                break

    # --------------------------------
    # Validation
    # --------------------------------
    if not first or not second:
        return (
            "I could not identify both SHL assessments "
            "to compare. Please mention the assessment names clearly."
        )

    # --------------------------------
    # Response
    # --------------------------------
    response = f"""{first['name']} focuses on: {first.get('description', 'No description available')}
    Key areas: {", ".join(first.get("keys", []))}

    ---

    {second['name']} focuses on: {second.get('description', 'No description available')}
    Key areas: {", ".join(second.get("keys", []))}
    """

    return response.strip()