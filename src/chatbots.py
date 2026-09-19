"""Question banks and helpers for Aptitude + HR practice chatbots."""
import random


# ---------------------------------------------------------------------------
# Aptitude MCQs (4 options each)
# ---------------------------------------------------------------------------

def _shuffle_options(correct, wrongs):
    opts = [correct] + wrongs[:3]
    random.shuffle(opts)
    return opts, correct


def generate_aptitude_mcq():
    """Return a friendly aptitude MCQ with 4 poll options."""
    generators = [
        _apt_percentage,
        _apt_train,
        _apt_series,
        _apt_ratio,
        _apt_average,
        _apt_profit_loss,
        _apt_time_work,
        _apt_odd_one,
        _apt_verbal,
        _apt_direction,
    ]
    return random.choice(generators)()


def _apt_percentage():
    num = random.randint(10, 100) * 10
    pct = random.choice([10, 15, 20, 25, 30, 40, 50, 60, 75])
    ans = int(num * pct / 100)
    wrongs = list({ans + d for d in [-20, -10, 10, 15, 25, 40] if ans + d > 0 and ans + d != ans})
    opts, correct = _shuffle_options(str(ans), [str(w) for w in wrongs])
    return {
        "question": f"What is {pct}% of {num}?",
        "options": opts,
        "answer": correct,
        "explanation": f"({pct}/100) × {num} = {ans}",
        "category": "Numerical",
    }


def _apt_train():
    speed = random.randint(40, 100)
    time = random.randint(5, 20)
    length = int((speed * 5 / 18) * time)
    wrongs = list({length + d for d in [-50, -25, 25, 50, 75, 100] if length + d > 0})
    opts, correct = _shuffle_options(str(length), [str(w) for w in wrongs])
    return {
        "question": f"A train running at {speed} km/hr crosses a pole in {time} seconds. Length of the train (meters)?",
        "options": opts,
        "answer": correct,
        "explanation": f"Speed = {speed}×(5/18) m/s. Distance = Speed×Time ≈ {length} m.",
        "category": "Numerical",
    }


def _apt_series():
    start = random.randint(2, 12)
    diff = random.randint(2, 7)
    series = [start + i * diff for i in range(4)]
    ans = series[-1] + diff
    wrongs = list({ans + d for d in [-diff, diff, 2, -2, 5] if ans + d != ans})
    opts, correct = _shuffle_options(str(ans), [str(w) for w in wrongs])
    return {
        "question": f"Find the next number: {series[0]}, {series[1]}, {series[2]}, {series[3]}, ?",
        "options": opts,
        "answer": correct,
        "explanation": f"Common difference is {diff}. So {series[3]} + {diff} = {ans}.",
        "category": "Logical",
    }


def _apt_ratio():
    a, b = random.randint(2, 8), random.randint(2, 8)
    total = random.choice([30, 40, 50, 60, 100])
    part_a = int(total * a / (a + b))
    wrongs = list({part_a + d for d in [-5, 5, 10, -10] if part_a + d > 0})
    opts, correct = _shuffle_options(str(part_a), [str(w) for w in wrongs])
    return {
        "question": f"If A:B = {a}:{b} and A+B = {total}, what is A?",
        "options": opts,
        "answer": correct,
        "explanation": f"A = ({a}/{a+b}) × {total} = {part_a}",
        "category": "Numerical",
    }


def _apt_average():
    nums = [random.randint(10, 50) for _ in range(4)]
    avg = sum(nums) // 4
    wrongs = list({avg + d for d in [-3, 3, 5, -5] if avg + d > 0})
    opts, correct = _shuffle_options(str(avg), [str(w) for w in wrongs])
    return {
        "question": f"Average of {', '.join(map(str, nums))} is?",
        "options": opts,
        "answer": correct,
        "explanation": f"Sum = {sum(nums)}; Average = {sum(nums)}/4 = {avg}",
        "category": "Numerical",
    }


def _apt_profit_loss():
    cp = random.choice([100, 200, 250, 400, 500])
    pct = random.choice([10, 20, 25, 30])
    sp = int(cp * (100 + pct) / 100)
    wrongs = list({sp + d for d in [-20, 20, 50, -50] if sp + d > 0})
    opts, correct = _shuffle_options(str(sp), [str(w) for w in wrongs])
    return {
        "question": f"Cost price is ₹{cp}. Sold at {pct}% profit. Selling price?",
        "options": opts,
        "answer": correct,
        "explanation": f"SP = CP × (100+{pct})/100 = {sp}",
        "category": "Numerical",
    }


def _apt_time_work():
    a_days = random.choice([6, 8, 10, 12])
    b_days = random.choice([8, 10, 12, 15])
    together = round((a_days * b_days) / (a_days + b_days), 1)
    wrongs = [str(round(together + d, 1)) for d in [-1.5, 1.5, 2, -2]]
    opts, correct = _shuffle_options(str(together), wrongs)
    return {
        "question": f"A finishes a job in {a_days} days, B in {b_days} days. Days if they work together?",
        "options": opts,
        "answer": correct,
        "explanation": f"1/A + 1/B = 1/{a_days} + 1/{b_days} → {together} days.",
        "category": "Numerical",
    }


def _apt_odd_one():
    sets = [
        (["Apple", "Mango", "Carrot", "Banana"], "Carrot", "Carrot is a vegetable; others are fruits."),
        (["Dog", "Cat", "Lion", "Table"], "Table", "Table is not an animal."),
        (["Circle", "Square", "Triangle", "Cube"], "Cube", "Cube is 3D; others are 2D shapes."),
        (["HTML", "CSS", "Python", "HTTP"], "Python", "Python is a programming language; others are web-related markup/protocol/styles."),
    ]
    options, answer, explanation = random.choice(sets)
    opts = options[:]
    random.shuffle(opts)
    return {
        "question": "Odd one out:",
        "options": opts,
        "answer": answer,
        "explanation": explanation,
        "category": "Logical",
    }


def _apt_verbal():
    sets = [
        ("Synonym of 'Happy'", "Joyful", ["Angry", "Sad", "Tired"], "'Joyful' means happy."),
        ("Antonym of 'Brave'", "Cowardly", ["Bold", "Courageous", "Strong"], "'Cowardly' is the opposite of brave."),
        ("Synonym of 'Quick'", "Rapid", ["Slow", "Late", "Idle"], "'Rapid' means fast/quick."),
        ("Complete: Better late than _____", "never", ["always", "early", "soon"], "Idiom: Better late than never."),
    ]
    q, ans, wrongs, exp = random.choice(sets)
    opts, correct = _shuffle_options(ans, wrongs)
    return {
        "question": q,
        "options": opts,
        "answer": correct,
        "explanation": exp,
        "category": "Verbal",
    }


def _apt_direction():
    return {
        "question": "A person walks 5 km North, then 5 km East, then 5 km South. How far from start?",
        "options": ["0 km", "5 km", "10 km", "15 km"],
        "answer": "5 km",
        "explanation": "North and South cancel; remaining is 5 km East.",
        "category": "Logical",
    }


# ---------------------------------------------------------------------------
# Technical Q&A by topic & difficulty
# ---------------------------------------------------------------------------

TECH_TOPICS = [
    "HTML", "CSS", "JavaScript", "Python", "SQL", "PHP",
    "AI", "ML", "DL", "Generative AI",
]

TECH_QUESTIONS = {
    "HTML": {
        "easy": [
            {
                "q": "What does HTML stand for?",
                "options": ["HyperText Markup Language", "High Tech Modern Language", "Hyper Transfer Markup Language", "Home Tool Markup Language"],
                "answer": "HyperText Markup Language",
                "explanation": "HTML = HyperText Markup Language — the standard for web pages.",
            },
            {
                "q": "Which tag creates a hyperlink?",
                "options": ["<a>", "<link>", "<href>", "<url>"],
                "answer": "<a>",
                "explanation": "The <a> (anchor) tag with href creates links.",
            },
            {
                "q": "Which tag is used for the largest heading?",
                "options": ["<h1>", "<h6>", "<head>", "<header>"],
                "answer": "<h1>",
                "explanation": "<h1> is the largest heading; <h6> is the smallest.",
            },
        ],
        "medium": [
            {
                "q": "What is the purpose of the <semantic> HTML5 tags like <article> and <section>?",
                "options": ["Describe meaning of content", "Only style the page", "Replace CSS", "Run JavaScript"],
                "answer": "Describe meaning of content",
                "explanation": "Semantic tags describe structure/meaning for accessibility and SEO.",
            },
            {
                "q": "Which attribute makes an input required?",
                "options": ["required", "mandatory", "validate", "needed"],
                "answer": "required",
                "explanation": "The boolean `required` attribute forces the field to be filled.",
            },
        ],
        "hard": [
            {
                "q": "Difference between <div> and <span>?",
                "options": ["div is block-level, span is inline", "span is block, div is inline", "Both are the same", "div is only for forms"],
                "answer": "div is block-level, span is inline",
                "explanation": "<div> starts on a new line (block); <span> stays inline.",
            },
            {
                "q": "What does the defer attribute on a <script> tag do?",
                "options": ["Runs script after HTML is parsed", "Blocks parsing immediately", "Disables the script", "Loads CSS first"],
                "answer": "Runs script after HTML is parsed",
                "explanation": "defer downloads in parallel and executes after document parsing.",
            },
        ],
    },
    "CSS": {
        "easy": [
            {
                "q": "What does CSS stand for?",
                "options": ["Cascading Style Sheets", "Computer Style Syntax", "Creative Style System", "Colorful Style Sheets"],
                "answer": "Cascading Style Sheets",
                "explanation": "CSS styles the presentation of HTML documents.",
            },
            {
                "q": "Which property changes text color?",
                "options": ["color", "font-color", "text-color", "fgcolor"],
                "answer": "color",
                "explanation": "Use `color` for text color in CSS.",
            },
        ],
        "medium": [
            {
                "q": "What does display: flex do?",
                "options": ["Creates a flexible layout container", "Hides the element", "Makes text bold", "Adds animation"],
                "answer": "Creates a flexible layout container",
                "explanation": "Flexbox lays out children along a row or column with flexible sizing.",
            },
            {
                "q": "specificity order (highest to lowest)?",
                "options": ["Inline > ID > Class > Element", "Class > ID > Inline > Element", "Element > Class > ID > Inline", "ID > Inline > Class > Element"],
                "answer": "Inline > ID > Class > Element",
                "explanation": "Inline styles beat IDs, which beat classes, which beat element selectors.",
            },
        ],
        "hard": [
            {
                "q": "What is the CSS Box Model order from inside out?",
                "options": ["Content → Padding → Border → Margin", "Margin → Border → Padding → Content", "Content → Border → Padding → Margin", "Padding → Content → Border → Margin"],
                "answer": "Content → Padding → Border → Margin",
                "explanation": "Innermost is content, then padding, border, and outermost margin.",
            },
            {
                "q": "position: absolute is relative to?",
                "options": ["Nearest positioned ancestor", "Always the viewport", "Only the body", "The next sibling"],
                "answer": "Nearest positioned ancestor",
                "explanation": "Absolute positioning uses the nearest ancestor with position not static.",
            },
        ],
    },
    "JavaScript": {
        "easy": [
            {
                "q": "Which keyword declares a block-scoped variable?",
                "options": ["let", "var only", "define", "dim"],
                "answer": "let",
                "explanation": "`let` (and `const`) are block-scoped; `var` is function-scoped.",
            },
            {
                "q": "What does === check?",
                "options": ["Value and type", "Only value", "Only type", "Reference only"],
                "answer": "Value and type",
                "explanation": "Strict equality compares both value and type without coercion.",
            },
        ],
        "medium": [
            {
                "q": "What is a Promise in JavaScript?",
                "options": ["Object for async success/failure", "A CSS animation", "A loop type", "A DOM tag"],
                "answer": "Object for async success/failure",
                "explanation": "Promises represent eventual completion (or failure) of async work.",
            },
            {
                "q": "What does Array.map() return?",
                "options": ["A new array", "The same array mutated", "A single value", "undefined"],
                "answer": "A new array",
                "explanation": "map creates a new array by transforming each element.",
            },
        ],
        "hard": [
            {
                "q": "What is event bubbling?",
                "options": ["Event propagates from child to parent", "Event jumps to sibling only", "Event never propagates", "Only used in CSS"],
                "answer": "Event propagates from child to parent",
                "explanation": "In bubbling, the event starts at the target and moves up the DOM tree.",
            },
            {
                "q": "What does async/await do?",
                "options": ["Write async code that looks synchronous", "Make loops faster", "Replace HTML", "Compile TypeScript"],
                "answer": "Write async code that looks synchronous",
                "explanation": "await pauses an async function until a Promise settles.",
            },
        ],
    },
    "Python": {
        "easy": [
            {
                "q": "How do you create a list in Python?",
                "options": ["[1, 2, 3]", "{1, 2, 3} only", "(1; 2; 3)", "<1, 2, 3>"],
                "answer": "[1, 2, 3]",
                "explanation": "Square brackets create lists. {} is set/dict; () is tuple.",
            },
            {
                "q": "What does len('hello') return?",
                "options": ["5", "4", "6", "Error"],
                "answer": "5",
                "explanation": "len counts characters: h-e-l-l-o → 5.",
            },
            {
                "q": "Which keyword defines a function?",
                "options": ["def", "function", "fun", "define"],
                "answer": "def",
                "explanation": "Python uses `def name():` to define functions.",
            },
        ],
        "medium": [
            {
                "q": "What is a Python dictionary?",
                "options": ["Key-value mapping", "Ordered only list", "A loop", "A module for math"],
                "answer": "Key-value mapping",
                "explanation": "dict stores data as key → value pairs, e.g. {'a': 1}.",
            },
            {
                "q": "What does list comprehension [x*2 for x in range(3)] produce?",
                "options": ["[0, 2, 4]", "[1, 2, 3]", "[0, 1, 2]", "[2, 4, 6]"],
                "answer": "[0, 2, 4]",
                "explanation": "range(3) → 0,1,2; doubled → 0,2,4.",
            },
            {
                "q": "Difference between append() and extend()?",
                "options": ["append adds one item; extend adds iterable elements", "They are identical", "extend adds one item only", "append merges two dicts"],
                "answer": "append adds one item; extend adds iterable elements",
                "explanation": "a.append([1,2]) adds one nested list; a.extend([1,2]) adds 1 and 2.",
            },
        ],
        "hard": [
            {
                "q": "What is a decorator in Python?",
                "options": ["Function that wraps another function", "A CSS style", "A loop keyword", "A database driver"],
                "answer": "Function that wraps another function",
                "explanation": "Decorators (@name) modify or enhance function behavior.",
            },
            {
                "q": "What does *args allow?",
                "options": ["Variable number of positional arguments", "Only keyword args", "Only one argument", "Import all modules"],
                "answer": "Variable number of positional arguments",
                "explanation": "*args packs extra positional args into a tuple.",
            },
            {
                "q": "GIL in CPython mainly affects?",
                "options": ["CPU-bound multi-threading", "Disk space", "HTML rendering", "SQL joins"],
                "answer": "CPU-bound multi-threading",
                "explanation": "The Global Interpreter Lock limits true parallel CPU threads in CPython.",
            },
        ],
    },
    "SQL": {
        "easy": [
            {
                "q": "Which command retrieves data?",
                "options": ["SELECT", "GET", "FETCH", "SHOW DATA"],
                "answer": "SELECT",
                "explanation": "SELECT is used to query rows from tables.",
            },
            {
                "q": "Which clause filters rows?",
                "options": ["WHERE", "ORDER BY", "GROUP BY", "HAVING only"],
                "answer": "WHERE",
                "explanation": "WHERE filters individual rows before grouping.",
            },
        ],
        "medium": [
            {
                "q": "What does INNER JOIN return?",
                "options": ["Matching rows from both tables", "All rows from left only", "All rows from both", "Unmatched rows only"],
                "answer": "Matching rows from both tables",
                "explanation": "INNER JOIN keeps rows that match the join condition in both tables.",
            },
            {
                "q": "PRIMARY KEY means?",
                "options": ["Unique + NOT NULL identifier", "Can have duplicates", "Only for dates", "Foreign reference only"],
                "answer": "Unique + NOT NULL identifier",
                "explanation": "A primary key uniquely identifies each row and cannot be NULL.",
            },
        ],
        "hard": [
            {
                "q": "Difference between WHERE and HAVING?",
                "options": ["WHERE filters rows; HAVING filters groups", "They are the same", "HAVING filters before GROUP BY", "WHERE is only for JOIN"],
                "answer": "WHERE filters rows; HAVING filters groups",
                "explanation": "HAVING is applied after GROUP BY on aggregated results.",
            },
            {
                "q": "What is a window function example?",
                "options": ["ROW_NUMBER() OVER (...)", "INNER JOIN", "CREATE INDEX", "DROP TABLE"],
                "answer": "ROW_NUMBER() OVER (...)",
                "explanation": "Window functions compute values across related rows without collapsing them.",
            },
        ],
    },
    "PHP": {
        "easy": [
            {
                "q": "PHP files usually end with?",
                "options": [".php", ".html", ".py", ".js"],
                "answer": ".php",
                "explanation": "Server-side PHP scripts use the .php extension.",
            },
            {
                "q": "Variables in PHP start with?",
                "options": ["$", "@", "#", "&"],
                "answer": "$",
                "explanation": "PHP variables are prefixed with $ like $name.",
            },
        ],
        "medium": [
            {
                "q": "What does mysqli / PDO help with?",
                "options": ["Database connectivity", "CSS styling", "Image editing", "DNS lookup only"],
                "answer": "Database connectivity",
                "explanation": "mysqli and PDO connect PHP apps to databases securely.",
            },
            {
                "q": "What is $_POST used for?",
                "options": ["Form data sent via POST", "URL query only", "Cookies", "Sessions only"],
                "answer": "Form data sent via POST",
                "explanation": "$_POST holds data from HTTP POST requests (forms).",
            },
        ],
        "hard": [
            {
                "q": "Why use prepared statements?",
                "options": ["Prevent SQL injection", "Speed up CSS", "Compile PHP to C", "Encrypt images"],
                "answer": "Prevent SQL injection",
                "explanation": "Prepared statements separate SQL from data, blocking injection attacks.",
            },
        ],
    },
    "AI": {
        "easy": [
            {
                "q": "What is Artificial Intelligence?",
                "options": ["Machines mimicking human intelligence", "Only robots with arms", "A database type", "A CSS framework"],
                "answer": "Machines mimicking human intelligence",
                "explanation": "AI systems perform tasks that typically need human intelligence.",
            },
            {
                "q": "Which is an AI application?",
                "options": ["Voice assistants", "Pencil sharpening only", "Paper printing only", "Screwdriver design only"],
                "answer": "Voice assistants",
                "explanation": "Siri/Alexa-style assistants use AI for speech and language.",
            },
        ],
        "medium": [
            {
                "q": "Narrow AI vs General AI?",
                "options": ["Narrow = task-specific; General = human-level broad", "They are identical", "Narrow is stronger", "General only does math"],
                "answer": "Narrow = task-specific; General = human-level broad",
                "explanation": "Today's systems are mostly Narrow AI; AGI is still aspirational.",
            },
        ],
        "hard": [
            {
                "q": "What is the Turing Test related to?",
                "options": ["Whether a machine's behavior is indistinguishable from a human", "Network speed", "Disk encryption", "GPU cooling"],
                "answer": "Whether a machine's behavior is indistinguishable from a human",
                "explanation": "Turing proposed evaluating machine intelligence via conversation indistinguishability.",
            },
        ],
    },
    "ML": {
        "easy": [
            {
                "q": "What is Machine Learning?",
                "options": ["Systems learning patterns from data", "Manual if-else only", "HTML templating", "Cable networking"],
                "answer": "Systems learning patterns from data",
                "explanation": "ML algorithms improve from data without being explicitly rule-coded for every case.",
            },
            {
                "q": "Supervised learning needs?",
                "options": ["Labeled data", "No data", "Only unlabeled images", "CSS files"],
                "answer": "Labeled data",
                "explanation": "Supervised ML trains on input-output pairs (labels).",
            },
        ],
        "medium": [
            {
                "q": "Overfitting means?",
                "options": ["Model memorizes training data; poor on new data", "Model is always undertrained", "Data has no features", "Accuracy is perfect on test forever"],
                "answer": "Model memorizes training data; poor on new data",
                "explanation": "Overfit models don't generalize — high train accuracy, weak test accuracy.",
            },
            {
                "q": "Train/test split is used to?",
                "options": ["Evaluate generalization", "Delete outliers only", "Encrypt labels", "Speed up HTML"],
                "answer": "Evaluate generalization",
                "explanation": "Held-out test data estimates how the model performs on unseen samples.",
            },
        ],
        "hard": [
            {
                "q": "Bias-variance tradeoff is about?",
                "options": ["Balancing underfitting vs overfitting", "CPU vs RAM price", "SQL vs NoSQL", "HTTP vs HTTPS"],
                "answer": "Balancing underfitting vs overfitting",
                "explanation": "High bias underfits; high variance overfits — we seek a balance.",
            },
        ],
    },
    "DL": {
        "easy": [
            {
                "q": "Deep Learning mainly uses?",
                "options": ["Neural networks with many layers", "Only Excel formulas", "Manual sorting", "Paper forms"],
                "answer": "Neural networks with many layers",
                "explanation": "DL stacks many layers to learn hierarchical features.",
            },
        ],
        "medium": [
            {
                "q": "What is an activation function example?",
                "options": ["ReLU", "SELECT", "margin", "href"],
                "answer": "ReLU",
                "explanation": "ReLU (and sigmoid/tanh) introduce non-linearity in neurons.",
            },
            {
                "q": "CNN is especially good for?",
                "options": ["Images", "Sorting integers only", "CSS layout", "DNS"],
                "answer": "Images",
                "explanation": "Convolutional Neural Networks excel at spatial patterns like images.",
            },
        ],
        "hard": [
            {
                "q": "Vanishing gradient problem affects?",
                "options": ["Training very deep networks", "CSS specificity", "SQL indexes", "File permissions"],
                "answer": "Training very deep networks",
                "explanation": "Gradients shrink through many layers, slowing/stopping learning — mitigated by ReLU, residuals, etc.",
            },
        ],
    },
    "Generative AI": {
        "easy": [
            {
                "q": "Generative AI primarily?",
                "options": ["Creates new content (text, images, code)", "Only deletes files", "Only sorts arrays", "Only compresses ZIP"],
                "answer": "Creates new content (text, images, code)",
                "explanation": "GenAI models generate novel outputs from learned patterns.",
            },
            {
                "q": "ChatGPT is an example of?",
                "options": ["Large Language Model (LLM)", "A relational database", "A CSS library", "A hardware chip only"],
                "answer": "Large Language Model (LLM)",
                "explanation": "LLMs are generative models trained on large text corpora.",
            },
        ],
        "medium": [
            {
                "q": "What is a prompt?",
                "options": ["Input instruction to a generative model", "A SQL primary key", "A CSS selector", "A Python decorator only"],
                "answer": "Input instruction to a generative model",
                "explanation": "Prompting guides what the model should produce.",
            },
            {
                "q": "Hallucination in LLMs means?",
                "options": ["Confident but incorrect output", "GPU overheating", "Empty responses only", "Faster training"],
                "answer": "Confident but incorrect output",
                "explanation": "Models may invent facts that sound plausible — verify important claims.",
            },
        ],
        "hard": [
            {
                "q": "RAG (Retrieval-Augmented Generation) helps by?",
                "options": ["Fetching external docs to ground answers", "Removing all training data", "Converting CSS to HTML", "Disabling GPUs"],
                "answer": "Fetching external docs to ground answers",
                "explanation": "RAG retrieves relevant context then generates answers with less hallucination.",
            },
        ],
    },
}


def get_tech_question(topics, difficulty="easy"):
    """Pick a tech MCQ from allowed topics at a difficulty."""
    difficulty = difficulty if difficulty in ("easy", "medium", "hard") else "easy"
    topic = random.choice(topics) if topics else random.choice(TECH_TOPICS)
    bank = TECH_QUESTIONS.get(topic, TECH_QUESTIONS["Python"])
    level_qs = bank.get(difficulty) or bank.get("easy") or []
    if not level_qs:
        # fall back across difficulties
        for d in ("easy", "medium", "hard"):
            if bank.get(d):
                level_qs = bank[d]
                break
    item = random.choice(level_qs)
    opts = item["options"][:]
    random.shuffle(opts)
    return {
        "topic": topic,
        "difficulty": difficulty,
        "question": item["q"],
        "options": opts,
        "answer": item["answer"],
        "explanation": item["explanation"],
    }


def next_difficulty(current, correct):
    order = ["easy", "medium", "hard"]
    i = order.index(current) if current in order else 0
    if correct:
        return order[min(i + 1, 2)]
    return order[max(i - 1, 0)]


# ---------------------------------------------------------------------------
# Coding tests (easy → hard)
# ---------------------------------------------------------------------------

CODING_TESTS = {
    "easy": [
        {
            "title": "Sum of two numbers",
            "prompt": "Write a function `add(a, b)` that returns a + b.\nExample: add(2, 3) → 5",
            "hint": "Just return a + b.",
            "sample_solution": "def add(a, b):\n    return a + b",
            "check_fn": "add",
            "tests": [((2, 3), 5), ((0, 0), 0), ((-1, 1), 0)],
        },
        {
            "title": "Maximum of list",
            "prompt": "Write `find_max(nums)` that returns the largest number in a list.\nExample: find_max([1, 5, 2]) → 5",
            "hint": "Use max(nums) or a loop.",
            "sample_solution": "def find_max(nums):\n    return max(nums)",
            "check_fn": "find_max",
            "tests": [(([1, 5, 2],), 5), (([-3, -1],), -1)],
        },
        {
            "title": "Palindrome check",
            "prompt": "Write `is_palindrome(s)` returning True if s reads the same forwards/backwards (ignore case).\nExample: is_palindrome('Racecar') → True",
            "hint": "Compare s.lower() with its reverse.",
            "sample_solution": "def is_palindrome(s):\n    s = s.lower()\n    return s == s[::-1]",
            "check_fn": "is_palindrome",
            "tests": [(("Racecar",), True), (("hello",), False), (("Aba",), True)],
        },
    ],
    "medium": [
        {
            "title": "Two Sum",
            "prompt": "Write `two_sum(nums, target)` returning indices of two numbers that add to target.\nExample: two_sum([2,7,11,15], 9) → [0, 1]",
            "hint": "Use a dict of value→index while iterating.",
            "sample_solution": (
                "def two_sum(nums, target):\n"
                "    seen = {}\n"
                "    for i, n in enumerate(nums):\n"
                "        if target - n in seen:\n"
                "            return [seen[target - n], i]\n"
                "        seen[n] = i\n"
            ),
            "check_fn": "two_sum",
            "tests": [(([2, 7, 11, 15], 9), [0, 1]), (([3, 2, 4], 6), [1, 2])],
        },
        {
            "title": "Valid parentheses",
            "prompt": "Write `is_valid(s)` that checks if brackets (), [], {} are balanced.\nExample: is_valid('()[]{}') → True",
            "hint": "Use a stack.",
            "sample_solution": (
                "def is_valid(s):\n"
                "    pair = {')':'(', ']':'[', '}':'{'}\n"
                "    st = []\n"
                "    for c in s:\n"
                "        if c in '([{':\n"
                "            st.append(c)\n"
                "        elif not st or st.pop() != pair[c]:\n"
                "            return False\n"
                "    return not st\n"
            ),
            "check_fn": "is_valid",
            "tests": [(("()[]{}",), True), (("(]",), False), (("({[]})",), True)],
        },
        {
            "title": "Word frequency",
            "prompt": "Write `word_count(text)` returning a dict of word → count (split on spaces, lowercase).\nExample: word_count('Hi hi there') → {'hi': 2, 'there': 1}",
            "hint": "Split, lower, count with a dict or Counter.",
            "sample_solution": (
                "def word_count(text):\n"
                "    d = {}\n"
                "    for w in text.lower().split():\n"
                "        d[w] = d.get(w, 0) + 1\n"
                "    return d\n"
            ),
            "check_fn": "word_count",
            "tests": [(("Hi hi there",), {"hi": 2, "there": 1})],
        },
    ],
    "hard": [
        {
            "title": "Longest substring without repeat",
            "prompt": "Write `length_of_longest_substring(s)` — length of longest substring without repeating characters.\nExample: 'abcabcbb' → 3",
            "hint": "Sliding window + set/dict of last indices.",
            "sample_solution": (
                "def length_of_longest_substring(s):\n"
                "    seen = {}\n"
                "    left = best = 0\n"
                "    for right, ch in enumerate(s):\n"
                "        if ch in seen and seen[ch] >= left:\n"
                "            left = seen[ch] + 1\n"
                "        seen[ch] = right\n"
                "        best = max(best, right - left + 1)\n"
                "    return best\n"
            ),
            "check_fn": "length_of_longest_substring",
            "tests": [(("abcabcbb",), 3), (("bbbbb",), 1), (("pwwkew",), 3)],
        },
        {
            "title": "Merge intervals",
            "prompt": "Write `merge(intervals)` that merges overlapping intervals.\nExample: [[1,3],[2,6],[8,10]] → [[1,6],[8,10]]",
            "hint": "Sort by start, then merge if overlap.",
            "sample_solution": (
                "def merge(intervals):\n"
                "    if not intervals:\n"
                "        return []\n"
                "    intervals = sorted(intervals)\n"
                "    out = [intervals[0]]\n"
                "    for s, e in intervals[1:]:\n"
                "        if s <= out[-1][1]:\n"
                "            out[-1][1] = max(out[-1][1], e)\n"
                "        else:\n"
                "            out.append([s, e])\n"
                "    return out\n"
            ),
            "check_fn": "merge",
            "tests": [([[[1, 3], [2, 6], [8, 10]],], [[1, 6], [8, 10]])],
        },
    ],
}


def get_coding_challenge(difficulty="easy"):
    bank = CODING_TESTS.get(difficulty, CODING_TESTS["easy"])
    return random.choice(bank)


def run_coding_tests(user_code, challenge):
    """Execute user code against challenge tests. Returns (passed, feedback)."""
    namespace = {}
    try:
        exec(user_code, namespace)  # noqa: S102 — intentional student sandbox practice
    except Exception as e:
        return False, f"Your code has an error while loading: `{e}`\n\nHere's a sample solution to learn from:\n```python\n{challenge['sample_solution']}\n```"

    fn = namespace.get(challenge["check_fn"])
    if not callable(fn):
        return False, (
            f"I couldn't find a function named `{challenge['check_fn']}`. "
            f"Please define it.\n\nSample solution:\n```python\n{challenge['sample_solution']}\n```"
        )

    failed = []
    for args, expected in challenge["tests"]:
        try:
            got = fn(*args)
            if got != expected:
                failed.append(f"Input {args} → expected `{expected}`, got `{got}`")
        except Exception as e:
            failed.append(f"Input {args} → crashed with `{e}`")

    if not failed:
        return True, "All test cases passed — awesome work!"
    feedback = "Some tests failed:\n- " + "\n- ".join(failed)
    feedback += f"\n\nHere's a correct approach:\n```python\n{challenge['sample_solution']}\n```"
    return False, feedback


# ---------------------------------------------------------------------------
# Project ideas (large rotatable bank — "endless" via combinations)
# ---------------------------------------------------------------------------

_PROJECT_DOMAINS = [
    "healthcare", "education", "finance", "e-commerce", "agriculture",
    "smart city", "social media", "fitness", "travel", "food delivery",
    "recruitment", "legal tech", "climate", "gaming", "IoT home",
]
_PROJECT_TECH = [
    "Python + Flask", "Python + Streamlit", "React + Node", "Django + PostgreSQL",
    "ML with scikit-learn", "Deep Learning (TensorFlow/PyTorch)", "Generative AI / RAG chatbot",
    "SQL analytics dashboard", "PHP + MySQL", "HTML/CSS/JS frontend",
]
_PROJECT_FEATURES = [
    "real-time notifications", "role-based login", "REST API", "charts & analytics",
    "mobile-responsive UI", "recommendation engine", "chat support", "PDF reports",
    "map integration", "payment mock flow", "admin panel", "CSV export",
]


def generate_project_ideas(n=8, skills=None):
    """Generate many unique-feeling real-time project ideas."""
    skills = skills or ["Python"]
    ideas = []
    templates = [
        "Build a **{domain}** web app with **{tech}** featuring {f1} and {f2}.",
        "Create a real-time **{domain}** monitor using **{tech}** — include {f1}.",
        "Design a **{domain}** platform ({tech}) with {f1}, {f2}, and user dashboards.",
        "Ship an MVP for **{domain}**: stack = **{tech}**, must-have = {f1}.",
        "Portfolio project: **{domain} assistant** powered by **{tech}** + {f1}.",
    ]
    # Prefer tech matching user skills
    preferred = [t for t in _PROJECT_TECH if any(s.lower() in t.lower() for s in skills)]
    tech_pool = preferred + _PROJECT_TECH

    seen = set()
    while len(ideas) < n:
        domain = random.choice(_PROJECT_DOMAINS)
        tech = random.choice(tech_pool)
        f1, f2 = random.sample(_PROJECT_FEATURES, 2)
        text = random.choice(templates).format(domain=domain, tech=tech, f1=f1, f2=f2)
        if text not in seen:
            seen.add(text)
            ideas.append(text)
    return ideas


STATIC_PROJECT_STARTERS = [
    "Placement prediction dashboard (you already have a start!) — add resume scoring.",
    "Campus lost-and-found app with image upload and claims workflow.",
    "Expense splitter for roommates with monthly charts.",
    "Job application tracker (status board + reminders).",
    "Study planner with spaced-repetition flashcards.",
    "Fake-news headline classifier (ML) with a simple Streamlit UI.",
    "Personal finance chatbot using Generative AI + your bank CSV.",
    "SQL practice playground that grades student queries.",
    "Attendance face-recognition prototype (DL) for a classroom.",
    "Recipe recommender based on ingredients you have.",
]


# ---------------------------------------------------------------------------
# Group discussion topics + communication prompts
# ---------------------------------------------------------------------------

GD_TOPICS = [
    {
        "topic": "Should AI replace entry-level coding jobs?",
        "points_for": ["Boosts productivity", "Automates boilerplate", "Frees humans for design"],
        "points_against": ["Juniors lose learning path", "Quality/security risks", "Bias & hallucinations"],
        "sample_opening": "Good morning everyone. I believe AI is a powerful assistant, but it shouldn't fully replace junior roles because those roles build fundamentals...",
    },
    {
        "topic": "Is remote work better than office work for freshers?",
        "points_for": ["Flexibility", "Global opportunities", "Less commute stress"],
        "points_against": ["Less mentoring", "Harder networking", "Distractions at home"],
        "sample_opening": "Hello team. As a fresher, I'd say a hybrid model works best — office time for mentoring, remote for deep focus...",
    },
    {
        "topic": "Are college grades more important than projects?",
        "points_for": ["Shows consistency", "Shortlists by HR", "Discipline signal"],
        "points_against": ["Projects show real skill", "Industry cares about impact", "Grades aren't everything"],
        "sample_opening": "Hi everyone. Grades open the door, but strong projects help you walk through it in technical rounds...",
    },
    {
        "topic": "Social media: boon or bane for students?",
        "points_for": ["Learning communities", "Personal branding", "Networking"],
        "points_against": ["Distraction", "Misinformation", "Mental health pressure"],
        "sample_opening": "Friends, social media is a tool — used well it accelerates learning; used poorly it steals focus...",
    },
    {
        "topic": "Should internships be mandatory for graduation?",
        "points_for": ["Industry exposure", "Soft skills", "Employability"],
        "points_against": ["Access inequality", "Quality varies", "Academic load"],
        "sample_opening": "I support structured internships because they bridge classroom theory with workplace practice...",
    },
    {
        "topic": "Will Generative AI make traditional exams obsolete?",
        "points_for": ["New skill reality", "Project-based assessment", "Real-world tools"],
        "points_against": ["Need fundamentals", "Integrity concerns", "Fair evaluation hard"],
        "sample_opening": "Exams may evolve, not vanish — we still need ways to verify understanding beyond copy-paste answers...",
    },
]

COMM_PROMPTS = [
    {
        "prompt": "Introduce yourself in 45–60 seconds for an HR round (include education, skills, one project, and a goal).",
        "tips": "Smile in tone, keep it under 1 minute, end with why you're excited about the role.",
        "sample": "Hi, I'm [Name], a final-year CSE student skilled in Python and basic ML. I built a placement prediction app using Streamlit. I'm looking for a role where I can grow as a software engineer and contribute to real products.",
    },
    {
        "prompt": "Explain a project you built to a non-technical HR manager.",
        "tips": "Avoid jargon; focus on problem → solution → impact.",
        "sample": "I built an app that estimates a student's chance of getting placed and suggests skills to improve — like a friendly coach for placements.",
    },
    {
        "prompt": "Describe a conflict in a team project and how you handled it.",
        "tips": "Use STAR: Situation, Task, Action, Result. Stay positive.",
        "sample": "Two teammates disagreed on the tech stack. I suggested a quick prototype comparison, we picked the simpler option, and delivered on time.",
    },
    {
        "prompt": "Give a polite disagreement in a meeting (practice tone).",
        "tips": "Acknowledge first, then offer an alternative with reason.",
        "sample": "I see your point about shipping faster. Could we also add basic tests so we don't create more bugs later?",
    },
    {
        "prompt": "Summarize this idea in simpler words: 'We leveraged a transformer-based LLM with RAG for domain QA.'",
        "tips": "Translate to everyday language.",
        "sample": "We built a smart search chatbot that looks up our documents and answers questions in normal language.",
    },
]


def score_communication(answer: str) -> tuple[int, str]:
    """Lightweight friendly feedback on communication answers."""
    text = (answer or "").strip()
    words = text.split()
    score = 50
    tips = []
    if len(words) < 12:
        tips.append("Try adding a bit more detail (aim for 40–80 words).")
        score -= 15
    elif len(words) > 180:
        tips.append("Great energy — try a shorter, clearer version for interviews.")
        score -= 5
    else:
        score += 15
    if any(w in text.lower() for w in ["i ", "my ", "we ", "our "]):
        score += 10
    else:
        tips.append("Use first person (I/we) so it sounds personal and confident.")
    fillers = sum(text.lower().count(f) for f in ["umm", "uhh", "like,", "you know"])
    if fillers:
        score -= 10
        tips.append("Reduce fillers like 'umm' / 'like' — pause instead.")
    else:
        score += 10
    if "?" in text or "!" in text:
        score += 5
    score = max(20, min(98, score))
    if not tips:
        tips.append("Clear structure — keep practicing aloud for fluency!")
    msg = f"Communication vibe score: **{score}/100**.\n" + "\n".join(f"- {t}" for t in tips)
    return score, msg


HR_WARM_OPENERS = [
    "Hey! Super glad you're here — we'll keep this friendly and useful.",
    "Welcome! No stress — this is practice, and I'm here to help you grow.",
    "Hi there! Let's practice together at your pace.",
]

FRIENDLY_CORRECT = [
    "Nice one!",
    "Yes — you got it!",
    "Awesome, that's correct!",
    "Great job!",
]

FRIENDLY_WRONG = [
    "No worries — learning moment!",
    "Almost! Here's the right take:",
    "That's okay — let's lock in the correct answer:",
    "Good try! The correct answer is:",
]


def friendly_correct():
    return random.choice(FRIENDLY_CORRECT)


def friendly_wrong():
    return random.choice(FRIENDLY_WRONG)
