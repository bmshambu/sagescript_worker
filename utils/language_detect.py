def detect_language_from_file(filename):
    if filename.endswith(".py"):
        return "Python"
    elif filename.endswith(".ts"):
        return "TypeScript"
    elif filename.endswith(".js"):
        return "JavaScript"
    elif filename.endswith(".java"):
        return "Java"
    else:
        return "Python"  # fallback