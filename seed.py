from app.models import db
from app.models import Pattern
from app import create_app

app = create_app()

patterns = [
    'Two Pointer',
    'Sliding Window',
    'Fast & Slow Pointer',
    'Binary Search',
    'DFS',
    'BFS',
    'Dynamic Programming 1D',
    'Dynamic Programming 2D',
    'Backtracking',
    'Greedy',
    'Heap / Priority Queue',
    'Graph',
    'Stack',
    'Monotonic Stack',
    'Trie',
    'Union Find',
    'Topological Sort',
    'Prefix Sum',
    'Intervals',
    'Bit Manipulation',
    'Linked List In-Place Reversal',
    'Matrix',
    'Math & Geometry'
]

with app.app_context():
    existing = {p.pattern_name for p in Pattern.query.all()}

    for name in patterns:
        if name not in existing:
            db.session.add(Pattern(pattern_name=name))
    
    db.session.commit()
    print('Patterns seeded successfully!')