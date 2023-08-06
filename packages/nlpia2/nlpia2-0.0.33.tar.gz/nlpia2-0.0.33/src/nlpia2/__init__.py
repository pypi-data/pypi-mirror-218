# nlpia2.__init__.py
from pathlib import Path
from wikipedia import wikipedia  # noqa


__all__ = [p.name[:-3] for p in Path(__file__).parent.glob('*.py')] 
