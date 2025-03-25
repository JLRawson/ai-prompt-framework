banned_extensions = [
    ".json", ".md", ".txt", ".csv", ".xml", ".yml", ".yaml", ".toml", 
    ".toc", ".seg",
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".webp", ".bmp", ".tiff", ".psd", # Images
    ".ttf", ".otf", ".woff", ".woff2", ".eot", # Fonts
    ".mp3", ".wav", ".ogg", ".mp4", ".mov", ".avi", ".webm",
    ".zip", ".tar", ".gz", ".rar", ".7z",
    ".exe", ".dll", ".bin", ".so", ".o", ".obj", ".class", ".jar", ".pyc", ".pyd",
    ".lock", ".log", ".db", ".sqlite", ".bak", ".map", # Dev/build tools
    ".DS_Store", ".env", ".crt", ".pem", ".key" # Misc
]

banned_filenames = [
    "MAIN_WRITELOCK",
    ".DS_Store", "Thumbs.db", "desktop.ini", 
    ".gitignore", ".gitattributes", ".gitkeep",
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "tsconfig.json",
    "webpack.config.js", "vite.config.js", "next.config.js", "babel.config.js",
    "debug.log", "error.log", "npm-debug.log",
    ".env", ".env.local", ".env.production", ".env.development",
    "__init__.py", "__pycache__",
    "node_modules", "dist", "build",
    ".vscode", ".idea",
    ".lock", "write.lock", "package-lock.yaml"
]
